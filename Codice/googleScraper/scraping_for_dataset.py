from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import re
from PIL import Image
from io import BytesIO
import requests
import base64
import io
import os
from resize import resize

import numpy as np


from create_driver import createDriver
import cv2




def save(string):
    response = requests.get(string)
    image = Image.open(BytesIO(response.content))

    # Convert Pillow image to OpenCV format (NumPy array)
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    folder = "peopleDataset"  # Specify the folder
    filename = os.path.basename(string)  # Extract the file name from the URL

    # Ensure the folder exists
    os.makedirs(folder, exist_ok=True)

    # Save the image to the folder
    image_path = os.path.join(folder, filename)
    resized_image = resize(image_cv, 224)
    cv2.imwrite(image_path, resized_image)





def getURLGoogleImage(driver, luogo):

    resultList=[]

    driver.get("https://www.google.com/search?q="+luogo.split(',')[0].replace(' ','+'))
    time.sleep(1)

    buttons=driver.find_elements(By.TAG_NAME,"button")
    for button in buttons:
        if button.text=="Rifiuta tutto": button.click(); break
    time.sleep(1)

    conteintoriImmagini=driver.find_elements(By.CLASS_NAME,"KWD3Pe")

    try:
        avantiButton = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Immagine successiva"]')

        for contenitore in conteintoriImmagini:
            immagine=contenitore.find_element(By.TAG_NAME,"img")

            url=immagine.get_attribute("src")

            width_match = re.search(r'=w(\d+)', url)  # Match 'w=' followed by digits
            height_match = re.search(r'-h(\d+)', url)  # Match 'h=' followed by digits

            if width_match and height_match: print(url)

            #print(link)
            avantiButton.click()
            #print('\n')
    except: pass

    #Andfiamo su google immagini
    immaginiButton = driver.find_elements(By.CSS_SELECTOR, 'div[role="listitem"]')[1]
    immaginiButton.click()
    time.sleep(1)

    immaginiContainer=driver.find_elements(By.CSS_SELECTOR,'div[jsname="qQjpJ"]')
    print('\n')

    i=0

    for immagine in immaginiContainer:
        immagine.click()

        time.sleep(1)
        try:

            imageDiv=driver.find_elements(By.CSS_SELECTOR,'div[jsname="figiqf"]')
            image=imageDiv[1]

            imgs=image.find_elements(By.TAG_NAME,'img')
            if len(imgs)==2: 
                url=imgs[0]
                save(url.get_attribute('src'))
                print(url.get_attribute('src'))
           
            i+=1
            
        except Exception as e:
            print(e); 
            i+=1; continue

    return resultList





driver=createDriver()
URLs=getURLGoogleImage(driver, "people in the background")


#Immagini di dataset oresi da
#   white people photo
#   black people photo
#   indian people photo
#   chinese people photo
#   people in the background
#   children

#come sono state gestite le immagini:
#   Ogni immagine è stata ridimensionata a 224x224 (in caso di immagini più grandi, sono ritagliate)
#   circa 50-70 immagini per ricerca
#   eleminazione manuali immagini non inerenti alla ricerca
#   eleminazione manuali immagini che potrebbero confondere il modello
#   eliminazione immagini con estensione Chrome HTML document 
#   tipi accettati JPG, JPEG, PNG