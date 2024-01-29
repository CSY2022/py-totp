from time import time
from time import sleep
from os import system
import ntplib
import hmac
import hashlib
import struct
import base64

def ntp():
    try:
      c = ntplib.NTPClient()
      response = c.request('http://cn.ntp.org.cn')
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
while True:  
  global current_time
  ntp_time = ntp()
  local_time = time()
  if ntp_time:
    current_time=int(ntp_time)
    delay_time=ntp_time-local_time
  else:
      current_time=int(local_time)
      delay_time=0
  secret_key = " Your secret key here"
  otp = generate_otp(secret_key)
  system('cls')
  print("生成的TOTP:", otp)
  print("有效期:",int(30-(current_time % 30)+0.5),"s")
  stop_time=30-(current_time % 30)
  while 30-(current_time % 30)<=stop_time and 30-(current_time % 30)>=0.5:
    current_time=delay_time+time()
    system('cls')
    print("生成的TOTP:", otp)
    print("有效期:",int(30-(current_time % 30)+0.5),"s")
    sleep(0.5)  
