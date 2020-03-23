#backlog use a headless browser

print('loading a new preview frame')

import os
import time
import shutil
import requests
from PIL import Image
from bs4 import BeautifulSoup
from selenium import webdriver

token = os.environ.get("USER_TOKEN")
graph_api_version = 'v6.0'
ad_preview_photo = '23844522939890593'
params = {'access_token': token,
    'ad_format': "DESKTOP_FEED_STANDARD"}

r = requests.get('https://graph.facebook.com/' + graph_api_version + '/' + ad_preview_photo + '/previews', params = params)
iframe = r.json()['data'][0]['body']
soup = BeautifulSoup(iframe, 'html.parser')
preview_url = soup.find_all('iframe')[0]['src']

def replace_innerHTML(xpath, new_text, driver):
    element = driver.find_element_by_xpath(xpath)
    new_element = "arguments[0].innerText = '" + new_text + "'"
    driver.execute_script(new_element, element)

def replace_logo(new_logo_url, driver):
    element = driver.find_element_by_class_name('_s0')
    new_element = "arguments[0].src = '" + new_logo_url + "'"
    driver.execute_script(new_element, element)

def replace_main_img(img_url,driver):
    current_size = driver.find_element_by_class_name('uiScaledImageContainer')
    size = current_size.get_attribute('style')
    width = int(size.split('width:')[1].split('px;')[0].strip())
    height = int(size.split('height:')[1].split('px;')[0].strip())
    ratio = width / height
    #get the ratio of the new image
    r = requests.get(img_url, stream = True)
    local_file = open('local_image.jpg', 'wb')
    r.raw.decode_content = True
    shutil.copyfileobj(r.raw, local_file)
    img = Image.open('local_image.jpg')
    new_height =  width * (img.height / img.width)
    new_ratio = 'width: ' + str(width) + 'px;' + ' height: ' + str(int(round(new_height,0))) + 'px;'
    new_element = "arguments[0].style = '" + new_ratio + "'"
    driver.execute_script(new_element, current_size)
    img_element = driver.find_element_by_class_name('scaledImageFitWidth')
    new_element = "arguments[0].src = '" + img_url + "'"
    driver.execute_script(new_element, img_element)


def screenshot_element(element_id, out_name, driver):
    element = driver.find_element_by_class_name(element_id)
    #element.screenshot('test.png')
    location = element.location
    size = element.size
    driver.save_screenshot(out_name);
    x = location['x']
    y = location['y']
    width = location['x']+size['width']
    height = location['y']+size['height']
    im = Image.open(out_name)
    im.height
    im.width
    im = im.crop((int(x), int(y), int(width) * 2, int(height) * 2))
    im.save(out_name)


def linked_ad_template(copy, new_img, logo, page_name,engagement, screenshot_element_id = '' ,screenshot_out = ''):
    driver = webdriver.Chrome(executable_path = "/Users/Nick/Downloads/chromedriver")
    driver.get(preview_url)
    #page_name
    replace_innerHTML('/html/body/div[1]/div/div/div/div/div/div[2]/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div[2]/h5/span/span/a', page_name, driver)
    #copy
    replace_innerHTML('/html/body/div[1]/div/div/div/div/div/div[2]/div[1]/div[2]/div[2]', copy,driver)
    #Engagement
    replace_innerHTML('/html/body/div[1]/div/div/div/div/div/div[2]/div[2]/form/div[1]/div/div/div/div[1]/div/a/span[1]', str(engagement) + ' Engagements', driver)
    replace_innerHTML('/html/body/div[1]/div/div/div/div/div/div[2]/div[2]/form/div[1]/div/div/div/div[1]/div/a/span[2]', '', driver)
    replace_innerHTML('/html/body/div[1]/div/div/div/div/div/div[2]/div[2]/form/div[1]/div/div/div/div[1]/div/a/span[3]', '', driver)
    #add logo
    replace_logo(logo,driver)
    #replace img
    replace_main_img(new_img,driver)
    if screenshot_out == '':
        driver.close()
    else:
        time.sleep(2)
        screenshot_element(screenshot_element_id, screenshot_out, driver)
        driver.close()
