#! /usr/bin/python

import requests
from bs4 import BeautifulSoup

TERM = '17F'

# Get web page and build a soup
def get_web_page(URL):    
    try:
        r = requests.get(URL)
    except:
        print "failure loading searching page"
        
    try:
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup
    except:
        print "Failure Creating Soup"

# get URL for detailed website
def get_class_info_basic(index):
    #initialize variables
    URL = 'https://sa.ucla.edu/ro/public/soc/Results?t='+TERM+'&sBy=classidnumber&id='+index+'&undefined=Go&btnIsInIndex=btn_inIndex'
    soup = get_web_page(URL)
    text = str(soup.find_all('p')) #find all tags
    loc1 = text.find("n<a href=\"") + 10
    loc2 = text.find("20\" target=") + 2
    string = "https://sa.ucla.edu" + text[loc1:loc2]
    string = string.replace("amp;", "")
    return string

''' order: 0subject, 1course number, 2title, 3website, 4status, 5waitlist status, 6days, 7time, 8location, 9units, 10instructor, 11final_exam_day, 12final_exam_weekday, 13final_exam_time, 14final_exam_avail, 15grade_type, 16restriction, 17impacted, 18individual studies, 19level, 20 requisite //TODO, 21course description, 22class description, 23GE requirement, 24writingII requirement, 25diversity requirement, 26class notes
'''

#extract features
from collections import OrderedDict
def get_class_info_detailed(URL):
    soup = get_web_page(URL)
    print "success loading URL"
    text = str(soup.find_all('p')) #find all tags
    info = OrderedDict()
    loc1 = 0
    loc2 = 0

    #Search and Store subject name
    loc1 = text.find("    ")+5
    loc2 = text.find(" ", loc1)
    info["subject"] = text[loc1:loc2]

    #Search and Store course catalog number
    loc1 = loc2 + 4
    loc2 = text.find(" ", loc1)
    info["course_number"] = text[loc1:loc2] 

    #Search and Store course title
    loc1 = text.find(" - ", loc2) + 3
    loc2 = text.find("</p>", loc1)
    info["course_title"] = text[loc1: loc2]

    #Search and Store course website
    loc1 = text.find("<a href=", loc2) + 9
    loc2 = text.find(">", loc1)
    info["course_website"] = text[loc1: loc2]

    #Instructors
    loc1 = text.find("Instructor(s)", loc2) + 26
    loc2 = text.find("</", loc1)
    info["status"] = text[loc1: loc2]

    #Search and Store WL status
    loc1 = text.find("<p>", loc2) + 3
    loc2 = text.find("</", loc1)
    info["waitlist_status"] = text[loc1: loc2]

    #Search and Store days
    loc1 = text.find("data-content", loc2) + 14
    loc2 = text.find("\" ", loc1)
    day = text[loc1: loc2]
    info["day"] =convert_to_weekday(day)

    #Search and Store time
    loc1 = text.find(", <p>", loc2) + 5
    loc2 = text.find("</p>", loc1)
    info["time"] = text[loc1: loc2]

    #Search and Store location
    loc1 = text.find(", <p>", loc2) + 5
    loc2 = text.find("</p>", loc1)
    info["location"] = text[loc1: loc2]

    #Search and Store units
    loc1 = text.find(", <p>", loc2) + 5
    loc2 = text.find("</p>", loc1)
    info["units"] = text[loc1: loc2]

    #Search and Store instructor
    loc1 = text.find(", <p>", loc2) + 5
    loc2 = text.find("</p>", loc1)
    info["Instructor"] = text[loc1: loc2]

    #Search and Store final date 
    loc1 = text.find("(s)</p>, <p>", loc2) + 12
    loc2 = text.find("</p>", loc1)
    info["final_date"] = text[loc1: loc2]

    #Search and Store final week day
    loc1 = text.find(", <p>", loc2) + 5
    loc2 = text.find("</p>", loc1)
    info["final_weekday"] = convert_to_weekday(text[loc1: loc2])
    
    #Search and Store final time 
    loc1 = text.find(", <p>", loc2) + 5
    loc2 = text.find("</p>", loc1)
    info["final_time"] = text[loc1: loc2]

    #Search and Store final location
    loc1 = text.find(", <p>", loc2) + 5
    loc2 = text.find("</p>", loc1)
    if text[loc1] == "C":
        info["final_location"] = None
    else:
        info["final_location"] = text[loc1 : loc2]

    # search and store grade type pnp or letter
    loc1 = text.find("Level</p>, <p>", loc2) + 14
    loc2 = text.find("</p>", loc1)
    type = text[loc1: loc2]
    info["grade_type"] = ""
    if type.find("Pass") != -1:
        info["grade_type"] += "PNP "
    if type.find("Letter") != -1:
        info["grade_type"] += "Letter"

    # search and store restriction
    loc1 = text.find(", <p>", loc2) + 5
    loc2 = text.find("</p>", loc1)
    info["restriction"] = isNone(text[loc1: loc2])

    
    loc1 = text.find(", <p>", loc2) + 5
    loc2 = text.find("</p>", loc1)
    info["impacted"] = isNone(text[loc1: loc2])


    loc1 = text.find(", <p>", loc2) + 5
    loc2 = text.find("</p>", loc1)
    info["individual_studies"] = isNone(text[loc1: loc2])

    
    loc1 = text.find(", <p>", loc2) + 5
    loc2 = text.find("</p>", loc1)
    type = text[loc1: loc2]
    info["level"] = get_class_level(type)

    #TODO: Prerequisites
    
    loc1 = text.find("breakLongText\">", loc2) + 15
    loc2 = text.find("</p>", loc1)
    info["course_description"] = text[loc1: loc2]

    loc1 = text.find("breakLongText\">", loc2) + 15
    loc2 = text.find("</p>", loc1)
    info["class_description"] = text[loc1: loc2]

    
    loc1 = text.find("breakLongText\">", loc2) + 15
    loc2 = text.find("</p>", loc1)
    info["GE"] = isNone(text[loc1: loc2])

    
    loc1 = text.find("breakLongText\">", loc2) + 15
    loc2 = text.find("</p>", loc1)
    info["writing_II"] = isNone(text[loc1: loc2])

    loc1 = text.find("breakLongText\">", loc2) + 15
    loc2 = text.find("</p>", loc1)
    info["diveristy"] = isNone(text[loc1: loc2])

    #TODO? class notes
    return info

import pandas as pd
def create_data_frame(list):
    df = pd.DataFrame(list)
    return df

def write_to_excel(df):
    writer = pd.ExcelWriter('example.xlsx', engine='xlsxwriter')
    df.to_excel('test.xlsx', 'Sheet1')
    writer.save()

def convert_to_weekday(string):
    loc = 0
    day = ""
    if string.find("M") != -1:
        day += "M "
    if string.find("Tu") != -1:
        day += "Tu "
    if string.find("W") != -1:
        day += "W "
    if string.find("Th") != -1:
        day += "Th "
    if string.find("F") != -1:
        day += "F "
    if string.find("Sat") != -1:
        day += "Sat "
    if string.find("Sun") != -1:
        day += "Sun "
    return day

def get_class_level(string):
    if string[0] == "U":
        return "Upper"
    elif string[0] == "L":
        return "Lower"
    elif string[0] == "G":
        return "Graduate"
    else:
        return string

def isNone(string):
    if string == "N/A":
        return None
    elif string == "No":
        return None
    elif string.find("None"):
        return None
    elif string.find("does not") != -1:
        return None
    else:
        return string

def find_valid_course_list(begin, end, step):
    task = []
    total = (end - begin)/step
    done = 0
    while begin < end:
        URL = get_class_info_basic(str(begin))
        if len(URL) > 30:
            print begin
            task.append(URL)
        done += 1
        if done % 10 == 0:
            print done * 100 /total
        begin = begin + step
    return task

def main():
    find_valid_course_list(262660000, 262660300, 10)
    
def main1():
    l = list()
    tasks = ["262660260"]
    for t in tasks:
        l.append(get_class_info_detailed(URL))
    try:
        df = create_data_frame(l)
        write_to_excel(df)
        print df
    except:
        print("ERR")

if __name__ == "__main__":
    main1()
