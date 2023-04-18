#!/usr/bin/env python
# -*- coding=utf-8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer

import urllib
from WXBizMsgCrypt import WXBizMsgCrypt
import xml.etree.cElementTree as ET
import os

token =  '{token}'
aeskey = '{aesey}'


config = {
    "token":token,
    "aeskey":aeskey
}

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        query = urllib.splitquery(path)
        args = query[1].split('&')
        q={}
        for arg in args:
            tmp = arg.split("=")
            q[tmp[0]] = urllib.unquote(tmp[1])
        for f in q:
            print f+" : "+q[f]
        wxcpt = WXBizMsgCrypt(config['token'],config['aeskey'],'')
        ret,echostr = wxcpt.VerifyURL(q['msg_signature'],q['timestamp'],q['nonce'],q['echostr'])
        print "verify result %d  %s" % (ret,echostr)
        if ret != 0:
            return

        self.send_response(200)
        self.send_header("Content-Length",str(len(echostr)))
        self.end_headers()
        self.wfile.write(echostr)

    def do_POST(self):
        query = urllib.splitquery(self.path)
        args = query[1].split("&")
        q={}
        for arg in args:
            tmp = arg.split("=")
            q[tmp[0]] = urllib.unquote(tmp[1])
        length = self.headers.get("Content-Length")
        if length is None:
            self.send_error(400,"Empty Content")
            return
        post_data = self.rfile.read(int(length))
        #post data 是一段XML，包含加密的数据<Encrypt>: <xml><Encrypt>![CDATA[XXXXXXX]]</Encrypt></xml>
        wxcpt = WXBizMsgCrypt(config['token'],config['aeskey'],'')
        ret,msg = wxcpt.DecryptMsg(post_data,q['msg_signature'],q['timestamp'],q['nonce'])
        if ret != 0:
            print ret
            self.send_error(400,"fail")
            return
        print msg
	msg=msg.replace('<','_')
	msg=msg.replace('>','_')
	msg=msg.replace(' ',',')
        msg=msg.replace(';',',')
        #print msg
	os.system("../shell/main.sh " + msg)
	#os.popen("./test.sh " + 'msg' )


        xml = ET.Element('xml')
        ET.SubElement(xml,'MsgType').text = 'text'
        #text = ET.SubElement(xml,'Text')
        #ET.SubElement(text,'Content').text = '妈耶'

        plain = ET.tostring(xml)
        ret,resp = wxcpt.EncryptMsg(plain,q['nonce'],q['timestamp'])
        if ret != 0:
            print "encrypt error"
            return
        self.send_response(200)
        self.send_header("Content-Length",str(len(resp)))
        self.end_headers()
        self.wfile.write(resp)
        return


if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 1234),RequestHandler)
    server.serve_forever()
