import fitz


def img2pdf(imgs, pdf_path):
    """
    利用图片生成pdf
    :param imgs: 图片列表, list类型
    :param pdf_path: 保存的pdf路径(包含文件名)
    :return: True 表示生成成功，False表示失败
    """
    with fitz.open() as doc:
        page_count = len(imgs)
        for i, img in enumerate(imgs):
            print('正在转换: %d/%d' % (i, page_count))
            imgdoc = fitz.open(img)
            pdfbytes = imgdoc.convertToPDF()
            imgpdf = fitz.open("pdf", pdfbytes)
            doc.insertPDF(imgpdf)
        doc.save(pdf_path)
