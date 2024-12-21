import pandas as pd  # Importa la libreria Pandas per la gestione dei dati
from instagram_scraper import getInfos  # Importa la funzione per estrarre dati dai post di Instagram
from create_driver import createDriver  # Importa la funzione per creare un WebDriver

# Creazione del driver
driver = createDriver()

# Lista dei link dei post di Instagram
links = [
    'https://www.instagram.com/p/DCMFXrou83J/',
    'https://www.instagram.com/p/DDLB-pfs2AS/',
    'https://www.instagram.com/p/DDpU1jDMDfX/',
    'https://www.instagram.com/p/DCgfA9JS6Ud/'
]

# Crea un DataFrame vuoto con le colonne predefinite
df = pd.DataFrame(columns=['Nome', 'Luogo', 'Like', 'Descrizione', 'Datetime', 'Followers', 'NumImmagini'])

# Iterazione sui link dei post
for link in links:
    try:
        # Prova a estrarre le informazioni dal post
        name, luogo, like, descrizione, datetime, followerNumber, numImmagini = getInfos(driver, link)
    except:
        # Se fallisce, chiudi il driver e ricrealo, quindi riprova
        driver.quit()
        driver = createDriver()
        name, luogo, like, descrizione, datetime, followerNumber, numImmagini = getInfos(driver, link)

    # Aggiungi una nuova riga al DataFrame con i dati estratti
    df = pd.concat([
        df,  # DataFrame corrente
        pd.DataFrame([[name, luogo, like, descrizione, datetime, followerNumber, numImmagini]],  # Nuova riga
                     columns=df.columns)  # Usa le stesse colonne del DataFrame originale
    ], ignore_index=True)  # Aggiorna gli indici per mantenere ordine continuo

# Chiudi il driver una volta completata l'operazione
driver.quit()

# Mostra il DataFrame per controllare i risultati
print(df)

# Salva il DataFrame in un file CSV (opzionale)
df.to_csv('instagram_posts.csv', index=False)  # Salva senza includere l'indice

