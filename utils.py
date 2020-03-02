import sys
from urllib.parse import urljoin
from auth_get import auth_get


def get_fmt(url, img_relpath, candi_fmts, session, username, password):
    """
    :param url: url前缀
    :param img_relpath: 图片目录的相对路径
    :param candi_fmts: 候选的格式列表
    :param session: Session 类型
    :param username: 学号
    :param password: 密码
    :return: 实际的图片格式
    """
    img_fmt = ''
    print('自动获取图片格式中...')
    for fmt in candi_fmts:
        img_url = urljoin(url, img_relpath + '1.' + fmt)
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
    return img_fmt


def get_best_size(url, img_relpaths, img_fmt, size, session, username, password):
    """
    获得清晰度最高时对应的相对路径
    :param url: 前缀url
    :param img_relpaths: 对应的三个相对路径的列表
    :param img_fmt: 图片格式
    :param size: 用户给定的size参数，若为None才寻找最高清晰度
    :param session: Session 类型
    :param username: 学号
    :param password: 密码
    :return: 返回最佳相对路径
    """
    img_relpath = img_relpaths[1]
    if size is None:
        print('自动获取最高清晰度中...')
        mx = 0
        size = None
        for i, relpath in enumerate(img_relpaths):
            img_url = urljoin(url, relpath + '1.' + img_fmt)
            img_res = auth_get(img_url, session, username, password)
            if img_res.status_code == 200:
                clen = int(img_res.headers.get('Content-Length', default=-1))
                print('-s %d: %d' % (i + 1, clen))
                if clen > mx:
                    mx = clen
                    img_relpath = img_relpaths[i]
                    size = i + 1
        if size is None:
            print('自动获取清晰度失败, 默认使用 -s 2')
            img_relpath = img_relpaths[1]
        else:
            print('自动获取清晰度成功：-s %d' % size)
    else:
        img_relpath = img_relpaths[size - 1]
    return img_relpath
