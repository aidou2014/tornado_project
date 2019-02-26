from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .db import Base, session
from sqlalchemy.sql import exists


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
