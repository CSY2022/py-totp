<h1 align="center">
  <br>
  TOTP on Python
  <br>
</h1>

<h4 align="center">一个Python实现的TOTP桌面端应用</h4>

![screenshot 1](https://mirror.ghproxy.com/?q=https://raw.githubusercontent.com/CSY2022/py-totp/main/img/5.png)
<h5 align="center">
  软件截图
</h5>

![screenshot 1](https://mirror.ghproxy.com/?q=https://raw.githubusercontent.com/CSY2022/py-totp/main/img/4.png)
<h5 align="center">
  软件截图
</h5>
<br>

## 软件特色

* 基于Python实现，可轻松在电脑运行，解决你没有手机就上不了Github的烦恼    
* 联网启动时自动连接NTP服务器同步时间，电脑时间不准不是问题 （然而软件不联网依然是可以运行的哦）
* 简单的GUI界面，傻瓜式的操作，轻量化的实现，体验飞一般的效率 ~~（其实是作者水平有限，只能写这么一点）~~     
* 开放源代码，安全可靠，您的密钥永远储存在本地，不必担心泄漏问题（指不必担心由本软件产生的泄漏问题）     

## 使用方法

1. 下载 - 您可以从下方的[Releases](https://github.com/CSY2022/py-totp/releases/)下载稳定版本。如果你极富有探险精神，你也可以去Github Actions最新构建的Artifacts中下载实时构建的测试版本(不推荐，由此造成的电脑死机，人类灭绝，地球爆炸，宇宙崩塌等后果责任自负)
 
Pyinstaller打包实时状态
<a href="https://github.com/CSY2022/py-totp/actions"><img src="https://shields.io/github/actions/workflow/status/CSY2022/py-totp/main.yml?branch=main&logo=github&label=Build&style=for-the-badge" align="center" /></a>
Nuitka打包实时状态
<a href="https://github.com/CSY2022/py-totp/actions"><img src="https://shields.io/github/actions/workflow/status/CSY2022/py-totp/main2.yml?branch=main&logo=github&label=Build&style=for-the-badge" align="center" /></a>

2. 下载完成后打开     
![screenshot 3](https://mirror.ghproxy.com/?q=https://raw.githubusercontent.com/CSY2022/py-totp/main/img/2.png)      
出现了上图所示的界面后输入你的 **Secret Key**
如果你手头上拿到的是一个二维码，而不是Secret Key，你可以使用解码器(如草料二维码)对你拿到的二维码解码(不会的可以百度)，
会得到那一串形如 otpauth://totp/Github/XXX?period=30&digits=6&algorithm=SHA1&secret=ABCDEFGHIJKLMNOP&issuer=XXXXXX   的东西，其中 **ABCDEFGHIJKLMNOP** 就是你的Secret Key，填入即可。     

3. 接着会出现如图的界面    
![screenshot 4](https://mirror.ghproxy.com/?q=https://raw.githubusercontent.com/CSY2022/py-totp/main/img/1.png)     
说明你已经完成了软件的配置（如报错，请检查 Secret Key输入是否正确！）

- Tip:只有第1次启动需要配置哦

## TO DO

- 增加对多个TOTP认证的支持
- 增加二维码相关功能
- 优化导入导出的方案
- 本地加密储存
- 优化软件大小以及启动速度
- 增加深色模式
- 还有好多好多......（欢迎PR，Fork使这个软件更加完善）


## 关于

- 作者是一个高一学生，平时学业也很紧张，这是寒假练手的一个项目，写的水平很差，大家请多多包容
- 欢迎PR，Fork等
- 使用的第三方库：ntplib pyperclip PySimpleGUI    


## 许可证

DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
