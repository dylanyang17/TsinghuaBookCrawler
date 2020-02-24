# coding:utf-8
import sys
import argparse
import getpass
import requests
import re
import os
from urllib.parse import urljoin
from auth_get import auth_get
from download_imgs import download_imgs
from img2pdf import img2pdf


def get_input():
    """
    获得输入的各参数
    :return: [username, password, url, processing_num, del_img, size]
    """
    parser = argparse.ArgumentParser(description='Download e-book from http://reserves.lib.tsinghua.edu.cn. '
                                                 'By default, the number of processes is four and the temporary images '
                                                 'will not be preserved. \nFor example, '
                                                 '"python main.py http://reserves.lib.tsinghua.edu.cn/book3//00003597/00003597000/FLASH/index.html".')
    parser.add_argument('url')
    parser.add_argument('-s', help='Optional(3 by default), [1~3]. The size of downloaded images. For example, "-s 3" '
                                   'means the biggest size.', type=int, default=3)
    parser.add_argument('-n', help='Optional(4 by default), [1~16]. The number of processes.', type=int, default=4)
    parser.add_argument('-p', '--preserve', help='Optional. Preserve the temporary images.', action='store_true')

    args = parser.parse_args()
    url = args.url
    size = args.s
    processing_num = args.n
    del_img = not args.preserve
    if size not in [1, 2, 3]:
        print('Please check your parameter: -s [1~3]')
        parser.print_usage()
        sys.exit()
    if processing_num not in list(range(1, 17)):
        print('Please check your parameter: -n [1~16]')
        parser.print_usage()
        sys.exit()
    print('Student ID:', end='')
    username = input()
    password = getpass.getpass('Password:')
    size = 's' if size == 1 else ('m' if size == 2 else 'l')
    return [username, password, url, processing_num, del_img, size]


if __name__ == '__main__':
    username, password, url, processing_num, del_img, size = get_input()
    xml_suffix = urljoin('data/', 'setting.xml')
    img_suffix = '../HTML5/%s/' % size
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
    save_dir = os.path.join('download', book_name)
    if os.path.exists(os.path.join(save_dir, book_name + '.pdf')):
        print('该书已经下载过, 停止下载')
        sys.exit()

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

    download_imgs(session, username, password, img_path, img_suffix, page_count, save_dir,
                  processing_num=processing_num)
    print('图片下载完成, 开始转换..')
    pdf_path = os.path.join(save_dir, book_name + '.pdf')
    imgs = [os.path.join(save_dir, '%d.%s' % (i, img_suffix)) for i in range(1, page_count + 1)]
    if os.path.exists(pdf_path):
        print('已经生成完毕, 跳过转换')
    else:
        img2pdf(imgs, pdf_path)
        print('生成pdf成功：' + book_name + '.pdf')
    if del_img:
        print('清理临时图片完成')
        for img in imgs:
            os.remove(img)

