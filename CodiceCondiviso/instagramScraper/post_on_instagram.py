from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.common.exceptions import NoSuchElementException
import time
import os
from ExploreWorld.CodiceCondiviso.instagramScraper.create_driver import createDriver

def login_to_instagram(driver, username, password):
    # Apre la pagina principale di Instagram
    driver.get("https://www.instagram.com/")
    time.sleep(5)  # Attende 5 secondi per permettere il caricamento della pagina

    # Tenta di cliccare sul pulsante per accettare i cookie (se appare)
    try:
        cookie_button = driver.find_element(By.XPATH, "//button[text()='Accetta tutti']")
        cookie_button.click()
    except:
        pass  # Se non c'è il pulsante, continua senza errori

    time.sleep(2)  # Attende per assicurarsi che il clic abbia effetto

    # Trova i campi di input per username e password
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")

    # Inserisce il nome utente e la password
    username_input.send_keys(username)
    password_input.send_keys(password)

    # Simula la pressione del tasto Enter per effettuare il login
    password_input.send_keys(Keys.RETURN)

    time.sleep(5)  # Attende 5 secondi per completare il processo di login

def upload_post(driver, image_path, description, location):
    # Trova il pulsante per creare un nuovo post (tramite l'icona del "+" nella barra superiore)
    new_post_button = driver.find_element(By.CSS_SELECTOR, "svg[aria-label='Nuovo post']")
    new_post_button.click()
    time.sleep(2)  # Attende il caricamento del popup per caricare l'immagine

    # Trova l'input nascosto per il caricamento del file e carica l'immagine
    upload_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    upload_input.send_keys("\n".join(image_path))  # Invia il percorso dell'immagine all'input
    time.sleep(5)  # Attende il caricamento dell'immagine

    # Clicca sul pulsante "Avanti" per procedere al passaggio successivo
   # avanti_button = driver.find_element(By.XPATH, "//button[text()='Avanti']")
    #avanti_button.click()
    #time.sleep(2)  # Attende il caricamento della schermata successiva

    button = driver.find_element(By.XPATH, "//div[@role='button' and text()='Avanti']")
    driver.execute_script("arguments[0].scrollIntoView();", button)
    button.click()
    time.sleep(5)

    button = driver.find_element(By.XPATH, "//div[@role='button' and text()='Avanti']")
    driver.execute_script("arguments[0].scrollIntoView();", button)
    button.click()
    time.sleep(5)

    #caption_area = driver.find_element(By.CSS_SELECTOR, "//div[@role='textarea' and text()='Scrivi una didascalia…']")
    #driver.execute_script("arguments[0].scrollIntoView();", caption_area)
    #caption_area.send_keys(description)
    #time.sleep(2)

    #caption_area = driver.find_element(By.CSS_SELECTOR, "textarea[aria-label='Scrivi una didascalia…']")
    #caption_area.send_keys(description)
    #time.sleep(2)

    #description_input = driver.find_element(By.CSS_SELECTOR, "input[aria-placeholder='Scrivi una didascalia...']")
    #description_input.send_keys(description)  # Inserisce la descrizione
    #time.sleep(5)

    # aggiunta della didascalia funzionante
    caption_area = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[@role='textbox' and @aria-placeholder='Scrivi una didascalia...']"))
    )
    caption_area.click()  # Fai clic prima di inviare testo
    caption_area.send_keys(description)

    # Aggiungi il luogo //Funziona
    #location_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Aggiungi luogo']")
    #location_input.send_keys(location)  # Inserisce il luogo
    #time.sleep(2)

    #riesce ad aggiungere quello richiesto
    location_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Aggiungi luogo']")
    location_input.send_keys(location)
    time.sleep(10)

    #buttons = driver.find_elements(By.XPATH, "//button")
    #for button in buttons:
       #print(button.text)  # Stampa il testo di ogni pulsante trovato


        # Trova tutti i bottoni sulla pagina
    buttons = driver.find_elements(By.XPATH, "//button")
    
    i=0
    for button in buttons:
        print(i,": ", button.text)  # Per debugging, stampa il testo di ogni bottone trovato
        i+=1
    buttons[3].click()

    #buttons[0].click()
    #exit()
    time.sleep(30)

        # Itera attraverso i bottoni per trovare quello con il testo corrispondente
       # for button in buttons:
        #    print(button.text)  # Per debugging, stampa il testo di ogni bottone trovato

           # if button.text.strip() == location.strip():  # Confronta il testo con il valore di `location`
               # time.sleep(2)
                #button.click()  # Clicca sul bottone corrispondente


       # else:
            # Se nessun bottone corrisponde al testo desiderato
        #    print(f"Errore: Nessun bottone corrisponde al luogo '{location}'")

    #except NoSuchElementException:
     #   print("Errore: Non è stato possibile trovare il bottone.")



    #Trova e clicca sul pulsante "Condividi" per pubblicare il post
    button = driver.find_element(By.XPATH, "//div[@role='button' and text()='Condividi']")
    driver.execute_script("arguments[0].scrollIntoView();", button)
    button.click()
    time.sleep(20)  # Attende il completamento della pubblicazione

def post(image_path,description,luogo):
    try:
        username = "calangeloorey"  # Sostituisci con il nome utente del tuo account
        password = "Fraccardo2003"  # Sostituisci con la password del tuo account

        driver  = createDriver()

        # Esegue il login e pubblica il post
        login_to_instagram(driver, username, password)
        upload_post(driver, image_path, description, luogo)
        print("Post pubblicato con successo!")
    except Exception as e:
        print("Si é verificato un errore")
        print(e)

    return