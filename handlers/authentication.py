import tornado.web
from .main import AuthBaseHandler
from utils.auth import login_verify, register
from models.account import User


class LoginHandler(AuthBaseHandler):
    """登录页面和处理登录请求"""

    def get(self, *args, **kwargs):
        next_url = self.get_argument('next', '/')
        self.render('login.html', next_url=next_url)

    def post(self, *args, **kwargs):
        next_url = self.get_argument('next', '')
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        login_correct = login_verify(self.db_session, username, password)
        if login_correct:
            self.session.set('USER', username)
            User.update_login_status(self.db_session, username)
            self.redirect(next_url)
        elif login_correct == None:
            self.render('signup.html', msg='你还未注册')
        else:
            self.render('login.html', next_url=next_url)


class LogoutHandler(AuthBaseHandler):
    """处理登出逻辑"""

    def get(self, *args, **kwargs):
        User.update_logout_status(self.db_session, self.current_user)
        self.session.delete('USER')
        self.redirect('/login')


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
                msg = register(self.db_session, username, password1)
                if msg == True:
                    self.session.set('USER', username)
                    self.redirect('/login')
                else:
                    self.render('signup.html', msg=msg)
            else:
                self.render('signup.html', msg='密码不匹配')
        else:
            self.render('signup.html', msg='register fail')
