#!/usr/bin/python
import json
from available_spot import *
PATH = "/home/ubuntu/"

def this_person_exists(person):
    with open(PATH + "data/index.json","r+") as datafile:
        data = json.load(datafile)
        names = data["list"] 
        if(person in names):
            return True
        datafile.seek(0)
        datafile.truncate()
        data["list"].append(person)
        datafile.write(json.dumps(data))
        f = open(PATH + "data/" + person + ".json","w+")
        d = dict()
        d["name"] = person
        d["email"] = ""
        d["list"] = [""]
        d["phone"] = "+14245356503"
        f.write(json.dumps(d))
        f.close()
        return False

def class_remove(person, class_id):
    with open(PATH + "data/"+person+".json","r+") as datafile:
        data = json.load(datafile)
        names = data["list"]
        names.remove(class_id)
        if "completed" in data:
            data["completed"].append(class_id)
        else:
            data["completed"] = [class_id]
        datafile.seek(0)
        datafile.truncate()
        datafile.write(json.dumps(data))

def import_from_csv(path):
    ostream = ""
    with open(path,'rb') as csvfile:
        data = csv.reader(csvfile)
        counter = 0
        for s in data:
            if(s[2] == "Preferred Name"):
                continue
            person = s[2]
            this_person_exists(person)
            classid1 = s[3]
            classid2 = s[5]
            classid3 = s[6]
            phone = s[4]
            email = s[1]            
            with open(PATH + "data/"+person+".json", "r+") as profile:
                prof = json.load(profile)
                for classid in [classid1, classid2, classid3]:
                    if(classid in prof["list"]):
                        continue
                    ret = getOpenSeats(classid)
                    if(ret == ""):
                        print(person + " wrong class id " + classid)
                        continue
                    prof["list"].append(classid)
                    prof["phone"] = "+1" + phone
                    prof["email"] = email
                    profile.seek(0)
                    profile.truncate()
                    profile.write(json.dumps(prof))
                    counter += 1
                    print("added " + person)
                ostream += person + " " + classid+ "\n"
    print("total added: " + str(counter))
    return counter, ostream

import sys
import csv
if __name__ == "__main__":
    # person = raw_input('Name: ')
    import_from_csv("../data/ClassUCLA RSVP (Responses) - Form Responses 1.csv")
