PySimpleGUI_License = 'etygJ1MDaOWJNvlHb5neNElLVoH9lzwBZ0S4IM6CIBk9RalhdXmVVzsvby3vBElpcBisItsbIjkBx1pMYf2ZV6ujcc2AVEJ3RPCiIR6ZMeTJccxsNXjUMY1hMxztEI10NHi9wXivTtGqlCjXZZWQ55zKZFUURblnclG3xbvzemWG1ilnbfn2RAWnZlXPJgzgacWZ97u6I4jCoJx5LFC3JlO6YiW11plLR1mslLykcN37QRiwOJieLhmQgPJp30mgu6pQAIioLMC5JlOsYXWk1plUTjGFFkzsdoCOIL66IMuKmTZriPC0IasRIYkwN6vxbqXgBahTbOnQkbikOIijINiWL8CzJNDRd6XGNy0Pbq2H1jl1cXk6lXEXIUj5onihMyjAEQ5tMOzYYiiCLhCOJUEhYKX5R7lZSiXUN4zrdcWyVdkiI8j8oTiXMnDHU2v6MhjpIWv6MPj4ArytNECmI2sTIFklReh1d7GVV1FaeVHEBypncUmaV1znIYjWoFimM1DVUxvcM1j5IKv3MVjKA1y8N0SUIMsMIXkIVqt2YvWDl7spQuWqR5kncnmGVgztcUyhIW6sI6nkRml0bZDBEr5dOFDLAN3xMDDFMc0ANpTkYz4aQNGW9N1QdHGPxnvcbI2usIuSYq2A9HtvI2ivwMiWSOVFB1BHZzGKRAy3ZcX6NFzGILjyo2icM3TlAqzTLFjEIW1aMFyP41yJNRCS4vyKMcjNMJiCfXQm=5=o786b600125d4eafa8d4f0cb3eadab10c9f1e52018321187cfee681115b757bd569ab009c2a408ae84161aeece4e559b2206cba74c2d4564c814d0be8632fae5b5631a8c94b1ff312015cc0c8964246776d0fca03a0f8c836a8b1152551019913fcf4b127c1661982d0b6e68f0f7dd99da5197c182de41f95c1723f2942b716fd4112d37742653d00a703ecbd0ea7b801b91b80dd46a1e05899d39ebdc5a3a0baf61e9d74cd72ced230712eb3e23902ac2a918c14766e51aaf15baa24a56189a8e40bc83a349e9bdb45675a1f2e9e15052cb68e41fb64d5a285125997862a2cdf49d88407aee4ac66cda4b548f3b2ba27435d00c79883a012147fc1fbcbac88b661ccce2f97723c5d3694421e80cd74531ac0c615a254e9e4b79ca7f7f75e5c126186a4d3d53c2ba28c311542c04b356d9921357d250c11a0fb692fbaffdb1e836813da093343b393b013e7d95e4413f753694822cfa5be12ac7fea873cbdf30e5804b7d2917ac89db377373e01e56d9982fd42d447009abcba93d86a34cd3366a2658b512f9739929a4b7d1b94dfacab6099b71f4092e48c641a141557dd5990bb442c79b6262ffdd8d83ba8e4567dcf97b8fd5a792f7dec4cb2016595d0505356c9f8cc17fbfb266d7f961322ed33300164d1935533bc4a0b019701f2d85234ce7fa357f57388a5215ff9e0b2434aa3c72362182ebf2556d0be6371af2b786c'
import PySimpleGUI as sg
# 写入剪切板
import pyperclip as cb
# 时间有关
from time import time
from time import sleep
from os import remove
# 提供退出实现
import sys
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
    global secret_key
    layout = [
    [sg.Text('请输入你的密钥：')],
    [ sg.InputText(size=(26,1),key='-KEY-',default_text='',password_char='•',enable_events=True)],
    [sg.Button("    确定    "),sg.Button("    粘贴    "),sg.Button(key='-HIDDEN-')],
    ]
    window=sg.Window("初始化",layout)
    event, values = window.read(timeout=0)
    window['-HIDDEN-'].update('显示')
    hidden=True
    while True:
        event, values = window.read(timeout=0)
        if event == sg.WIN_CLOSED:
            window.close()
            sys.exit()
        if event == "    确定    " and str(values['-KEY-']) != '':
            secret_key = str(values['-KEY-'])
            break
        if event == "    粘贴    ":
            window['-KEY-'].update(str(sg.clipboard_get()))
        if event == "-HIDDEN-" and hidden == False:
            window['-KEY-'].update(password_char='•')
            window['-HIDDEN-'].update('显示')
            hidden=True
        else:
            if event == "-HIDDEN-" and hidden == True:
                window['-KEY-'].update(password_char='')
                window['-HIDDEN-'].update('隐藏')
                hidden=False
    # 格式化密钥
    secret_key=secret_key.replace(' ','').replace('\n','').replace('\r','')
    # 创建key.txt并储存密钥
    try:
        remove("key.txt")
    except:
        pass   
    f=open('./key.txt' ,'x')
    f.close()
    f=open('./key.txt' ,'w')
    f.write(secret_key)
    f.close()
    window.close()
    return secret_key
# 与NTP服务器同步时间
def ntp():
    try:
        # 向NTP服务器发送请求
        c = ntplib.NTPClient()
        response = c.request('ntp2.aliyun.com')
        return response.tx_time
    except:
        # 网络错误的处理
        return None
# 生成密钥
def generate_otp(secret,digits=6, hash_func=hashlib.sha1):
    # 这一段是网上抄的，至今都没有看懂
    global current_time
    global secret_key    
    try:
        time_step_count = current_time // 30
        time_step_bytes = struct.pack(">Q", time_step_count)
        hmac_hash = hmac.new(base64.b32decode(secret, casefold=True), time_step_bytes, hash_func).digest()
        offset = hmac_hash[-1] & 0x0F
        hash_value = hmac_hash[offset:offset+4]
        otp_value = struct.unpack(">I", hash_value)[0]
        otp_value = otp_value & 0x7FFFFFFF
        otp_value = str(otp_value % (10 ** digits)).zfill(digits)
    except:
        otp_value=None
    return otp_value
# 主程序 
def setup():
    # 规定字体字号与主题
    global secret_key
    sg.set_options(font=('Arial Bold', 18))
    sg.theme('Reddit')
    # 尝试获取密钥
    try:
        f=open('./key.txt' ,'r')
        secret_key=f.readline()
        f.close()
    except:
        secret_key=init()
    if secret_key == '':
        remove("key.txt")
        secret_key=init()
def mainfuction():
    global current_time
    global secret_key
    # 规定布局并显示主界面
    layout = [
        [sg.Text('TOTP:'), sg.Text(key='-TOTP-')],
        [sg.Text('有效期:'), sg.Text(key='-TIME-')],
        [sg.Button(" 复制 TOTP ")],
    ]
    window = sg.Window("TOTP",layout)
    wrong = False
    while True:
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
        # 计算有效期
        stop_time=30-(current_time % 30)
        start_time=current_time
        # 防止重复计算，浪费资源
        # 调用函数生成OTP
        otp = generate_otp(secret_key)
        if otp == None:
            wrong=True
        else:
            wrong=False    
        while 30-(current_time % 30)<=stop_time and 30-(current_time % 30)>=0 and (current_time-start_time)<30 and wrong == False:
        # 防止重复读取时间，浪费资源
            current_time=delay_time+time()
            # 显示实时刷新的窗口
            event, values = window.read(timeout=0.5)
            # 实时更新数据
            window['-TOTP-'].update(str(otp))
            window['-TIME-'].update(str(int(30-(current_time % 30)+1))+'s')
            # 检测按钮事件
            if event==" 复制 TOTP ":
                cb.copy(str(otp))
                window.close()
                sys.exit()
            if event == sg.WIN_CLOSED:
                window.close()
                sys.exit()
        if wrong == True:
            sg.popup_ok('密钥有误')
            init()                  
setup()
mainfuction()
