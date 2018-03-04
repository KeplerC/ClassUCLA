#!/usr/bin/python
import time
import os
import datetime
from available_spot import *
import subprocess
from sms import *
from management import *
import time

PATH = "/home/ubuntu/"
def get_ostream(data, empty_send = False):
    should_send = False
    ostream='Your class\'s ready\n'
    print(data["name"])
    for ID in data["list"]:
        print(ID)
        stream = getOpenSeats(ID)
        if(stream == None or stream == ""):
            continue
        else:
            k = stream.split("\n")
            stream = k[0] + "\n" + k[1] + "\n"
            if(stream.find("Open") == -1 and stream.find("Waitlist") == -1):
                continue
            if(stream.find("Closed: No Waitlist") != -1):
                continue
            for i in k[2:]:
                if(i.find("Open") != -1 or i.find("Waitlist: ") != -1):
                   stream += i
                   stream += "\n"
            ostream+= stream
            should_send = True
            class_remove(data["name"], ID)
    ostream+='''If full again, wx me.\nKepler'''
    return ostream, should_send
    
def send_to(data, mean = "sms"):
    ostream, should_send = get_ostream(data)
    if(should_send):
        send_sms(ostream, data["phone"])
        ostream += data["name"]
        sendEmail(ostream, "")
        print(ostream)
        log_file = open(PATH + "ClassUCLA/log.txt", 'a')
        log_file.write(time.asctime(time.localtime(time.time())))
        log_file.write(ostream)
        log_file.write(data["name"] + str(data["list"]) + "\n")
        log_file.close()    
    else:
        print("Full")
        print(time.asctime(time.localtime(time.time())))
        log_file = open(PATH + "ClassUCLA/log.txt", 'a')
        log_file.write(time.asctime(time.localtime(time.time())))
        log_file.write("  FULL\n")
        log_file.write(data["name"] + str(data["list"]) + "\n")
        log_file.close()    

def process():
    with open (PATH + 'data/index.json') as data_file:
        data = json.load(data_file)
        names = data['list']
        
    for name in names:
        path = PATH + 'data/' + name + '.json'
        with open(path) as data_file:
            data = json.load(data_file)
            send_to(data)
    time_stamp = "{} : {}\n".format(os.getpid(), str(datetime.datetime.now()))
    with open(PATH + "ClassUCLA/log.txt", "a") as log:
        log.write(time_stamp)
        log.close()

def main():
    counter = 0
    while True:
        process()
        #time.sleep(3600)
        counter += 1
        # if(counter == 10):
        #     child =subprocess.call(['./script.sh'])
        #     print(child)
        #     if(child == 0):
        #         time.sleep(randrange(0, 1000))


if __name__ == "__main__":
    #main()
    process()
