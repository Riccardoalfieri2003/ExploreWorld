from flask import Flask, render_template, request, jsonify
import re
import emoji

import os
import sys
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_path)

# Percorso per il modulo like_model
instagram_scraper_path = os.path.abspath(os.path.join(project_path, 'Models'))
sys.path.append(instagram_scraper_path)


from googleScraper.google_scraping_thread import getURLs
from Models.LikeModel.regressione import predictLikes
from Models.getModelPredictions import getPredictions


"""
palette:
scuro: 1F1D36
medio scuro: 3F3351
medio: #5C3B65
medio chiaro: 864879
chiaro: E9A6A6
"""


app = Flask(__name__)



@app.route("/") 
def index():
    return render_template("index.html")



@app.route("/getURLs", methods=["POST"])
def getURLs_interface(): 
    print("Funzione chiamata")
    # Prendi il parametro dal corpo della richiesta
    data = request.json
    luogoUtente = data.get("luogoUtente", "")  # Default a stringa vuota se non fornito

    # Chiama la funzione getURLs e ottieni i tre valori
    lista_stringhe, tupla_double, stringa = getURLs(luogoUtente, "Specifico")

    print(tupla_double)
    print(stringa)

    # Restituisci i tre valori come un dizionario JSON
    return jsonify({
        "lista_stringhe": lista_stringhe,
        "tupla_double": tupla_double,
        "stringa": stringa
    })





# Funzioni di analisi del testo
def count_words(text):
    return len(text.split()) if text else 0

def count_emoticons(text):
    return sum(1 for char in text if char in emoji.EMOJI_DATA) if text else 0

def count_mentions(text):
    mention_pattern = r'(?<!\S)@(\w+)(?!\.\w)'
    return len(re.findall(mention_pattern, text)) if text else 0

def count_hashtags(text):
    hashtag_pattern = r'#\w+'
    return len(re.findall(hashtag_pattern, text)) if text else 0


# Funzione per contare quante volte il luogo è menzionato nella descrizione
def count_location_occurrences(descrizione,luogo):
    descrizione=descrizione.lower()
    luogo=luogo.lower()

    # Rimuove caratteri di separazione come virgole, punti, ecc.
    luogo_pulito = re.sub(r'[^\w\s]', '', luogo)  # Mantiene solo lettere e spazi
    luogo_parole = luogo_pulito.split()  # Divide in parole singole

    luogo_count = 0
    # Conta le occorrenze di ciascuna parola significativa del luogo
    for parola in luogo_parole:
        # Ignora parole troppo generiche come "new", "city", ecc.
        if len(parola) > 2:  # Solo parole con più di 2 lettere
            # Conta le occorrenze sovrapposte della parola isolata
            luogo_count += len(re.findall(f"(?={re.escape(parola)})", descrizione))

    return luogo_count


@app.route("/predictLike", methods=["POST"])
def predict_like():
    print("Siamoa a predict")

    data = request.json
    descrizione = data.get("descrizione", "")
    num_immagini = data.get('numImmagini')
    luogo = data.get('stringa')
    num_follower = int(data.get('numeroFollower'))

    wordCount = count_words(descrizione)
    emoticonCount = count_emoticons(descrizione)
    mentionsCount = count_mentions(descrizione)
    hashtagCount = count_hashtags(descrizione)
    OccCount = count_location_occurrences(descrizione,luogo)



    new_data = {
        'Followers': num_follower,
        'NumImmagini': num_immagini,
        'Numero di Parole':  wordCount,
        'Numero di Emoticon': emoticonCount,
        'Numero di Menzioni': mentionsCount,
        'Numero di Hashtag': hashtagCount,
        'Associazione a luogo': True,
        'Occorrenze del Luogo': OccCount
    }
    print(new_data)

    predicted_likes = predictLikes(new_data)
    print("Like predetti ",predicted_likes)

    return jsonify(predicted_likes)







@app.route("/processaAzione", methods=["POST"])
def processa_azione():
    # Ottieni i dati inviati dal frontend
    dati = request.json

    print("Siamo qui")

    # Estrai i valori dei checkbox e l'array risultati
    opzioni1 = dati.get("opzioni1", [])
    opzioni2 = dati.get("opzioni2", [])
    opzioni3 = dati.get("opzioni3", [])
    print("Opzioni fatte")
    listaStringhe = dati.get("listaStringhe", [])

    #print(listaStringhe)

    """ 
    listaStringhe = [
    "https://lh5.googleusercontent.com/p/AF1QipP1y1Rt6sL6iJuJKLAzn5GaQ0HDBuAKdyFm9kVC=w2030-h477-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipPkC8y1ssyxvFdijmQ_1JsBZow6TLXv00Pi7U_n=w2030-h1520-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipPpVFP7t-OvtjS_5UIMJ9CN1JtjupF46m8ngBEG=w2030-h454-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipPyMO_WqF9mfLFEnJ0SEWrp-5za3T0auD-3tHA=w2030-h2700-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipMiwn6SeUjiOFpLCs5I-_Om01G5QFDiC4rzRR_o=w2030-h2700-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipNjVZx43664nulLrKRxletJ24afoEZUYuFQxR23=w2030-h2530-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipPCtHCskMro4wHBYnnowOp4-k3rF_lcROViy_EP=w2030-h1350-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipPdBJU8iPLUh2jyH7cP3mr_7USS7jTiLr65673H=w2030-h1520-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipPqAwmVQyjXZrROyscbMUPHlBCRNEF3nnfMU7Tu=w2030-h1520-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipMaGnqOoQja6EHd7rTDosiMDXaagUd9L60Kr3Zh=w2030-h1140-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipOB-ORlTWo-a4to7K9dgzyxNMhtTdqk-yj00ZNu=w2030-h1350-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipPpZGqW7Ov9-2-l92ngyNPxpmpZVWfNo0gcM1R8=w2030-h1520-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipOO3PNLrGt8wO-LnOb0Kx4mJp-d-vY8KMcQuV9f=w2030-h914-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipPCByv-8Xy5LOhNZVndqlrQMcOTfAnQOPTv0_Nn=w2030-h2700-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipNN03YyFfQxjrMbqni3E_9CTfKlY1SMQHYKIrW6=w2030-h1140-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipM9tZD1LUzZQ6GI3NZRfFlzYYsPiAP9_GMTZNrb=w2030-h1140-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipNmiFP-MIrYpQOfdb5Ymddk4dCee9LyjTwhSktr=w2030-h1520-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipNkJIWdUVQvHnFQ_FOi14DnU931iAQMlnUwbmnL=w2030-h2480-k-no",
    "https://lh3.googleusercontent.com/p/AF1QipORtSwKhJ2mVPqQ5UgbBqyOoz6bqkMELg61EpM=w2030-h3600-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipO57PZxYbrPHxhvzwMmc6ia4jeS6h-c0TFSImRS=w2030-h966-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipPx5hJk_pGUqr8y_p1FnkhN0kHSqJLxRZ3oBPQR=w2030-h1180-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipO3axLhF6Y9zPkBkaKJhB5R0rOGvdffeemKmFXy=w2030-h1350-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipO7_knU96V9ClocBiHZkJwvBd1WwP-H1uwKZKTy=w2030-h1350-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipM69EjANIDi1vWRWaf-G38VyruxtVLAGFgaKBx-=w2030-h1220-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipPVoHC7nj29mrZoymMLsiqXpphdZ4SPnziiELKg=w2030-h1350-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipMEjUdcZH5GeRgzwJ_EmJ64GRKf7GGKVTXWM9cy=w2030-h1520-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipPTBAVAG88G28semH07FLjOkCxHB1Ry2tU8ZeES=w2030-h1520-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipOgV0BeIIDrLDnbJP6bhSeNzpX7nQjLIZFpS_HX=w2030-h1172-n-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipP4XRW15cUQjjCvgOtGPKC60e6pgFpE7gdHuUiK=w2030-h1172-n-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipOCoXANG1iMu8J5PXXv-m_Hlg13MHaTcu-xSZVx=w2030-h1520-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipO4EfJh2jfBTCs2jlZYxUDSe8YiBOGQgEqcA7wG=w2030-h1172-n-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipOoL06bGpyeqyEtGJahohuS5WDpRT5C5vr25hZU=w2030-h1350-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipMi5lokhgUcYVV9YYcV87iButtZQZpuDybbiW9K=w2030-h1520-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipNYIAxfRrQAD7W-4mZB6IWSgQ4gv1FWt6ZRoTA4=w2030-h1520-k-no",
    "https://lh5.googleusercontent.com/proxy/jTj8BUH7KEcwbWyoC0tIKz-jVFLfqh1xlF1udDOc1VrRgcaDF8wMBY8QofIamLQvJLtiSS9X5hKxyoAo_oyQrtLLehimOSQDC44MbF3_hJJeeHLhGoubcDN-669XB4KOth-TYFKLGIMMhTbXLDHtUxX0rSUwBQ=w2030-h1172-n-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipM72j2YrlmEDMgCYY9Od4elrjbxdhdy2qMnNHKU=w2030-h1140-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipPuhbgS4E0gPYv_YVNB0oN9gk5OTMypbzjPTblm=w2030-h1172-n-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipNgjDB44rjFRXiltZ2ALNp5Nnu8Mo43y90SK-Xt=w2030-h1010-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipN5i_zLkhP4By3Au2_j28Pg5wUm8NydPmEigmT3=w2030-h1140-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipOyWFixaMwgsbYJjc52vDwKq4VGyFI_a1SKFUrC=w2030-h1350-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipP3E77hzN8wxqM5F2zPZk3e57RtY3ePq3i5mYlQ=w2030-h1172-n-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipPqOFoZQddTAP6iJtQo8pJp9xKxtH6vYIDbDq4o=w2030-h1350-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipOEx1ZsUK9MvPhZ9y_moGfq8sddTTP5eN2d2UTo=w2030-h1172-n-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipNGQYUsTj9O8J-t4D4aH3Fq1aTdeCrQzL9E3K8K=w2030-h1172-n-k-no",
    "https://lh5.googleusercontent.com/p/AF1QipOEDkx_ZS0Fr1YIpP-pp5F0nrlDPXNHJjEoW4Xj=w2030-h1172-n-k-no"
    ]"""

    # Stampa i dati per debug (puoi rimuoverlo in produzione)
    
    print("Opzioni 1:", opzioni1)
    print("Opzioni 2:", opzioni2)
    print("Opzioni 3:", opzioni3)
    #print("Risultati:", risultati)

    urlValidi=[]
    for url in listaStringhe:
        try:
            predictions=getPredictions(url)

            print(url)
            print(predictions)

            if predictions[0]!=0: continue



            if len(opzioni1)==1:
                if 'Mattina' in opzioni1 and predictions[2]!=0: continue
                if 'Alba/Tramonto' in opzioni1 and predictions[2]!=1: continue
                if 'Notte' in opzioni1 and predictions[2]!=2: continue

            if len(opzioni1)==2:
                if 'Mattina' not in opzioni1 and predictions[2]==0: continue
                if 'Alba/Tramonto' not in opzioni1 and predictions[2]==1: continue
                if 'Notte' not in opzioni1 and predictions[2]==2: continue


            


            if len(opzioni2)==1:
                if 'Persone' in opzioni2 and predictions[1]==0: continue
                if 'No Persone' in opzioni2 and predictions[1]==1: continue

     



            if len(opzioni3)==1:
                if 'Mare' in opzioni3 and predictions[3]==0: continue
                if 'Montagna' in opzioni3 and predictions[4]==0: continue
                if 'Città' in opzioni3 and predictions[5]==0: continue

            if len(opzioni3)==2:
                if 'Mare' not in opzioni3 and predictions[3]==1: continue
                if 'Montagna' not in opzioni3 and predictions[4]==1: continue
                if 'Città' not in opzioni3 and predictions[5]==1: continue



            urlValidi.append(url)
            print("url valido")
            #print(url)
        except Exception as e: 
            print(e)
            print("Prossima immagine")
            continue

    # Restituisci gli URL validi al frontend
    print("URL validati")
    return jsonify({"urlValidi": urlValidi})


        






    # Qui puoi fare quello che vuoi con i dati
    # Ad esempio, chiamare altre funzioni Python o salvare i dati in un database

    # Restituisci una risposta al frontend
    #return jsonify({"status": "success", "message": "Dati ricevuti e processati!"})





if __name__ == "__main__":
    app.run(debug=True)