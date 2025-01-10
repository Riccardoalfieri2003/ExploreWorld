import cv2
import numpy as np


"""
def resize_with_padding(image, target_size):
    # Get the original dimensions
    h, w = image.shape[:2]

    # Calculate the scaling factor
    scale = min(target_size / h, target_size / w)

    # Resize the image
    resized_image = cv2.resize(image, (int(w * scale), int(h * scale)))

    # Create a square canvas
    delta_w = target_size - resized_image.shape[1]
    delta_h = target_size - resized_image.shape[0]
    top, bottom = delta_h // 2, delta_h - (delta_h // 2)
    left, right = delta_w // 2, delta_w - (delta_w // 2)

    # Add padding
    padded_image = cv2.copyMakeBorder(resized_image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])
    return padded_image
"""

def resize(image, target_size):
    h, w = image.shape[:2]
    crop_size = min(h, w)

    # Calculate the center crop box
    start_x = (w - crop_size) // 2
    start_y = (h - crop_size) // 2

    # Crop and resize
    cropped_image = image[start_y:start_y+crop_size, start_x:start_x+crop_size]
    resized_image = cv2.resize(cropped_image, (target_size, target_size))
    return resized_image







from PIL import Image
import os

def resize_images(input_folder, output_folder, size=(244, 244)):
    # Crea la cartella di output se non esiste
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Itera su tutti i file nella cartella di input
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        
        # Apri l'immagine
        try:
            with Image.open(input_path) as img:
                # Trova il lato più corto e centra il ritaglio
                img = img.convert("RGB")  # Converte in RGB se necessario
                width, height = img.size
                min_side = min(width, height)
                left = (width - min_side) / 2
                top = (height - min_side) / 2
                right = (width + min_side) / 2
                bottom = (height + min_side) / 2
                
                # Ritaglia l'immagine al quadrato
                img = img.crop((left, top, right, bottom))
                
                # Ridimensiona a 244x244
                img = img.resize(size, Image.LANCZOS)
                
                # Salva l'immagine nella cartella di output
                img.save(output_path)
                print(f"Immagine {filename} ridimensionata e salvata in {output_path}")
        except Exception as e:
            print(f"Errore con l'immagine {filename}: {e}")

