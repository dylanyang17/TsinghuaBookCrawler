import sys

import requests
import re
import os
from urllib.parse import urljoin
from auth_get import auth_get
from download_imgs import download_imgs
from img2pdf import img2pdf

if __name__ == '__main__':
    username = ''
    password = ''
    url = 'http://reserves.lib.tsinghua.edu.cn/book3//00001561/00001561009/FLASH/index.html'
    processing_num = 8  # 进程数
    del_img = True      # 下载完毕之后是否删除过程中保存的图片

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

    save_dir = os.path.join('download', book_name)
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
        print('删除图片完成')
        for img in imgs:
            os.remove(img)

