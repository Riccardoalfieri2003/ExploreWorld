from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def createDriver():

    current_dir = os.path.dirname(os.path.abspath(__file__))
    chrome_driver_path = os.path.join(current_dir, 'chromedriver-win64', 'chromedriver.exe')

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")  # Set a standard screen size
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    #options.add_argument("--disable-gpu")
    options.add_argument("--use-gl=swiftshader")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")  # Use shared memory, prevents memory issues
    options.add_argument("--enable-unsafe-swiftshader")
    options.add_argument("--enable-webgl")
    #options.add_argument("--disable-software-rasterizer")

    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(service=Service(executable_path=chrome_driver_path), options=options)
    return driver