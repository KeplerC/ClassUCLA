from twilio.rest import Client
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config

def send_sms(content, phone):
    if(content == ""):
        return False
    
    client = Client(config.account, config.token)
    message = client.messages.create(to=phone, from_ = config.phone, body=content)
    return True
