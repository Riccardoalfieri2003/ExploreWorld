from Regression_Like import train_model, split_data, preprocess_data, load_dataset, evaluate_model, predict_likes
from Regressione_Few_Follower import model_operations, predictFewFollowerLike
import pandas as pd

def main():
    #Dataset
    file_path = "instagram_posts.csv"
    data = load_dataset(file_path)
    X, y = preprocess_data(data)
    X_train, X_test, y_train, y_test = split_data(X, y)


    model_high_followers = train_model(X_train, y_train)  # Modello per follower > 46700
    model_low_followers = model_operations()  # Modello per follower <= 46700

    #Dati di esempio per la predizione
    num_follower = 50700
    new_data = {
        'Followers': num_follower,
        'NumImmagini': 3,
        'Numero di Parole': 10,
        'Numero di Emoticon': 1,
        'Numero di Menzioni': 1,
        'Numero di Hashtag': 1,
        'Occorrenze del Luogo': 3
    }

    if num_follower > 46700:
        print("Regression Like")
        new_data_df = pd.DataFrame([new_data])
        predicted_likes = predict_likes(model_high_followers, new_data_df)
        predicted_likes = predicted_likes[0]  # Estrai il primo elemento
    elif num_follower <= 47600:
        print("Regression Few Follower Like")
        predicted_likes = predictFewFollowerLike(model_low_followers, new_data)

    print(f"Numero di Followers: {num_follower}, Predicted Likes: {predicted_likes:.2f}")

if __name__ == "__main__":
    main()
