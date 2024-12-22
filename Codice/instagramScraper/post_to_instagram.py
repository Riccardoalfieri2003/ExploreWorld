from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

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
    upload_input.send_keys(image_path)  # Invia il percorso dell'immagine all'input
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

    # Trova e inserisce la descrizione nel campo "Scrivi una didascalia"
    try:
        caption_area = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//textarea[@aria-label='Scrivi una didascalia...']"))
        )
        caption_area.send_keys(description)
        time.sleep(2)
    except Exception as e:
        print(f"Errore nell'inserimento della descrizione: {e}")

    # Aggiungi il luogo
    location_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Aggiungi luogo']")
    location_input.send_keys(location)  # Inserisce il luogo
    time.sleep(2)

    # Attendi l'apparizione del suggerimento e selezionalo (se necessario)
    try:
        first_suggestion = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class, 'suggestions') and text()='" + location + "']"))
        )
        first_suggestion.click()
    except:
        print("Nessun suggerimento selezionato, procedo senza selezione.")


    #buttons = driver.find_elements(By.XPATH, "//button")
    #for button in buttons:
       #print(button.text)  # Stampa il testo di ogni pulsante trovato



    #Trova e clicca sul pulsante "Condividi" per pubblicare il post
    button = driver.find_element(By.XPATH, "//div[@role='button' and text()='Condividi']")
    driver.execute_script("arguments[0].scrollIntoView();", button)
    button.click()
    time.sleep(20)  # Attende il completamento della pubblicazione

if __name__ == "__main__":
    # Percorso del driver di Chrome
    chrome_driver_path = r'C:\Users\Ciccio Mascolo\Desktop\chromedriver-win64\chromedriver.exe'

    # Configurazione delle opzioni del driver di Chrome
    options = Options()
    options.add_argument("--start-maximized")  # Avvia il browser in modalità a schermo intero
    options.add_argument("--disable-notifications")  # Disabilita le notifiche del browser

    # Inizializza il driver con le opzioni e il percorso specificato
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        # Credenziali dell'account Instagram
        username = "explore_world_30"  # Sostituisci con il nome utente del tuo account
        password = "FraRic2003"  # Sostituisci con la password del tuo account

        # Percorso dell'immagine da caricare
        image_path = r"C:\Users\Ciccio Mascolo\Desktop\Ischia.jpg"  # Percorso dell'immagine

        # Descrizione del post
        description = "Panorama di ischia"  # Testo della descrizione

        location = "Ischia";

        # Esegue il login e pubblica il post
        login_to_instagram(driver, username, password)
        upload_post(driver, image_path, description,location)

        print("Post pubblicato con successo!")  # Messaggio di conferma
    except Exception as e:
        print(f"Errore: {e}")  # Mostra eventuali errori
    finally:
        driver.quit()  # Chiude il browser anche in caso di errori


