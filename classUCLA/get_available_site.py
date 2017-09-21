#! /usr/bin/python
import requests
from bs4 import BeautifulSoup
TERM = '17F'
fail_list = []

def find_valid_course_list(begin, end, step):
    total = (end - begin)/step
    done = 0
    fsuccess = open("success", "w")
    ffail = open("Fail", "w")
    while begin < end:
        URL = get_class_info_basic(str(begin))
        if len(URL) > 30:
            update(URL, "Success", fsuccess)
        else:
            update(begin, "Failed", ffail)
        
        done += 1
        if done % 10 == 0:
            print str(done * 100 /total) + "%"
        begin = begin + step
    return task

# Get web page and build a soup
def get_web_page(URL):
    try:
        #print URL
        r = requests.get(URL)
    except:
        fail_list.append(URL)
        print "failed on" + URL
    try:
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup
    except:
        print "Failure Creating Soup"

def update(ID, status, file_descriptor):
    if status == "Success":
        file_descriptor.write(ID + "\n")
    else:
        file_descriptor.write(str(ID) + "\n")
    
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


def main():
    find_valid_course_list(000000000, 400000000, 1)

if __name__ == "__main__":
    main()
