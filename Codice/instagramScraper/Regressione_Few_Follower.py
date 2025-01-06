import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import math


# Funzione di compensazione
def compensate(num_follower):
    if num_follower < 2939:
        p1 = num_follower - 2000
        p1 *= -1
        p1 /= 50000
        denum = 1 + (math.pow(math.e, p1))
        return (2.5 / denum) - 1.222
    else:
        return num_follower / (47600 * 2.15)


# Funzione di predizione
def predictFewFollowerLike(model, new_post):
    """
    Predice il numero di Like per un nuovo post dato il modello addestrato
    e le caratteristiche del post.

    Parametri:
        - model: Modello addestrato
        - new_post_features: Dizionario con le caratteristiche del nuovo post
    Restituisce:
        - Predicted likes
    """
    # Estrai il numero di follower dalle caratteristiche del nuovo post
    num_follower = new_post['Followers']

    # Calcola la compensazione basata sul numero di follower
    compensation_factor = compensate(num_follower)

    # Rimuovi il numero di follower dalle caratteristiche per la predizione
    new_post_features_copy = new_post.copy()
    del new_post_features_copy['Followers']

    # Conversione delle caratteristiche in DataFrame
    new_post_df = pd.DataFrame([new_post_features_copy])

    # Predizione logaritmica
    predicted_likes_log = model.predict(new_post_df)[0]

    # Conversione della predizione logaritmica in valore effettivo
    predicted_likes = np.expm1(predicted_likes_log) * compensation_factor

    print(f"Numero di Followers: {num_follower}, Predicted Likes: {predicted_likes:.2f}")
    return predicted_likes


def model_operations():
    # Caricamento dei dati
    file_path = 'instagram_posts.csv'  # Cambia con il tuo file CSV
    data = pd.read_csv(file_path)

    # Selezione delle colonne rilevanti
    features = ['NumImmagini', 'Numero di Parole', 'Numero di Emoticon', 'Numero di Menzioni', 'Numero di Hashtag',
                'Occorrenze del Luogo']
    target = 'Like'

    # Trasformazione logaritmica dei like
    data['Like'] = np.log1p(data['Like'])

    X = data[features]
    y = data['Like']

    # Preprocessing: scaling delle caratteristiche numeriche
    preprocessor = ColumnTransformer(
        transformers=[('num', StandardScaler(), features)]
    )

    # Modello
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', GradientBoostingRegressor(n_estimators=200, learning_rate=0.1, random_state=42))
    ])

    # Suddivisione del dataset in training e test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Addestramento del modello
    model.fit(X_train, y_train)

    return model


if __name__ == "__main__":
    # Addestra il modello
    model = model_operations()

    # Esegui predizione per vari follower
    for num_follower in range(1000, 47601, 200):  # Da 1000 a 47600 con incremento di 200
        # Nuovo post come DataFrame
        new_post = {
            'Followers': num_follower,
            'NumImmagini': 3,
            'Numero di Parole': 10,
            'Numero di Emoticon': 1,
            'Numero di Menzioni': 1,
            'Numero di Hashtag': 1,
            'Occorrenze del Luogo': 3
        }

        # Predizione
        predicted_likes = predictFewFollowerLike(model, new_post)
        print(f"Numero di Followers: {num_follower}, Predicted Likes: {predicted_likes:.2f}")
