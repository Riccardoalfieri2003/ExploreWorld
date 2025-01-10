import tkinter as tk

"""
# Funzione per ottenere il testo inserito
def get_text():
    testo_inserito = text_area.get("1.0", tk.END)  # Ottiene tutto il testo
    print("Testo inserito:", testo_inserito)

# Funzione per ottenere la selezione del Radio Button
def ottieni_selezione():
    print("Selezione attuale:", scelta.get())


# Creazione della finestra principale
root = tk.Tk()
root.title("Finestra Ridimensionabile")
root.geometry("900x450")  # Larghezza x Altezza
root.resizable(True, True)  # Finestra ridimensionabile

# Creazione di una Text Area
text_area = tk.Text(root, wrap="word", height=1, width=10)
text_area.grid(row=0, column=0, padx=10, pady=10, sticky="nw")  # Allinea in alto a sinistra

# Creazione di un frame per i Radio Button
radio_frame = tk.Frame(root)
radio_frame.grid(row=0, column=1, padx=20, pady=20, sticky="n")  # Allinea a destra della Text Area

# Variabile per memorizzare la selezione del Radio Button
scelta = tk.StringVar(value="opzione1")  # Imposta un valore predefinito

# Creazione dei Radio Button (uno accanto all'altro)
radio1 = tk.Radiobutton(radio_frame, text="Opzione 1", variable=scelta, value="opzione1")
radio1.pack(side=tk.LEFT, padx=5)  # Posiziona a sinistra con un po' di spazio

radio2 = tk.Radiobutton(radio_frame, text="Opzione 2", variable=scelta, value="opzione2")
radio2.pack(side=tk.LEFT, padx=5)  # Posiziona a sinistra, accanto al primo

# Pulsante per ottenere la selezione del Radio Button
button_selezione = tk.Button(root, text="Ottieni Selezione", command=ottieni_selezione)
button_selezione.grid(row=1, column=0, columnspan=2, pady=10)  # Posiziona il pulsante sotto i widget

# Pulsante per ottenere il testo inserito
button_testo = tk.Button(root, text="Ottieni Testo", command=get_text)
button_testo.grid(row=2, column=0, columnspan=2, pady=10)  # Posiziona il pulsante sotto gli altri widget

# Avvio del loop principale dell'interfaccia grafica
root.mainloop()
"""

root = tk.Tk()
root.title("Finestra Ridimensionabile")
root.geometry("900x450")  # Larghezza x Altezza
root.resizable(True, True)  # Finestra ridimensionabile




# Sezione 1: Header
header_frame = tk.Frame(root, bg="lightblue", height=50)
header_frame.pack(fill=tk.X, padx=10, pady=10)
header_frame.pack_propagate(False)  # Disabilita il ridimensionamento automatico

# Aggiungi una Text Area all'header
text_area = tk.Text(header_frame, wrap="word", height=1, width=30)
text_area.pack(side=tk.LEFT, padx=10, pady=10)  # Allinea a sinistra con un po' di spazio

# Variabile per memorizzare la selezione del Radio Button
scelta = tk.StringVar(value="opzione1")  # Imposta un valore predefinito

# Aggiungi un frame per i Radio Button
radio_frame = tk.Frame(header_frame, bg="lightblue")
radio_frame.pack(side=tk.LEFT, padx=10, pady=10)  # Allinea a sinistra con un po' di spazio

# Aggiungi i Radio Button al frame
radio1 = tk.Radiobutton(radio_frame, text="Specifico", variable=scelta, value="specifico", bg="lightblue")
radio1.pack(side=tk.LEFT, padx=5)  # Allinea a sinistra con un po' di spazio

radio2 = tk.Radiobutton(radio_frame, text="Generale", variable=scelta, value="generale", bg="lightblue")
radio2.pack(side=tk.LEFT, padx=5)  # Allinea a sinistra con un po' di spazio


# Funzione per ottenere il contenuto della Text Area
def ottieni_contenuto():
    contenuto = text_area.get("1.0", tk.END) # Recupera il contenuto 
    print("Contenuto della Text Area:", contenuto)

# Aggiungi un pulsante a destra dell'header
button = tk.Button(header_frame, text="Ottieni Contenuto", command=ottieni_contenuto)
button.pack(side=tk.RIGHT, padx=10, pady=10)  # Allinea a destra con un po' di spazio








# Sezione 2: Corpo principale (altezza fissa)
main_frame = tk.Frame(root, bg="lightgray", height=300)  # Altezza fissa di 200 pixel
main_frame.pack(fill=tk.X, padx=10, pady=10)
main_frame.pack_propagate(False)  # Disabilita il ridimensionamento automatico

# Aggiungi un pulsante al corpo principale
label_main = tk.Label(main_frame, text="Foto luogo", font=("Arial", 16), bg="lightgray")
label_main.pack(pady=20)



# Sezione 3: Footer
footer_frame = tk.Frame(root, bg="lightgreen", height=200)
footer_frame.pack(fill=tk.X, padx=10, pady=10)
footer_frame.pack_propagate(False)  # Disabilita il ridimensionamento automatico

# Aggiungi un'eticheta al footer
label_footer = tk.Label(footer_frame, text="Text area per la descrizione", font=("Arial", 12), bg="lightgreen")
label_footer.pack(pady=10)





# Sezione 4: Contenuto sotto il corpo principale (verrà "spinto" fuori se la finestra è troppo piccola)
extra_frame = tk.Frame(root, bg="yellow", height=20)  # Altezza fissa di 300 pixel
extra_frame.pack(fill=tk.X, padx=10, pady=10)
extra_frame.pack_propagate(False)  # Disabilita il ridimensionamento automatico


# Aggiungi un widget alla sezione extra
label_extra = tk.Label(extra_frame, text="Pulsanti di post", font=("Arial", 14), bg="yellow")
label_extra.pack(pady=20)







root.mainloop()