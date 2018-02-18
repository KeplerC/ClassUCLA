#!/usr/bin/python
import json

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
        d["list"] = ["262458200"]
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
if __name__ == "__main__":
    person = raw_input('Name: ')
    this_person_exists(person)
    with open("../data/"+person+".json") as datafile:
        data= json.load(datafile)
        cl = raw_input('class: ')
        data["list"].append(cl)
