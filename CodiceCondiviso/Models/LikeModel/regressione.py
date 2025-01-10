"""
import os
import sys
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_path)"""

import os
from like_model import train_model, split_data, preprocess_data, load_dataset, evaluate_model, predict_likes
from pochiFollower_regressione import model_operations, predictFewFollowerLike
import pandas as pd

def predictLikes(post):

    num_follower=post['Followers']

    #Dataset
    #file_path = "Datasets/postDataset/instagram_posts.csv" 

     # Dataset
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Directory corrente del file regressione.py
    project_root = os.path.dirname(current_dir)  # Salire di un livello (ExploreWorld)
    file_path = os.path.join(project_root, "Datasets", "postDataset", "instagram_posts.csv")  # Percorso assoluto

    data = load_dataset(file_path)
    X, y = preprocess_data(data)
    X_train, X_test, y_train, y_test = split_data(X, y)


    model_high_followers = train_model(X_train, y_train)  # Modello per follower > 46700
    model_low_followers = model_operations()  # Modello per follower <= 46700

    if num_follower > 47600:
        #print("Regression Like")
        new_data_df = pd.DataFrame([post])
        predicted_likes = predict_likes(model_high_followers, new_data_df)
        predicted_likes = predicted_likes[0]  # Estrai il primo elemento
        return predicted_likes

    else:
        #print("Regression Few Follower Like")
        predicted_likes = predictFewFollowerLike(model_low_followers, post)
        return predicted_likes


"""
#TESTING
def main():

    #Dati di esempio per la predizione
    num_follower = 1250
    new_data = {
        'Followers': num_follower,
        'NumImmagini': 4,
        'Numero di Parole': 13,
        'Numero di Emoticon': 2,
        'Numero di Menzioni': 1,
        'Numero di Hashtag': 10,
        'Associazione a luogo':True,
        'Occorrenze del Luogo': 2
    }

    predicted_likes=predictLikes(new_data)
    print(f"Numero di Followers: {num_follower}, Predicted Likes: {predicted_likes:.2f}")

if __name__ == "__main__":
    main()"""