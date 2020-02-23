import sys

import requests
import re
import os
from urllib.parse import urljoin
from auth_get import auth_get
from download_imgs import download_imgs

if __name__ == '__main__':
    username = ''
    password = ''
    url = 'http://reserves.lib.tsinghua.edu.cn/book3//00004804/00004804000/FLASH/index.html'
    processing_num = 8  # 进程数

    xml_suffix = urljoin('data/', 'setting.xml')
    img_suffix = '../HTML5/m/'
    candidate_img_suffix = ['jpg', 'png']
    session = requests.session()
    xml_url = urljoin(url, xml_suffix)
    img_path = urljoin(url, img_suffix)

    xml_res = auth_get(xml_url, session, username, password)
    s = str(xml_res.content, xml_res.apparent_encoding)
    page_count = int(re.search('<pagecount>(.*)</pagecount>', s).group(1))
    book_name = re.search('<ad_title>(.*)</ad_title>', s).group(1)
    if book_name.find('CDATA') != -1:
        book_name = re.search('CDATA\\[(.*?)\\]', book_name).group(1).strip()
    print('书名: %s  页数: %d' % (book_name, page_count))

    img_suffix = ''
    for suf in candidate_img_suffix:
        img_url = urljoin(img_path, '1.' + suf)
        print(img_url)
        img_res = auth_get(img_url, session, username, password)
        if img_res.status_code == 200:
            img_suffix = suf
            break
    if img_suffix == '':
        print('获取图片格式失败')
        sys.exit()
    else:
        print('图片格式:', img_suffix)

    download_imgs(session, username, password, img_path, img_suffix, page_count, os.path.join('download', book_name),
                  processing_num=processing_num)
    print('图片下载完成, 开始转换..')