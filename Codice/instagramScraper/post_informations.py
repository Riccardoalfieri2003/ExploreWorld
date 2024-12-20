from instagram_scraper import getInfos
from create_driver import createDriver


driver=createDriver()

links=[
    'https://www.instagram.com/p/DCMFXrou83J/',
    'https://www.instagram.com/p/DDLB-pfs2AS/',
    'https://www.instagram.com/p/DDpU1jDMDfX/',
    'https://www.instagram.com/p/DCgfA9JS6Ud/'
]



for link in links:
    try: name,luogo,like,descrizione,datetime,followerNumber,numImmagini=getInfos(driver,link)
    except: 
        driver.quit()
        driver=createDriver()
        name,luogo,like,descrizione,datetime,followerNumber,numImmagini=getInfos(driver,link)
        
    print("Nome: ",name)
    print("Luogo: ", luogo)
    print("Like: ",like)
    print("Descrizione: ",descrizione)
    print("Datetime: ",datetime)
    print("Followers: ",followerNumber)
    print("numImmagini: ",numImmagini)
    print("\n")
