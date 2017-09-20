#! /usr/bin/python

import requests
from bs4 import BeautifulSoup

TERM = '17F'

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

def get_class_info_basic(index):
    #initialize variables
    #https://sa.ucla.edu/ro/Public/SOC/Results/ClassDetail?term_cd=17F&subj_area_cd=MATH%20%20%20&crs_catlg_no=0170A%20%20%20&class_id=262660210&class_no=%20002%20%20
    #https://sa.ucla.edu/ro/Public/SOC/Results/ClassDetail?term_cd=17F&subj_area_cd=MATH%20%20%20&crs_catlg_no=0170A%20%20%20&class_id=262660200&class_no=%20001%20%20
    #
    
    URL = 'https://sa.ucla.edu/ro/public/soc/Results?t='+TERM+'&sBy=classidnumber&id='+index+'&undefined=Go&btnIsInIndex=btn_inIndex'
    soup = get_web_page(URL)
    text = str(soup.find_all('p')) #find all tags
    loc1 = text.find("n<a href=\"") + 10
    loc2 = text.find("20\" target=") + 2
    string = "https://sa.ucla.edu" + text[loc1:loc2]
    string = string.replace("amp;", "")
    return string
    
def main():
    URL = get_class_info_basic("262660200")
    #print URL
    print get_web_page(URL)

if __name__ == "__main__":
    main()
