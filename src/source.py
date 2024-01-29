from time import time
from time import sleep
from os import system
import ntplib
import hmac
import hashlib
import struct
import base64
import PySimpleGUI as sg
import pyperclip as cb

def init():
    secret_key = sg.popup_get_text('输入你的密钥：', title="初始化") 
    secret_key.replace(' ','')
    secret_key.replace('\n','')
    secret_key.replace('\r','')
    f=open('./key.txt' ,'x')
    f.close()
    f=open('./key.txt' ,'w')
    f.write(secret_key)
    f.close()
    return secret_key
def ntp():
    try:
      c = ntplib.NTPClient()
      response = c.request('http://cn.pool.ntp.org')
      return response.tx_time
    except:
      return None
    
def generate_otp(secret,digits=6, hash_func=hashlib.sha1):
    time_step_count = current_time // 30
    time_step_bytes = struct.pack(">Q", time_step_count)
    hmac_hash = hmac.new(base64.b32decode(secret, casefold=True), time_step_bytes, hash_func).digest()
    offset = hmac_hash[-1] & 0x0F
    hash_value = hmac_hash[offset:offset+4]
    otp_value = struct.unpack(">I", hash_value)[0]
    otp_value = otp_value & 0x7FFFFFFF
    otp_value = str(otp_value % (10 ** digits)).zfill(digits)
    return otp_value
sg.set_options(font=('Arial Bold', 18))
sg.theme('DarkAmber')
try:
    f=open('./key.txt' ,'r')
    secret_key=f.readline()
    f.close()
except:
    secret_key=init()
if secret_key==None:
    secret_key=init()
layout = [
   [sg.Text('TOTP:'), sg.Text(key='-TOTP-')],
   [sg.Text('有效期:'), sg.Text(key='-TIME-')],
   [sg.Button(" 复制 TOTP ")],
]
window=sg.Window("TOTP",layout)
while True:
  if secret_key == None:
      break
  global current_time
  ntp_time = ntp()
  local_time = time()
  if ntp_time:
    current_time=int(ntp_time)
    delay_time=ntp_time-local_time
  else:
      current_time=int(local_time)
      delay_time=0
  otp = generate_otp(secret_key)
  stop_time=30-(current_time % 30)
  while 30-(current_time % 30)<=stop_time and 30-(current_time % 30)>=0.5:
    current_time=delay_time+time()
    event, values = window.read(timeout=0)
    window['-TOTP-'].update(str(otp))
    window['-TIME-'].update(str(int(30-(current_time % 30)+1))+'s')
    if event==" 复制 TOTP ":
        cb.copy(str(otp))
        window.close()
    sleep(0.5)
