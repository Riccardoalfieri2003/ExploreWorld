from instagram_scraper import getInfos
from create_driver import createDriver


driver=createDriver()

links=[
    'https://www.instagram.com/p/DCMFXrou83J/',
    'https://www.instagram.com/p/DDLB-pfs2AS/'
]



for link in links:
    name,luogo,like,descrizione,datetime,followerNumber=getInfos(driver,link)
    print("Nome: ",name)
    print("Luogo: ", luogo)
    print("Like: ",like)
    print("Descrizione: ",descrizione)
    print("Datetime: ",datetime)
    print("Followers: ",followerNumber)
    print("\n")