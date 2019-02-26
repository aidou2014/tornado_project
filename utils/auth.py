import hashlib


def hashed(text):
    """
    利用hashlib内部的md5算法来加密
    :param text: 需要加密的字符串
    :return: 加密的md5串
    """
    return hashlib.md5(text.encode()).digest()


users = {
    'username': 'qq',
    'password': hashed('123')
}


def login_verify(username, password):
    """
    处理登录验证逻辑
    :param username: 用户输入的用户名
    :param password: 用户输入的密码
    :return: True or False
    """
    if username and password:
        is_match = (username == users['username']) and (hashed(password) == users['password'])
        return is_match
    else:
        return False
