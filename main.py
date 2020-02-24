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
    :return: [username, password, url, processing_num, del_img, size, links_cnt]
    分别表示username学号、password密码、url爬取的首个链接、processing_num进程数、del_img是否删除临时图片、
    size图片大小（清晰度选择）、links_cnt（链接数，也即章节数）
    """
    parser = argparse.ArgumentParser(description='Version: v1.2. Download e-book from http://reserves.lib.tsinghua.edu.cn. '
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
    links_cnt = input('Number of chapters(1 by default):')
    if links_cnt == '':
        links_cnt = 1
    links_cnt = int(links_cnt)
    if links_cnt <= 0:
        print('There must be one chapter to download at least.')
        exit()
    size = 's' if size == 1 else ('m' if size == 2 else 'l')
    return [username, password, url, processing_num, del_img, size, links_cnt]


if __name__ == '__main__':
    username, password, url0, processing_num, del_img, size, links_cnt = get_input()
    xml_relpath = './HTML5/setting.xml'
    img_relpath = './HTML5/%s/' % size
    candidate_img_suffix = ['jpg', 'png']
    session = requests.session()

    # 获取每一章的链接前缀, 存放到 urls 中
    urls = []
    st, ed = re.search('(/([^/]*)/)((FLASH)|(HTML5)|(index))', url0).span(2)
    chap_len = ed - st
    chap0 = int(url0[st:ed])
    zero_len = chap_len - len(str(chap0))
    for i in range(links_cnt):
        url = url0[:st] + ''.join(['0' for _ in range(zero_len)]) + str(chap0 + i) + '/'
        urls.append(url)

    # 获取图片格式, 存放到 img_fmt
    img_fmt = ''
    for fmt in candidate_img_suffix:
        img_url = urljoin(urls[0], img_relpath + '1.' + fmt)
        print(img_url)
        img_res = auth_get(img_url, session, username, password)
        if img_res.status_code == 200:
            img_fmt = fmt
            break
    if img_fmt == '':
        print('获取图片格式失败')
        sys.exit()
    else:
        print('图片格式:', img_fmt)

    # 获得需要下载的所有图片url, 并存放在 img_urls 中
    book_name = ''
    page_cnt = 0
    img_urls = []
    for url in urls:
        xml_url = urljoin(url, xml_relpath)
        xml_res = auth_get(xml_url, session, username, password)
        s = str(xml_res.content, xml_res.apparent_encoding)
        page_now = int(re.search('<pagecount>(.*)</pagecount>', s).group(1))
        if book_name == '':
            book_name = re.search('<ad_title>(.*)</ad_title>', s).group(1)
            if book_name.find('CDATA') != -1:
                book_name = re.search('CDATA\\[(.*?)\\]', book_name).group(1).strip()
        for i in range(1, page_now + 1):
            img_url = urljoin(url, img_relpath + '%d.%s' % (i, img_fmt))
            img_urls.append(img_url)
        page_cnt += page_now

    print('书名: %s  总页数: %d' % (book_name, page_cnt))
    save_dir = os.path.join('download', book_name)
    if os.path.exists(os.path.join(save_dir, book_name + '.pdf')):
        print('该书已经下载过, 停止下载')
        sys.exit()

    download_imgs(session, username, password, img_urls, page_cnt, save_dir,
                  processing_num=processing_num)
    print('图片下载完成, 开始转换..')
    pdf_path = os.path.join(save_dir, book_name + '.pdf')
    imgs = [os.path.join(save_dir, '%d.%s' % (i, img_fmt)) for i in range(1, page_cnt + 1)]
    if os.path.exists(pdf_path):
        print('已经生成完毕, 跳过转换')
    else:
        img2pdf(imgs, pdf_path)
        print('生成pdf成功：' + book_name + '.pdf')
    if del_img:
        print('清理临时图片完成')
        for img in imgs:
            os.remove(img)
