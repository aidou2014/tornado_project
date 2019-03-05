import tornado.websocket
import tornado.web
from handlers.authentication import AuthBaseHandler
from pycket.session import SessionMixin
import tornado.escape
import uuid


class RoomHandler(AuthBaseHandler):
    """处理聊天室的逻辑"""

    def get(self, *args, **kwargs):
        self.render('room2.html', message=ChatWsHandler.history)


class BaseWebsocketHandler(tornado.websocket.WebSocketHandler, SessionMixin):
    """用于实现websocket通信"""

    def get_current_user(self):
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

    def on_close(self):
        """websocket断开时，自动调用"""
        print('close ws {}'.format(self))
        ChatWsHandler.users.remove(self)

    def on_message(self, message):
        """服务器收到信息后，自动调用"""
        print(message)
        parsed = tornado.escape.json_decode(message)
        print(repr(parsed))
        chat = {
            "id": str(uuid.uuid4()),
            "body": parsed["body"]
        }
        print(repr(chat))
        H = tornado.escape.to_basestring(
            self.render_string('message.html', chat=chat))
        messages_html = {
            "html": H,
            "id": chat["id"]
        }
        print(repr(messages_html))
        ChatWsHandler.send_update(messages_html)

    @classmethod
    def send_update(cls, messages_html):
        ChatWsHandler.history.append(messages_html)
        for user in ChatWsHandler.users:
            user.write_message(messages_html)
