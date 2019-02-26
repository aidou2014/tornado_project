import tornado.ioloop
import tornado.web
import tornado.options
from tornado.options import define, options
# from handlers.main import IndexHandler, ExploreHandler, PostHandler
from handlers import main, authentication

define('port', default=8080, help='listen port', type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", main.IndexHandler),
            (r"/explore", main.ExploreHandler),
            (r"/upload", main.UploadHandler),
            (r"/login", authentication.LoginHandler),
            (r"/logout", authentication.LogoutHandler),
            (r"/signup", authentication.SignupHandler),
            (r"/post/(?P<post_id>[0-9]+)", main.PostHandler),
        ]
        settings = dict(
            debug=True,
            template_path = 'templates',
            static_path = 'static',
            # static_url_prefix = '/pics/'
            cookie_secret='qwe123',
            login_url='/login',
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
    application.listen(options.port)
    print('Server start on port {}'.format(options.port))
    tornado.ioloop.IOLoop.current().start()
