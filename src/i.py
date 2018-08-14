from synorchestrator.orchestrator import set_queue_from_user_json, run_all, run_submission
from synorchestrator.wes.client import WESClient
from synorchestrator.config import wes_config

# set_queue_from_user_json('/home/quokka/git/orchid/orchestrator/src/tests/data/user_submission_example.json')
# run_all()

# run_submission("Argon-Globus", "140814152850149946")

# run_all()


# ,
#  "Xenon-SevenBridges":
#    {"NWD119836_downsampled":
#       {"wf_name": "wdl_UoM_align",
#        "jsonyaml": "file://tests/data/xenon/NWD119836.json"},
#     "NWD136397_downsampled":
#       {"wf_name": "wdl_UoM_align",
#        "jsonyaml": "file://tests/data/xenon/NWD136397.json"},
#     "NWD176325_downsampled":
#       {"wf_name": "wdl_UoM_align",
#        "jsonyaml": "file://tests/data/xenon/NWD176325.json"},
#     "NWD231092_downsampled":
#       {"wf_name": "wdl_UoM_align",
#        "jsonyaml": "file://tests/data/xenon/NWD231092.json"},
#     "NWD315403_downsampled":
#       {"wf_name": "wdl_UoM_align",
#        "jsonyaml": "file://tests/data/xenon/NWD315403.json"}
#   }


client = WESClient(wes_config()["Argon-Globus"])
i = client.get_run_status("140814152850127827")['state']
print(i)
