import requests
import re
import os
from PIL import Image
import pytesser3

s = requests.Session()

#验证码临时路径
PATH='F:/1.jpg'

#验证码二值化临时路径
PATH2='F:/2.jpg'

#学号自己填
NAME=''

#密码自己填
PASSWORD=''

retrycount=0

totalcount=0

#二值化用
threshold = 140
table = []

def initTable():
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

def loadVcode(path):
    url = 'http://elite.nju.edu.cn/jiaowu/ValidateCode.jsp'
    data = s.get(url).content
    open(path, 'wb').write(data)

def twrify(name, save):
    im = Image.open(name)
    #转化到灰度图
    imgry = im.convert('L')
    #二值化，采用阈值分割法，threshold为分割点
    out = imgry.point(table,'1')
    region = (1, 1, 79, 19)
    #裁切黑边
    out = out.crop(region)
    out.save(save)

def getVcode(language):
    loadVcode(PATH)
    twrify(PATH, PATH2)
    s=pytesser3.image_file_to_string(PATH2, language=language)
    num=4
    result=''
    for c in s:
        if num==0:
            break
        elif c==" ":
            pass
        else:
            result+=c
            num-=1
    return result

def deleteVcode():
    if os.path.exists(PATH):
        os.remove(PATH)
    if os.path.exists(PATH2):
        os.remove(PATH2)

def login(name, password, language):
    try:
        vcode=getVcode(language)
        loginurl='http://elite.nju.edu.cn/jiaowu/login.do'
        postData = {'userName': name,
                    'password': password,
                    'returnUrl': 'null',
                    'ValidateCode': vcode
                    }
        po=s.post(loginurl,data=postData).content
        upo=po.decode('utf-8')
        erlist = re.compile('验证码错误')
        ernum = re.findall(erlist, upo)
        if len(ernum)!=0:
            print('验证码错误。将重试。')
            global retrycount
            global totalcount
            retrycount+=1
            totalcount+=1
            deleteVcode()
            login(name, password, language)
        else:
            global retrycount
            print('登陆成功。重试'+str(retrycount)+"次。\ncookie:")
            retrycount = 0
            deleteVcode()
############# cookie在这，随便用
            print(s.cookies)
############# cookie在这，随便用
    except:
        print("未知错误")
        global retrycount
        global totalcount
        retrycount += 1
        totalcount += 1
        deleteVcode()
        login(name, password, language)

if __name__=="__main__":
    initTable()
    for i in range(50):
        login(NAME,PASSWORD, language='fontyp')
    global totalcount
    print("识别率：")
    print(100*100/(totalcount+100))
