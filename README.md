# TsinghuaBookCrawler

## 背景

最近疫情严重，购买教材较为困难，为了方便大家在线学习，写了一个爬取清华教参的 python 脚本，因为还有很多其它事情要做(Orz毛概还没写完呢)，所以就写得比较简单了。

功能上可以多进程爬取整本书的每一张图片（清晰度很高，可参见下面的实例），并自动合并得到 pdf 文件。下载过程支持“断点续传”，不会重复下载图片。由于双因子认证，脚本不再要求输入用户名和密码，而是需要手动获取 token。

另外注意此脚本**仅供方便清华师生学习之用**，下载得到的电子书请务必不要进行传播（尤其是对校外的未授权者），也坚决反对任何批量下载书籍的违规行为。请大家自觉维护版权，合理使用资源，一切滥用该脚本导致的不良后果，作者概不负责。

## 使用说明

### 环境

python 版本为 python3（已测试 python 3.7-3.13），使用 requirements.txt 一键安装依赖：``pip install -r requirements.txt``。

### 使用

用于下载清华教参平台上的电子书pdf版本，清华教参平台：https://ereserves.lib.tsinghua.edu.cn/ 。

使用 ``python main.py -h`` 可以打印帮助信息：

```
usage: main.py [-h] -t TOKEN [-n N] [-q Q] [-d] [-r] url

Version: v3.0. Download e-book from http://ereserves.lib.tsinghua.edu.cn. By default, the
number of processes is four and the temporary images WILL BE preserved. For example, "python
main.py https://ereserves.lib.tsinghua.edu.cn/bookDetail/c01e1db11c4041a39db463e810bac8f9
4af518935a1ec46ef --token eyJhb...". Note that you need to manually login the ereserves
website and obtain the token from the FIRST request after login, like "/index?token=xxx", due
to two-factor authentication (2FA).

positional arguments:
  url

options:
  -h, --help            show this help message and exit
  -t TOKEN, --token TOKEN
                        Required. The token from the "/index?token=xxx".
  -n N                  Optional, [1~16] (4 by default). The number of processes.
  -q Q                  Optional, [3~10] (10 by default). The quality of the generated PDF.    
                        The bigger the value, the higher the resolution.
  -d, --del-img         Optional. Delete the temporary images.
  -r, --auto-resize     Optional. Automatically unify page sizes.
```

一般来说只需要加上参数 --token 使用即可，默认进程数为4。例子如上帮助信息所述，在存放main.py的目录下用命令行执行：``"python main.py https://ereserves.lib.tsinghua.edu.cn/bookDetail/c01e1db11c4041a39db463e810bac8f9
4af518935a1ec46ef --token eyJhb...``，将自动下载到 download 子目录下。

必需参数说明：
* 链接：书籍的详情页面链接，例如 https://ereserves.lib.tsinghua.edu.cn/bookDetail/c01e1db11c4041a39db463e810bac8f9
* token：在浏览器中用 F12 打开开发者工具，选择 “Network”。此时登录教参平台（注意需要先打开开发者工具，再登录），可以看到一条 “index?token=eyJh...” 的请求，等号之后的内容即为 token，复制下来作为参数传递给程序即可。


### 高级

#### 自动统一页面尺寸 (beta)

一些书籍不同页面的尺寸不同，影响观感，所以加入了 -r/--auto-resize 可选参数，用于自动统一页面尺寸。

## 特性

### v3.0 —— 2024/11/7

教参平台再次更新（变为 ereserves，而不是原本的 reserves），所以更新了 v3.0 版本。由于联邦认证要求双因子认证（2FA），目前的脚本取消了用户名和密码输入机制，改为手动获取 token 作为参数传入。

随之更新的一些其他特性：

* 修复了下载图片时 Ctrl+C 异常的问题；
* 修正 requirements.txt 以及 multiprocessing 处理代码，兼容不同 python 版本。
* 目前默认保留下载图片，可以加上 -d 取消保留。

### v2.1.3 —— 2023/11/17

* 增加了 -r/--auto-resize 参数，可以自动统一页面尺寸。

### v2.1.2 —— 2023/9/18

修复了下载部分书籍时存在的 bug，包括：

* 部分书籍网页信息中不存在 book_name，导致无法下载；
* 部分书籍章节序号不连续。

### v2.1.1 —— 2023/1/22

* 更新 PyMyPDF 版本

### v2.1 —— 2021/3/4

* 大幅优化了几乎同等质量下生成的 PDF 文件大小；
* 支持质量选项 ``-q [3~10]``，默认为 10 （最高质量），调小该值可以在降低清晰度的前提下降低 PDF 文件大小，若需多次测试合适清晰度建议开启 ``-p`` 选项以避免多次下载图片文件。

### v2.0 —— 2021/2/21

由于教参平台接口更新，于是该脚本也迎来了 v2.0 版本，目前测试中发现影响不大，受到影响的特性有：

* 书名提取可能失效，此时按照旧版本习惯会使用数字串进行代替；
* 由于新接口似乎只提供了唯一清晰度，于是清晰度选择被取消。

如果遇到问题，请及时联系作者，谢谢。

### v1.2.2

* 对于多章节最高清晰度不同的少数情况进行了处理，将对每个章节链接都进行一遍最高清晰度和图片格式的确定；
* 改进异常处理，修复网络状况不稳定时进程阻塞的bug。

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

* 感谢 awx 同学对清晰度选择的建议，由此新增了 v1.2 中清晰度选择的功能；
* 感谢 cyz 同学对默认清晰度问题的反馈，由此新增了 v1.2.1 中自动选择清晰度的功能；
* 感谢 sck 同学对不同章节最高清晰度设定可能不同这一问题的反馈，由此在 v1.2.2 中改进了自动选择清晰度的功能；
* 感谢 Thinzhang 同学反馈教参平台采用的新接口相关问题，由此更新了 v2.0 版本；
* 感谢 zhaofeng-shu33 和 HongYurui 同学反馈 PyMyPDF 版本问题，由此更新了 v2.1.1 版本。
* 感谢 Tsingshanyuan 同学反馈部分书籍网页信息中不存在 book_name 的问题，感谢 Long-Miao 同学反馈部分书籍存在章节序号不连续的问题，由此更新了 v2.1.2 版本。
* 感谢 Long-Miao 同学反馈页面尺寸统一性问题，并提交初步 PR，由此更新了 v2.1.3 版本。
* 感谢 baron0426 同学对 ereserves 新版教参平台 API 的分析，并完成了对应的核心代码编写，以此为基础更新了 v3.0 版本。


近期时间有限，非常感谢各位反馈的同学，尤其是 zhaofeng-shu33, Tsingshanyuan， Long-Miao 直接提 PR 完成了修复。此外，特别感谢 baron0426 对 v3.0 版本的贡献。

## 说明

作者邮箱：315629555@qq.com, yyr22@mails.tsinghua.edu.cn

能力和时间均有限，若有写得不好的地方，还望指正。
