import json

class PEP:

    def __init__(self):
        return

    def receive_message(self,msg):
        return self.formulate_request(msg)
        
    '''
    rever isto
    '''
    def formulate_request(self,msg):
        intermediate={"name":msg}
        message=json.dumps(intermediate)
        return self.send_request(message)
        
    def send_request(self,msg):
        return msg #PDP().receive_request(msg)
    
    def receive_response(self,msg):
        #json loads da resposta do PDP
        message=json.loads(msg)
        return self.enforce(message)
        
    def enforce(self,msg): 
        if msg["response"]=="DENY":
            return 0
        return 1

    def close_connection(self):
        return NotImplementedError
