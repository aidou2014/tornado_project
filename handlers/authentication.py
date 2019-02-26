import tornado.web
from .main import AuthBaseHandler
from utils.auth import login_verify


class LoginHandler(AuthBaseHandler):
    """登录页面和处理登录请求"""

    def get(self, *args, **kwargs):
        next_url = self.get_argument('next', '')
        self.render('login.html', next_url=next_url)

    def post(self, *args, **kwargs):
        next_url = self.get_argument('next', '')
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')

        if login_verify(username, password):
            self.session.set('USER', username)
            self.redirect(next_url)
            self.write(username + 'and' + password)

        else:
            self.render('login.html', next_url=next_url)
