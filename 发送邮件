# !/usr/bin/python3

import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 第三方 SMTP 服务
mail_host = "smtp.163.com"  # 设置服务器
mail_user = "{用户名}"  # 用户名
mail_pass = "{口令}"  # 口令

sender = '{发送者}'
receivers = ['{邮件接收者}']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

message1 = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
message1['From'] = Header("test", 'utf-8')
message1['To'] = Header("测试", 'utf-8')

subject = 'Python SMTP 邮件测试'
message1['Subject'] = Header(subject, 'utf-8')

try:
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message1.as_string())
    print("邮件发送成功")
except smtplib.SMTPException:
    print("Error: 无法发送邮件")
