# TsinghuaBookCrawler

## 背景

最近疫情严重，为了方便大家在线学习，写了一个爬清华教参的 python 脚本，因为还有其它很多事情要处理，所以就写得比较简单了，也没有加图形界面。脚本中用户名和密码均仅用于清华服务的认证，不保存在本地，也不会上传到别处，这点我可以用人格担保，不放心的同学也可以自行阅读检查代码。

另外注意此脚本仅供方便大家学习之用，请勿将下载得到的电子书外传。

## 使用说明

清华教参平台：http://reserves.lib.tsinghua.edu.cn

main.py 中的前五行为可以设置的部分：

```
username = ''
password = ''
url = 'http://reserves.lib.tsinghua.edu.cn/book3//00004804/00004804000/FLASH/index.html'
processing_num = 8
del_img = True
```

username 为学号，password 为密码，url 为需要爬取的书籍（点击阅读全文之后的页面，这里暂时只能用http），processing\_num 为下载使用的进程数，del\_img 为是否删除下载过程中临时保存的图片。

设置完毕之后直接运行 main.py 即可，会自动下载到download目录下。

请大家注意自己的账户安全，下载完毕之后将username和password这两项清空。

## 环境

python 版本为 python3，需要安装 pymupdf：``pip install pymupdf``。

## 特性

### v1.0

* 支持自动认证清华身份，使用简单；
* 支持多进程快速下载；
* 支持"断点续传"，不会重复下载已经下载完成的部分；
* 支持自动识别书名和页数（书名也可能得到一串数字）。

## 示例

如果无法直接显示，可以下载下来看，图片存储在 example 文件夹下。

![example1](https://github.com/lflame/TsinghuaBookCrawler/blob/master/example/1.png)

![example2](https://github.com/lflame/TsinghuaBookCrawler/blob/master/example/2.png)

![example3](https://github.com/lflame/TsinghuaBookCrawler/blob/master/example/3.png)

## 说明

作者邮箱：315629555@qq.com, yangyr17@mails.tsinghua.edu.cn

能力和时间均有限，若有写得不好的地方，还望指正。
