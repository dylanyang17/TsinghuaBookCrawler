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
from utils import get_fmt

def get_input():
    """
    获得输入的各参数
    :return: [username, password, url, processing_num, quality, del_img, size, auto_resize, links_cnt]
    分别表示 username 学号、password 密码、url 爬取的首个链接、processing_num 进程数、quality PDF 质量（越高则PDF越清晰但大小越大）、
    del_img 是否删除临时图片、auto_resize 是否自动统一页面尺寸、links_cnt（链接数，也即章节数）
    """
    parser = argparse.ArgumentParser(description='Version: v2.1.3. Download e-book from http://reserves.lib.tsinghua.edu.cn. '
                                                 'By default, the number of processes is four and the temporary images '
                                                 'will not be preserved. \nFor example, '
                                                 '"python main.py http://reserves.lib.tsinghua.edu.cn/book5//00004634/00004634000/mobile/index.html".')
    parser.add_argument('url')
    parser.add_argument('-n', help='Optional, [1~16] (4 by default). The number of processes.', type=int, default=4)
    parser.add_argument('-q', help='Optional, [3~10] (10 by default). The quality of the generated PDF. The bigger the value, the higher the resolution.', type=int, default=10)
    parser.add_argument('-p', '--preserve', help='Optional. Preserve the temporary images.', action='store_true')
    parser.add_argument('-r', '--auto-resize', help='Optional. Automatically unify page sizes.', action='store_true')

    args = parser.parse_args()
    url = args.url
    processing_num = args.n
    quality = args.q
    del_img = not args.preserve
    auto_resize = args.auto_resize
    if processing_num not in list(range(1, 17)):
        print('Please check your parameter: -n [1~16]')
        parser.print_usage()
        sys.exit()
    if quality not in list(range(3, 11)):
        print('Please check your parameter: -q [3~11]')
        parser.print_usage()
        sys.exit()
    print('Student ID: ', end='')
    username = input()
    password = getpass.getpass('Password: ')
    links_cnt = input('Number of chapters(1 by default): ')
    if links_cnt == '':
        links_cnt = 1
    links_cnt = int(links_cnt)
    if links_cnt <= 0:
        print('There must be one chapter to download at least.')
        sys.exit()
    return [username, password, url, processing_num, quality, del_img, auto_resize, links_cnt]


if __name__ == '__main__':
    username, password, url0, processing_num, quality, del_img, auto_resize, links_cnt = get_input()
    js_relpath = 'mobile/javascript/config.js'
    img_relpath = 'files/mobile/'
    candi_fmts = ['jpg', 'png']
    session = requests.session()

    # 获取每一章的链接前缀, 存放到 urls 中
    urls = []
    if re.search('mobile/index.html', url0) is None:
        url0 = url0.replace('/index.html', '/mobile/index.html')
    st, ed = re.search('(/([^/]*)/)(mobile)', url0).span(2) # 获取"/mobile/"前一个分隔的首尾位置，如当url0="/products/mobile/smartphone"时返回(1,9)
    chap_len = ed - st
    chap0 = int(url0[st:ed])
    zero_len = chap_len - len(str(chap0))

    # 获得需要下载的所有图片url, 并存放在 img_urls 中
    book_name = ''
    page_cnt = 0
    img_urls = []
    displacement = 0
    for ind in range(links_cnt):
        while True:
            url = url0[:st] + ''.join(['0' for _ in range(zero_len)]) + str(chap0 + ind + displacement) + '/'
            js_url = urljoin(url, js_relpath)
            js_res = auth_get(js_url, session, username, password)
            s = str(js_res.content, js_res.apparent_encoding)
            if re.search(r'totalPageCount=(\d+)', s) is not None:
                break
            displacement += 1
        print(js_url)
        page_now = int(re.search(r'totalPageCount=(\d+)', s).group(1))
        if book_name == '':
            book_names =  re.search(r'bookConfig.bookTitle="(\d+)"', s);
            if(book_names is None):
                book_name = input("Book name Not Found! Please input the book name:")
                if(book_name is None):
                    book_name = "book"
            else:
                book_name = re.search(r'bookConfig.bookTitle="(\d+)"', s).group(1)
        print(book_name, page_now)
        print('Chapter: %d' % (ind + 1))
        img_fmt = get_fmt(url, img_relpath, candi_fmts, session, username, password)  # 获取图片格式
        # img_relpath = get_best_size(url, img_relpaths, img_fmt, size, session, username, password)  # 获取对应清晰度的相对路径
        print('')
        for i in range(1, page_now + 1):
            img_url = urljoin(url, img_relpath + '%d.%s' % (i, img_fmt))
            img_urls.append(img_url)
            print(img_url)
        page_cnt += page_now

    print('书名: %s  总页数: %d' % (book_name, page_cnt))
    save_dir = os.path.join('download', book_name)
    pdf_path = os.path.join(save_dir, book_name + '.pdf')
    if os.path.exists(pdf_path):
        print('该书已经下载, 停止下载')
        sys.exit()

    download_imgs(session, username, password, img_urls, page_cnt, save_dir,
                  processing_num=processing_num)
    print('图片下载完成')

    print('原始大小 PDF 转换中... quality：%d' % quality)
    imgs = [os.path.join(save_dir, '%d.%s' % (i, img_fmt)) for i in range(1, page_cnt + 1)]
    if os.path.exists(pdf_path):
        print('已经生成完毕, 跳过转换')
    else:
        img2pdf(imgs, pdf_path, quality, auto_resize)
        print('生成 PDF 成功：' + os.path.basename(pdf_path))

    if del_img:
        for img in imgs:
            if os.path.exists(img):
                os.remove(img)

        print('清理临时图片完成')
