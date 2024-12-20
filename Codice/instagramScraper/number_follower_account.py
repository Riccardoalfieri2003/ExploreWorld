from create_driver import createDriver
from selenium.webdriver.common.by import By
import time

def getNumberAccountFollowers(driver, accountName):

    driver.get("https://www.instagram.com/"+accountName+'/')
    time.sleep(5)

    infos = driver.find_elements(By.CSS_SELECTOR, "li.xl565be")
    return infos[1].text.split(' ')[0]