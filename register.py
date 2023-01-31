#coding=utf-8

import tornado.web
import tornado.ioloop
import MySQLdb

def _getConn():
    return MySQLdb.connect(host='{数据库ip}',user='{用户}',passwd='{密码}',db='{数据库}',port={端口})

class RegisterHandler(tornado.web.RequestHandler):
    def initialize(self,conn):
        self.conn = conn


    def get(self, *args, **kwargs):
        self.render('templates/register.html')

    def post(self, *args, **kwargs):
        #获取请求参数
        uname = self.get_argument('uname')
        pwd = self.get_argument('pwd')

        #将数据插入到数据库中
        try:
            cursor = self.conn.cursor()
            cursor.execute('insert into users values(null,"%s","%s",now())'%(uname,pwd))
            self.conn.commit()
            self.write('注册成功！')
        except:
            self.conn.rollback()
            self.redirect('/register/')




app = tornado.web.Application([
    (r'^/register/$',RegisterHandler,{'conn':_getConn()})
])

app.listen(8800)

tornado.ioloop.IOLoop.instance().start()
