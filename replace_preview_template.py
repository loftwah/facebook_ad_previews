#backlog
#Create a new preview based on fb api, so everything is always up to date

import os
from selenium import webdriver
import preview_templates as preview

driver = webdriver.Chrome(executable_path = "/Users/Nick/Downloads/chromedriver")

img_url = 'https://media.nu.nl/m/8kyx5eaaukfh_wd640.jpg/kabinet-schrapt-centrale-eindexamens-schoolexamens-leidend.jpg'
logo_url = 'https://cdn.worldvectorlogo.com/logos/opel-6.svg'
img1 = 'https://www.volkswagen.nl/-/media/vwpkw/images/elektrisch-rijden/elektrische-modellen/e-golf-teaser.ashx?w=2067&q=70&hash=45DFBAE12A1255EB370435ABC7E52E80F6C70AC1'
img2 = 'https://www.volkswagen.nl/-/media/vwpkw/images/elektrisch-rijden/elektrische-modellen/step-in-id-space-vizzion-1x1.ashx?w=2067&q=70&hash=461F34C2821402CBAC655E0986D0FCD74D51F937'
#add screenshot

preview.linked_ad_template('Dit is een random post', img_url, logo_url, 'Opel Auto', 150, driver ,'_5pcb', 'local_image.png', video = True)
preview.full_linked_ad_template('Dit is een random post', img_url, logo_url, 'Opel Auto','Learn More', 'I am a cool link', 'This is an even cooler subtitle' ,driver ,'_5pcb', 'local_image.png', video = False)
preview.carousel_template(copy = 'Dit is een nieuwe post', new_img1 = img1, new_img2 = img2, logo = logo_url, page_name = 'Opel Auto', cta = 'Kopen', title1 = 'Volkswagen Elktrisch', title2 = 'Deze met Benzine', subtitle1 = 'Veel PK', subtitle2 = 'Nog meer PK nu', driver = driver,screenshot_element_id = '_5pcb' , screenshot_out = 'local_image.png', video = False, sleep = 2)

driver.close()
