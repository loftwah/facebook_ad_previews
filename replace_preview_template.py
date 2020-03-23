#backlog
#Create a new preview based on fb api, so everything is always up to date

import os
import preview_templates as preview

img_url = 'https://media.nu.nl/m/okrxd84a8uf8_std640.jpg'
logo_url = 'https://cdn.worldvectorlogo.com/logos/opel-6.svg'

#add screenshot
preview.linked_ad_template('Dit is een random post', img_url, logo_url, 'Opel Auto', 150,'_5pcb', 'local_image.png', video = True)
