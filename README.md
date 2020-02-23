# TsinghuaBookCrawler

## 背景

最近疫情严重，为了方便大家在线学习，写了一个爬清华教参的 python 脚本，因为还有其它很多事情要处理，所以就写得比较简单了，也没有加图形界面。脚本中要求输入的学号和密码为清华大学电子身份服务认证所需要，均仅用于清华官方服务的认证，以获得允许访问教参平台的书籍。学号和密码信息不会保存在本地，更不会上传到别处，这点我可以用人格担保，不放心的同学也可以自行阅读检查代码。

另外注意此脚本仅供方便大家学习之用，请勿将下载得到的电子书外传，以便于保护版权。一切滥用该脚本导致的不良后果，作者均不担责。

## 使用说明

### 环境

python 版本为 python3，需要安装 pymupdf：``pip install pymupdf``。

### 使用

用于下载清华教参平台上的电子书pdf版本，清华教参平台：http://reserves.lib.tsinghua.edu.cn

使用 ``python main.py -h`` 可以打印帮助信息：

```
usage: main.py [-h] [-n N] [-p] url

Download e-book from http://reserves.lib.tsinghua.edu.cn. By default, the number of processes is four and the temporary images will not be preserved.

For example, "python main.py http://reserves.lib.tsinghua.edu.cn/book3//00003597/00003597000/FLASH/index.html".

positional arguments:
  url

optional arguments:
  -h, --help      show this help message and exit
  -n N            Optional. The number of processes.
  -p, --preserve  Optional. Preserve the temporary images.
```

一般来说不加参数使用即可，默认进程数为4，例子如上帮助信息所述，在存放main.py的目录下用命令行执行：``python main.py http://reserves.lib.tsinghua.edu.cn/book3//00003597/00003597000/FLASH/index.html``，会自动下载到download子目录下。

## 特性

### v1.1

* 更改参数输入方式，提高安全性。

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
