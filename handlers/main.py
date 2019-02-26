import tornado.web
from pycket.session import SessionMixin
from utils.process_photo import get_imgs, save_upload_picture, make_thumb


class AuthBaseHandler(tornado.web.RequestHandler, SessionMixin):
    """使用pycket的session来验证用户"""

    def get_current_user(self):
        current_user = self.session.get('USER')
        if current_user:
            return current_user
        return None


class IndexHandler(AuthBaseHandler):
    """首页，说管子的用户图片流"""
    def get(self):
        imgs = get_imgs('static/upload')
        self.render('index.html', imgs=imgs)


class ExploreHandler(AuthBaseHandler):
    """发现货最近上传的图片页面"""

    @tornado.web.authenticated
    def get(self):
        imgs = get_imgs('static/upload/thumb')
        self.render('explore.html', imgs=imgs)


class PostHandler(tornado.web.RequestHandler):
    """单个图片详情页面"""
    def get(self,post_id):
        self.render('post.html',post_id=post_id)


class UploadHandler(tornado.web.RequestHandler):
    """处理图片上传逻辑"""

    def get(self, *args, **kwargs):
        self.render('upload.html')

    def post(self, *args, **kwargs):
        img_list = self.request.files.get('picture', [])
        # """存放文件的列表，每一个文件都是一个字典形式"""
        # 格式为{'filename': '1.jpg'，'body': b'\xff\xd8',content_type': 'image/jpeg'}
        # 格式为{'filename': 上传文件名称，'body': 文件二进制数据,content_type': 文件类型}
        for upload_img in img_list:
            # if img_list:
            #     upload_img = img_list[0]  # 循环方式更加完美
            save_to_path = save_upload_picture(upload_img)
            make_thumb(save_to_path)

        self.write('ok')
        # self.redirect('/upload')
