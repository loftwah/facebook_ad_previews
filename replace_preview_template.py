#backlog
#Create a new preview based on fb api, so everything is always up to date

import os
from selenium import webdriver
import preview_templates as preview

driver = webdriver.Chrome(executable_path = "/Users/Nick/Downloads/chromedriver")

img_url = 'https://media.nu.nl/m/8kyx5eaaukfh_wd640.jpg/kabinet-schrapt-centrale-eindexamens-schoolexamens-leidend.jpg'
logo_url = 'https://cdn.worldvectorlogo.com/logos/opel-6.svg'

#add screenshot

preview.linked_ad_template('Dit is een random post', img_url, logo_url, 'Opel Auto', 150, driver ,'_5pcb', 'local_image.png', video = True)
preview.full_linked_ad_template('Dit is een random post', img_url, logo_url, 'Opel Auto','Learn More', 'I am a cool link', 'This is an even cooler subtitle' ,driver ,'_5pcb', 'local_image.png', video = False)

driver.close()
