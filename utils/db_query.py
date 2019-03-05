from sqlalchemy import desc

from models.account import User, PostPicture, Like
from sqlalchemy.sql import exists


class DBProcess(object):
    """处理数据的交互的操作"""

    def __init__(self, db_session, username):
        self.db = db_session
        self.user = username

    def get_user(self):
        """查询user表的用户"""
        user = self.db.query(User).filter_by(username=self.user).first()
        return user

    def post_pictures(self, image_url, thumb_url, user_id, category, description):
        """
        将上传图片的url保存到数据库
        :param image_url: 大图url
        :param thumb_url: 缩略图url
        :param user_id: 用户id字段
        :return: None
        """
        pictures = PostPicture(image_url=image_url, thumb_url=thumb_url,
                               user_id=user_id, category=category, content=description)
        self.db.add(pictures)
        self.db.commit()

    def query_pictures_for_one(self):
        """
        查询用户已经上传的图片,按倒序排列
        :param user_id:当前用户的id
        :return:包含大图和缩略图的元组，所有元组合成一个列表
        """
        user = self.get_user()
        pictures_info = self.db.query(PostPicture).filter(PostPicture.user_id == user.id,
                                                          PostPicture.is_delete == False).order_by(
            desc(PostPicture.id)).all()
        return pictures_info

    def query_all_pictures(self):
        """
        查询所有用户已经上传的图片,当未删除的图片,同时不是自己上传的图片,倒序
        :return: 所有查询出来的图像对象
        """
        user = self.get_user()
        pictures_info = self.db.query(PostPicture).filter(PostPicture.is_delete == False,
                                                          PostPicture.user_id != user.id).order_by(
            desc(PostPicture.id)).all()
        return pictures_info

    def query_pictures_use_id(self, id):
        """
        查询用户点击后的详情页图片
        :return: 所有查询出来的图像对象
        """
        pictures_info = self.db.query(PostPicture).filter_by(id=id).first()
        return pictures_info

    def query_for_good_num(self):
        """
        依据用户的点赞数，来排序
        :return: 对象
        """
        pictures_info = self.db.query(PostPicture).filter(PostPicture.is_delete == False).order_by(
            desc(PostPicture.good_num)).limit(6).all()
        return pictures_info

    def update_post_good_num(self, id, status):
        """更改图片的点赞数
        :id 图片的id
        :status 是增加还是减小
        :return: 一个新的int数据
        """
        old_good_num = self.query_pictures_use_id(id).good_num
        if status:
            new_good_num = old_good_num + 1
        else:
            new_good_num = old_good_num - 1
        self.db.query(PostPicture).filter(PostPicture.id == id).update({PostPicture.good_num: new_good_num})
        self.db.commit()
        return new_good_num

    def update_post_col_num(self, id, status):
        """更改图片的收藏数
        :id 图片的id
        :status 是增加还是减小
        :return: 一个新的int数据
        """
        old_like_num = self.query_pictures_use_id(id).like_num
        if status:
            new_like_num = old_like_num + 1
        else:
            new_like_num = old_like_num - 1
        self.db.query(PostPicture).filter(PostPicture.id == id).update({PostPicture.like_num: new_like_num})
        self.db.commit()
        return new_like_num

    def delete_post(self, id):
        """删除图片
        :id 图片的id
        :return: 删除的状态
        """
        # pictures_info = PostPicture.query_pictures_use_id(id)
        result = self.db.query(PostPicture).filter(PostPicture.id == id).update({PostPicture.is_delete: True})
        self.db.commit()
        return result

    def query_one_like(self):
        """
        查询用于收藏的所有图片,并去除自己上传的图片,应当按照收藏时间
        :param username: 当前用户名
        :return: 一个对象
        """
        user = self.get_user()
        pictures_info = self.db.query(PostPicture).filter(Like.user_id == user.id,
                                                          Like.post_id == PostPicture.id,
                                                          user.id != PostPicture.id).all()
        return pictures_info

    def page_div_for_index(self, page, num):
        """处理主页分页的图片"""
        user = self.get_user()
        pictures_info = self.db.query(PostPicture).filter(
            PostPicture.user_id == user.id, PostPicture.is_delete == False).order_by(desc(PostPicture.id)).slice(
            (page - 1) * num, page * num).all()
        return pictures_info

    def page_div_for_explore(self, page, num):
        """处理分页的图片"""
        user = self.get_user()
        pictures_info = self.db.query(PostPicture).filter(
            PostPicture.user_id != user.id, PostPicture.is_delete == False).order_by(desc(PostPicture.id)).slice(
            (page - 1) * num, page * num).all()
        return pictures_info

    def page_div_for_like(self, page, num):
        """处理分页的图片  太复杂"""
        user = self.get_user()
        pictures_info = self.db.query(PostPicture).filter(
            PostPicture.user_id != user.id, PostPicture.is_delete == False).slice((page - 1) * num, page * num).all()
        return pictures_info
