from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import re

def getInfos(driver, link):

    driver.get(link)
    time.sleep(3)

    lista=[]
    lista_elem=[]

    descrizione = driver.find_elements(By.CSS_SELECTOR, "div.x9f619")
    for e in descrizione: 
        lista.append(e.get_attribute("outerHTML"))
        lista_elem.append(e)

    tempo = driver.find_elements(By.CLASS_NAME, "xsgj6o6")
    for e in tempo: 
        lista.append(e.get_attribute("outerHTML"))
        lista_elem.append(e)


    # Regex to extract the value of datetime
    match = re.search(r'datetime="([^"]+)"', lista[8])
    if match: datetime_value = match.group(1)  # Extract the value inside the quotes
    else: datetime_value=None


    lista_string=(lista_elem[8].text+'\n'+datetime_value).split('\n')
    filtered_list = lista_string[:-4] + [lista_string[-1]]
    del filtered_list[1]
    del filtered_list[1]

    name=filtered_list[0]
    if "Piace a " in filtered_list[1]: 
        luogo=None
        like=filtered_list[1].split(' ')[2]
        filtered_list=filtered_list[3:]
        descrizione=' '.join(filtered_list[:-1])
        datetime=filtered_list[-1]
    else: 
        luogo=filtered_list[1]
        like=filtered_list[2].split(' ')[2]
        filtered_list=filtered_list[4:]
        descrizione=' '.join(filtered_list[:-1])
        datetime=filtered_list[-1]

    followersNumber=getNumberAccountFollowers(driver, name)

    return name,luogo,like,descrizione,datetime, followersNumber
