# sqlmap-autoproxy
config sqlmap use proxy automatically(自动获取代理IP)

自己通过修改sqlmap源码实现了sqlmap注入时自动走代理的功能(自动获取免费代理,由于地域原因,获取的都是中国国内的代理IP)

## Install
方法1:
 > - 将autoproxy.py放到thirdparty目录下
 > - 用option.py 替换lib/core/option.py

方法2:
> 其实option.py只是修改了如下两处,也可以将autoproxy.py放到thirdparty下,然后自行修改lib/core/option.py文件
> 1. 添加`from thirdparty.autoproxy import main as getproxyip`
> 2. 在`conf.proxyList = []`后添加:
> ```python
> conf.proxyList = []
>     if conf.proxyFile == 'auto':
>         getproxyip()
>         for line in open(paths.SQLMAP_ROOT_PATH +"/thirdparty/proxy.txt", 'r'):
>             conf.proxyList.append("http://"+line)
>         return
> ```
图示:https://s1.ax1x.com/2020/08/06/ac5kct.png

## Usage
使用sqlmap时添加参数: --proxy-file auto 一定要是auto

## 原理
其实就是自己实现了一个自动获取代理的脚本,自动检测可用性后记录到文件,在sqlmap的init函数中,调用了`_setProxyList()`函数,该函数用于将代理文件中的IP放入conf.proxyList中,sqlmap会从这个列表中自动获取代理.所以魔改该函数使得当--proxy-file的值为auto时,自动调用获取代理的脚本,使用获取到的IP作为sqlmap的代理.

**autoproxy.py可以单独使用,生成的proxy.txt在autoproxy的同级目录中**

展示:https://s1.ax1x.com/2020/08/06/agx7vT.png

欢迎交流~共同进步~欢迎各位大佬帮忙提建议~
