#backlog
#Create a new preview based on fb api, so everything is always up to date

import os
import preview_templates as preview

img_url = 'https://uploads-ssl.webflow.com/5cc447337c5efa0f49d294cd/5e1cf67d2024a83762dffc13_large_1578955165472609-p-800.jpeg'
logo_url = 'https://cdn.worldvectorlogo.com/logos/opel-6.svg'

#add screenshot
preview.linked_ad_template('Dit is een random post', img_url, logo_url, 'Opel Auto', 150,'_5pcb', 'local_image.png')
