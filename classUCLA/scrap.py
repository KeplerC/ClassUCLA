#! /usr/bin/python

import requests
from bs4 import BeautifulSoup

TERM = '17F'

# Get web page and build a soup
def get_web_page(URL):    
    try:
        r = requests.get(URL)
    except:
        print("check your input")
        
    try:
        soup = BeautifulSoup(r.text, 'html.parser')
    except:
        print("parser failed")
    return soup

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
import pandas as pd
def get_class_info_detailed(URL):
    soup = get_web_page(URL)
    text = str(soup.find_all('p')) #find all tags
    info = dict()
    loc1 = 0
    loc2 = 0

    loc1 = text.find("    ")+5
    loc2 = text.find(" ", loc1)
    info["subject"] = text[loc1:loc2]

    loc1 = loc2 + 4
    loc2 = text.find(" ", loc1)
    info["course_number"] = text[loc1:loc2] 

    loc1 = text.find(" - ", loc2) + 3
    loc2 = text.find("</p>", loc1)
    info["course_title"] = text[loc1: loc2]

    loc1 = text.find("<a href=", loc2) + 9
    loc2 = text.find(">", loc1)
    info["courser_website"] = text[loc1: loc2]

    loc1 = text.find("Instructor(s)", loc2) + 26
    loc2 = text.find("</", loc1)
    info["status"] = text[loc1: loc2]
    
    loc1 = text.find("<p>", loc2) + 3
    loc2 = text.find("</", loc1)
    info["waitlist_status"] = text[loc1: loc2]

    loc1 = text.find("data-content", loc2) + 14
    loc2 = text.find("\" ", loc1)
    info["days"] = text[loc1: loc2]

    loc1 = text.find(", <p>", loc2) + 5
    loc2 = text.find("</p>", loc1)
    info["time"] = text[loc1: loc2]

    loc1 = text.find(", <p>", loc2) + 5
    loc2 = text.find("</p>", loc1)
    info["location"] = text[loc1: loc2]

    loc1 = text.find(", <p>", loc2) + 5
    loc2 = text.find("</p>", loc1)
    info["units"] = text[loc1: loc2]

    loc1 = text.find(", <p>", loc2) + 5
    loc2 = text.find("</p>", loc1)
    info["Instructor"] = text[loc1: loc2]

    loc1 = text.find("(s)</p>, <p>", loc2) + 12
    loc2 = text.find("</p>", loc1)
    info["final_date"] = text[loc1: loc2]
    
    loc1 = text.find(", <p>", loc2) + 5
    loc2 = text.find("</p>", loc1)
    info["final_weekday"] = text[loc1: loc2]

    loc1 = text.find(", <p>", loc2) + 5
    loc2 = text.find("</p>", loc1)
    info["final_time"] = text[loc1: loc2]
    
    loc1 = text.find(", <p>", loc2) + 5
    loc2 = text.find("</p>", loc1)
    if text[loc1] == "C":
        info["final_location"] = None
    else:
        info["final_location"] = text[loc1 : loc2]

    loc1 = text.find("Level</p>, <p>", loc2) + 14
    loc2 = text.find("</p>", loc1)
    info["grade_type"] = text[loc1: loc2]

    loc1 = text.find(", <p>", loc2) + 5
    loc2 = text.find("</p>", loc1)
    info["restriction"] = text[loc1: loc2]

    
    loc1 = text.find(", <p>", loc2) + 5
    loc2 = text.find("</p>", loc1)
    info["impacted"] = text[loc1: loc2]


    loc1 = text.find(", <p>", loc2) + 5
    loc2 = text.find("</p>", loc1)
    info["individual_studies"] = text[loc1: loc2]

    
    loc1 = text.find(", <p>", loc2) + 5
    loc2 = text.find("</p>", loc1)
    info["level"] = text[loc1: loc2]

    #TODO: Prerequisites

    
    loc1 = text.find("breakLongText\">", loc2) + 15
    loc2 = text.find("</p>", loc1)
    info["course_description"] = text[loc1: loc2]

    loc1 = text.find("breakLongText\">", loc2) + 15
    loc2 = text.find("</p>", loc1)
    info["class_description"] = text[loc1: loc2]

    
    loc1 = text.find("breakLongText\">", loc2) + 15
    loc2 = text.find("</p>", loc1)
    info["GE"] = text[loc1: loc2]

    
    loc1 = text.find("breakLongText\">", loc2) + 15
    loc2 = text.find("</p>", loc1)
    info["writing_II"] = text[loc1: loc2]

    loc1 = text.find("breakLongText\">", loc2) + 15
    loc2 = text.find("</p>", loc1)
    info["diveristy"] = text[loc1: loc2]

    #TODO? class notes
    return info
    
def main():
    #URL = get_class_info_basic("262660200")
    #print URL
    get_class_info_detailed("https://sa.ucla.edu/ro/Public/SOC/Results/ClassDetail?term_cd=17F&subj_area_cd=MATH%20%20%20&crs_catlg_no=0170A%20%20%20&class_id=262660210&class_no=%20002%20%20")

if __name__ == "__main__":
    main()
