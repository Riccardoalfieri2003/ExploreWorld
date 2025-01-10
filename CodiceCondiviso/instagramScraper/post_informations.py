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
    'https://www.instagram.com/p/DD2M3wsgoyt/'
]

# Lista per memorizzare i dati dei post
data = []

for link in links:
    try:
        # Estrazione delle informazioni
        name, luogo, like, descrizione, datetime, followerNumber, numImmagini = getInfos(driver, link)
    except:
        # Ricrea il driver in caso di errore
        driver.quit()
        driver = createDriver()
        print(link)
        pass
        #name, luogo, like, descrizione, datetime, followerNumber, numImmagini = getInfos(driver, link)

    print("Nome: ",name)
    print("Luogo: ", luogo)
    print("Like: ",like)
    print("Descrizione: ",descrizione)
    print("Datetime: ",datetime)
    print("Followers: ",followerNumber)
    print("numImmagini: ",numImmagini)
    print("\n")

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

print(data)
# Creazione del DataFrame
df = pd.DataFrame(data)

# Mostra il DataFrame
print(df)

# Salvataggio del DataFrame in un file CSV
df.to_csv('instagram_posts.csv', index=False)