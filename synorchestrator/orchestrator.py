#!/usr/bin/env python
"""
Takes a given ID/URL for a workflow registered in a given TRS
implementation; prepare the workflow run request, including
retrieval and formatting of parameters, if not provided; post
the workflow run request to a given WES implementation;
monitor and report results of the workflow run.
"""
import logging
import sys
import time
import os
import datetime as dt
from IPython.display import display, clear_output
from synorchestrator import config
from synorchestrator.util import get_json, ctime2datetime, convert_timedelta
from synorchestrator.wes.client import WESClient
from synorchestrator.eval import (create_submission,
                                  get_submission_bundle,
                                  get_submissions,
                                  update_submission_run,
                                  update_submission_status,
                                  submission_queue)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def run_submission(wes_id, submission_id):
    """
    For a single submission to a single evaluation queue, run
    the workflow in a single environment.
    """
    submission = get_submission_bundle(wes_id, submission_id)

    logger.info(" Submitting to WES endpoint '{}':"
                " \n - submission ID: {}"
                .format(wes_id, submission_id))

    client = WESClient(config.wes_config()[wes_id])
    run_data = client.run_workflow(submission['data']['wf'],
                                   submission['data']['jsonyaml'],
                                   submission['data']['attachments'])
    run_data['start_time'] = dt.datetime.now().ctime()
    update_submission_run(wes_id, submission_id, run_data)
    update_submission_status(wes_id, submission_id, 'SUBMITTED')
    return run_data


def run_next_queued(wes_id):
    """
    Run the next submission slated for a single WES endpoint.

    Return None if no submissions are queued.
    """
    queued_submissions = get_submissions(wes_id, status='RECEIVED')
    if not queued_submissions:
        return None
    for submission_id in sorted(queued_submissions):
        return run_submission(wes_id, submission_id)


def monitor_service(wf_service):
    status_dict = {}
    # for run ID######## in each
    submissions = get_json(submission_queue)
    for run_id in submissions[wf_service]:
        if 'run' not in submissions[wf_service][run_id]:
            continue
        run = submissions[wf_service][run_id]['run']
        client = WESClient(config.wes_config()[wf_service])
        updated_status = client.get_workflow_run_status(run['run_id'])['state']
        run['state'] = updated_status
        if run['state'] in ['QUEUED', 'INITIALIZING', 'RUNNING']:
            etime = convert_timedelta(dt.datetime.now() - ctime2datetime(run['start_time']))
        elif 'elapsed_time' not in run:
            etime = 0
        else:
            etime = run['elapsed_time']
        run['elapsed_time'] = etime
        status_dict.setdefault(wf_service, {})[run_id] = {
            'wf_id': submissions[wf_service][run_id]['wf_id'],
            'run_id': run['run_id'],
            'run_status': updated_status,
            'wes_id': wf_service,
            'start_time': run['start_time'],
            'elapsed_time': etime}
    return status_dict

def monitor():
    """Monitor progress of workflow jobs."""
    import pandas as pd
    pd.set_option('display.width', 100)

    statuses = []
    submissions = get_json(submission_queue)
    # for local, toil, cromwell, arvados, cwltool, etc.
    for wf_service in submissions:
        statuses.append(monitor_service(wf_service))

    status_df = pd.DataFrame.from_dict(
        {(i, j): status[i][j]
         for status in statuses
         for i in status.keys()
         for j in status[i].keys()},
        orient='index')

    clear_output(wait=True)
    os.system('clear')
    display(status_df)
    sys.stdout.flush()
    if True:  # any(status_df['run_status'].isin(['QUEUED', 'INITIALIZING', 'RUNNING'])):
        time.sleep(1)
        monitor()
    else:
        print("Done!")


submission_id = create_submission(wes_id='local',
                                  submission_data={'wf': '/home/quokka/git/workflow-service/testdata/md5sum.wdl',
                                                   'jsonyaml': 'file:///home/quokka/git/workflow-service/testdata/md5sum.wdl.json',
                                                   'attachments': ['file:///home/quokka/git/workflow-service/testdata/md5sum.input']},
                  wf_name='wflow0',
                  type='cwl')
#
# print(get_submission_bundle("local", "040804130201818647"))
print(run_submission("local", submission_id))
i = get_submissions("local", status='RECEIVED')
print(i)
j = get_json(submission_queue)
monitor()
