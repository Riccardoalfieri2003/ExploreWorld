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

    folder = "treesDataset"  # Specify the folder
    filename = os.path.basename(string)  # Extract the file name from the URL

    # Ensure the folder exists
    os.makedirs(folder, exist_ok=True)

    # Save the image to the folder
    image_path = os.path.join(folder, filename)
    resized_image = resize(image_cv, 224)
    cv2.imwrite(image_path, resized_image)





import threading
import time
from selenium.webdriver.common.by import By

def process_image(immagine, driver):
    try:
        immagine.click()
        time.sleep(1)
        imageDiv = driver.find_elements(By.CSS_SELECTOR, 'div[jsname="figiqf"]')
        image = imageDiv[1]
        imgs = image.find_elements(By.TAG_NAME, 'img')
        if len(imgs) == 2:
            url = imgs[0]
            save(url.get_attribute('src'))
            print(url.get_attribute('src'))
        return True  # Indica che l'elaborazione è riuscita
    except Exception as e:
        print(e)
        return False  # Indica che l'elaborazione è fallita

def run_with_timeout(func, args, timeout=10):
    result = [None]  # Per condividere il risultato con il thread principale
    exception = [None]

    def target():
        try:
            result[0] = func(*args)
        except Exception as e:
            exception[0] = e

    thread = threading.Thread(target=target)
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        print("Timeout raggiunto, procedo con la prossima immagine.")
        thread.join(0)  # Forza la terminazione del thread (il codice interno non sarà completato)
    if exception[0]:
        raise exception[0]
    return result[0]


def getURLGoogleImage(driver, luogo):

    resultList=[]

    driver.get("https://www.google.com/search?q="+luogo.split(',')[0].replace(' ','+'))
    time.sleep(1)

    buttons=driver.find_elements(By.TAG_NAME,"button")
    for button in buttons:
        if button.text=="Rifiuta tutto": button.click(); break
    time.sleep(1)

    
    
    

    #Andfiamo su google immagini
    buttons=driver.find_elements(By.CSS_SELECTOR, 'div[role="listitem"]')
    
    for button in buttons: 
        if button.text=="Immagini":
            immaginiButton=button
            break
    #immaginiButton = driver.find_elements(By.CSS_SELECTOR, 'div[role="listitem"]')[1]
    immaginiButton.click()
    time.sleep(1)

    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #time.sleep(1)
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)
    
    
    

    immaginiContainer=driver.find_elements(By.CSS_SELECTOR,'div[jsname="qQjpJ"]')
    print('\n')

    i=0

    

    for immagine in immaginiContainer:

        for immagine in immaginiContainer:
            try:
                success = run_with_timeout(process_image, (immagine, driver), timeout=10)
                if success: pass
                    #print("Immagine elaborata con successo.")
                else:
                    print("Elaborazione immagine fallita.")
            except Exception as e:
                print(f"Errore durante l'elaborazione: {e}")

        """
        
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
        """

    return resultList





driver=createDriver()
URLs=getURLGoogleImage(driver, "trees")


#Immagini di dataset oresi da



#Questi 2 sono potenzioati da human detection sataset di kaggle

#Persone
#   white people photo
#   black people photo
#   indian people photo
#   chinese people photo
#   people in the background
#   children
#   people from behind
#   side profile person(x2)
#   crowds(x2)

#NoPeopleDataset
#   nature photos (x2)
#   city photos (x2)
#   aniaml photos (x2)
#   trees
#   pillars
#   tall vases(x2)
#   exotic trees
#   palm trees
#   observatories

#Montagne
#   mountains
#   montagne
#   green mointains
#   montagne senza neve

#Mare
#   mare
#   sea
#   spiaggia
#   beaches

#Città
#   cities
#   towns
#   snowy towns
#   towns at night
#   cities at night

#Ricerche combinate
#   Cities on beaches
#   Mountains on sea
#   City squqres
#   cities on mountains


#Meteo
"""Mattina, Tramonto, Notte sono mutualmente esclusive"""
#Mattina
#   foto in mattinata
#   sunny city photos
#   sunny nature photos
#   sunny towns
#   sunny weather
#   sunny mountains

#Tramonto
#   sunset photos
#   city sunset
#   sunset nature
#   sunset pictures
#   crepuscolo (x2)
#   citta crepuscolo (x2)

#Notte
#   night
#   city at night
#   foto di notte
#   night nature photos
#   starry sky (x2)

#Aurora boreale
#   Aurora Borealis (x4)
#   Lapponia aurora borealis 
#   red aurora borealis (x2)




"""Foto vere e non sono mutualmente esclusive"""
#Distinguere foto vere da non
#   Foto vere: photos(x2), aniaml photos, nature photos, people photos (* x2), new york, tropical cities
#   Foto false suddivise in:
    #Drawings: drawimgs, drawings color, disegni e disegni a colori, black and white drawings
    #Illustartions: illsustrations (x3)
    #Maps: maos (x3), game maps
    #Charts: charts(x3)
    #CGI images (forse)
    


#come sono state gestite le immagini:
#   Ogni immagine è stata ridimensionata a 224x224 (in caso di immagini più grandi, sono ritagliate)
#   circa 50-70 immagini per ricerca (il x3 indica che è statp scrollato 3 volte per ottenere il triplo delle immagini)
#   eleminazione manuali immagini non inerenti alla ricerca
#   eleminazione manuali immagini che potrebbero confondere il modello
#   eliminazione immagini con estensione Chrome HTML document e altri strani
#   tipi accettati JPG, JPEG, PNG