# validateCode
南大教务系统验证码识别自动登录

1.安装Tesseract-OCR引擎，引擎自己网上找

2.安装pytesser3库
pip install pytesser3

3.在你Python库的site-packages里找到pytesser3的文件夹，先替换__init__.py，再把__init__.py中的tesseract_exe_name改为你tesseract的文件夹

4.写上自己的学号和密码，完成，登陆成功后session在cookie失效前都可以随便访问教务网了
