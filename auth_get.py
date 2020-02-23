# coding:utf-8
import requests
import re
import sys

def auth_get(url, session, username, password, timeout=None):
    """
    利用session采用自动认证清华服务器的GET访问，若已经认证则不会重复认证
    :param url: 访问的url
    :param session: 会话
    :param username: 用户名
    :param password: 密码
    :param timeout: 超时时间，默认为空
    :return: 返回获得的响应
    """
    login_url = 'https://id.tsinghua.edu.cn/do/off/ui/auth/login/check'
    res = session.get(url, timeout=timeout, verify=False)
    try:
        if str(res.content, 'utf-8').find('清华大学用户电子身份服务系统') != -1:
            print('正在进行自动认证...')
            data = {}
            data['i_user'] = username
            data['i_pass'] = password
            login_res = session.post(login_url, data=data)
            content = str(login_res.content, 'utf-8')
            tmp = re.search('(http.*ticket.*)"', content)
            if tmp == None:
                print('认证失败, 请检查用户名和密码')
                sys.exit()
            print('认证成功')
            ticket_url = tmp.group(1)
            res = session.get(ticket_url, timeout=timeout, verify=False)
    except UnicodeDecodeError:
        pass
    return res