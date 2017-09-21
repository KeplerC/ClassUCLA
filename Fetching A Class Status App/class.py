#! /usr/bin/python

import requests
from bs4 import BeautifulSoup

TERM = '17F'
CLASS_ID = '263030210'

def getOpenSeats():
    URL = 'https://sa.ucla.edu/ro/public/soc/Results?t='+TERM+'&sBy=classidnumber&id='+CLASS_ID+'&undefined=Go&btnIsInIndex=btn_inIndex'
    try:
        r = requests.get(URL)
    except:
        print("Check your input")

    try:
        soup = BeautifulSoup(r.text, 'html.parser')
    except:
        print("parser failed")

    #string processing    
    text = soup.find_all('p') #find all tags
    flag = -1
    printed = False #a flag for printing class names
    ostream = ""
    for i in range(len(text)):
        string = str(text[i])
        #print(string)
        if flag != -1:
            #print(string)
            #message parsers
            try:
                loc1 = string.find("</i>")+4
                loc2 = string.find("<br/>")
                loc3 = string.find("</p>")
            except:
                print("cannot parse the website")
            #output stream
            if loc2 == -1: #class is cancelled
                ostream+=" is cancelled \n"
            else:
                msg1 = string[loc1: loc2]
                msg2 = string[loc2+5: loc3]
                ostream+=" is " + msg1
                ostream+=". Its status is "+msg2+"\n"
            flag = -1
        if string.find("Lec") != -1:
            #print(string)
            i+=1        #jump two lines
            flag = 0    #found it
        if string.find("Dis") != -1 and len(string) > 200:
            #print(string)
            i+=1        #jump two lines
            flag = 1    #found it
        if flag != -1 and printed == False:
            printed = True
            try:
                loc1 = string.find("subj_area_cd=") + 13 #class title
                loc2 = string.find("%20")
                loc3 = string.find("catlg_no=") + 10  #class number
                loc4 = string.find("%20", loc3) #find next after loc3
            except:
                print("cannot parse the website")
            
            ostream += string[loc1 : loc2]
            ostream += " "
            if string[loc3] == '0':
                loc3 += 1
            ostream += string[loc3 : loc4]
            ostream += '\n'
        if flag != -1:
            loc1 = string.find("</a>")
            loc2 = loc1 - 6         
            if(string[loc2] == '>'):
                loc2 += 1
            msg = string[loc2 : loc1]
            
            ostream += string [loc2 : loc1]
            
    print(ostream)
            
if __name__ == '__main__':
    ID = str(raw_input("Please enter class ID\n")).strip()
    if(ID != ""):
        CLASS_ID = ID
    getOpenSeats()
#    except:
#        print("Invalid Input")
