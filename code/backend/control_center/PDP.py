import json

class PDP:

    def __init__(self):
        return
    
    def receive_request(self):
        #json loads do PEP
        return

    def evaluate(self):
        '''
        workflow of this function
            - pre-processing of request (filter, prepare db request, etc)
            - request to DB
            - get request from DB
            - post-processing of response (clean response from db, etc)
            - DECIDE (PERMIT, DENY) 
        '''
        #return "PERMIT" or return "DENY"
        return

    def send_response(self):
        #json dumps da decisão
        return