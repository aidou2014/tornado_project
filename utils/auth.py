import hashlib
from models.account import User

def hashed(text):
    """
    利用hashlib内部的md5算法来加密
    :param text: 需要加密的字符串
    :return: 加密的md5串
    """
    return hashlib.md5(text.encode()).hexdigest()


def login_verify(db_session, username, password):
    """
    处理登录验证逻辑
    :param username: 用户输入的用户名
    :param password: 用户输入的密码
    :return: True or False
    """
    if username and password:
        user = User.query_User(db_session, username)
        if user:
            is_match = (hashed(password) == user.password)
            return is_match
        else:
            return None
    else:
        return False


def register(db_session, username, password):
    """
    用于处理注册逻辑，将用户信息保存到数据库
    :param username:
    :param password:
    :return:
    """
    if User.is_exist(db_session, username):
        return 'user is existed'
    else:
        return User.add_user(db_session, username, hashed(password))

# def show(username):
#     """展示主页的图片等"""
#     user_obj = User.query_User(username).post_pictures
#     for obj in user_obj:  # 利用表关系，只是查询一次数据库
#         imgs = obj.image_url, obj.thumb_url
#         yield imgs
