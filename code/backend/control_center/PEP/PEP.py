import json

class PEP:

<<<<<<< HEAD
    def receive_message(self,msg):
        return self.formulate_request(msg)
        
    def formulate_request(self,msg):
        '''
        This message comes from the messaging system. It could be one of the following:
        - REQUEST_TWEET_LIKE = 5
        - REQUEST_TWEET_RETWEET = 6
        - REQUEST_TWEET_REPLY = 7
        - REQUEST_FOLLOW_USER = 8
        So, it is put in a dictionary, converted to json and sent to the PDP
        '''
        message=json.dumps(msg)
=======
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
>>>>>>> RESTRUCTURE
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
