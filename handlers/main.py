import json
import tornado.web
from pycket.session import SessionMixin
from utils.process_photo import UploadProcess
from models.account import PostPicture, User, Like
import random
from utils.process_page import process_all_page, process_page_data, process_page_index
from models.db import DBSession
from utils.db_query import DBProcess


class AuthBaseHandler(tornado.web.RequestHandler, SessionMixin):
    """使用pycket的session来验证用户"""

    def get_current_user(self):
        current_user = self.session.get('USER')
        if current_user:
            return current_user
        return None

    def prepare(self):
        self.db_session = DBSession()
        self.db = DBProcess(self.db_session, self.current_user)

    def on_finish(self):
        self.db_session.close()


class IndexHandler(AuthBaseHandler):
    """首页，说管子的用户图片流"""

    @tornado.web.authenticated
    def get(self):
        posts = self.db.query_pictures_for_one()
        all_page, first_page = process_all_page(posts, 8)  # 每页八张
        post_for_user = self.db.query_all_pictures()
        post_4 = random.sample(post_for_user, 4)
        self.render('index.html', posts=first_page, post_for_user=post_4, all_page=all_page)  # 返回所有列表
        # self.render('index.html', imgs=show(self.current_user))   # yield返回


class ExploreHandler(AuthBaseHandler):
    """发现货最近上传的图片页面"""

    @tornado.web.authenticated
    def get(self):
        posts = self.db.query_all_pictures()
        all_page, page_post = process_all_page(posts, 24)  # 列表内的元组
        good_post = self.db.query_for_good_num()
        self.render('explore.html', posts=page_post, good_post=good_post, all_page=all_page)


class PostHandler(AuthBaseHandler):
    """单个图片详情页面"""

    @tornado.web.authenticated
    def get(self, post_id):
        post = self.db.query_pictures_use_id(post_id)
        self.render('post.html', post=post)

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        is_delete = self.get_argument('delete', '')
        if is_delete:
            pass


class UploadHandler(AuthBaseHandler):
    """处理图片上传逻辑"""

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('upload.html')

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        img_list = self.request.files.get('picture', [])
        # online_img = self.get_argument('online','')
        description = self.get_argument('text', '')
        category = self.get_argument('Select1', '')
        # """存放文件的列表，每一个文件都是一个字典形式"""
        # 格式为{'filename': '1.jpg'，'body': b'\xff\xd8',content_type': 'image/jpeg'}
        # 格式为{'filename': 上传文件名称，'body': 文件二进制数据,content_type': 文件类型}
        if img_list:
            for upload_img in img_list:
                upload_obj = UploadProcess(self.settings['static_path'], upload_img['filename'])
                upload_obj.save_to_local(upload_img['body'])
                upload_obj.make_thumb()
                # 需要查询出user_id 是个问题
                user = self.db.get_user()
                self.db.post_pictures(upload_obj.make_image_url, upload_obj.make_thumb_url,
                                      user_id=user.id, category=category, description=description)
            self.redirect('/')
        else:
            self.render('upload.html')


class UserLikeHandler(AuthBaseHandler):

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        name = self.get_argument('name', '')
        if name:
            self.db.user = name
            upload_posts = self.db.query_pictures_for_one()
        else:
            upload_posts = []
        like_posts = self.db.query_one_like()
        like_all_page, first_like_page = process_all_page(like_posts, 12)
        upload_all_page, first_upload_page = process_all_page(upload_posts, 12)
        self.render('like.html', posts=first_like_page, name=self.db.user, upload_posts=first_upload_page,
                    like_all_page=like_all_page, uplaod_all_page=upload_all_page)


class BetterHandler(AuthBaseHandler):

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        id = self.get_argument('id', '')
        flag = self.get_argument('flag', '')
        count = self.db.update_post_good_num(id, flag)
        self.write(str(count))


class CollectionHandler(AuthBaseHandler):

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        id = self.get_argument('id', '')
        flag = self.get_argument('flag', '')
        count = self.db.update_post_col_num(id, flag)
        self.write(str(count))


class DeleteHandler(AuthBaseHandler):

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        id = self.get_argument('id', '')
        result = self.db.delete_post(id)
        if result:
            data = {"index_url": "http://120.78.90.247/"}
            data = json.dumps(data)
            self.write(data)
        else:
            pass  # 弹窗


class PageHandler(AuthBaseHandler):

    @tornado.web.authenticated
    def get(self, current, page):
        if current == '/':
            index_page_num = 8
            page_post = self.db.page_div_for_index(page=int(page), num=index_page_num)
            post_for_user = self.db.query_all_pictures()
            post_4 = random.sample(post_for_user, 4)
            page_data = process_page_index(page_post, post_4)
            self.write(page_data)
            # self.render('page.html', posts=page_post, post_for_user=post_4, all_page=int(all_page_1))  # 返回所有列表

        elif current == '/explore':
            index_page_num = 24
            page_post = self.db.page_div_for_explore(page=int(page), num=index_page_num)
            page_post_data = process_page_data(page_post)
            self.write(page_post_data)
            # self.render('explore.html', posts=page_post, good_post=good_post, all_page=all_page)

        elif current == '/like':
            index_page_num = 12
            page_post = self.db.page_div_for_like(page=int(page), num=index_page_num)
            page_post_data = process_page_data(page_post)
            self.write(page_post_data)

        else:
            self.redirect('/')
        # print(current)
        # print(page)
