# -*-coding=utf-8-*-
from PIL import Image
import matplotlib.pyplot as plt
import requests,time
session = requests.Session()
import readconfig

username=readconfig.config().get('username','').strip()
password=readconfig.config().get('password','').strip()

def getCode():
    headers = {
        'Host': 'vexx.pro', 'Referer': 'http://vexx.pro/login.html', 'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
    url = 'http://vexx.pro/verify/code.html'
    s = session.get(url=url, headers=headers)

    with open('code.png', 'wb') as f:
        f.write(s.content)

    time.sleep(3)

    im=Image.open('code.png')
    plt.figure()
    plt.imshow(im)
    plt.show()
    
    code = raw_input('input the code: ')
    # im=Image.open('code.png')
    # im.show()
    print 'code is ', code

    login_url = 'http://vexx.pro/login/up_login.html'
    post_data = {
        'moble': user,
        'mobles': '+86',
        'password': password,
        'verify': code,
        'login_token': ''}

    login_header = {
        'Origin': 'http://vexx.pro',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Host': 'vexx.pro', 'X-Requested-With': 'XMLHttpRequest', 'Pragma': 'no-cache',
        'Referer': 'http://vexx.pro/login.html'}

    login_s = session.post(url=login_url, headers=login_header, data=post_data)
    print login_s.status_code

    zzc_url = 'http://vexx.pro/ajax/check_zzc/'
    zzc_header = {
        'X-Requested-With': 'XMLHttpRequest', 'Host': 'vexx.pro',
        'Referer': 'http://vexx.pro/finan/award.html', 'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
    zzc_s = session.get(url=zzc_url, headers=zzc_header)
    print zzc_s.text

def main():
    getCode()

if __name__ == '__main__':
    main()
