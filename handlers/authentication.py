import tornado.web
from .main import AuthBaseHandler
from utils.auth import login_verify, register


class LoginHandler(AuthBaseHandler):
    """登录页面和处理登录请求"""

    def get(self, *args, **kwargs):
        next_url = self.get_argument('next', '/explore')
        self.render('login.html', next_url=next_url)

    def post(self, *args, **kwargs):
        next_url = self.get_argument('next', '')
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')

        if login_verify(username, password):
            self.session.set('USER', username)
            self.redirect(next_url)
        else:
            self.render('login.html', next_url=next_url)


class LogoutHandler(AuthBaseHandler):
    """处理登出逻辑"""

    def get(self, *args, **kwargs):
        self.session.delete('USER')
        self.write('logout done')


class SignupHandler(AuthBaseHandler):
    """处理注册逻辑"""

    def get(self, *args, **kwargs):
        self.render('signup.html', msg='')

    def post(self, *args, **kwargs):
        username = self.get_argument('username', '')
        password1 = self.get_argument('password1', '')
        password2 = self.get_argument('password2', '')

        if username and password1 and password2:
            if password1 == password2:
                msg = register(username, password1)
                if msg == True:
                    self.session.set('USER', username)
                    self.redirect('/explore')
                else:
                    self.render('signup.html', msg=msg)
            else:
                self.render('signup.html', msg='密码不匹配')
        else:
            self.render('signup.html', msg='register fail')
