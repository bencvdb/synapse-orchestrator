#!/usr/bin/env python
import sys
import argparse
import pkg_resources  # part of setuptools
import logging

from synorchestrator.config import show
from synorchestrator.orchestrator import queue
from synorchestrator.util import get_json

logging.basicConfig(level=logging.INFO)


"""Takes a user script and queues the entries inside."""


def main(argv=sys.argv[1:]):

    parser = argparse.ArgumentParser(description='Synapse Workflow Orchestrator')
    parser.add_argument("--version", action="store_true", default=False)
    parser.add_argument("--setupFromFile", required=False)
    args = parser.parse_args(argv)

    if args.version:
        pkg = pkg_resources.require('synapse-orchestrator')
        print(u"%s %s" % (sys.argv[0], pkg[0].version))
        exit(0)

    print('Setting up the queue.  Currently available configurations:\n\n\n')
    show()

    default_yaml = '/home/quokka/git/current_demo/orchestrator/synorchestrator/config_files/user_submission_example.json'

    # TODO verify terms match between configs
    sdict = get_json(default_yaml)
    for wf_service in sdict:
        for sample in sdict[wf_service]:
            wf_name = sdict[wf_service][sample]['wf_name']
            wf_jsonyaml = sdict[wf_service][sample]['jsonyaml']
            print('Queueing "{}" on "{}" with data: {}'.format(wf_name, wf_service, sample))
            queue(wf_service, wf_name, wf_jsonyaml)


if __name__ == '__main__':
    main(sys.argv[1:])
