import pandas as pd
from instagram_scraper import getInfos
from create_driver import createDriver

# Creazione del driver
driver = createDriver()

# Lista dei link dei post
links = [
    'https://www.instagram.com/p/DCMFXrou83J/',
    'https://www.instagram.com/p/DDLB-pfs2AS/',
    'https://www.instagram.com/p/DDpU1jDMDfX/',
    'https://www.instagram.com/p/DCgfA9JS6Ud/',
    'https://www.instagram.com/p/DDzmAuWsEEG/',
    'https://www.instagram.com/p/DCrJ0Hkyc8K/',
    'https://www.instagram.com/p/DDtq3qWMGux/',
    'https://www.instagram.com/p/DDpuCWOsl2B/',
    'https://www.instagram.com/p/DDp6OQZz24Z/',
    'https://www.instagram.com/p/DDim7w-tg54/',
    'https://www.instagram.com/p/DDcLdspRrb_/',
    'https://www.instagram.com/p/DDiPVtqz_BV/',
    'https://www.instagram.com/p/DDwvP2DSSzo/',
    'https://www.instagram.com/p/C5U38NtSdc2/',
    'https://www.instagram.com/p/DDlu0m1zVoT/',
    'https://www.instagram.com/p/DDFtGUYsFiO/',
    'https://www.instagram.com/p/DDzDefoCLIS/',
    'https://www.instagram.com/p/DDC5694uZvK/',
    'https://www.instagram.com/p/DDu-1uYx_H_/',
    'https://www.instagram.com/p/DDpX4_8qYAy/',
    'https://www.instagram.com/p/DBgaUrbSKfr/',
    'https://www.instagram.com/p/DCM8jUtRxDC/',
    'https://www.instagram.com/p/DD2PzoyOy54/',
    'https://www.instagram.com/p/DAVsKoQyUCe/',
    'https://www.instagram.com/p/DDfR8MiOmaM/',
    'https://www.instagram.com/p/DDTnjGHtder/',
    'https://www.instagram.com/p/DCw9uvgim1K/',
    'https://www.instagram.com/p/DDgfYCEISCU/',
    'https://www.instagram.com/p/DDcK7J0inkw/',
    'https://www.instagram.com/p/DD2atUApT7c/',
    'https://www.instagram.com/p/C6T7AV1CYMq/',
    'https://www.instagram.com/p/DDcerdCvRA6/',
    'https://www.instagram.com/p/DDz9JYTyc91/',
    'https://www.instagram.com/p/DCSS_Q_iUTr/',
    'https://www.instagram.com/p/DDAZ8qfux9F/',
    'https://www.instagram.com/p/DCztSTaob6m/',
    'https://www.instagram.com/p/DDzrlFot5yc/',
    'https://www.instagram.com/p/DD4S9zAoVP3/',
    'https://www.instagram.com/p/DDVW7WJSt0O/',
    'https://www.instagram.com/p/DD27F1RAq_H/',
    'https://www.instagram.com/p/DD2bttrNzjl/',
    'https://www.instagram.com/p/DDXaQNoI4e1/',
    'https://www.instagram.com/p/DDzs26NTm-v/',
    'https://www.instagram.com/p/DD4aqIsvfJm/',
    'https://www.instagram.com/p/DBHVSWaRjxK/',
    'https://www.instagram.com/p/DD1bj_6vccd/',
    'https://www.instagram.com/p/DDhnNycPq8F/',
    'https://www.instagram.com/p/DD4etAgxtlD/',
    'https://www.instagram.com/p/DCtA4HaO0vv/',
    'https://www.instagram.com/p/DD2M3wsgoyt/',
    'https://www.instagram.com/p/DD6zHSVuHDe/',
    'https://www.instagram.com/p/DDXiI3etOmN/',
    'https://www.instagram.com/p/DDNEtqLCXF7/',
    'https://www.instagram.com/p/Cs8ULXCu5jG/',
    'https://www.instagram.com/p/DB_Dbcyu0g7/',
    'https://www.instagram.com/p/DDuu8dayt8k/',
    'https://www.instagram.com/p/DD64rYCIfnw/',
    'https://www.instagram.com/p/C8UDTkoNacf/',
    'https://www.instagram.com/p/DDptXT-IHHE/',
    'https://www.instagram.com/p/C84vFWNokXU/',
    'https://www.instagram.com/p/DA1UVXBM137/',
    'https://www.instagram.com/p/DCJExUkNPDN/',
    'https://www.instagram.com/p/DC_ncp1MMiM/',
    'https://www.instagram.com/p/DC3LtRONqxU/',
    'https://www.instagram.com/p/C_izV9LJXo8/',
    'https://www.instagram.com/p/DB2Xu9UTEbu/',
    'https://www.instagram.com/p/CdN15pisbww/',
    'https://www.instagram.com/p/DBtgjdroMSe/',
    'https://www.instagram.com/p/DBt1B3pRtF5/',
    'https://www.instagram.com/p/DCWoxxHNP5I/',
    'https://www.instagram.com/p/BYgaGQ1BgN9/',
    'https://www.instagram.com/p/Bj2o5s2hnBO/',
    'https://www.instagram.com/p/BsxjdO1jN3N/',
    'https://www.instagram.com/p/C8wu9CvRbVZ/',
    'https://www.instagram.com/p/DBxJ4rYyocB/',
    'https://www.instagram.com/p/C9Uz5TYP5i9/',
    'https://www.instagram.com/p/C8-TOxQSsUS/',
    'https://www.instagram.com/p/DBlNZ7qTaEl/',
    'https://www.instagram.com/p/C8t1LhNIKkK/',
    'https://www.instagram.com/p/C9kdCZeOwl1/',
    'https://www.instagram.com/p/B-ocK1vp6vp/',
    'https://www.instagram.com/p/CHpWvutBDBq/',
    'https://www.instagram.com/p/BscRBoSgjhi/',
    'https://www.instagram.com/p/C-Av8tioe_A/',
    'https://www.instagram.com/p/DDtS60Tvv3c/',
    'https://www.instagram.com/p/C9SWKtIMZfi/',
    'https://www.instagram.com/p/DBHUgAGN6I1/',
    'https://www.instagram.com/p/DDSbrDCoEUw/',
    'https://www.instagram.com/p/DC0VMHcPDer/',
    'https://www.instagram.com/p/DBcM-vsy86h/'
    ]

# Lista per memorizzare i dati dei post
data = []

for link in links:
    try:
        # Estrazione delle informazioni
        name, luogo, like, descrizione, datetime, followerNumber, numImmagini = getInfos(driver, link)
        print(link + " inserito")
    except:
        # Ricrea il driver in caso di errore
        driver.quit()
        driver = createDriver()
        print(link)
        pass
        #name, luogo, like, descrizione, datetime, followerNumber, numImmagini = getInfos(driver, link)

    # Salvataggio delle informazioni in un dizionario
    data.append({
        'Nome': name,
        'Luogo': luogo,
        'Like': like,
        'Descrizione': descrizione,
        'Datetime': datetime,
        'Followers': followerNumber,
        'NumImmagini': numImmagini,
    })

# Chiusura del driver
driver.quit()

# Scrittura dei dati in un file .txt
with open('instagram_posts.txt', 'w', encoding='utf-8') as file:
    for post in data:
        file.write(f"Nome: {post['Nome']}\n")
        file.write(f"Luogo: {post['Luogo']}\n")
        file.write(f"Like: {post['Like']}\n")
        file.write(f"Descrizione: {post['Descrizione']}\n")
        file.write(f"Datetime: {post['Datetime']}\n")
        file.write(f"Followers: {post['Followers']}\n")
        file.write(f"NumImmagini: {post['NumImmagini']}\n")
        file.write("\n" + "-"*40 + "\n")  # Separatore tra i post

print("Dati salvati nel file instagram_posts.txt")
