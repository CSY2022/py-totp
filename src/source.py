# 生成图形界面
import PySimpleGUI as sg
# 写入剪切板
import pyperclip as cb
# 时间有关
from time import time
from time import sleep
# 联网获取时间
import ntplib
# 生成密钥有关
import hmac
import hashlib
import struct
import base64
# 初始化:输入并保存密钥
def init():
    # 提示用户输入密钥的界面
    secret_key = sg.popup_get_text('输入你的密钥：', title="初始化") 
    # 格式化密钥
    secret_key=secret_key.replace(' ','').replace('\n','').replace('\r','')
    # 创建key.txt并储存密钥
    f=open('./key.txt' ,'x')
    f.close()
    f=open('./key.txt' ,'w')
    f.write(secret_key)
    f.close()
    return secret_key
# 与NTP服务器同步时间
def ntp():
    try:
      c = ntplib.NTPClient()
      # 向NTP服务器发送请求
      response = c.request('http://cn.pool.ntp.org')
      return response.tx_time
    except:
      # 网络错误的处理
      return None
# 生成密钥
def generate_otp(secret,digits=6, hash_func=hashlib.sha1):
    # 这一段是网上抄的，至今都没有看懂
    time_step_count = current_time // 30
    time_step_bytes = struct.pack(">Q", time_step_count)
    hmac_hash = hmac.new(base64.b32decode(secret, casefold=True), time_step_bytes, hash_func).digest()
    offset = hmac_hash[-1] & 0x0F
    hash_value = hmac_hash[offset:offset+4]
    otp_value = struct.unpack(">I", hash_value)[0]
    otp_value = otp_value & 0x7FFFFFFF
    otp_value = str(otp_value % (10 ** digits)).zfill(digits)
    return otp_value
# 主程序 
# 规定字体字号与主题
sg.set_options(font=('Arial Bold', 18))
sg.theme('Reddit')
# 尝试获取密钥
try:
    f=open('./key.txt' ,'r')
    secret_key=f.readline()
    f.close()
except:
    secret_key=init()
if secret_key==None:
    secret_key=init()
# 规定布局并显示主界面
layout = [
   [sg.Text('TOTP:'), sg.Text(key='-TOTP-')],
   [sg.Text('有效期:'), sg.Text(key='-TIME-')],
   [sg.Button(" 复制 TOTP ")],
]
window=sg.Window("TOTP",layout)
while True:
  # 防止空文件引发的bug
  if secret_key == None:
      break
  # 获取时间
  ntp_time = ntp()
  local_time = time()
  # 计算时间差
  if ntp_time:
    current_time=int(ntp_time)
    delay_time=ntp_time-local_time
  else:
      current_time=int(local_time)
      delay_time=0
  # 调用函数生成OTP
  otp = generate_otp(secret_key)
  # 计算有效期
  stop_time=30-(current_time % 30)
  # 防止重复计算，浪费资源
  while 30-(current_time % 30)<=stop_time and 30-(current_time % 30)>=0.5:
    # 防止重复读取时间，浪费资源
    current_time=delay_time+time()
    # 显示实时刷新的窗口
    event, values = window.read(timeout=0)
    # 实时更新数据
    window['-TOTP-'].update(str(otp))
    window['-TIME-'].update(str(int(30-(current_time % 30)+1))+'s')
    # 检测按钮事件
    if event==" 复制 TOTP ":
        cb.copy(str(otp))
        window.close()
    sleep(0.5)
