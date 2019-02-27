import tornado.web
from pycket.session import SessionMixin
from utils.process_photo import UploadProcess
from models.account import PostPicture, User
from utils.auth import show


class AuthBaseHandler(tornado.web.RequestHandler, SessionMixin):
    """使用pycket的session来验证用户"""

    def get_current_user(self):
        current_user = self.session.get('USER')
        if current_user:
            return current_user
        return None


class IndexHandler(AuthBaseHandler):
    """首页，说管子的用户图片流"""

    @tornado.web.authenticated
    def get(self):
        posts = User.query_User(self.current_user).post_pictures
        self.render('index.html', posts=posts)  # 返回所有列表
        # self.render('index.html', imgs=show(self.current_user))   # yield返回


class ExploreHandler(AuthBaseHandler):
    """发现货最近上传的图片页面"""

    @tornado.web.authenticated
    def get(self):
        posts = PostPicture.query_all_pictures()  # 列表内的元组
        self.render('explore.html', posts=posts)


class PostHandler(tornado.web.RequestHandler):
    """单个图片详情页面"""

    def get(self, post_id):
        post = PostPicture.query_pictures_use_id(post_id)
        self.render('post.html', post=post)


class UploadHandler(AuthBaseHandler):
    """处理图片上传逻辑"""

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('upload.html')

    def post(self, *args, **kwargs):
        img_list = self.request.files.get('picture', [])
        # """存放文件的列表，每一个文件都是一个字典形式"""
        # 格式为{'filename': '1.jpg'，'body': b'\xff\xd8',content_type': 'image/jpeg'}
        # 格式为{'filename': 上传文件名称，'body': 文件二进制数据,content_type': 文件类型}
        if img_list:
            for upload_img in img_list:
                upload_obj = UploadProcess(self.settings['static_path'], upload_img['filename'])
                upload_obj.save_to_local(upload_img['body'])
                upload_obj.make_thumb()

                # 需要查询出user_id 是个问题
                user = User.query_User(self.current_user)
                PostPicture.post_pictures(upload_obj.make_image_url, upload_obj.make_thumb_url, user_id=user.id)

            self.redirect('/')
        else:
            self.render('upload.html')
