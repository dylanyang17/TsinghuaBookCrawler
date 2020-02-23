import os
import random
import requests
from multiprocessing.pool import Pool
from urllib.parse import urljoin
from auth_get import auth_get


def randstr(num):
    H = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    ret = ''
    for i in range(num):
        ret += random.choice(H)
    return ret


def get_tmpname():
    """
    返回一个随机的临时名字
    :return:
    """
    return '.tmp' + randstr(16)


def download_one(session, username, password, url, save_dir, filename):
    """
    下载一张图片
    :param session: Session 类型
    :param url: 下载的url
    :param save_dir: 保存的目录
    :param filename: 文件名
    :return:
    """
    save_path = os.path.join(save_dir, filename)
    try:
        res = auth_get(url, session, username, password, timeout=15)
    except requests.exceptions.Timeout:
        print('请求超时:', filename)
        return
    print('开始下载：' + filename)
    while True:
        tmp_name = get_tmpname()
        tmp_path = os.path.join(save_dir, tmp_name)
        if not os.path.exists(tmp_path):
            break
    with open(tmp_path, 'wb') as f:
        f.write(res.content)
    os.rename(tmp_path, save_path)
    print('下载图片成功：' + filename)


def download_imgs(session, username, password, img_path, img_suffix, page_count, save_dir, processing_num=4):
    """
    下载一本书的所有图片
    :param session: Session类型
    :param username: 用户名
    :param password: 密码
    :param img_path: 除了如"*.jpg"以外的url路径
    :param img_suffix: 图片后缀
    :param page_count: 页数
    :param save_dir: 保存的目录
    :param processing_num: 进程数，默认为 4
    :return:
    """
    os.makedirs(save_dir, exist_ok=True)
    fail = True
    while fail:
        p = Pool(processing_num)
        fail = False
        for i in range(1, page_count+1):
            filename = '%d.%s' % (i, img_suffix)
            url = urljoin(img_path, filename)
            path = os.path.join(save_dir, filename)
            if os.path.exists(path):
                print('已下载：%s, 跳过' % filename)
                continue
            fail = True
            p.apply_async(download_one, args=(session, username, password, url, save_dir, filename))
        p.close()
        p.join()