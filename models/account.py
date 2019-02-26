from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from .db import Base, session
from sqlalchemy.sql import exists
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

    # create_time = Column(DateTime, default=datetime.now)
    # email = Column(String(100))

    def __repr__(self):
        return "<User(#{}:{})".format(self.id, self.username)

    @classmethod
    def is_exist(cls, username):
        """
        判断用户是否已经存在于数据库
        :param username: 输入的用户名
        :return: True or False
        """
        return session.query(exists().where(User.username == username)).scalar()

    @classmethod
    def add_user(cls, username, password):
        """
        向数据库添加用户
        :param username: 用户名
        :param password: 密码，md5之后
        :return: None
        """
        person = User(username=username, password=password)
        session.add(person)
        session.commit()
        return True

    @classmethod
    def query_password(cls, username):
        """
        依据用户名获取对应的密码
        :param username: 输入的用户名
        :return: None or 对应密码 int
        """
        return session.query(User.password).filter_by(username=username).scalar()

    @classmethod
    def query_User(cls, username):
        """
        依据用户名获取对应的密码
        :param username: 输入的用户名
        :return: None or 一个对象
        """
        return session.query(User).filter_by(username=username).first()

    @classmethod
    def query_user_id(cls, username):
        """
        针对程序中总是出现需要用户id的情况，所以定义一个查询特定用户id的方法
        :param username:当前登录的用户名
        :return:对应的id
        """
        user_id = session.query(User.id).filter_by(username=username).scalar()
        return user_id


class PostPicture(Base):
    """完成用户上传图片，并存入数据库的逻辑"""
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    image_url = Column(String(200), nullable=False)
    thumb_url = Column(String(200), nullable=False)
    upload_time = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey('users.id'))

    post_user = relationship('User', backref='post_pictures', uselist=False, cascade='all')

    def __repr__(self):
        return "<Post(#图片id{}:用户id{})".format(self.id, self.user_id)

    @classmethod
    def post_pictures(cls, image_url, thumb_url, user_id):
        """
        将上传图片的url保存到数据库
        :param image_url: 大图url
        :param thumb_url: 缩略图url
        :param user_id: 用户id字段
        :return: None
        """
        pictures = PostPicture(image_url=image_url, thumb_url=thumb_url, user_id=user_id)
        session.add(pictures)
        session.commit()

    @classmethod
    def query_pictures(cls, user_id):
        """
        查询用户已经上传的图片
        :param user_id:当前用户的id
        :return:包含大图和缩略图的元组，所有元组合成一个列表
        """
        pictures_info = session.query(PostPicture.image_url, PostPicture.thumb_url).filter_by(user_id=user_id).all()
        return pictures_info
