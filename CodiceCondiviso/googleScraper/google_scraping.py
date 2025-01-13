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

from create_driver import createDriver

#LUOGO="Oahu"


# Filepath to save the image
#output_file = "image.jpg"

def modifySizeInURL(url):
    width_match = re.search(r'=w(\d+)', url)  # Match 'w=' followed by digits
    height_match = re.search(r'-h(\d+)', url)  # Match 'h=' followed by digits
    
    # Extract the values if matches are found
    width = int(width_match.group(1)) if width_match else None
    height = int(height_match.group(1)) if height_match else None

    new_width = 10*width
    new_height = 10*height


    # Replace the width and height in the URL
    modified_url = re.sub(r'=w\d+', f'=w{new_width}', url)  # Replace width
    modified_url = re.sub(r'-h\d+', f'-h{int(new_height)}', modified_url)  # Replace height

    return modified_url

def getCoordinates(url):
    #print(url)
    #print(url.split('@')[1])
    #print(url.split('@')[1].split('/')[0])
    return url.split('@')[1].split('/')[0].split(',')[:2]






# Download and save the image
def download_image(image_url, save_path):
    response = requests.get(image_url)
    if response.status_code == 200:  # Check if the request was successful
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Image successfully downloaded: {save_path}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")



def getURLGoogleMaps(driver, luogo, luogoType):
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
        """
        else:
            print("Luogo: ",elements[0].text.split('\n')[1])
            elements[0].click()
        """


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





    #Premiamo il luogo per avere le foto
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.aoRNLd.kn2E5e.NMjTrf.lvtCsd"))
    )
    button.click()

    print("Immagini mostrate")

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

            url_match = re.search(r'url\("([^"]+)"\)', src)

            # Check if a match was found
            if url_match: url = url_match.group(1)  # Extract the URL
            else:print("No URL found")

        
            modified_url=modifySizeInURL(url)
            print(modified_url)
    except: pass

    #recuperiamo coordinate
    coordinates=getCoordinates(driver.current_url)
    print(coordinates)


















def getURLGoogleImage(driver, luogo):

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
            #driver.execute_script("arguments[0].setAttribute('aria-hidden', arguments[1]);", immagine, "true")
            #print(immagine.get_attribute("outerHTML"))
            url=immagine.get_attribute("src")

            width_match = re.search(r'=w(\d+)', url)  # Match 'w=' followed by digits
            height_match = re.search(r'-h(\d+)', url)  # Match 'h=' followed by digits

            if width_match and height_match: print(url)

            #print(link)
            avantiButton.click()
            #print('\n')
    except: pass




    #Andfiamo su google immagini
    buttons=driver.find_elements(By.CSS_SELECTOR, 'div[role="listitem"]')
    
    for button in buttons: 
        if button.text=="Immagini":
            immaginiButton=button
            break
    #immaginiButton = driver.find_elements(By.CSS_SELECTOR, 'div[role="listitem"]')[1]
    immaginiButton.click()
    time.sleep(1)

    #driver.get("https://www.google.com/search?sca_esv=25db03e20fe2a1e6&rlz=1C1RXQR_itIT1022IT1022&sxsrf=ADLYWIJ5H0319Ri_X8b9dtyjNPnDIvD6bA:1734788200798&q=Oahu+Hawaii&udm=2&fbs=AEQNm0Be9hsxO5zOUoY5v2srYNPRIvTz_02aG-_CVE5t-hWDE06WxR4AozRhC3xtwSMagk1O2QChZpIz3rsq9rdep5YcgMAbjj8_PCkRpvyhL2yzPRBHtiiKfDEArRE2SCpvzynWrbA-UzVBffiplXDF2CGx2x8i4-3prxK7S88ojOr1YYek69n1f4ssmFwRTVeE82Vh3yuj&sa=X&ved=2ahUKEwjT-t_T_biKAxX19wIHHTA0C8gQtKgLegQIFRAB&biw=1341&bih=911&dpr=2")

    immaginiContainer=driver.find_elements(By.CSS_SELECTOR,'div[jsname="qQjpJ"]')
    print('\n')

    i=0
    #immaginiContainer=driver.find_elements(By.CSS_SELECTOR,'div[jsname="figiqf"]')
    #print(len(immaginiContainer))
    for immagine in immaginiContainer:
        immagine.click()
        #time.sleep(1)
        #print('\n')
        time.sleep(0.5)
        try:
            

            imageDiv=driver.find_elements(By.CSS_SELECTOR,'div[jsname="figiqf"]')
            image=imageDiv[1]
            #print(image.get_attribute('outerHTML'))
            imgs=image.find_elements(By.TAG_NAME,'img')
            if len(imgs)==2: 
                url=imgs[0]
                print(url.get_attribute('src'))
            #print(len( image.find_elements(By.TAG_NAME,'img') ))
            """
            for image in imageDiv: 
                print(image.get_attribute('outerHTML')); 
                imgs=image.find_elements(By.TAG_NAME,'img')
                if len(imgs)==2:
                    url=imgs[0].get_attribute('src')
            """
            #print('\n\n')
            #if i==10: break
            
            """
            try: 

                imageDiv=driver.find_elements(By.CSS_SELECTOR,'div[jsname="figiqf"]')
                for image in imageDiv: print(image.get_attribute('outerHTML'))
                print('\n')
                if i==5: break           
                
                
                imageDiv=driver.find_elements(By.CSS_SELECTOR,'div[jsname="figiqf"]')[i]

                if i>=2: imageDiv=driver.find_elements(By.CSS_SELECTOR,'div[jsname="figiqf"]')[1]
                else: imageDiv=driver.find_elements(By.CSS_SELECTOR,'div[jsname="figiqf"]')[i]


                if i==2:
                
                    print("i=2!")
                    imageDiv=driver.find_elements(By.CSS_SELECTOR,'div[jsname="figiqf"]')
                    for e in imageDiv: print(e.get_attribute('outerHTML'))
                    print('\n')
                    imageDiv=driver.find_elements(By.CSS_SELECTOR,'div[jsname="figiqf"]')[1]
                    print(imageDiv.get_attribute('outerHTML'))
                    break
                    
                
                    

            except: 
                imageDiv=driver.find_elements(By.CSS_SELECTOR,'div[jsname="figiqf"]')
                for e in imageDiv: print(e.get_attribute('outerHTML'))
                break
            """


            #print(immagine.get_attribute('outerHTML'))
            #print('\n')

            
            #print(len(imageDiv.find_elements(By.TAG_NAME,'img')))
            #try: g_img=imageDiv.find_element(By.CSS_SELECTOR,'img[jsname="kn3ccd"]')

            #image=imageDiv.find_element(By.CSS_SELECTOR,'img[jsname="kn3ccd"]')
            #images=imageDiv.find_elements(By.TAG_NAME,'img')
            #for image in images: print(image.get_attribute('src'))


            #url=image.get_attribute('src')
            #print(imageDiv.get_attribute('outerHTML'))
            #print(url)
            #print('\n')
            i+=1
            
        except Exception as e:print(e); print(immagine.get_attribute('outerHTML')); print('\n'); i+=1; continue
        #image=imageDiv.find_elements(By.TAG_NAME,"img")
        #for i in image: print(i.get_attribute("outerHTML"))
        #url=image.get_attribute("src")
        
        #break


#Creazione driver
luogoType="generico"
luogo="Spiagge a Big Island Hawaii"
driver=createDriver()
#getURLGoogleMaps(driver,luogo,luogoType)
getURLGoogleImage(driver,"Big Island")
















"""
#for image in images: image.click()
i=0
for image in images:
    if i==5: break
    image.click()
    time.sleep(1)
    canvas = driver.find_element(By.TAG_NAME, "canvas")
    canvas_data_url = driver.execute_script("return arguments[0].toDataURL('image/png');", canvas)

    header, encoded = canvas_data_url.split(",", 1)
    image_data = base64.b64decode(encoded)

    # Load the image with PIL
    image = Image.open(io.BytesIO(image_data))

    # Convert image to RGB and get pixel data
    rgb_image = image.convert("RGB")
    pixels = rgb_image.load()

    # Get image dimensions
    width, height = rgb_image.size

    # Initialize cropping coordinates
    left, top, right, bottom = width, height, 0, 0

    # Detect bounding box of non-black region
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            if r > 0 or g > 0 or b > 0:  # If not black
                left = min(left, x)
                top = min(top, y)
                right = max(right, x)
                bottom = max(bottom, y)
    
    # Check if the bounding box is valid (i.e., if we found any non-black pixels)
    if left < right and top < bottom:
        # Crop and save the image
        print("Image saved as cropped_canvas_image"+str(i)+".png")
        cropped_image = rgb_image.crop((left, top, right + 1, bottom + 1))
        cropped_image.save("cropped_canvas_image"+str(i)+".png")
        #cropped_image.show()
    else:
        print("No non-black pixels found. Skipping crop.")
        cropped_image = rgb_image
        cropped_image.save("cropped_canvas_image"+str(i)+".png")

    

    i+=1
"""


#<a class="hfpxzc" aria-label="Hawaii" href="https://www.google.com/maps/place/Hawaii/data=!4m7!3m6!1s0x7bffdb064f79e005:0x4b7782d274cc8628!8m2!3d19.8986819!4d-155.6658568!16zL20vMDNnaDQ!19sChIJBeB5Twbb_3sRKIbMdNKCd0s?authuser=0&amp;hl=it&amp;rclk=1" jsaction="pane.wfvdle25;focus:pane.wfvdle25;blur:pane.wfvdle25;auxclick:pane.wfvdle25;keydown:pane.wfvdle25;clickmod:pane.wfvdle25" jslog="12690;track:click,contextmenu;mutable:true;metadata:WyIwYWhVS0V3aUZvOVNvOUx1S0F4VWdPN2tHSGQ3T1BCa1E4QmNJQXlnQSIsbnVsbCwwXQ=="></a>