#backlog use a headless browser
#add score in a different color as option
#add video option
#get the previews from the sqm ad account

#remove sponsored if the post is organic
#fb_play button size based on the width of the image?
#delay the screenshot

print('loading a new preview frame')

import os
import time
import uuid
import shutil
import requests
import datetime
from PIL import Image
from PIL import ImageFile
from bs4 import BeautifulSoup
from selenium import webdriver
from google.cloud import storage

ImageFile.LOAD_TRUNCATED_IMAGES = True

token = os.environ.get("USER_TOKEN")
graph_api_version = 'v6.0'
ad_preview_photo = '23842919686400018'
link_ad_preview = '23844429402070018'
carousel_preview = '23843867557790018'
params = {'access_token': token,
    'ad_format': "DESKTOP_FEED_STANDARD"}

r = requests.get('https://graph.facebook.com/' + graph_api_version + '/' + ad_preview_photo + '/previews', params = params)
iframe = r.json()['data'][0]['body']
soup = BeautifulSoup(iframe, 'html.parser')
preview_url = soup.find_all('iframe')[0]['src']

r = requests.get('https://graph.facebook.com/' + graph_api_version + '/' + link_ad_preview + '/previews', params = params)
iframe = r.json()['data'][0]['body']
soup = BeautifulSoup(iframe, 'html.parser')
link_ad_preview_url = soup.find_all('iframe')[0]['src']

r = requests.get('https://graph.facebook.com/' + graph_api_version + '/' + carousel_preview + '/previews', params = params)
iframe = r.json()['data'][0]['body']
soup = BeautifulSoup(iframe, 'html.parser')
carousel_preview = soup.find_all('iframe')[0]['src']

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get("GCS_DATA_STORE")
client = storage.Client()
bucket = client.get_bucket('ig_post_img')

def replace_innerHTML(xpath, new_text, driver):
    element = driver.find_element_by_xpath(xpath)
    new_element = "arguments[0].innerText = '" + new_text + "'"
    driver.execute_script(new_element, element)

def replace_logo(new_logo_url, driver):
    element = driver.find_element_by_class_name('_s0')
    new_element = "arguments[0].src = '" + new_logo_url + "'"
    driver.execute_script(new_element, element)


def add_video_image(img_path):
    button_path =  '/Users/Nick/Documents/Python_Scripts/facebook_ad_previews/fb_play_button.png'
    button = Image.open(button_path).convert("RGBA")
    img_w, img_h = button.size
    img = Image.open(img_path).convert("RGBA")
    bg_w, bg_h = img.size
    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
    img.paste(button, offset,mask=button)
    #export the image file
    video_export_name = 'video_out.png'
    img.save(video_export_name)
    #upload this to google and return a url
    blob_export_name = 'video_previews/' + str(uuid.uuid1()) + '.png'
    blob = bucket.get_blob(blob_export_name)
    blob2 = bucket.blob(blob_export_name)
    blob2.upload_from_filename(filename=video_export_name)
    blob2 = bucket.blob(blob_export_name)
    return('https://storage.googleapis.com/ig_post_img/' + blob_export_name)


def replace_main_img(img_url,driver, video = False):
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
    if video == True:
        img_url = add_video_image('local_image.jpg')
    new_height =  width * (img.height / img.width)
    new_ratio = 'width: ' + str(width) + 'px;' + ' height: ' + str(int(round(new_height,0))) + 'px;'
    new_element = "arguments[0].style = '" + new_ratio + "'"
    driver.execute_script(new_element, current_size)
    img_element = driver.find_element_by_class_name('scaledImageFitWidth')
    new_element = "arguments[0].src = '" + img_url + "'"
    driver.execute_script(new_element, img_element)


def replace_carousel_img(img_url,driver, item ,video = False):
    element = driver.find_elements_by_class_name('_kvn')
    new_element = "arguments[0].src = '" + img_url + "'"
    driver.execute_script(new_element, element[item])

def replace_custom_element(class_name, driver, subelement, new_text):
    full_element = driver.find_element_by_class_name(class_name)
    attribute = full_element.get_attribute(subelement)
    new_element = "arguments[0]." + subelement + " = '" + new_text + "'"
    driver.execute_script(new_element, full_element)
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


def linked_ad_template(copy, new_img, logo, page_name,engagement, driver, creation_time, screenshot_element_id = '' ,screenshot_out = '', video = False, sleep = 2, sponsored = False):
    driver.get(preview_url)
    #page_name
    replace_innerHTML('/html/body/div[1]/div/div/div/div/div/div[2]/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div[2]/h5/span/span/a', page_name, driver)
    #copy
    replace_innerHTML('/html/body/div[1]/div/div/div/div/div/div[2]/div[1]/div[2]/div[2]', copy,driver)
    #Engagement
    replace_innerHTML('/html/body/div[1]/div/div/div/div/div/div[2]/div[2]/form/div[1]/div/div/div/div[1]/div/a/span[1]', str(engagement) , driver)
    #this preview has no comments and shares, so the lines below are commented out
    #replace_innerHTML('/html/body/div[1]/div/div/div/div/div/div[2]/div[2]/form/div[1]/div/div/div/div[1]/div/a/span[2]', '', driver)
    #replace_innerHTML('/html/body/div[1]/div/div/div/div/div/div[2]/div[2]/form/div[1]/div/div/div/div[1]/div/a/span[3]', '', driver)
    #add logo
    replace_logo(logo,driver)
    #replace img
    replace_main_img(new_img,driver, video)
    #replace sponsored
    if sponsored != True:
        date_text = datetime.datetime.strptime(creation_time.split('+')[0], '%Y-%m-%dT%H:%M:%S').strftime('%d %b at %H:%M')
        replace_innerHTML('/html/body/div[1]/div/div/div/div/div/div[2]/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div[2]/div/a[1]', date_text, driver)
    if screenshot_out == '':
        driver.close()
    else:
        time.sleep(sleep)
        screenshot_element(screenshot_element_id, screenshot_out, driver)
        #driver.close()

def full_linked_ad_template(copy, new_img, logo, page_name, cta, title, subtitle , driver, screenshot_element_id = '' , screenshot_out = '', video = False, sleep = 2):
    driver.get(link_ad_preview_url)
    #replace the CTA
    replace_innerHTML('/html/body/div[1]/div/div/div/div/div/div[2]/div[1]/div[2]/div[3]/div/div/div/div/div[1]/span/div[2]/div/div/div[3]/div/div/a', cta, driver)
    #replace the tile
    replace_innerHTML('/html/body/div[1]/div/div/div/div/div/div[2]/div[1]/div[2]/div[3]/div/div/div/div/div[1]/span/div[2]/div/div/div[2]/div[2]/div[1]/a', title, driver)
    #subtitle
    replace_innerHTML('/html/body/div[1]/div/div/div/div/div/div[2]/div[1]/div[2]/div[3]/div/div/div/div/div[1]/span/div[2]/div/div/div[2]/div[2]/div[2]', subtitle, driver)
    #remove the url
    element = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/div/div[2]/div[1]/div[2]/div[3]/div/div/div/div/div[1]/span/div[2]/div/div/div[2]/div[1]/div/div[1]")
    driver.execute_script("arguments[0].remove()",element)
    #remove_engagement
    element = driver.find_element_by_class_name("_524d")
    driver.execute_script("arguments[0].remove()",element)
    #page_name
    replace_innerHTML('/html/body/div[1]/div/div/div/div/div/div[2]/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div[2]/h5/span/span/a', page_name, driver)
    #copy
    replace_innerHTML('/html/body/div[1]/div/div/div/div/div/div[2]/div[1]/div[2]/div[2]', copy,driver)
    #add logo
    replace_logo(logo,driver)
    #replace img
    replace_main_img(new_img,driver, video)
    if screenshot_out == '':
        driver.close()
    else:
        time.sleep(sleep)
        screenshot_element(screenshot_element_id, screenshot_out, driver)
        #driver.close()


def carousel_template(copy, new_img1, new_img2, logo, page_name, cta, title1, title2, subtitle1, subtitle2 , driver, screenshot_element_id = '' , screenshot_out = '', video = False, sleep = 2):
    driver.get(carousel_preview)
    #replace the CTA
    replace_innerHTML('/html/body/div[1]/div/div/div/div/div/div[2]/div[1]/div[2]/div[3]/div/div/div/div/ul/li[1]/div/div/div/div/div[1]/a[2]', cta, driver)
    #replace the titles
    replace_innerHTML('/html/body/div[1]/div/div/div/div/div/div[2]/div[1]/div[2]/div[3]/div/div/div/div/ul/li[1]/div/div/div/div/div[2]/div[1]', title1, driver)
    replace_innerHTML('/html/body/div[1]/div/div/div/div/div/div[2]/div[1]/div[2]/div[3]/div/div/div/div/ul/li[2]/div/div/div/div/div[2]/div[1]', title2, driver)
    #subtitle
    replace_innerHTML('/html/body/div[1]/div/div/div/div/div/div[2]/div[1]/div[2]/div[3]/div/div/div/div/ul/li[1]/div/div/div/div/div[2]/div[2]', subtitle1, driver)
    replace_innerHTML('/html/body/div[1]/div/div/div/div/div/div[2]/div[1]/div[2]/div[3]/div/div/div/div/ul/li[2]/div/div/div/div/div[2]/div[2]', subtitle2, driver)
    #page_name
    replace_innerHTML('/html/body/div[1]/div/div/div/div/div/div[2]/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div[2]/h5/span/span/a', page_name, driver)
    #copy
    replace_innerHTML('/html/body/div[1]/div/div/div/div/div/div[2]/div[1]/div[2]/div[2]', copy,driver)
    #add logo
    replace_logo(logo,driver)
    #replace img
    replace_carousel_img(new_img1, driver, 0)
    replace_carousel_img(new_img2, driver, 1)
    if screenshot_out == '':
        driver.close()
    else:
        time.sleep(sleep)
        screenshot_element(screenshot_element_id, screenshot_out, driver)
        #driver.close()
