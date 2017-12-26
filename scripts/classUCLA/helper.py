# !/usr/bin/python

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
