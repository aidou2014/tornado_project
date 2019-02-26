import tornado.ioloop
import tornado.web
import tornado.options
from tornado.options import define, options

# from handlers.main import IndexHandler, ExploreHandler, PostHandler
from handlers import main

define('port', default=8080, help='listen port', type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", main.IndexHandler),
            (r"/explore", main.ExploreHandler),
            (r"/upload", main.UploadHandler),
            (r"/post/(?P<post_id>[0-9]+)", main.PostHandler),
        ]
        settings = dict(
            debug=True,
            template_path = 'templates',
            static_path = 'static',
            # static_url_prefix = '/pics/'
        )
        super().__init__(handlers, **settings)


application = Application()

if __name__ == "__main__":
    tornado.options.parse_command_line()
    application.listen(options.port)
    print('Server start on port {}'.format(options.port))
    tornado.ioloop.IOLoop.current().start()
