#! /usr/bin/python

TERM = '18S'

import requests
from bs4 import BeautifulSoup

#wrapper class for class information
class Class:
    def __init__(self, index):
        self.index = index
        self.info = get_detailed_class_info(self.index)
        self.ostream = self.print_open_seats()
    def print_open_seats(self):
        ostream = self.info["subject"] + " " + self.info["course_number"] + " " + self.info["course_title"] + "\n"
        ostream += "The status is " + self.info["status"]
        ostream += "\nIts waitlist status is " + self.info["waitlist_status"] + "\n"
        self.ostream = ostream
        return ostream
    def is_available(self):
        return (not "Closed" in self.info["status"])
    def get_info(self):
        return self.info
    def get_ostream(self):
        return self.ostream

def get_open_seats(index):
    #string processing    
    info = get_detailed_class_info(index)
    ostream = info["subject"] + " " + info["course_number"] + " " + info["course_title"] + "\n"
    ostream += "The status is " + info["status"]
    ostream += "\nIts waitlist status is " + info["waitlist_status"] + "\n"
    return info, ostream 


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


from collections import OrderedDict
def get_detailed_class_info(index):
    soup = get_web_page(get_class_info_basic(index))
    text = str(soup.find_all('p')) #find all tags

    info = OrderedDict()
    loc1 = 0
    loc2 = 0
    #Search and Store subject name
    loc1 = text.find("    ")+5
    loc2 = text.find(" ", loc1)
    info["subject"] = text[loc1:loc2]

    #Search and Store course catalog number
    loc1 = loc2 + 3
    if(text[loc1] == " "):
        loc1 +=1  
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
    return info


import pandas as pd
def create_data_frame(list):
    df = pd.DataFrame(list)
    return df

def write_to_excel(df):
    writer = pd.ExcelWriter('example.xlsx', engine='xlsxwriter')
    df.to_excel('class_info.xlsx', 'Sheet1')
    writer.save()

#Helper Functions

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
    if (string == "N/A" != -1):
        return None
    elif (string == "No" != -1):
        return None
    elif (string.find("None") != -1):
        return None
    elif string.find("does not") != -1:
        return None
    else:
        return string
