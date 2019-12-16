from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains  
import os
from PIL import Image
import requests
from io import BytesIO
import pytesseract 
import time
import cv2
import configparser

config = configparser.ConfigParser()
config.read('configuration.conf')
#My name ; My password
name = config.get('settings','name')
password = config.get('settings','password')
#网页截图保存路径
code_url =  config.get('settings','code_url')
#二维码截图保存路径
crop_url =  config.get('settings','crop_url')
#浏览器驱动所在路径
chromeDriver = config.get('settings','chromeDriver')


def startBrowser():
    #开启浏览器
    browser = webdriver.Chrome(chromeDriver)
    browser.get("http://kq.neusoft.com")
    time.sleep(3)

    #定位元素
    input_name = browser.find_elements_by_class_name("textfield")[0]
    input_secret = browser.find_elements_by_class_name("textfield")[1]
    input_code = browser.find_element_by_class_name("a")
    login_btn = browser.find_element_by_id("loginButton")
    code_img = browser.find_element_by_id("imgRandom")

    #验证码 位置 大小
    code_location = code_img.location
    print(code_location)
    size = code_img.size
    left = code_location['x']
    top = code_location['y']
    right = left + size['width']
    bottom = top + size['height']
    browser.save_screenshot(crop_url)
    image_all_page = Image.open(crop_url)
    snap_image = image_all_page.crop((left, top, right, bottom))
    snap_image.save(code_url)
    """ 
    #opencv 解析验证码 越解越乱
    cv2_img = cv2.imread(code_url)
    cv2_img = cv2.cvtColor(cv2_img,cv2.COLOR_BGR2GRAY)#灰值化
    cv2_img = cv2.adaptiveThreshold(cv2_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 1)#二值化    
    #线降噪
    w,h = cv2_img.shape[:2]
    for x in range(1,w-1):
        for y in range(1,h-1):
        #点降噪
            interference_point(cv2_img,x,y)
            count = 0
            if cv2_img[x-1,y] > 245 :
                count += 1
            if cv2_img[x,y-1] > 245 :
                count += 1
            if cv2_img[x+1,y] > 245 :
                count += 1
            if cv2_img[x,y+1] > 245 :
                count += 1
            if count >= 2 :
                cv2_img[x,y] = 245
    cv2.imwrite(code_url,cv2_img)                
    """    
    #解析验证码
    #browser.find_element_by_tag_name("body").send_keys(Keys.CONTROL + "t")
    #browser.get(image_url)

    #response = requests.get(image_url)
    #image = Image.open(BytesIO(response.content))
    #image.save(code_url)
    #verified_code = pytesseract.image_to_string(Image.open(code_url))
    verified_code = pytesseract.image_to_string(snap_image)
    if verified_code == "" :
        browser.quit()
        startBrowser()
        print("========= 正 =========")
    else :
        print(verified_code)
        print(len(verified_code))
        #输入用户名 密码 验证码
        time.sleep(3)
        #browser.back()

        input_name.send_keys(name)

        input_secret.send_keys(password)

        input_code.send_keys(verified_code)

        login_btn.click()
        
        #TODO 打卡
        time.sleep(3)
        sign_btn = browser.find_elements_by_class_name("mr36")[0]
        sign_btn.click()
        time.sleep(5)        


# 点降噪
def interference_point(img, x = 0, y = 0):
  
    # todo 判断图片的长宽度下限
    cur_pixel = img[x,y]# 当前像素点的值
    width,height = img.shape[:2]

    for x in range(0, width - 1):
      for y in range(0, height - 1):
        if y == 0:  # 第一行
            if x == 0:  # 左上顶点,4邻域
                # 中心点旁边3个点
                sum = int(cur_pixel) \
                      + int(img[x, y + 1]) \
                      + int(img[x + 1, y]) \
                      + int(img[x + 1, y + 1])
                if sum <= 2 * 245:
                  img[x, y] = 0
            elif x == height - 1:  # 右上顶点
                sum = int(cur_pixel) \
                      + int(img[x, y + 1]) \
                      + int(img[x - 1, y]) \
                      + int(img[x - 1, y + 1])
                if sum <= 2 * 245:
                  img[x, y] = 0
            else:  # 最上非顶点,6邻域
                sum = int(img[x - 1, y]) \
                      + int(img[x - 1, y + 1]) \
                      + int(cur_pixel) \
                      + int(img[x, y + 1]) \
                      + int(img[x + 1, y]) \
                      + int(img[x + 1, y + 1])
                if sum <= 3 * 245:
                  img[x, y] = 0
        elif y == width - 1:  # 最下面一行
            if x == 0:  # 左下顶点
                # 中心点旁边3个点
                sum = int(cur_pixel) \
                      + int(img[x + 1, y]) \
                      + int(img[x + 1, y - 1]) \
                      + int(img[x, y - 1])
                if sum <= 2 * 245:
                  img[x, y] = 0
            elif x == height - 1:  # 右下顶点
                sum = int(cur_pixel) \
                      + int(img[x, y - 1]) \
                      + int(img[x - 1, y]) \
                      + int(img[x - 1, y - 1])

                if sum <= 2 * 245:
                  img[x, y] = 0
            else:  # 最下非顶点,6邻域
                sum = int(cur_pixel) \
                      + int(img[x - 1, y]) \
                      + int(img[x + 1, y]) \
                      + int(img[x, y - 1]) \
                      + int(img[x - 1, y - 1]) \
                      + int(img[x + 1, y - 1])
                if sum <= 3 * 245:
                  img[x, y] = 0
        else:  # y不在边界
            if x == 0:  # 左边非顶点
                sum = int(img[x, y - 1]) \
                      + int(cur_pixel) \
                      + int(img[x, y + 1]) \
                      + int(img[x + 1, y - 1]) \
                      + int(img[x + 1, y]) \
                      + int(img[x + 1, y + 1])

                if sum <= 3 * 245:
                  img[x, y] = 0
            elif x == height - 1:  # 右边非顶点
                sum = int(img[x, y - 1]) \
                      + int(cur_pixel) \
                      + int(img[x, y + 1]) \
                      + int(img[x - 1, y - 1]) \
                      + int(img[x - 1, y]) \
                      + int(img[x - 1, y + 1])

                if sum <= 3 * 245:
                  img[x, y] = 0
            else:  # 具备9领域条件的
                sum = int(img[x - 1, y - 1]) \
                      + int(img[x - 1, y]) \
                      + int(img[x - 1, y + 1]) \
                      + int(img[x, y - 1]) \
                      + int(cur_pixel) \
                      + int(img[x, y + 1]) \
                      + int(img[x + 1, y - 1]) \
                      + int(img[x + 1, y]) \
                      + int(img[x + 1, y + 1])
                if sum <= 4 * 245:
                  img[x, y] = 0    
    return img

if __name__ == "__main__":
    startBrowser()
