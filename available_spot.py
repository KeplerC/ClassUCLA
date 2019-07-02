#!/usr/bin/python

import requests
from bs4 import BeautifulSoup

import smtplib
from email.mime.text import MIMEText
from email.header import Header

def getOpenSeats(index):
    if(index == ""):
        return None
    URL = 'https://sa.ucla.edu/ro/public/soc/Results?t='+TERM+'&sBy=classidnumber&id='+index+'&undefined=Go&btnIsInIndex=btn_inIndex'
    try:
        r = requests.get(URL)
    except:
        print("Check your input")

    try:
        soup = BeautifulSoup(r.text, 'html.parser')
    except:
        print("parser failed")

    #string processing    
    text = soup.find_all('p') #find all tags
    flag = -1
    printed = False #a flag for printing class names
    ostream = ""
    #print(text)
    have_seats = False
    for i in range(len(text)):
        string = str(text[i])
        #print(string)
        if flag != -1:
            #print(string)
            #message parsers
            try:
                loc1 = string.find("</i>")+4
                loc2 = string.find("<br/>")
                loc3 = string.find("</p>")
            except:
                print("cannot parse the website")
            #output stream
            if loc2 == -1: #class is cancelled
                ostream+=" is cancelled \n"
            else:
                msg1 = string[loc1: loc2]
                msg2 = string[loc2+5: loc3]
                ostream+=" is " + msg1
                #print(msg1)
                if(msg1.find("Closed") == -1):
                    have_seats = True
                msg2 = msg2.replace("<br/>", " with ");
                if(msg1.find("Open") != -1):
                    ostream+=": "+msg2+"\n"
                else:
                    ostream+= ": "+str(text[i+1])[3:-4] + "\n"
            flag = -1
        if string.find("Lec") != -1:
            #print(string)
            i+=1        #jump two lines
            flag = 0    #found it
        if string.find("Dis") != -1 and len(string) > 200:
            #print(string)
            i+=1        #jump two lines
            flag = 1    #found it
        if flag != -1 and printed == False:
            printed = True
            try:
                loc1 = string.find("subj_area_cd=") + 13 #class title
                loc2 = string.find("%20")
                loc3 = string.find("catlg_no=") + 10  #class number
                loc4 = string.find("%20", loc3) #find next after loc3
            except:
                print("cannot parse the website")
            
            s = string[loc1 : loc2].split("&")[0]
            ostream += s
            ostream += " "
            if string[loc3] == '0':
                loc3 += 1
            ostream += string[loc3 : loc4]
            ostream += '\n'
        if flag != -1:
            loc1 = string.find("</a>")
            loc2 = loc1 - 6         
            if(string[loc2] == '>'):
                loc2 += 1
            msg = string[loc2 : loc1]
            
            ostream += string [loc2 : loc1]
    if(have_seats == False):
        return None
    return ostream 

mail_host="smtp.mailgun.org"
mail_user="postmaster@mg.keplerc.com"
mail_pass="bd7ed1bb6605599dd5251e1ca952efb3-4412457b-790af2ae"
#mail_host = "email-smtp.us-east-1.amazonaws.com"
#mail_user = "AKIAIJWZXSBNAMJHV2VA"
#mail_pass = "AuYUdbO0gBEwtShshVSa3XM3OkrAZfx5qdF4uarUq/m7"

TERM = '19S'
#CLASS_ID = ["262447200", "262576200"]
#RECEIVER="Kaiyuan Chen"
#RECEIVER_ADDR='chenkaiyuan@ucla.edu'

def sendEmail(content, address):
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = Header("UCLA Class Assistant", 'utf-8')
    message['To'] =  Header("Kepler", 'utf-8')
    message['Subject'] = Header("Class Update", 'utf-8')

    receivers = [str(address), "keplerc98@yahoo.com"]
    sender = "kc@keplerc.com"
    #receivers.append(address)
    smtpObj = smtplib.SMTP(mail_host, 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.ehlo()
    smtpObj.login(mail_user,mail_pass)
    print receivers
    print address
    smtpObj.sendmail(sender, receivers, message.as_string())
    smtpObj.quit()
    print "success"

import time
import json
if __name__ == '__main__':
    sendEmail("what", "")
    # with open ('./index.json') as data_file:
    #     data = json.load(data_file)
    #     names = data['list']
        
    # for name in names:
    #     path = './' + name + '.json'
    #     with open(path) as data_file:
    #         data = json.load(data_file)
    #         send_email_to(data)
