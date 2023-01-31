#!/user/bin/env python
# -*- coding:utf-8 -*-
from wxpy import *
import time

bot = Bot(cache_path=True)
groups = bot.groups()

my_friend = bot.friends().search("马面")[0]
my_friend.send("hello world!")

while True:
    for i in range(10):
        # 找到目标群
        group = groups.search("我和我的")[0]
        group.send("机器人自动发的消息，请忽略！发送10次，间隔2。5秒")
        time.sleep(2.5)
