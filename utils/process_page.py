import json


def process_all_page(post, num):
    """
    处理总页面数
    :param post: 数据库查询出来的图片列表
    :return: int 总页数
    """
    if len(post) < num:
        all_page = 1
        first_page = post
    elif len(post) % num == 0:
        all_page = len(post) // num
        first_page = post[:num]
    else:
        all_page = len(post) // num + 1
        first_page = post[:num]

    return all_page, first_page


def process_page_data(post):
    """
    处理后端的数据为json格式
    :param post: 数据库查询返回的对象
    :return: json的数据
    """
    my_list = []
    for p in post:
        my_dict = {}
        my_dict['id'] = p.id
        my_dict['thumb_url'] = p.thumb_url
        my_dict['image_url'] = p.image_url
        my_dict['user'] = p.post_user.username
        my_dict['better'] = p.good_num
        my_dict['collection'] = p.like_num
        my_list.append(my_dict)

    data = json.dumps(my_list)
    return data


def process_page_index(post1, post2):
    """
    处理后端的数据为json格式
    :param post: 数据库查询返回的对象
    :return: json的数据
    """
    all_dict = {}
    my_list1 = []
    my_list2 = []
    for p in post1:
        my_dict = {}
        my_dict['id'] = p.id
        my_dict['thumb_url'] = p.thumb_url
        my_dict['image_url'] = p.image_url
        my_dict['user'] = p.post_user.username
        my_dict['better'] = p.good_num
        my_dict['collection'] = p.like_num
        my_list1.append(my_dict)

    for p in post2:
        my_dict = {}
        my_dict['id'] = p.id
        my_dict['thumb_url'] = p.thumb_url
        my_dict['image_url'] = p.image_url
        my_dict['user'] = p.post_user.username
        my_dict['better'] = p.good_num
        my_dict['collection'] = p.like_num
        my_list2.append(my_dict)

    all_dict['left'] = my_list1
    all_dict['right'] = my_list2

    data = json.dumps(all_dict)
    return data
