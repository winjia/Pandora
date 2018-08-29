import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options
from mainhandler import MainHandler
import config


class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            cookie_secret="bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            login_url="/",
            debug=True,
        )
        super(Application, self).__init__([(r'/wx', MainHandler)], **settings)


def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(8081)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()

