#!/usr/bin/python
import re
from wxpy import *
from iclass import Class as c
from iclass import *
DLMT = "dgqk"
INSTR = '''
Welcome. 
为了与我正常的信息分开，请使用这个功能的时候在信息前面加上dgqk（大哥抢课）
例如：dgqkl
下面是使用指南。
dgqk 可以重新显示本条消息
a+9位课号 把相应的课加入scan列表，如dgqka187780200,可以帮你scan下学期CS180
d+9位课号 从scan列表中移除该课
r+9位课号 每天固定时间给你发消息看status的update
l 查daily report中课程 
其他功能，例如设置，陆续更新中。

'''
@bot.register(my_friend, TEXT, except_self=False)
def reply_my_friend(msg):
    return process_text(msg)
    #return 'received: {} ({})'.format(msg.text, msg.type)

import json
import os
def process_text(text):
    #not related
    if(text.strip(' ').lower()[:3] != DLMT):
        return None

    text = text[4:]
    ostream = ""
    #instruction
    if(len(text) == 0 or text[0] == 'h'):
        return INSTR
    #load json file    
    usr = text.receiver
    path = "./"+usr+".json"
    if(os.path.exists(path)):
        with open(path) as datafile:
            data = json.load(datafle)
    else:
        data = {"usr":usr, "class_list":list(), "report_list":list()]
        
    if(text[0] == 'a'):
        add_list = re.findall(r"\b\d{9}\b",text)
        for num in add_list:
            if(num in data["class_list"):
                continue
            s = iclass.get_class_info_basic(num)
            if("Non results" in s):
               ostream += "No class as {}\n".format(num)
            else:
               data["class_list"].append(num)
               ostream += "Added {}\n".format(num)
        return ostream
    if(text[0] == 'd'):
        remove_list = re.findall(r"\b\d{9}\b",text)
        for num in remove_list:
            data["class_list"].remove(num)
    if(text[0] == 'r'):        
        add_list = re.findall(r"\b\d{9}\b",text)
        for num in add_list:
            if(num in data["class_list"):
                continue
            s = iclass.get_class_info_basic(num)
            if("Non results" in s):
               ostream += "No class as {}\n".format(num)
            else:
               data["report_list"].append(num)
               ostream += "Added {}\n".format(num)
    if(text[0] == 'l'):
        pass
    return None



if __name__ == "__main__":
    bot = Bot(console_qr=True)
    my_friend = bot.friends()
    embed()


