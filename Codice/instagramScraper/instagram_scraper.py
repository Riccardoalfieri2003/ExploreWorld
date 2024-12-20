from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import re

from number_follower_account import getNumberAccountFollowers
from get_immagini_instagram import getNumImmagini

def getInfos(driver, link):

    driver.get(link)
    time.sleep(5)

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

    if datetime_value!=None: lista_string=(lista_elem[8].text+'\n'+datetime_value).split('\n')
    else: lista_string=(lista_elem[8].text+'\n'+'None').split('\n')

    #if datetime_value!=None: 
    filtered_list = lista_string[:-4] + [lista_string[-1]]
    #else: 
    #print(filtered_list)
    try:
        del filtered_list[1]
        del filtered_list[1]
    except Exception as e: pass
    """
        print("Errore")
        print(lista_string)
        #time.sleep(30)
        driver.quit()
        driver=createDriver()
        return getInfos(driver, link)
        #print(filtered_list)
        #print(e)
        """


    name=filtered_list[0]
    if "Piace a " in filtered_list[1]: 
        luogo=None
        like=filtered_list[1].split(' ')[2]
        filtered_list=filtered_list[3:]

        if datetime_value!=None: 
            descrizione=' '.join(filtered_list[:-1])
            datetime=filtered_list[-1]
        else: descrizione=' '.join(filtered_list[:-0])

    else: 
        luogo=filtered_list[1]
        like=filtered_list[2].split(' ')[2]
        filtered_list=filtered_list[4:]

        if datetime_value!=None: 
            descrizione=' '.join(filtered_list[:-1])
            datetime=filtered_list[-1]
        else: descrizione=' '.join(filtered_list[:-0])

    followersNumber=getNumberAccountFollowers(driver, name)
    numImmagini=getNumImmagini(driver,link)

    """
    print("Nome: ",name)
    print("Luogo: ", luogo)
    print("Like: ",like)
    print("Descrizione: ",descrizione)
    print("Datetime: ",datetime)
    """

    return name,luogo,like,descrizione,datetime, followersNumber,numImmagini
