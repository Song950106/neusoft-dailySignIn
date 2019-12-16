1.安装python 附3.7版本安装包

2.将chromeDriver 拷贝至 chrome的安装路径下 默认是C:\Users\XXX\AppData\Local\Google\Chrome\Application
	请使用与chrome版本相匹配的webDriver 
	附版本匹配的webdriver 和 chrome安装包

3.下载python的依赖库
	// 如果不能直接访问外网 请设置代理 windows下密码中特殊字符可能需要转译
	set https_proxy=https://userName:password@IP:PORT
	//install libraries
	pip install -r requirements.txt

4.安装tesseract 附tesseract64位安装包

5.修改pytesseract配置
	修改路径 : python安装路径\Python37\Lib\site-packages\pytesseract\pytesseract.py
	修改pytesseract.py 中 tesseract_cmd的值;eg:
	tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'  #tesseract的默认安装路径

6.run script
python chrome.py