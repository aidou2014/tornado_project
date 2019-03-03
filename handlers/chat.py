from tornado.websocket import WebSocketHandler
import tornado.web
from handlers.authentication import AuthBaseHandler
import tornado.escape
from pycket.session import SessionMixin
import uuid
import time


class RoomHandler(AuthBaseHandler):
    """处理聊天室的逻辑"""

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('room1.html')


class BaseWebsocketHandler(WebSocketHandler, SessionMixin):
    """用于实现websocket通信"""

    def get_current_user(self):
        # current_user = self.get_secure_cookie('user.ID')
        current_user = self.session.get('USER')
        if current_user:
            return current_user
        return None


class ChatWsHandler(BaseWebsocketHandler):
    """处理和响应websocket连接"""

    users = set()
    history = list()  # 存放历史消息

    def open(self, *args, **kwargs):
        """新的websocket连接打开，自动调用"""
        print('open ws {}'.format(self))
        ChatWsHandler.users.add(self)
        for user in ChatWsHandler.users:
            user.write_message('%s-%s上线了' % (self.current_user, time.strftime('%d-%m-%Y %H:%M:%S')))

    def on_close(self):
        """websocket断开时，自动调用"""
        print('close ws {}'.format(self))
        ChatWsHandler.users.remove(self)
        for user in self.users:
            user.write_message('%s-%s下线了' % (self.current_user, time.strftime('%d/%m/%Y %H:%M:%S')))

    def on_message(self, message):
        """服务器收到信息后，自动调用"""
        for user in ChatWsHandler.users:
            user.write_message('%s-%s：%s' % (self.current_user, time.strftime('%d/%m/%Y %H:%M:%S'), message))
