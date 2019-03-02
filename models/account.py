from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, desc
from models.db import Base, session
from datetime import datetime
from sqlalchemy.sql import exists
from sqlalchemy.orm import relationship



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
    def update_login_status(cls, username):
        """
        改变用户的登录状态，设为登录
        :param username: 登录的用户名
        """
        session.query(User).filter(User.username == username).update({User.is_local: True})
        session.commit()

    @classmethod
    def update_logout_status(cls, username):
        """
        改变用户的登录状态，设为下线
        :param username: 登录的用户名
        """
        session.query(User).filter(User.username == username).update({User.is_local: False})
        session.commit()

    @classmethod
    def query_User(cls, username):
        """
        依据用户名获取对应的密码
        :param username: 输入的用户名
        :return: None or 一个对象
        """
        return session.query(User).filter_by(username=username).first()



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

    @classmethod
    def post_pictures(cls, image_url, thumb_url, user_id):
        """
        将上传图片的url保存到数据库
        :param image_url: 大图url
        :param thumb_url: 缩略图url
        :param user_id: 用户id字段
        :return: None
        """
        pictures = PostPicture(image_url=image_url, thumb_url=thumb_url, user_id=user_id, )
        session.add(pictures)
        session.commit()

    @classmethod
    def query_pictures_for_one(cls, username):
        """
        查询用户已经上传的图片
        :param user_id:当前用户的id
        :return:包含大图和缩略图的元组，所有元组合成一个列表
        """
        user = User.query_User(username)
        pictures_info = session.query(PostPicture).filter(PostPicture.user_id == user.id,
                                                          PostPicture.is_delete == False).all()
        return pictures_info

    @classmethod
    def query_all_pictures(self, username):
        """
        查询所有用户已经上传的图片,当未删除的图片
        :return: 所有查询出来的图像对象
        """
        user = User.query_User(username)
        pictures_info = session.query(PostPicture).filter(PostPicture.is_delete == False,
                                                          PostPicture.user_id != user.id).all()
        return pictures_info

    @classmethod
    def query_pictures_use_id(self, id):
        """
        查询用户点击后的详情页图片
        :return: 所有查询出来的图像对象
        """
        pictures_info = session.query(PostPicture).filter_by(id=id).first()
        return pictures_info

    @classmethod
    def query_for_good_num(self):
        """
        依据用户的点赞数，来排序
        :return: 对象
        """
        pictures_info = session.query(PostPicture).filter(PostPicture.is_delete == False).order_by(
            desc(PostPicture.good_num)).limit(10).all()
        return pictures_info


class Like(Base):
    __tablename__ = 'likes'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'), primary_key=True)
    dot_like = Column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return '<Like(用户id：{}--照片id{}--是否关注：{})'.format(self.user_id, self.post_id, self.dot_like)

    @classmethod
    def query_one_like(self, username):
        """
        查询用于收藏的所有图片,并去除自己上传的图片
        :param username: 当前用户名
        :return: 一个对象
        """
        user = User.query_User(username)
        pictures_info = session.query(PostPicture).filter(Like.user_id == user.id,
                                                          Like.post_id == PostPicture.id,
                                                          user.id != PostPicture.id).all()
        return pictures_info


if __name__ == '__main__':
    Base.metadata.create_all()
