# coding:utf-8
import os
import fitz
import shutil
from PIL import Image


def img2pdf(imgs, pdf_path, quality):
    """
    利用图片生成pdf
    :param imgs: 图片列表, list类型
    :param pdf_path: 保存的pdf路径(包含文件名)
    :param quality: 质量参数，默认为 10
    :return: True 表示生成成功，False表示失败
    """
    intermediate_dir = os.path.join(os.path.dirname(pdf_path), 'intermediate')
    if not os.path.exists(intermediate_dir):
        os.mkdir(intermediate_dir)
    with fitz.open() as doc:
        page_count = len(imgs)
        for i, img in enumerate(imgs):
            print('正在转换: %d/%d' % (i+1, page_count))
            # 生成相应质量的临时文件
            tmp_img = os.path.join(intermediate_dir, os.path.basename(img))
            img_obj = Image.open(img)
            w, h = img_obj.size
            img_obj.resize((int(w / 10 * quality), int(h / 10 * quality))).save(tmp_img, "JPEG")

            # 插入到 PDF 中
            imgdoc = fitz.open(tmp_img)
            pdfbytes = imgdoc.convert_to_pdf()
            imgpdf = fitz.open("pdf", pdfbytes)
            doc.insert_pdf(imgpdf)
        doc.save(pdf_path)
    shutil.rmtree(intermediate_dir)
