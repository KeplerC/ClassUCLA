2#!/usr/bin/python
import time
import os
import datetime
from available_spot import *
from daily_report import * 
import subprocess


def management():
    with open("./index.json","w") as datafile:
        data = dict()
        data["list"] = ["kepler"]
        datafile.write(json.dumps(data))
    

def process():
    with open ('./index.json') as data_file:
        data = json.load(data_file)
        names = data['list']
        
    for name in names:
        path = './' + name + '.json'
        with open(path) as data_file:
            data = json.load(data_file)
            send_email_to(data)
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
