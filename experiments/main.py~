#!/usr/local/cs/bin/python3
import time
import os
import datetime
import subprocess

def process():
    time_stamp = "{} : {}".format(os.getpid(), str(datetime.datetime.now()))
    print(time_stamp)
    with open("./log", "a") as log:
        log.write(time_stamp + "\n")
        log.close()

def main():
    counter = 0
    while True:
        process()
        time.sleep(2)
        counter += 1
        if(counter == 4):
            child =subprocess.call(['./script.sh'])
            print(child)
            if(child == 0):
                time.sleep(1)

if __name__ == "__main__":
    main()
