# coding:utf-8
import os
import sys
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
    try:
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
    except KeyboardInterrupt:
        pid = os.getpid()
        print('子进程 %d 被终止...' % pid)
    except Exception as e:
        print(e)


def download_imgs(session, username, password, img_urls, page_count, save_dir, processing_num):
    """
    下载一本书的所有图片
    :param session: Session类型
    :param username: 用户名
    :param password: 密码
    :param img_urls: 要下载的所有图片路径
    :param page_count: 页数
    :param save_dir: 保存的目录
    :param processing_num: 进程数
    :return:
    """
    os.makedirs(save_dir, exist_ok=True)
    fail = True
    img_fmt = img_urls[0][img_urls[0].rfind('.')+1:]
    try:
        while fail:
            p = Pool(processing_num)
            fail = False
            for i, img_url in enumerate(img_urls):
                filename = '%d.%s' % (i+1, img_fmt)
                path = os.path.join(save_dir, filename)
                if os.path.exists(path):
                    print('已下载：%s, 跳过' % filename)
                    continue
                fail = True
                p.apply_async(download_one, args=(session, username, password, img_url, save_dir, filename))
            p.close()
            p.join()
    except KeyboardInterrupt:
        print('父进程被终止')
        pid = os.getpid()
        os.popen('taskkill.exe /f /pid:%d' % pid)
