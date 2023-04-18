#!/bin/bash

rtx_name=$1
chatid=$2
chat_type=$3
WebhookUrl=$4
content_real=$5

function send_msg ()
{
    chatid=$1
    result_info=$2
    WebhookUrl=$3
    curl ''$WebhookUrl'' \
    -H 'Content-Type: application/json;charset=UTF-8' \
    -d '
    {
        "chatid": "'"$chatid"'",
        "msgtype": "text",
        "text": {
            "content": "'"${result_info}"'"
        }
    }'
}

#获取你输入的第一个关键字，变量名可以随意替换
get_content=`echo ${content_real} |awk -F"," '{print $1}'`

#填入具体逻辑
#	最终返回结果用result_info="XXXX"
result_info=`python3 /getxid.py `
#result_info="我是样例"
#理论上一次回话只返回一次结果


send_msg $chatid "${result_info}" $WebhookUrl
