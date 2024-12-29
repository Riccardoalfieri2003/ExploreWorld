from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import threading
import time
import re

from googleScraper.create_driver import createDriver

from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC





def getCoordinates(url): return url.split('@')[1].split('/')[0].split(',')[:2]


def modifySizeInURL(url):
    width_match = re.search(r'=w(\d+)', url)  # Match 'w=' followed by digits
    height_match = re.search(r'-h(\d+)', url)  # Match 'h=' followed by digits
    
    # Extract the values if matches are found
    width = int(width_match.group(1)) if width_match else None
    height = int(height_match.group(1)) if height_match else None

    new_width = 2030
    new_height = height*(new_width/width)


    # Replace the width and height in the URL
    modified_url = re.sub(r'=w\d+', f'=w{new_width}', url)  # Replace width
    modified_url = re.sub(r'-h\d+', f'-h{int(new_height)}', modified_url)  # Replace height

    return modified_url



def getLuogo(driver, luogo, luogoType):
    driver.get("https://www.google.com/maps/")

    #Aspettiamo i bottono per i cookie e privacy
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME,"button"))
        )

    except TimeoutException:
        print("Element not found within the timeout period.")
        driver.save_screenshot("timeout_screenshot.png")

    #Prendiamo e premiamo i bottoni
    buttons = driver.find_elements(By.TAG_NAME, "button")
    clickable_buttons = []

    for button in buttons:
        if button.is_enabled() and button.is_displayed():
            clickable_buttons.append(button)

    try:
        third_button = clickable_buttons[2]
        third_button.click()
    except IndexError:
        print("Error: The third button does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")



    #Aspettiamo il form per inserire il luogo
    form = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME,"input"))
    )
    form.clear()
    form.send_keys(luogo)

    time.sleep(2)


    #Se presente il luogo inmodo diretto, premere
    try:
        
        if luogoType=="Generico": raise Exception

        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ydp1wd-haAclf"))
        )
        
        #elements = table.find_elements(By.CSS_SELECTOR, "[jsaction='suggestion.select']")

        elements = table.find_elements(By.CSS_SELECTOR, "[jslog='6986;mutable:true;']")

        #for element in elements: print(element.text)

        name=elements[0].find_element(By.CSS_SELECTOR,"span.cGyruf")

        #print('Ayo')

        #for name in names: print(name.text)

        #print()

        #<span class="cGyruf fontBodyMedium RYaupb "><span class="XYuRPe">Hawaii</span><span> Poke Sushi</span></span>

        if ',' in name.text: 
            #names[0].click()
            #elements[0].click()
            luogo= name.text.split('\n')[1]
            name.click()
            time.sleep(1)
           
        else: 
            #names[0].click()
            #elements[0].click()
            luogo= name.text
            name.click()
            time.sleep(1)
            
        
        #print(luogo)
        return luogo


        #if ',' in elements[0].text: return elements[0].text.split('\n')[1]
        #else: return elements[0].text

        #<div class="ZHeE1b " jslog="6986;mutable:true;"><div class="l0wghb " role="row"><div class="DgCNMb " id="cell0x0" role="gridcell"><div class="jlzIOd"><span class="google-symbols" aria-hidden="true" style="font-size: 21px;"></span></div><span></span><span class="cGyruf fontBodyMedium RYaupb "><span class="XYuRPe">Hawaii</span></span> <span class="EmLCAe fontBodyMedium"><span>Stati Uniti</span></span></div></div></div>

        #time.sleep(200)
        for element in elements:
            if ',' in element.text:
                #print("Luogo: ",element.text.split('\n')[1])
                luogo=element.text.split('\n')[1]
                element.click()
                time.sleep(1)
                return luogo
                #time.sleep(1)
                #break

    #Altrimnti si va alla lista dei possibili luoghi
    except Exception as e:
        print(e)
        buttonInvio = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mL3xi"))
        )
        time.sleep(1)
        buttonInvio.click()
        time.sleep(3)

        luoghi=driver.find_elements(By.CSS_SELECTOR,"a.hfpxzc")
        #print(len(luoghi))
        for luogo in luoghi: print(luogo.get_attribute('aria-label'))
        time.sleep(1)

        luogoSelezionato=input("Seleziona luogo")

        for luogo in luoghi:
            if luogo.get_attribute('aria-label')==luogoSelezionato: 
                luogoNome=luogo.get_attribute('aria-label')
                luogo.click()
                time.sleep(1)
                return luogoNome




            


def getURLGoogleMaps(driver, result_list, lock):
    #driver.get("https://www.google.com/maps/")

    """

    #Aspettiamo i bottono per i cookie e privacy
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME,"button"))
        )

    except TimeoutException:
        print("Element not found within the timeout period.")
        driver.save_screenshot("timeout_screenshot.png")

    #Prendiamo e premiamo i bottoni
    buttons = driver.find_elements(By.TAG_NAME, "button")
    clickable_buttons = []

    for button in buttons:
        if button.is_enabled() and button.is_displayed():
            clickable_buttons.append(button)

    try:
        third_button = clickable_buttons[2]
        third_button.click()
    except IndexError:
        print("Error: The third button does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")



    #Aspettiamo il form per inserire il luogo
    form = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME,"input"))
    )
    form.clear()
    form.send_keys(luogo)

    time.sleep(2)


    #Se presente il luogo inmodo diretto, premere
    try:
        
        if luogoType=="generico": raise Exception

        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ydp1wd-haAclf"))
        )

        elements = table.find_elements(By.CSS_SELECTOR, "[jsaction='suggestion.select']")
        for element in elements:
            if ',' in element.text:
                print("Luogo: ",element.text.split('\n')[1])
                element.click()
                time.sleep(1)
                break
        


    #Altrimnti si va alla lista dei possibili luoghi
    except Exception as e:
        print(e)
        buttonInvio = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mL3xi"))
        )
        time.sleep(1)
        buttonInvio.click()
        time.sleep(3)

        luoghi=driver.find_elements(By.CSS_SELECTOR,"a.hfpxzc")
        print(len(luoghi))
        for luogo in luoghi: print(luogo.get_attribute('aria-label'))
        time.sleep(1)

        luogoSelezionato=input("Seleziona luogo")

        for luogo in luoghi:
            if luogo.get_attribute('aria-label')==luogoSelezionato: luogo.click()

    """





    #Premiamo il luogo per avere le foto
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.aoRNLd.kn2E5e.NMjTrf.lvtCsd"))
    )
    button.click()

    #print("Immagini mostrate")

    images = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "OKAoZd"))
    )

    images = driver.find_elements(By.CLASS_NAME, "OKAoZd")
    driver.execute_script("arguments[0].scrollIntoView({ block: 'center' });", images[-1])
    time.sleep(1)
    images = driver.find_elements(By.CLASS_NAME, "OKAoZd")



    #Prendiamo gli url da tutte le immagini e le modifichiamo per averle im alta definzione
    try:
        for image in images:
            image.click()
            internalDiv=image.find_element(By.TAG_NAME,"div")
            src=internalDiv.get_attribute("style")
            #print("qui")

            url_match = re.search(r'url\("([^"]+)"\)', src)

            # Check if a match was found
            if url_match: url = url_match.group(1)  # Extract the URL
            else:print("No URL found")

        
            modified_url=modifySizeInURL(url)

            with lock: 
                result_list.append(modified_url)
                #print(modified_url)

    except Exception as e: print(e); pass

    #recuperiamo coordinate
    #coordinates=getCoordinates(driver.current_url)
    #print(coordinates)


def getURLGoogleImage(driver, luogo, result_list, lock):

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

            if width_match and height_match:
                with lock: 
                    result_list.append(modifySizeInURL(url)) 
                    #print(modifySizeInURL(url))

            avantiButton.click()
    except: pass


    #Andfiamo su google immagini
    buttons=driver.find_elements(By.CSS_SELECTOR, 'div[role="listitem"]')
    
    for button in buttons: 
        if button.text=="Immagini":
            immaginiButton=button
            break
    immaginiButton.click()
    time.sleep(1)

    immaginiContainer=driver.find_elements(By.CSS_SELECTOR,'div[jsname="qQjpJ"]')
    #print('\n')

    i=0
    for immagine in immaginiContainer:
        immagine.click()
        time.sleep(0.5)
        try:

            imageDiv=driver.find_elements(By.CSS_SELECTOR,'div[jsname="figiqf"]')
            image=imageDiv[1]

            imgs=image.find_elements(By.TAG_NAME,'img')
            if len(imgs)==2: 
                url=imgs[0]
                with lock: 
                    result_list.append(url.get_attribute('src'))
                    #print(url.get_attribute('src'))
            
            
            i+=1
            
        except Exception as e:#print(e); print(immagine.get_attribute('outerHTML')); print('\n'); 
            i+=1; continue



def getURLs(luogo, luogoType):

    driverMaps=createDriver()
    driverImages=createDriver()


    result_list = []
    # Create a lock to ensure thread-safe access to the list
    lock = threading.Lock()

    luogo=getLuogo(driverMaps, luogo, luogoType)
    #coordinate=getCoordinates(driverMaps.current_url)

    #time.sleep(10)
    
    #getURLGoogleMaps(driver)
    #getURLGoogleMaps(driver,luogo,luogoType)
    #getURLGoogleImage(driver,luogo)

    #print("Inizio")
    #start_time = time.time()
    # Crea i thread per eseguire le funzioni contemporaneamente
    thread1 = threading.Thread(target=getURLGoogleMaps, args=(driverMaps,result_list,lock,))
    thread2 = threading.Thread(target=getURLGoogleImage, args=(driverImages,luogo,result_list,lock,))

    # Start the threads
    thread1.start()
    thread2.start()

    # Wait for both threads to finish
    thread1.join()
    thread2.join()

    #end_time = time.time()

    #elapsed_time = end_time - start_time
    #print(f"Elapsed time: {elapsed_time:.6f} seconds")


    #print(result_list)
    return result_list


#Creazione driver
#luogoType="Normale"
#luogo="Big Island Hawaii"
#print(getURLs(luogo,luogoType))