#!/usr/bin/python
import json

def this_person_exists(person):
    with open("data/index.json","r+") as datafile:
        data = json.load(datafile)
        names = data["list"] 
        if(person in names):
            return True
        datafile.seek(0)
        datafile.truncate()
        data["list"] = names
        datafile.write(json.dumps(data))
        f = open("data/" + person + ".json","w+")
        d = dict()
        d["name"] = person
        d["email"] = ""
        d["list"] = []
        d["phone"] = "+14245356503"
        f.close()
        return False
        
import sys
if __name__ == "__main__":
    person = raw_input('Name: ')
    this_person_exists(person)
    with open("data/"+person+".json") as datafile:
        data= json.load(datafile)
        cl = raw_input('class: ')
        data["list"].append(cl)