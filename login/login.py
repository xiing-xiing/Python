#coding=utf-8
import tornado.web
import tornado.ioloop
import MySQLdb

class LoginHandler(tornado.web.RequestHandler):
    def initialize(self,conn):
        self.conn = conn
    def prepare(self):
        #判断当前请求方式
        if self.request.method == 'POST':
            #获取请求参数
            self.uname = self.get_argument('uname')
            self.pwd = self.get_argument('pwd')

    def get(self, *args, **kwargs):
        self.render('templates/login.html')

    def post(self, *args, **kwargs):
        cursor = self.conn.cursor()
        cursor.execute('select * from users where uname="%s" and pwd="%s"'%(self.uname,self.pwd))
        user = cursor.fetchone()
        print(user)
        if user:
            self.render('templates/success.html')
        else:
            self.write(u'登录失败！')

    def write_error(self, status_code, **kwargs):
        self.render('templates/error.html')
    def set_default_headers(self):
        self.set_header('Server','SXTServer/1.0')

settings={'debug':True}
dbconfig={
    'host':'{数据库ip}}',
    'user':'{用户名}',
    'passwd':'{数据库密码}',
    'db':'{用户名}',
    'port':{端口}
}

app = tornado.web.Application([
    (r'^/login/$',LoginHandler,{'conn':MySQLdb.connect(**dbconfig)})
],**settings)

app.listen(8000)
tornado.ioloop.IOLoop.instance().start()