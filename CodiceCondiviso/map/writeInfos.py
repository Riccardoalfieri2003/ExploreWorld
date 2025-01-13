def salva_in_txt(nome_luogo, coordinate, lista_url):
    """
    Salva le informazioni in un file .txt con il formato:
    Nome luogo, (coordinate), (url1, url2, ...)

    """
    try:
        # Formatta le coordinate e la lista di URL
        coordinate_str = f"({coordinate[0]}, {coordinate[1]})"  # Es. (lat, lon)
        url_str = ", ".join(lista_url)  # Concatena gli URL separati da virgola
        urls_formattati = f"({url_str})"
        
        # Stringa finale da salvare
        contenuto = f"{nome_luogo}, {coordinate_str}, {urls_formattati}\n"
        
        # Scrive i dati nel file
        with open("map/infos.txt", 'a', encoding='utf-8') as file:  # Usa 'a' per aggiungere al file esistente
            file.write(contenuto)
        print(f"Dati salvati con successo in infos.txt!")
    except Exception as e:
        print(f"Errore durante il salvataggio: {e}")


"""
# Dati da salvare
nome_luogo = "Napoli"
coordinate = (40.682440, 14.768096)  # Latitudine e longitudine
lista_url = ["https://images.lonelyplanetitalia.it/uploads/mraWpFhkXoq7uk8yrpk50VPJPYrVKIOL.jpg?q=80&p=slider&s=d8b0b65fd3a26a1662967428ada0109d", 
             "https://images.winalist.com/blog/wp-content/uploads/2024/10/15134347/shutterstock_2456673629-1500x1000.jpg"]

# Salva i dati nel file
salva_in_txt(nome_luogo, coordinate, lista_url)

"""
