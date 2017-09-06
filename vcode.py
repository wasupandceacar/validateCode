import requests
import re
from PIL import Image
import pytesser3

s = requests.Session()

PATH='F:/1.jpg'

PATH2='F:/2.jpg'

NAME='151250063'

PASSWORD='Hyj123456'

retrycount=0

#二值化
threshold = 140
table = []

def initTable():
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

def loadVcode():
    url = 'http://elite.nju.edu.cn/jiaowu/ValidateCode.jsp'
    data = s.get(url).content
    open(PATH, 'wb').write(data)

def twrify(name, save):
    #打开图片
    im = Image.open(name)
    #转化到灰度图
    imgry = im.convert('L')
    #保存图像
    #二值化，采用阈值分割法，threshold为分割点
    out = imgry.point(table,'1')
    region = (1, 1, 79, 19)
    # 裁切图片
    out = out.crop(region)
    out.save(save)

def getVcode():
    loadVcode()
    twrify(PATH, PATH2)
    s=pytesser3.image_file_to_string(PATH2)
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

def login(name, password):
    vcode=getVcode()
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
        retrycount+=1
        login(name, password)
    else:
        global retrycount
        print('登陆成功。重试'+str(retrycount)+"次。\ncookie:")
        print(s.cookies)
        retrycount=0

if __name__=="__main__":
    initTable()
    login(NAME,PASSWORD)
