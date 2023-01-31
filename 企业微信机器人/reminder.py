#! -*- coding: utf-8 -*-
#Author: xing
#Create type_time: 2022-7-28
#Info: 定期向企业微信推送消息

import requests, json
import datetime
import time

wx_url = "{wehook地址替换}"    # 将此网址替换成你的群聊机器人Webhook地址
send_message1 = "早上你打卡了吗？？？？？？？？？？"
send_message2 = "下午你打卡了吗？？？？？？？？？？"

def get_current_time():
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    hour = datetime.datetime.now().strftime("%H")
    mm = datetime.datetime.now().strftime("%M")
    ss = datetime.datetime.now().strftime("%S")
    return now_time, hour, mm, ss

def sleep_time(hour, m, sec):
    return hour * 3600 + m * 60 + sec

def send_msg(content):
    data = json.dumps({"msgtype": "text", "text": {"content": content, "mentioned_list":["@all"]}})
    r = requests.post(wx_url, data, auth=('Content-Type', 'application/json'))
    print(r.json)

def every_time_send_msg(interval_h=0, interval_m=0, interval_s=31, special_h1="09",special_h2="18", special_m="00", mode="special"):    #此处定义了每多长时间重复一次此指令，在这里我设置的是每31秒重复一次。且此处设置定时发送消息的时间点（24小时制），在这里我设置的是8点和12点整。

    second = sleep_time(interval_h, interval_m, interval_s)
    while True:
        c_now, c_h, c_m, c_s = get_current_time()
        print("当前时间：", c_now, c_h, c_m, c_s)
        if c_h == special_h1 and c_m == special_m:
            print('正在发送提醒')
            send_msg(send_message1)
        else:
            print('未到早8点提醒时间')
            
        if c_h == special_h2 and c_m == special_m:
            print('正在发送提醒')
            send_msg(send_message2)
        else:
            print('未到下午18点提醒时间')
         
        print("每隔" + str(interval_h) + "小时" + str(interval_m) + "分" + str(interval_s) + "秒执行一次")
        time.sleep(second)
        
if __name__ == '__main__':
    every_time_send_msg(mode="no")

