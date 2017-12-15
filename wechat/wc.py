#!/usr/bin/python
from wxpy import *

bot = Bot(console_qr=True)
my_friend = bot.friends()

@bot.register(my_friend, TEXT, except_self=False)
def reply_my_friend(msg):
    return 'received: {} ({})'.format(msg.text, msg.type)

embed()

def process_text(text):
    result = {
        'a': lambda x: x * 5,
        'b': lambda x: x + 4
    }[value](x)
