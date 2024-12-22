from create_driver import createDriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

def getNumImmagini(driver, link):
    driver.get(link)
    time.sleep(5)

    cookieButtons=driver.find_elements(By.CSS_SELECTOR,"button._a9--")
    if len(cookieButtons)>0: cookieButtons[0].click()

    time.sleep(2)

    xButtons=driver.find_elements(By.CSS_SELECTOR,"div.x1i10hfl")

    if len(xButtons)>0: 
        if len(xButtons)==5:xButtons[4].click()

    #time.sleep(20)


    #<button class="_a9-- _ap36 _a9_1" tabindex="0">Rifiuta cookie facoltativi</button>
    #<div class="x1i10hfl x972fbf xcfux6l x1qhh985 xm0m39n x9f619 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x6s0dn4 xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x1ypdohk x78zum5 xl56j7k x1y1aw1k x1sxyh0 xwib8y2 xurb0ha xcdnw81" role="button" tabindex="0"><div class="x6s0dn4 x78zum5 xdt5ytf xl56j7k"><svg aria-label="Chiudi" class="x1lliihq x1n2onr6 x1roi4f4" fill="currentColor" height="18" role="img" viewBox="0 0 24 24" width="18"><title>Chiudi</title><polyline fill="none" points="20.643 3.357 12 12 3.353 20.647" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="3"></polyline><line fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="3" x1="20.649" x2="3.354" y1="20.649" y2="3.354"></line></svg></div></div>


    #immagini=driver.find_elements(By.CLASS_NAME,"_aagv")
    buttons=driver.find_elements(By.CSS_SELECTOR,"button._afxw")
    #print(len(buttons))
    for button in buttons: print(button.text)

    if len(buttons)==0: return 1
    else: button=buttons[0]


    press_count = 0

    # Loop to press the button until it disappears
    while True:
        try:
            # Check if the button is still present and visible
            if button.is_displayed():

                #print("qui")

                #nascosto= driver.find_elements(By.CSS_SELECTOR,"div._acuq")
                #print(len(nascosto))
                #for nas in nascosto: print(nas.get_attribute('outerHTML'))

                #time.sleep(2)

                print(f"Button presente")

                #driver.execute_script("arguments[0].scrollIntoView(true);", button)
                driver.execute_script("arguments[0].setAttribute('tabindex', '1');", button)
                button.click()  # Press the button
                press_count += 1  # Increment the counter
                #print(f"Button pressed {press_count} times.")
                time.sleep(0.5)  # Add a small delay to prevent rapid clicks
                # Optionally, re-find the button after each click (in case it reloads)
                #button = driver.find_element(By.CSS_SELECTOR, 'button_selector')
            else:
                #print("Button is no longer visible.")
                break  # Exit the loop if the button is not visible
        except Exception as e:
            print(f"Error: {e}")
            break  # Exit the loop if an error occurs (e.g., element not found)

    return press_count+1


#driver= createDriver()
#numIm=getNumImmagini(driver,'https://www.instagram.com/p/DCgfA9JS6Ud/')
#print(numIm)
