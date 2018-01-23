#-*-coding=utf-8-*-
import requests,json

with open('headers.json','r') as f:
    headers=json.load(f).get('headers')

def sendmail(email):
    url="https://www.nova98.com/sendmail.php"
    form_data={"email":email}
    ret=requests.post(url=url,data=form_data,headers=headers)
    print ret.status_code
    print ret.text
    try:
        print ret.json().get('info',"Fail to get info")
    except Exception,e:
        print e


def main():
    email='weigesysu@qq.com'
    sendmail(email)

if __name__ == '__main__':
    main()