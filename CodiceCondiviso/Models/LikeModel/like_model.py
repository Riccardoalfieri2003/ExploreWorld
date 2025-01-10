import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error





# 1. Caricamento del dataset
def load_dataset(file_path):
    data = pd.read_csv(file_path)
    return data


# 2. Pre-processing dei dati
def preprocess_data(data):
    # Converti le colonne numeriche in tipo numerico
    numeric_columns = ['Like', 'Followers', 'NumImmagini', 'Numero di Parole', 'Numero di Emoticon',
                       'Numero di Menzioni', 'Numero di Hashtag', 'Associazione a luogo' ,'Occorrenze del Luogo']
    for col in numeric_columns:
        data[col] = pd.to_numeric(data[col], errors='coerce')

    # Rimuovi righe con valori nulli
    data = data.dropna()

    # Separazione delle feature e del target
    X = data[['Followers', 'NumImmagini', 'Numero di Parole', 'Numero di Emoticon', 'Numero di Menzioni',
              'Numero di Hashtag','Associazione a luogo', 'Occorrenze del Luogo']]
    y = data['Like']

    return X, y


# 3. Divisione dei dati
def split_data(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test


# 4. Addestramento del modello
def train_model(X_train, y_train):
    model = RandomForestRegressor(random_state=42, n_estimators=100)
    model.fit(X_train, y_train)
    return model


# 5. Valutazione del modello
def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))

    print(f"Mean Absolute Error: {mae}")
    print(f"Root Mean Squared Error: {rmse}")
    return mae, rmse


# 6. Predizione dei like
def predict_likes(model, new_data):
    # Predici i like usando il modello
    prediction = model.predict(new_data)

    # Calcolare il numero medio di follower nel set di addestramento
    #avg_followers_train = X_train['Followers'].mean()
    #print(avg_followers_train)

    avg_followers_train = 229423.5975714286

    # Ridimensionare la previsione in base alla proporzione tra i follower
    scaling_factor = new_data['Followers'] / avg_followers_train

    # Moltiplicare la previsione per il fattore di scalatura
    final_prediction = prediction * scaling_factor

    # Salva i follower originali
    original_followers = new_data['Followers'].copy()

    #Corretto

    # Correzione per il range di follower tra 5 e 10.000
    for i in range(len(new_data)):
        if 1 <= new_data.iloc[i]['Followers'] <= 10000:
            # Aggiungi una correzione logaritmica o moltiplicativa per evitare valori troppo bassi
            #final_prediction[i] = max(final_prediction[i], np.log1p(new_data.iloc[i]['Followers']) * 10)
            print("La predizione e' influenzata in maniera negativa dal numero di Follower troppo bassi!")
            # Imposta i follower a 100,000 e predici nuovamente
            new_data.loc[i, 'Followers'] = 100000
            new_prediction = model.predict(new_data.iloc[[i]])
            print(f"Se la pagina che ha postato avesse avuto 100,000 follower:")
            print(f"Numero di Followers della pagina: 100000, Predicted Likes: {new_prediction[0]:.2f}")

    # Ripristina i follower originali
    new_data['Followers'] = original_followers

    return final_prediction



"""

# Script principale
if __name__ == "__main__":
    # Percorso al file CSV creato
    file_path = "instagramScraper/instagram_posts.csv"

    # Caricamento e preprocessing
    data = load_dataset(file_path)
    X, y = preprocess_data(data)

    # Divisione train-test
    X_train, X_test, y_train, y_test = split_data(X, y)

    # Addestramento del modello
    model = train_model(X_train, y_train)

    # Valutazione
    evaluate_model(model, X_test, y_test)

    num_follower=47601

    # Esempio di predizione su nuovi dati
    new_data = pd.DataFrame({
        'Followers': [num_follower],
        'NumImmagini': [3], #tic piu immagini portano piu like
        'Numero di Parole': [10], #tic con numero di parole piu grande da minori like
        'Numero di Emoticon': [1], #tic piu emoticon portano piu like
        'Numero di Menzioni': [1], #tic piu emoticon portano piu' like
        'Numero di Hashtag': [1], #tic il numero di hashtag non influenzano tanto il numero di like
        'Associazione a luogo': [True],
        'Occorrenze del Luogo': [3]
    })

    #if num_follower<=47600: predicted_likes=predict_likes(model, new_data)+compensate(num_follower)
    #else: predicted_likes = 
    predicted_likes = predict_likes(model, new_data)
    followers = new_data.iloc[0]['Followers']  # Prende il numero di follower reali dal dataframe
    print(f"Numero di Followers della pagina: {followers}, Predicted Likes: {predicted_likes[0]:.2f}")
"""
"""
def predictLikes(model, new_post):
    predicted_likes = predict_likes(model, new_post)
    followers = new_post.iloc[0]['Followers']  # Prende il numero di follower reali dal dataframe
    print(f"Numero di Followers della pagina: {followers}, Predicted Likes: {predicted_likes[0]:.2f}")"""