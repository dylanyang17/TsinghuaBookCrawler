# coding:utf-8
import sys
import argparse
import getpass
import requests
import re
import os
from download_imgs import download_imgs
from img2pdf import img2pdf
from utils import is_image, get_chap_page
from add_toc import add_toc

def get_input():
    """
    获得输入的各参数
    :return: [url, token, processing_num, quality, del_img]
    分别表示 url 爬取的首个链接、token、processing_num 进程数、quality PDF 质量（越高则PDF越清晰但大小越大）、
    del_img 是否删除临时图片、auto_resize 是否自动统一页面尺寸
    """
    parser = argparse.ArgumentParser(description='Version: v3.0. Download e-book from http://ereserves.lib.tsinghua.edu.cn. '
                                                 'By default, the number of processes is four and the temporary images '
                                                 'WILL BE preserved. \nFor example, '
                                                 '"python main.py https://ereserves.lib.tsinghua.edu.cn/bookDetail/c01e1db11c4041a39db463e810bac8f9 --token eyJhb...". \n'
                                                 'Note that you need to manually login the ereserves website and obtain the token from the FIRST request after login, like "/index?token=xxx", due to two-factor authentication (2FA).')
    parser.add_argument('url')
    parser.add_argument('-t', '--token', help='Required. The token from the "/index?token=xxx".', type=str, required=True)
    parser.add_argument('-n', help='Optional, [1~16] (4 by default). The number of processes.', type=int, default=4)
    parser.add_argument('-q', help='Optional, [3~10] (10 by default). The quality of the generated PDF. The bigger the value, the higher the resolution.', type=int, default=10)
    parser.add_argument('-d', '--del-img', help='Optional. Delete the temporary images.', action='store_true')
    parser.add_argument('-r', '--auto-resize', help='Optional. Automatically unify page sizes.', action='store_true')

    args = parser.parse_args()
    url = args.url
    token = args.token
    processing_num = args.n
    quality = args.q
    del_img = args.del_img
    auto_resize = args.auto_resize
    return [url, token, processing_num, quality, del_img, auto_resize]


def get_scan_id(url, token):
    get_book_read_id_url_format = 'https://ereserves.lib.tsinghua.edu.cn/userapi/MyBook/getBookDetail?bookId={book_view_id}'
    get_book_resource_url = 'https://ereserves.lib.tsinghua.edu.cn/userapi/ReadBook/GetResourcesUrl'
    get_book_read_id_url = get_book_read_id_url_format.format(book_view_id=url.split('/')[-1])
    res = requests.get(get_book_read_id_url, headers={'Jcclient': token})
    if res.json()['data'] is None:
        print('Token 不正确或过期，请重新获取')
        exit(1)
    book_real_id = res.json()['data']['jc_ebook_vo']['urls'][0]['READURL']
    res = requests.post(get_book_resource_url, json={'id': book_real_id}, headers={'Jcclient': token})
    book_access_url = res.json()['data']
    res = requests.get(book_access_url, allow_redirects=False)
    cookies = res.cookies
    botu_read_kernel = cookies.get('BotuReadKernel')
    res = requests.get(res.headers['Location'], cookies=cookies)
    scan_id = re.search(r'<input type="hidden" id="scanid" name="scanid" value="([^"]+)">', res.text).group(1)
    return [botu_read_kernel, book_real_id, scan_id]


def get_book_chapters(botu_read_kernel, scan_id):
    url = 'https://ereserves.lib.tsinghua.edu.cn/readkernel/KernelAPI/BookInfo/selectJgpBookChapters'
    res = requests.post(url, headers={'BotuReadKernel': botu_read_kernel}, data={'SCANID': scan_id})
    json_data = res.json()['data']
    return [x['EMID'] for x in json_data], [x['EFRAGMENTNAME'] for x in json_data]


def get_book_pages(botu_read_kernel, book_real_id, emids):
    url = 'https://ereserves.lib.tsinghua.edu.cn/readkernel/KernelAPI/BookInfo/selectJgpBookChapter'
    page_urls = []
    for emid in emids:
        res = requests.post(url, headers={'BotuReadKernel': botu_read_kernel}, data={'EMID': emid, 'BOOKID': book_real_id})
        page_urls.append([x['hfsKey'] for x in res.json()['data']['JGPS']])
    return page_urls


def get_chapter_front(imgs, chap_names):
    chap_front = {}
    for i, img in enumerate(imgs):
        chap, page = get_chap_page(img)
        if page == 0:
            chap_front[chap_names[chap]] = i
    return chap_front


if __name__ == '__main__':
    url, token, processing_num, quality, del_img, auto_resize = get_input()
    query_chapters_url  = 'https://ereserves.lib.tsinghua.edu.cn/readkernel/KernelAPI/BookInfo/selectJgpBookChapters'
    query_chapter_url = 'https://ereserves.lib.tsinghua.edu.cn/readkernel/KernelAPI/BookInfo/selectJgpBookChapter'
    botu_read_kernel, book_real_id, scan_id = get_scan_id(url, token)
    emids, chap_names = get_book_chapters(botu_read_kernel, scan_id)
    page_urls = get_book_pages(botu_read_kernel, book_real_id, emids)

    save_dir = os.path.join('downloads', book_real_id)
    print('Book ID: %s' % (book_real_id))
    pdf_path = os.path.join(save_dir, book_real_id + '.pdf')
    if os.path.exists(pdf_path):
        print('该书已经下载, 停止下载')
        sys.exit()

    download_imgs(botu_read_kernel, page_urls, save_dir, processing_num)
    print('图片下载完成')

    print('原始大小 PDF 转换中... quality：%d' % quality)

    imgs = list(sorted(filter(is_image, os.listdir(save_dir)), key=get_chap_page))
    chap_front = get_chapter_front(imgs, chap_names)
    chap_front = sorted(chap_front.items(), key=lambda x: x[1])
    named_pdf_path = os.path.join(save_dir, chap_front[0][0] + '.pdf')

    if len(imgs) == 0:
        print('图片格式可能未列入，请检查 utils.py 中的 IMG_SUFFIXES')
        exit(1)

    imgs = list(map(lambda x: os.path.join(save_dir, x), imgs))
    img2pdf(imgs, pdf_path, quality, auto_resize)
    print('生成 PDF 成功：' + os.path.basename(pdf_path))
    add_toc(pdf_path, named_pdf_path, chap_front)
    print('添加目录完成')

    if del_img:
        for img in imgs:
            if os.path.exists(img):
                os.remove(img)
        print('清理临时图片完成')
