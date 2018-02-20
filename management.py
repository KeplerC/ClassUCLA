#!/usr/bin/python
import json
from available_spot import *
def this_person_exists(person):
    with open("../data/index.json","r+") as datafile:
        data = json.load(datafile)
        names = data["list"] 
        if(person in names):
            return True
        datafile.seek(0)
        datafile.truncate()
        data["list"].append(person)
        datafile.write(json.dumps(data))
        f = open("../data/" + person + ".json","w+")
        d = dict()
        d["name"] = person
        d["email"] = ""
        d["list"] = [""]
        d["phone"] = "+14245356503"
        f.write(json.dumps(d))
        f.close()
        return False

def class_remove(person, class_id):
    with open("../data/"+person+".json","r+") as datafile:
        data = json.load(datafile)
        names = data["list"]
        names.remove(class_id)
        datafile.seek(0)
        datafile.truncate()
        datafile.write(json.dumps(data))

import sys
import csv
if __name__ == "__main__":
    # person = raw_input('Name: ')

    with open("../data/ClassUCLA RSVP (Responses) - Form Responses 1.csv",'rb') as csvfile:
        data = csv.reader(csvfile)
        counter = 0
        for s in data:
            print(s)
            if(s[2] == "Preferred Name"):
                continue
            person = s[2]
            this_person_exists(person)
            classid = s[3]
            phone = s[4]
            email = s[1]
            ret = getOpenSeats(classid)
            if(ret == ""):
                print(person + " wrong class id " + classid)
                continue
            
            with open("../data/"+person+".json", "r+") as profile:
                prof = json.load(profile)
                if(classid in prof["list"]):
                    continue
                prof["list"].append(classid)
                prof["phone"] = "+1" + phone
                prof["email"] = email
                profile.seek(0)
                profile.truncate()
                profile.write(json.dumps(prof))
                
