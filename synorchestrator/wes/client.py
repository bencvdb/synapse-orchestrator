from bravado.requests_client import RequestsClient
from wes_client.util import build_wes_request, wes_client, run_wf

# arvclient = WESClient(config.wes_config['arvados-wes'])
# cromclient = WESClient(config.wes_config['hca-cromwell'])


class WESClient(object):
    def __init__(self, service):
        self.host = service['host']
        self.auth = service['auth']
        self.auth_type = service['auth_type']
        self.proto = service['proto']

        self.http_client = RequestsClient()
        self.client = wes_client(self.http_client, self.auth, self.proto, self.host)

    def get_service_info(self):
        return self.client.GetServiceInfo()

    def run_workflow(self, wf, json, attachments):
        return run_wf(wf,
                      json,
                      attachments,
                      self.http_client,
                      self.auth,
                      self.proto,
                      self.host)

    def get_workflow_run(self, run_id):
        pass

    def get_workflow_run_status(self, run_id):
        return self.client.GetRunStatus(run_id).result()
