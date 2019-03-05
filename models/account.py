from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, exists
from models.db import Base, DBSession
from datetime import datetime
from sqlalchemy.orm import relationship

session = DBSession()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    create_time = Column(DateTime, default=datetime.now)
    is_local = Column(Boolean, default=False, nullable=False)


    def __repr__(self):
        return "<User(#{}:{})".format(self.id, self.username)

    @classmethod
    def query_User(cls, db_session, username):
        """查询user表的用户"""
        user = db_session.query(User).filter_by(username=username).first()
        return user

    @classmethod
    def is_exist(cls, db_session, username):
        """
        判断用户是否已经存在于数据库
        :return: True or False
        """
        return db_session.query(exists().where(User.username == username)).scalar()

    @classmethod
    def add_user(cls, db_session, username, password):
        """
        向数据库添加用户
        :param username: 用户名
        :param password: 密码，md5之后
        :return: None
        """
        person = User(username=username, password=password)
        db_session.add(person)
        db_session.commit()
        return True

    @classmethod
    def update_login_status(cls, db_session, name):
        """
        改变用户的登录状态，设为登录
        :param username: 登录的用户名
        """
        db_session.query(User).filter(User.username == name).update({User.is_local: True})
        db_session.commit()

    @classmethod
    def update_logout_status(cls, db_session, name):
        """
        改变用户的登录状态，设为下线
        :param username: 登录的用户名
        """
        db_session.query(User).filter(User.username == name).update({User.is_local: False})
        db_session.commit()



class PostPicture(Base):
    """完成用户上传图片，并存入数据库的逻辑"""
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    image_url = Column(String(200), nullable=False)
    thumb_url = Column(String(200), nullable=False)
    upload_time = Column(DateTime, default=datetime.now)
    is_delete = Column(Boolean, default=False, nullable=False)
    good_num = Column(Integer, default=0, nullable=False)  # 点赞数
    like_num = Column(Integer, default=0, nullable=False)  # 收藏数
    content = Column(Text, nullable=False, default='')  # 内容
    category = Column(String(50), default='', nullable=False)  # 分类
    user_id = Column(Integer, ForeignKey('users.id'))

    post_user = relationship('User', backref='post_pictures', uselist=False, cascade='all')

    def __repr__(self):
        return "<Post(#图片id{}:用户id{})".format(self.id, self.user_id)



class Like(Base):
    __tablename__ = 'likes'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'), primary_key=True)
    dot_like = Column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return '<Like(用户id：{}--照片id{}--是否关注：{})'.format(self.user_id, self.post_id, self.dot_like)


    @classmethod
    def like_verify(self, username):
        """
        判断用户时候已经收藏
        :return:
        """
        user = User.query_User(username)
        TF = session.query(Like.dot_like).filter(user.id == Like.user_id, Like.post_id == PostPicture.id).scalar()
        return TF


if __name__ == '__main__':
    Base.metadata.create_all()
