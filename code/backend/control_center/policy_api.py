from PEP.PEP import PEP
from PDP.PDP import PDP


class PolicyAPI():
    def __init__(self):
        self.pep = PEP()
        self.pdp = PDP()

    def lifecycle(self, msg):

        #request ready to be sent to PDP
        alfa = self.pep.receive_message(msg)

        #response ready to be sent to PEP
        beta = self.pdp.receive_request(alfa)

        #enforce
        resp= self.pep.receive_response(beta)

        return resp