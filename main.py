#!/usr/bin/python
import time
import os
import datetime
from available_spot import *
import subprocess
from sms import *

import time
def get_ostream(data, empty_send = False):
    should_send = False
    ostream='''Dear, 
Your Class is Available: 
'''
    ostream+='\n'
    for ID in data["list"]:
        stream = getOpenSeats(ID)
        if(stream == None or stream == ""):
            continue
        else:
            should_send = True
            ostream+= stream
            ostream+='\n'
    ostream+='''

B.R.
Kepler :)'''
    return ostream, should_send
    
def send_to(data, mean = "sms"):
    ostream, should_send = get_ostream(data)
    if(should_send):
        if(mean == "email"):
            sendEmail(ostream, data["email"])
        if(mean == "sms"):
            send_sms(ostream, data["phone"])
    else:
        print("Full")
        print(time.asctime(time.localtime(time.time())))
        log_file = open("./log.txt", 'a')
        log_file.write(time.asctime(time.localtime(time.time())))
        log_file.write("  FULL\n")
        log_file.close()


def management():
    with open("data/index.json","w") as datafile:
        data = dict()
        data["list"] = ["kepler"]
        datafile.write(json.dumps(data))
    

def process():
    with open ('data/index.json') as data_file:
        data = json.load(data_file)
        names = data['list']
        
    for name in names:
        path = 'data/' + name + '.json'
        with open(path) as data_file:
            data = json.load(data_file)
            send_to(data)
    time_stamp = "{} : {}\n".format(os.getpid(), str(datetime.datetime.now()))
    with open("./log.txt", "a") as log:
        log.write(time_stamp)
        log.close()

def main():
    counter = 0
    while True:
        process()
        time.sleep(3600)
        counter += 1
        if(counter == 23):
            child =subprocess.call(['./script.sh'])
            print(child)
            if(child == 0):
                time.sleep(1)


if __name__ == "__main__":
    main()
