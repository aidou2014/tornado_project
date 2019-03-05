import os
from uuid import uuid4
from PIL import Image


class UploadProcess(object):
    UPLOAD_DIR = 'upload'
    SIZE = (300, 300)
    THUMB_DIR = 'thumb'

    def __init__(self, static_path, filename):
        self.static_path = static_path
        self.origin_name = filename
        self.new_name = self.get_new_name

    @property
    def get_new_name(self):
        """生成唯一的图片名"""
        _, ext = os.path.splitext(self.origin_name)
        return uuid4().hex + ext

    @property
    def upload_local_path(self):
        return os.path.join(self.static_path, self.make_image_url)

    def save_to_local(self, content):
        # save_to_path = 'static/upload/{}'.format(upload_img['filename'])
        with open(self.upload_local_path, 'wb') as f:
            f.write(content)

    @property
    def make_image_url(self):
        return os.path.join(self.UPLOAD_DIR, self.new_name)

    def make_thumb(self):
        im = Image.open(self.upload_local_path)
        im.thumbnail(self.SIZE)
        save_thumb_path = os.path.join(self.static_path, self.make_thumb_url)
        im.save(save_thumb_path)

    @property
    def make_thumb_url(self):
        name, ext = os.path.splitext(self.new_name)
        thumb_name = '{}_{}x{}{}'.format(name, *self.SIZE, ext)
        return os.path.join(self.UPLOAD_DIR, self.THUMB_DIR, thumb_name)
