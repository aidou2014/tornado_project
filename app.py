import tornado.ioloop
import tornado.web
import tornado.options
from tornado import httpserver
from tornado.options import define, options
from handlers import main, authentication, chat1

define('port', default=8010, help='listen port', type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", main.IndexHandler),
            (r"/explore", main.ExploreHandler),
            (r"/upload", main.UploadHandler),
            (r"/like", main.UserLikeHandler),
            (r"/better", main.BetterHandler),
            (r"/collection", main.CollectionHandler),
            (r"/delete", main.DeleteHandler),
            (r"(?P<current>.*?)/page/(?P<page>[0-9]+)", main.PageHandler),
            (r"/post/(?P<post_id>[0-9]+)", main.PostHandler),
            (r"/login", authentication.LoginHandler),
            (r"/logout", authentication.LogoutHandler),
            (r"/signup", authentication.SignupHandler),
            (r"/room", chat1.RoomHandler),
            (r"/ws", chat1.ChatWsHandler),

        ]
        settings = dict(
            debug=False,
            template_path = 'templates',
            static_path = 'static',
            # static_url_prefix = '/pics/'
            cookie_secret='qwe123',
            login_url='/login',
            autoescape=None,
            pycket={
                'engine': 'redis',
                'storage': {
                    'host': 'localhost',
                    'port': 6379,
                    'db_sessions': 6,
                    # 'db_notifications':11,
                    'max_connections': 2 ** 30,
                },
                'cookies': {
                    'expires_days': 30
                },
            }
        )
        super().__init__(handlers, **settings)


application = Application()

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = httpserver.HTTPServer(application)
    http_server.listen(options.port)  # 加入httpserver非阻塞服务器
    print('Server start on port {}'.format(options.port))
    tornado.ioloop.IOLoop.current().start()
