from twilio.rest import Client
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import config
#from .. import config

def send_sms(content, phone):
    if(content == ""):
        return False
    
    client = Client(config.account, config.token)
    message = client.messages.create(to=phone, from_ = config.phone, body=content)
    
    return True


mail_host=config.mail_host
mail_user=config.mail_user
mail_pass=config.mail_pass

def sendEmail(content, address):
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = Header("UCLA Class Assistant", 'utf-8')
    message['To'] =  Header("Kepler", 'utf-8')
    message['Subject'] = Header("Class Update", 'utf-8')
    try:
        receivers = ["chenkaiyuan@ucla.edu"]
        sender = "chenkaiyuan@ucla.edu"
        receivers.append(address)
        smtpObj = smtplib.SMTP('smtp.mailgun.org', 587)
        smtpObj.login(mail_user,mail_pass)
        print receivers
        print address
        smtpObj.sendmail(sender, receivers, message.as_string())
        smtpObj.quit()
        return True
    except:
        return False
