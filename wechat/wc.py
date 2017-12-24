#!/usr/bin/python
#encoding:utf-8

import re
from wxpy import *
from iclass import Class as c
import iclass

JSON_PATH='/home/ubuntu/ClassUCLA/wechat/debug/'
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
import json
import os
'''
Respond to the text message 
User Interface 
'''
def process_text(msg):
    #not related
    text = msg.text.strip(' ').lower()
    usr = msg.receiver
    if(text[:4] != DLMT):
        #return "Received {}\n".format(msg.text)
        return ""

    text = text[4:]
    ostream = ""

    #load json file    
    path = JSON_PATH +usr+".json"
    print(path)
    if(os.path.exists(path)):
        print(path)
        with open(path) as datafile:
            data = json.load(datafile)
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
        data = {"name":usr, "class_list":list(),"daily_report": False}
        index_path = JSON_PATH + "index.json"
        print("Creating new profile for {}".format(usr))
        if(not os.path.exists(index_path)):            
            indices = dict()
            indices["usrs"] = list()
            indices["usrs"].append(usr)
        else:
            with open(index_path) as datafile:
                indices = json.load(datafile)
                indices["usrs"].append(usr)
        write_to = open(index_path, "w")
        write_to.write(json.dumps(indices))
        write_to.close()
        
    if(text[0] == 'a'):
        num = text[1:10]
        if(len(num) != 9):
            ostream += "length of class id is {}, required 9".format(len(num))
            return ostream
        if(num in data["class_list"]):
            ostream += "Class is already in your list\n"
        else:
            s = iclass.get_class_info_basic(num)
            if("Non results" in s):
                ostream += "No class as {}\n".format(num)
            else:
                data["class_list"].append(num)
                ostream += "Added {}\n".format(num)
                
    if(text[0] == 'r'):
        num = text[1:10]
        if(num in data["class_list"]):
            data["class_list"].remove(num)
            ostream += "Class ID with {} is removed\n".format(num)
        else:
            ostream += "No such class as {}".format(num)
            
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

    write_to  = open(path, "w")
    write_to.write(json.dumps(data))
    write_to.close()
    
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
                ostream +="Your {} {} {} is available! Now its status is {}. To stop scanning for this class, please reply dgqkr{} \n".format(class_info["subject"], class_info["course_number"], class_info["course_title"], class_info["status"], c)
            else:
                log_to("{} is Full")
        else:    
            ostream += new_class.print_open_seats()
    return ostream

import types
def send_to_usr(usr, ostream):
    if(ostream == None or ostream == ""):
        return
    try:
        search_name = None
        if(type(usr) == types.StringType or type(usr) == types.UnicodeType): 
            search_name = usr
        else:
            search_name = usr["name"]
        target = bot.friends().search(usr["name"])[0]
        target.send(ostream)
        #print(usr, ostream)
    except:
        print("Send Error!")


def polling(only_available = True):
    with open(JSON_PATH + "index.json") as data_file:
        idx =  json.load(data_file)
        for usr_name in idx["usrs"]:
            usr_path = JSON_PATH + usr_name + ".json"
            usr_json = open(usr_path, "rw")
            ostream = ""
            l = json.load(usr_json)
            ostream += report_to_usr(l, only_available=only_available)
            send_to_usr(usr_name, ostream)
            #l["times"] += len(l["class_list"])
            #usr_json.write(json.dumps(l))
            #usr_json.close()


import time
import schedule 
def log_to(ostream):
    log_file = open("/home/ubuntu/data/log.txt", 'a')
    log_file.write(time.asctime(time.localtime(time.time())))
    log_file.write(ostream + "\n")
    log_file.close()

    
bot = Bot(console_qr=True)
my_friend = bot.friends()
# schedule.every().day.at("12:00").do(polling, False)
# schedule.every(30).minutes.do(polling)
# while True:
#     schedule.run_pending()

@bot.register(my_friend, TEXT)
def reply_my_friend(msg):
    #print("Received {}\n".format(msg.text))
    return process_text(msg)

embed()
