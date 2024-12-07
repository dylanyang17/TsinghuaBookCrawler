# coding:utf-8
import os
import sys
import random
import signal

import requests
from multiprocessing.pool import Pool
from multiprocessing import Value
from urllib.parse import urljoin, quote
from auth_get import auth_get


terminate_flag = Value('b', False)

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


def download_one(botu_read_kernel, img_path, save_dir, filename):
    """
    下载一张图片
    :param botu_read_kernel: token
    :param img_path: 下载的url
    :param save_dir: 保存的目录
    :param filename: 文件名
    :param terminate_flag: 终止标志
    :return:
    """
    with terminate_flag.get_lock(): 
        if terminate_flag.value:
            return
    
    url_template = 'https://ereserves.lib.tsinghua.edu.cn/readkernel/JPGFile/DownJPGJsNetPage?filePath={img_path}'

    try:
        save_path = os.path.join(save_dir, filename)
        try:
            res = requests.get(url_template.format(img_path=quote(img_path)), cookies={'BotuReadKernel': botu_read_kernel})
            print(url_template.format(img_path=quote(img_path)))
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
        with terminate_flag.get_lock():
            terminate_flag.value = True
    except Exception as e:
        print(e)


def download_imgs(botu_read_kernel, page_urls, save_dir, processing_num):
    """
    下载一本书的所有图片
    :param botU_read_kernel: 下载token
    :param page_urls: 要下载的所有图片路径
    :param save_dir: 保存的目录
    :param processing_num: 进程数
    :return:
    """
    os.makedirs(save_dir, exist_ok=True)

    pool = None

    def terminate_pool(sig, frame):
        print('terminating')
        with terminate_flag.get_lock():
            terminate_flag.value = True
        if pool is None:
            exit(0)


    signal.signal(signal.SIGINT, terminate_pool)
    signal.signal(signal.SIGTERM, terminate_pool)

    fail = True

    try:
        while fail:
            pool = Pool(processing_num)
            fail = False
            download_names = []
            for chap_num, img_urls in enumerate(page_urls):
                for page_num, img_path in enumerate(img_urls):
                    filename = str(chap_num) + '_' + str(page_num) + '.' + img_path.split('/')[-1].split('.')[-1]
                    path = os.path.join(save_dir, filename)
                    if os.path.exists(path):
                        print('已下载：%s, 跳过' % filename)
                        continue
                    fail = True
                    download_names.append(filename)
                    pool.apply_async(download_one, args=(botu_read_kernel, img_path, save_dir, filename), error_callback=lambda x: print(x))
            if len(download_names) != 0:
                print(f'即将下载：', end='')
                for name in download_names:
                    print(name, end=' ')
                print(f'\n共需下载图片数：{len(download_names)}')
            pool.close()
            pool.join()
            pool = None

            with terminate_flag.get_lock():
                if terminate_flag.value:
                    exit(0)
    finally:
        if pool:
            pool.terminate()
