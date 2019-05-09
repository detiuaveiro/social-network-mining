from PEP import PEP
from PDP import PDP

pep=PEP()
pdp=PDP()
'''
define the lifecycle of PDP and PEP to avoid circular imports
solve PDP.send_response(msg)
solve PEP.send_request(msg)
'''
class PolicyAPI():
    def lifecycle(self, msg):
        #request ready to be sent to PDP
        alfa=pep.receive_message(msg)
        #response ready to be sent to PEP
        beta=pdp.receive_request(alfa)
        #enforce
        resp=pep.receive_response(beta)
        return resp