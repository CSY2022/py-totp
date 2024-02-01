# 一个Python实现的TOTP桌面端应用
- 一个基于python实现的totp应用，联网自动同步时间运行（当然也可以断网，但前提是你本地时间是准确的），解决电脑端登录Github不方便的问题。  
- 源码在src文件夹内，Github Actions会自动编译,最新的exe文件在artifact中，下载解压即可。（不保证100%可正常运行）
- 稳定版的exe可以去release下载
- 作者用PySimpleGUI写的图形界面，凑合着用吧。     
- 初始化的时候输入的密钥，储存在和exe文件同目录的key.txt中，可用文本编辑器修改
- 欢迎PR,Fork
