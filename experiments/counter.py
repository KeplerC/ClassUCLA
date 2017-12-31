#!/usr/bin/python
import time
import os
import datetime
import subprocess

start = datetime.datetime.now()

def process():
    time_stamp = ('{}: (hh:mm:ss.ms) {}'.format(datetime.datetime.now(), datetime.datetime.now()-start))
    print(time_stamp)
    with open("./still_alive_log", "a") as log:
        log.write(time_stamp + "\n")
        log.close()

def main():
    counter = 0
    while True:
        process()
        time.sleep(2)
        
if __name__ == "__main__":
    main()
