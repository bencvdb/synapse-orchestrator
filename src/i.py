from synorchestrator.orchestrator import set_queue_from_user_json, run_all, run_submission
from synorchestrator.wes.client import WESClient
from synorchestrator.config import wes_config

# set_queue_from_user_json('/home/quokka/git/orchid/orchestrator/src/tests/data/user_submission_example.json')
# run_all()

# run_submission("Argon-Globus", "140814152850149946")

run_all()





# client = WESClient(wes_config()["Argon-Globus"])
# i = client.get_run_status("3a88e3f2c25b7d5b-218dfd90703970fe")
# print(i)





# "Calcium-Toil-AWS":
#    {"NWD119836_downsampled":
#       {"wf_name": "wdl_UoM_align",
#        "jsonyaml": "file://tests/data/calcium/NWD119836.json"},
#     "NWD136397_downsampled":
#       {"wf_name": "wdl_UoM_align",
#        "jsonyaml": "file://tests/data/calcium/NWD136397.json"},
#     "NWD176325_downsampled":
#       {"wf_name": "wdl_UoM_align",
#        "jsonyaml": "file://tests/data/calcium/NWD176325.json"},
#     "NWD231092_downsampled":
#       {"wf_name": "wdl_UoM_align",
#        "jsonyaml": "file://tests/data/calcium/NWD231092.json"},
#     "NWD315403_downsampled":
#       {"wf_name": "wdl_UoM_align",
#        "jsonyaml": "file://tests/data/calcium/NWD315403.json"}
#   },
#  "Argon-Globus":
#    {"NWD119836_downsampled":
#       {"wf_name": "wdl_UoM_align",
#        "jsonyaml": "file://tests/data/argon/NWD119836.json"},
#     "NWD136397_downsampled":
#       {"wf_name": "wdl_UoM_align",
#        "jsonyaml": "file://tests/data/argon/NWD136397.json"},
#     "NWD176325_downsampled":
#       {"wf_name": "wdl_UoM_align",
#        "jsonyaml": "file://tests/data/argon/NWD176325.json"},
#     "NWD231092_downsampled":
#       {"wf_name": "wdl_UoM_align",
#        "jsonyaml": "file://tests/data/argon/NWD231092.json"},
#     "NWD315403_downsampled":
#       {"wf_name": "wdl_UoM_align",
#        "jsonyaml": "file://tests/data/argon/NWD315403.json"}
#   }
