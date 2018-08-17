#!/usr/bin/env python

import unittest
import os
import json
from synorchestrator import config, util


class ConfigTests(unittest.TestCase):

    def setUp(self):
        super(ConfigTests, self).setUp()
        self.config_loc = os.path.join(os.path.expanduser('~'), 'test_orchestrator_config.json')
        if os.path.exists(self.config_loc):
            raise RuntimeError('Please move your orchestrator_config.json')


    def tearDown(self):
        super(ConfigTests, self).tearDown()

        try:
            os.remove(self.config_loc)
        except OSError:
            pass

    def testConfigPathWritesFile(self):
        """Make sure that if 'orchestrator_config.json' does not exist, config_path() will create one."""
        # Check that it doesnt exist
        expected_loc = self.config_loc
        self.assertFalse(os.path.isfile(expected_loc))
        returned_loc = config.config_path(self.config_loc)  # Should write file.
        self.assertEqual(expected_loc, returned_loc)
        self.assertTrue(os.path.isfile(returned_loc))
        with open(config.config_path(self.config_loc), 'r') as f:
            self.assertEqual(f.read(), '{"workflows": {},\n'
                                        ' "toolregistries": {},\n'
                                        ' "workflowservices": {}'
                                        '}\n')

    def testConfigPathFindsFile(self):
        """Make sure that config_path() finds the appropriate file."""
        with open(self.config_loc, 'w') as f:
            f.write('test')

        with open(config.config_path(self.config_loc), 'r') as f:
            self.assertEqual(f.read(), 'test')

    def testConfigs(self):
        """
        Make sure that the various config fetching functions  reads the right data from the config file.

        This test checks that the following functions return as expected:
            config.wf_config()
            config.trs_config()
            config.wes_config()
        """
        config_entries = {'workflows': config.wf_config,
                          'toolregistries': config.trs_config,
                          'workflowservices': config.wes_config}

        config.config_path(self.config_loc)  # Write the empty file.
        for entry, get_func in config_entries.items():
            config_file = util.get_json(self.config_loc)
            config_file[entry] = entry  # X_config() returns whatever is stored here.
            util.save_json(self.config_loc, config_file)
            self.assertEqual(get_func(), entry)

    def testAddWorkflow(self):
        """Test that add_workflow() adds entries to the config properly."""
        config.config_path(self.config_loc)  # Write the empty file.
        config.add_workflow('cactus',
                            'Toil',
                            'wf_url',
                            'workflow_attachments',
                            'submission_type',
                            'trs_id',
                            'version_id')
        config_file = util.get_json(self.config_loc)

        self.assertTrue('workflows' in config_file)
        self.assertTrue('cactus' in config_file['workflows'])
        var_name = config_file['workflows']['cactus']
        self.assertEqual(var_name['submission_type'], 'submission_type')
        self.assertEqual(var_name['trs_id'], 'trs_id')
        self.assertEqual(var_name['version_id'], 'version_id')
        self.assertEqual(var_name['workflow_url'], 'wf_url')
        self.assertEqual(var_name['workflow_attachments'], 'workflow_attachments')
        self.assertEqual(var_name['workflow_type'], 'Toil')