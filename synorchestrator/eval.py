import logging
import os
import json
import datetime as dt

from synorchestrator import config
from synorchestrator.util import get_json, save_json

logger = logging.getLogger(__name__)

submission_queue = '/home/quokka/git/orchestrator/synorchestrator/submission_queue.json'


def create_submission(wes_id, wf_name, submission_data, type):
    """
    Submit a new job request to an evaluation queue.
    """
    submissions = get_json(submission_queue)
    submission_id = dt.datetime.now().strftime('%d%m%d%H%M%S%f')

    submissions.setdefault(wes_id, {})[submission_id] = {'status': 'RECEIVED',
                                                         'data': submission_data,
                                                         'wf_id': wf_name,
                                                         'type': type}
    save_json(submission_queue, submissions)
    logger.info("Created new job submission:"
                "\n - submission ID: {}".format(submission_id))
    return submission_id


def get_submissions(wes_id, status='RECEIVED'):
    """Return all ids with the requested status."""
    submissions = get_json(submission_queue)
    return [id for id, bundle in submissions[wes_id].items() if bundle['status'] == status]


def get_submission_bundle(wes_id, submission_id):
    """Return the submission's info."""
    return get_json(submission_queue)[wes_id][submission_id]


def update_submission_status(wes_id, submission_id, status):
    """Update the status of a submission."""
    submissions = get_json(submission_queue)
    submissions[wes_id][submission_id]['status'] = status
    save_json(submission_queue, submissions)


def update_submission_run(wes_id, submission_id, run_data):
    """Update information for a workflow run."""
    evals = get_json(submission_queue)
    evals[wes_id][submission_id]['run'] = run_data
    save_json(submission_queue, evals)
