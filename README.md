# TsinghuaBookCrawler

## 背景

最近疫情严重，购买教材较为困难，为了方便大家在线学习，写了一个爬取清华教参的 python 脚本，因为还有很多其它事情要做(Orz毛概还没写完呢)，所以就写得比较简单了。

功能上可以多进程爬取整本书的每一张图片（清晰度很高，可参见下面的实例），并自动合并得到 pdf 文件。下载过程支持“断点续传”，不会重复下载图片。脚本中要求输入的学号和密码为清华大学电子身份服务认证所需要，均仅用于清华官方服务的认证，以获得允许访问教参平台的书籍。学号和密码信息不会保存在本地，更不会上传到别处，这点我可以用人格担保，不放心的同学也可以自行阅读检查代码。

另外注意此脚本**仅供方便清华师生学习之用**，下载得到的电子书请务必不要进行传播（尤其是对校外的未授权者），也坚决反对任何批量下载书籍的违规行为。请大家自觉维护版权，合理使用资源，一切滥用该脚本导致的不良后果，作者概不负责。

## 使用说明

### 环境

python 版本为 python3，需要安装 pymupdf：``pip install pymupdf``。

### 使用

用于下载清华教参平台上的电子书pdf版本，清华教参平台：http://reserves.lib.tsinghua.edu.cn 。找到自己需要的书籍之后，进入阅读界面将网址复制过来即可。此处也可用https，但教参平台的证书过期，会导致打印很多Warning。

使用 ``python main.py -h`` 可以打印帮助信息：

```
usage: main.py [-h] [-s S] [-n N] [-p] url

Version: v1.2.1. Download e-books from http://reserves.lib.tsinghua.edu.cn. By default, the number of processes is four and the temporary images will not be preserved. For example, "python main.py http://reserves.lib.tsinghua.edu.cn/book3//00003597/00003597000/FLASH/index.html".

positional arguments:
  url

optional arguments:
  -h, --help      show this help message and exit
  -s S            Optional, [1~3] (Automatically choose the biggest size by
                  default). The size of downloaded images.
  -n N            Optional, [1~16] (4 by default). The number of processes.
  -p, --preserve  Optional. Preserve the temporary images.
```

一般来说不加参数使用即可，默认进程数为4，且将会自动下载最高清的版本。例子如上帮助信息所述，在存放main.py的目录下用命令行执行：``python main.py http://reserves.lib.tsinghua.edu.cn/book3//00003597/00003597000/FLASH/index.html``，在提示输入用户名和密码(密码不会显示)以及章节数后，将自动下载到download子目录下。

对于一般书籍来说，在提示输入章节数时直接回车跳过即可。

#### 多链接书籍下载——章节数参数

章节数为 v1.2 中加入特性，实际上指链接数。主要是为了方便下载给出了多个链接的少部分书目。此时只需要将第一个链接作为 url 传入，并且提示输入章节数时输入实际链接数即可。

例如书籍：``http://reserves.lib.tsinghua.edu.cn/Search/BookDetail?bookId=3cf9814a-33ce-4489-b025-c58140c26263``，找到其第一个链接之后，执行 ``python http://reserves.lib.tsinghua.edu.cn/book3//00001044/00001044000/FLASH/index.html``，并在提示输入章节数时输入 5 即可。

#### 有关清晰度

``-s {1, 2, 3}`` 可以显式设定清晰度，一般来说, 1、2、3 对应的清晰度依次递增，然而存在一些特例。故在 v1.2.1 版本中加入了对清晰度的自动选择（而不是默认``-s 3``），在没有指定清晰度时，将自动找到最高清晰度进行下载。

## 特性

### v1.2.1

* 修复v1.2中默认清晰度的设置，当不显式使用 ``-s {1, 2, 3}`` 指定清晰度时，将自动地对三种清晰度进行确认，将选择最高清晰度。

### v1.2

* 加入多章节书籍的一键下载和自动合并，使用更加方便；
* 加入``-s {1, 2, 3}``清晰度选择，且**提高默认清晰度**；
* 加入链接正则化统一处理，既可打开阅读页面再复制链接，也可以在进入阅读页面前用右键复制链接。

### v1.1

* 更改参数输入方式，提高安全性；
* 教参平台url支持 https。

版本 v1.0 中对于教参平台url不支持使用https，是因为教参平台的证书已经过期，会导致验证出错。考虑之后还是将 get 的 verify 关掉了，这会导致在使用https的时候产生很多警告（而不是直接抛出异常）。不过身份认证平台的证书并未过期，故该脚本对于涉及学号和密码的请求一直都使用更加安全的 https。

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

## 鸣谢

* 感谢awx同学对清晰度选择的建议，由此新增了清晰度选择的功能；
* 感谢cyz同学对默认清晰度问题的反馈，由此新增了自动选择清晰度的功能。

## 说明

作者邮箱：315629555@qq.com, yangyr17@mails.tsinghua.edu.cn

能力和时间均有限，若有写得不好的地方，还望指正。
