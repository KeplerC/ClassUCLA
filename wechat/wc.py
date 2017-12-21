#!/usr/bin/python
import re
from wxpy import *
from iclass import Class as c
from iclass import *

bot = None
JSON_PATH='.'
DLMT = "dgqk"
INSTR = '''
Welcome. 
为了与我正常的信息分开，请使用这个功能的时候在信息前面加上dgqk（大哥抢课）
例如：dgqkl 
下面是使用指南。
dgqk 可以重新显示本条消息
dgqk+
    a+9位课号 把相应的课加入scan列表，如dgqka187780200,可以帮你scan下学期CS180
    r+9位课号 从scan列表中移除该课
    d 开启/关闭daily report
    l 查report/在抢的课程 
其他功能，例如设置，会陆续更新中。
欢迎提各种意见/帮忙找bug
谢谢
'''
@bot.register(my_friend, TEXT, except_self=False)
def reply_my_friend(msg):
    return process_text(msg)
    #return 'received: {} ({})'.format(msg.text, msg.type)

import json
import os
'''
Respond to the text message 
User Interface 
'''
def process_text(msg):
    #not related
    text = msg.text.strip(' ').lower()
    if(text[:3] != DLMT):
        return None

    text = text[4:]
    ostream = ""

    #load json file    
    usr = msg.receiver
    path = JSON_PATH +usr+".json"
    if(os.path.exists(path)):
        with open(path) as datafile:
            data = json.load(datafle)
    else:
        '''Create a new profile 
        Name: user's wechat name
        class_list: a list of 9 digit string as class id
            which will verify when typed in 
        daily report: choose to report or not report
            TODO: later might change to specific time
        times: how many times that is scanner checks for you
            mostly placebo and debug use
        '''
        data = {"name":usr, "class_list":list(),"daily_report": True, "times": 0]
        with open(JSON_PATH + "/index.json") as datafile:
            indices = json.load(datafile)
            indices["usrs"].append(usr)
            #TODO: store json

    if(text[0] == 'a'):
        add_list = re.findall(r"\b\d{9}\b",text)
        for num in add_list:
            if(num in data["class_list"]):
                continue
            s = iclass.get_class_info_basic(num)
            if("Non results" in s):
               ostream += "No class as {}\n".format(num)
            else:
               data["class_list"].append(num)
               ostream += "Added {}\n".format(num)
    if(text[0] == 'r'):
        remove_list = re.findall(r"\b\d{9}\b",text)
        for num in remove_list:
            data["class_list"].remove(num)
        ostream += "Class ID with {} is removed\n".format(num)
    if(text[0] == 'd'):
        data["daily_report"] = not data["daily_report"]
        if(data["daily_report"]):
            ostream += "Now daily report status is on\n"
        else:
            ostream += "Now daily report status is off\n"
    if(text[0] == 'l'):
        ostream += report_to_usr(data)
        if(ostream == ""):
            ostream += "No class in the list. Please type dgqka + 9 digit class id to get started!"
    #TODO: store json file
    if(ostream == ""):
        ostream = INSTR
    return ostream

def report_to_usr(usr, only_available = False):
    ostream = ""
    for c in usr["class_list"]:
        new_class = iclass.Class(c)
        if(only_available):
            if(new_class.is_available()):
                class_info = new_class.get_info()
                ostream +="Your {} {} is available! Now its status is {}. To stop scanning for this class, please reply dgqkr{}"
                    .format(class_info["subject"], class_info["course_number"], class_info["status"], class_info["number"])
            pass #TODO: print class is available information
        else:    
            ostream += new_class.print_open_seats()
    send_to_usr(ostream)


def send_to_usr(usr, ostream):
    if(ostream == None):
        return
    try:
        target = bot.friends().search(usr["name"])[0]
        target.send(ostream)
    except:
        print("Send Error!")


def polling(only_available = True):
    data_file =  open(JSON_PATH + "index.json")
    idx =  json.load(datafile)
    for usr_name in idx["usrs"]:
        with open(JSON_PATH + usr_name + ".json") as usr_json:
            ostream = ""
            l = json.load(usr_json)
            ostream += report_to_usr(l)
            l["times"] += len(l["class_list"])
            #TODO: send a file 
                    

if __name__ == "__main__":
    bot = Bot(console_qr=True)
    my_friend = bot.friends()
    while(True):
        polling()

