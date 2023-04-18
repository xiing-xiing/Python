#!/bin/bash

function send_msg ()
{
    chatid=$1
    result_info=$2
    WebhookUrl=$3
    curl ''${WebhookUrl}'' \
    -H 'Content-Type: application/json;charset=UTF-8' \
    -d '
    {
	"chatid": "'$chatid'",
	"msgtype": "text",
	"text": {
	    "content": "'${result_info}'"
	}
    }'
}


date_today=`date  +%Y%m%d`
input_info=$1
content=`echo ${input_info} | awk -F"Content" '{print $2}' | awk -F"[" '{print $3}' | awk -F"]" '{print $1}'`
rtx_name=`echo ${input_info} | awk -F"Alias" '{print $2}' | awk -F"[" '{print $3}' | awk -F"]" '{print $1}'`
chatid=`echo ${input_info} | awk -F"ChatId" '{print $2}' | awk -F"[" '{print $3}' | awk -F"]" '{print $1}'`
WebhookUrl=`echo ${input_info} | awk -F"WebhookUrl" '{print $2}' | awk -F"[" '{print $3}' | awk -F"]" '{print $1}'`

#检查是群聊还是单独对话
chat_type=`echo ${input_info} | awk -F"ChatType" '{print $2}' | awk -F"[" '{print $3}' | awk -F"]" '{print $1}'`
if [[ ${chat_type} == single ]];then
    content_real=`echo $content | sed 's/,/ /g' | awk '$1=$1' | tr " " ","`
elif [[ ${chat_type} == group ]];then
    content_real=`echo $content | sed 's/,/ /'|awk '{print $2}' | sed 's/,/ /g' | awk '$1=$1' | tr " " ","`
else
    result_info="接收到的chat_type有问题，烦请检查"
    send_msg $chatid ${result_info}
    exit 0
fi

#查看请求是否为重试请求
MsgId=`echo ${input_info} | awk -F"MsgId" '{print $2}' | awk -F"[" '{print $3}' | awk -F"]" '{print $1}'`
grep "${MsgId}" ../MsgId/MsgId_${date_today} > /dev/null 2>&1
if [ $? -eq 0 ];then
        exit 0
else
        echo ${MsgId} >> ../MsgId/MsgId_${date_today}
fi
#过滤添加机器人&激活机器人的自动回复
event_type=`echo ${input_info} | awk -F"EventType" '{print $2}' | awk -F"[" '{print $3}' | awk -F"]" '{print $1}'`
if [[ ${event_type} == add_to_chat || ${event_type} == enter_chat ]];then
        exit 0
fi
last_content=`echo ${content_real} |awk -F"," '{print $NF}'`

case ${last_content} in
    2)
    ../shell/other/xunjian.sh ${rtx_name} ${chatid} ${chat_type} ${WebhookUrl} ${content_real}
    ;;
    1)
    ../shell/other/zhouhui.sh ${rtx_name} ${chatid} ${chat_type} ${WebhookUrl} ${content_real}
    ;;
    *)

        result_info="{默认回复}"
        send_msg $chatid "${result_info}" $WebhookUrl
    ;;
esac


