from twilio.rest import Client

account = "ACd1a95e95cf7c1a0e19382908a58708d7"
token = "e12cdd81b0803239c8cfa02648d60676"

def send_sms(content):
    if(content == ""):
        return False
    client = Client(account, token)
    message = client.messages.create(to="+14245356503", from_="+13235537537", body=content)
    return True
