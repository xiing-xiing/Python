#coding=utf-8

from tornado.web import RequestHandler,Application
from tornado.ioloop import IOLoop

class IndexHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render('templates/show.html',uname='nihao',PWD='')


app = Application([
    (r'^/$',IndexHandler)
])

app.listen(8200)
IOLoop.instance().start()