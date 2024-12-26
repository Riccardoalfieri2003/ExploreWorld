import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, r2_score

def main():
    # Caricamento dei dati
    file_path = 'instagram_posts.csv'  # Cambia con il tuo file CSV
    data = pd.read_csv(file_path)

    # Selezione delle colonne rilevanti (escludendo il numero di immagini e includendo occorrenze del luogo)
    features = ['Numero di Parole', 'Numero di Emoticon', 'Numero di Menzioni', 'Numero di Hashtag', 'Occorrenze del Luogo']
    target = 'Like'

    # Trasformazione logaritmica dei like
    data['Like'] = np.log1p(data['Like'])

    X = data[features]
    y = data['Like']

    # Preprocessing: scaling delle caratteristiche numeriche
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), features)
        ]
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

    # Valutazione del modello
    y_pred = model.predict(X_test)

    # Inversione della trasformazione log per interpretazione
    y_test_original = np.expm1(y_test)
    y_pred_original = np.expm1(y_pred)

    mae = mean_absolute_error(y_test_original, y_pred_original)
    r2 = r2_score(y_test_original, y_pred_original)

    print(f"Mean Absolute Error (MAE): {mae}")
    print(f"R-squared (R²): {r2}")

    # Predizione per un nuovo post
    new_post = {
        'Numero di Parole': 10, #Cerca di limitare la scrittura scrivendo di meno e in maniera piu' coincisa permette di prendere l attenzione del lettore
        'Numero di Emoticon': 0, #questo valore non e' di cosi tanto importanza poiche oscurerebbe la lettura della descrizione
        'Numero di Menzioni': 5, #inserendo piu' persone possibili allarga il raggio delle persone che lo vedranno
        'Numero di Hashtag': 3, #rappresenta un parametro fondamentale perche' grazie agli hashtag i post sono visibili a tutti
        'Occorrenze del Luogo': 0
    }

    # Conversione del nuovo post in un DataFrame
    new_post_df = pd.DataFrame([new_post])

    # Predizione
    predicted_likes_log = model.predict(new_post_df)[0]
    predicted_likes = np.expm1(predicted_likes_log)

    print(f"Predicted Likes for the new post: {predicted_likes}")

if __name__ == "__main__":
    main()
