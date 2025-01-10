import pandas as pd
import re
import emoji  # Libreria per il supporto alle emoticon Unicode

# Funzione per leggere il file e creare un DataFrame
def txt_to_dataframe(file_path):
    data = []
    post = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()

            # Se è una linea vuota o un separatore, significa che un post è completo
            if line == '' or line.startswith('-'):
                if post:  # Se ci sono dati nel dizionario
                    data.append(post)
                    post = {}
            else:
                # Splitta la riga in "chiave: valore"
                key_value = line.split(': ', 1)
                if len(key_value) == 2:
                    key, value = key_value
                    post[key] = value

    # Aggiunge l'ultimo post se esiste
    if post:
        data.append(post)

    # Crea un DataFrame dai dati estratti
    df = pd.DataFrame(data)

    # Dividi "Datetime" in "Data" e "Ora"
    if 'Datetime' in df.columns:
        df[['Data', 'Ora']] = df['Datetime'].str.split('T', expand=True)
        df['Ora'] = df['Ora'].str.replace('Z', '')  # Rimuove la "Z" dall'orario
        df['Ora'] = df['Ora'].str.slice(0, 5)  # Mantiene solo HH:MM
        df = df.drop(columns=['Datetime'])  # Rimuove la colonna originale "Datetime"

    return df


# Funzione per calcolare il numero di parole in un testo
def count_words(text):
    return len(text.split()) if text else 0

# Funzione per calcolare il numero di emoticon in un testo
def count_emoticons(text):
    # Usa la libreria emoji per rilevare emoticon Unicode
    return sum(1 for char in text if char in emoji.EMOJI_DATA) if text else 0

# Funzione per calcolare il numero di menzioni in un testo
def count_mentions(text):
    # Regular expression per rilevare menzioni (esclude le email)
    mention_pattern = r'(?<!\S)@(\w+)(?!\.\w)'  # Trova menzioni che non sono seguite da domini di email
    return len(re.findall(mention_pattern, text)) if text else 0


# Funzione per calcolare il numero di hashtag in un testo
def count_hashtags(text):
    # Regular expression per rilevare hashtag
    hashtag_pattern = r'#\w+'
    return len(re.findall(hashtag_pattern, text)) if text else 0

# Funzione per aggiungere le colonne al DataFrame
def add_text_columns(df):
    # Aggiungi nuove colonne calcolate dalla Descrizione
    df['Numero di Parole'] = df['Descrizione'].apply(count_words)
    df['Numero di Emoticon'] = df['Descrizione'].apply(count_emoticons)
    df['Numero di Menzioni'] = df['Descrizione'].apply(count_mentions)
    df['Numero di Hashtag'] = df['Descrizione'].apply(count_hashtags)
    return df

# Funzione per controllare se il luogo è menzionato nella descrizione
def check_location_association(row):
    if "None" in row['Luogo']: return False
    else: return True
    
# Funzione per contare quante volte il luogo è menzionato nella descrizione
def count_location_occurrences(row):
    luogo = row['Luogo'].lower()  # Nome del luogo in minuscolo
    descrizione = row['Descrizione'].lower()  # Descrizione in minuscolo

    # Rimuove caratteri di separazione come virgole, punti, ecc.
    luogo_pulito = re.sub(r'[^\w\s]', '', luogo)  # Mantiene solo lettere e spazi
    luogo_parole = luogo_pulito.split()  # Divide in parole singole

    # Conta le occorrenze sovrapposte del nome completo del luogo
    luogo_count = len(re.findall(f"(?={re.escape(luogo_pulito)})", descrizione))

    # Conta le occorrenze di ciascuna parola significativa del luogo
    for parola in luogo_parole:
        # Ignora parole troppo generiche come "new", "city", ecc.
        if len(parola) > 2:  # Solo parole con più di 2 lettere
            # Conta le occorrenze sovrapposte della parola isolata
            luogo_count += len(re.findall(f"(?={re.escape(parola)})", descrizione))

    return luogo_count

# Percorso al file txt generato
file_path = 'instagram_posts.txt'

# Creazione del DataFrame
df = txt_to_dataframe(file_path)

# Riordina le colonne nel caso in cui siano disordinate
colonne_ordinate = ['Nome','Luogo', 'Like', 'Descrizione', 'Data', 'Ora', 'Followers', 'NumImmagini']
df = df[colonne_ordinate]

# Aggiungi le colonne di analisi del testo
df = add_text_columns(df)

# Aggiungi la colonna "Associazione a luogo" controllando la presenza del luogo nella descrizione
df['Associazione a luogo'] = df.apply(check_location_association, axis=1)

# Aggiungi la colonna "Associazione a luogo" con il conteggio delle occorrenze del luogo nella descrizione
df['Occorrenze del Luogo'] = df.apply(count_location_occurrences, axis=1)

#df = df.drop(columns=['Descrizione'])  # Rimuove la colonna "Descrizione"
#df = df.drop(columns=['Nome'])

# Mostra i primi 5 record
print(df.head())

# Salva il DataFrame in un file CSV
df.to_csv('instagram_posts.csv', index=False, encoding='utf-8')

print("Dataset Creato con Successo")