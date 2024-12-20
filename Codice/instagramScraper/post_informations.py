from instagram_scraper import getInfos
from create_driver import createDriver


driver=createDriver()

links=[
    'https://www.instagram.com/p/DCMFXrou83J/'
]



for link in links:
    name,luogo,like,descrizione,datetime=getInfos(driver,link)
    print(name,luogo,like,descrizione,datetime)