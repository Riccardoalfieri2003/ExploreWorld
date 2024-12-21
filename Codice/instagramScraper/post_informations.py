import pandas as pd
from instagram_scraper import getInfos
from create_driver import createDriver

# Creazione del driver
driver = createDriver()

# Lista dei link dei post
links = [
    #'https://www.instagram.com/p/DCMFXrou83J/',
    #'https://www.instagram.com/p/DDLB-pfs2AS/',
    #'https://www.instagram.com/p/DDpU1jDMDfX/',
    'https://www.instagram.com/p/DCgfA9JS6Ud/'
]

# Lista per memorizzare i dati dei post
data = []

for link in links:
    try:
        # Estrazione delle informazioni
        name, luogo, like, descrizione, datetime, followerNumber, numImmagini = getInfos(driver, link)
        #print(f"Post: {link}, NumImmagini: {numImmagini}")
    except:
        # Ricrea il driver in caso di errore
        driver.quit()
        driver = createDriver()
        name, luogo, like, descrizione, datetime, followerNumber, numImmagini = getInfos(driver, link)


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
