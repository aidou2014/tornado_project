import glob  # 图片展示
import os

from PIL import Image


def get_imgs(path):
    """
    用于获取特定目录的文件列表
    :return: 一个带路径的文件列表
    """
    return glob.glob('{}/*.jpg'.format(path))


def save_upload_picture(upload_img):
    """
    处理上传文件的保存工作
    :param upload_img: 单个文件字典
    :return: 返回路径save_to_path
    """
    save_to_path = 'static/upload/{}'.format(upload_img['filename'])
    with open(save_to_path, 'wb') as f:
        f.write(upload_img['body'])
    return save_to_path


def make_thumb(save_to_path):
    """
    制作上传文件的缩略图
    :param save_to_path: 文件路径参数
    :param thumb_name: 缩略图名称
    :return: None
    """
    size = (200, 200)
    im = Image.open(save_to_path)
    im.thumbnail(size)
    name, ext = os.path.splitext(os.path.basename(save_to_path))
    im.save('static/upload/thumb/thumb_{}_{}x{}{}'.format(
        name, *size, ext
    ))
