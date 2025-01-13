import os
import sys
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_path)

from keras.models import load_model

from keras.preprocessing.image import load_img, img_to_array
from keras.models import load_model
from io import BytesIO
from PIL import Image
import numpy as np
import requests

from PeopleModel.PgetPredictionClass import PeopleGetClassPrediction
from TimeModel.TgetClassPrediction import TimeGetClassPrediction
from PhotoOrNotModel.PHgetClassPrediction import PhotoGetClassPrediction
from MareModel.MGetPredictionClass import MareGetClassPrediction
from MontagneModel.MountGetPredictionClass import MountainGetClassPrediction
from CittaModel.CGetPredictionClass import CittaGetClassPrediction


# Ottieni il percorso assoluto della directory del progetto
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Percorsi assoluti per i modelli
people_model_path = os.path.join(project_path, 'Models', 'PeopleModel', 'PeopleModel_quantized.tflite')
time_model_path = os.path.join(project_path, 'Models', 'TimeModel', 'TimeModel_quantized.tflite')
photo_model_path = os.path.join(project_path, 'Models', 'PhotoOrNotModel', 'PhotoModel_quantized.tflite')
mare_model_path = os.path.join(project_path, 'Models', 'MareModel', 'MareModel_quantized.tflite')
montagna_model_path = os.path.join(project_path, 'Models', 'MontagneModel', 'MontagneModel_quantized.tflite')
citta_model_path = os.path.join(project_path, 'Models', 'CittaModel', 'CittaModel_quantized.tflite')

# Caricamento dei modelli
PeopleModel = load_model(people_model_path)
TimeModel = load_model(time_model_path)
PhotoModel = load_model(photo_model_path)
MareModel = load_model(mare_model_path)
MontagnaModel = load_model(montagna_model_path)
CittaModel = load_model(citta_model_path)


print("Modelli caricati")


def imageForModel(url):
    # Fetch the image
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful

    # Load the image into Pillow
    image = Image.open(BytesIO(response.content))

    # Convert the image to BytesIO 
    image_bytes = BytesIO() 
    image.save(image_bytes, format=image.format) 
    image_bytes.seek(0) # Move the cursor to the beginning of the file

    # Load the image
    img = load_img(image_bytes, target_size=(244, 244)) # Resize to match model input size

    # Convert the image to a NumPy array
    img_array = img_to_array(img)

    # Expand dimensions to match the model's input shape (batch size, height, width, channels)
    img_array = np.expand_dims(img_array, axis=0)

    # Normalize the pixel values
    img_array = img_array / 255.0

    return img_array

def getPredictions_noTimeout(url):
    img=imageForModel(url)

    
    TimeModelPrediction = TimeGetClassPrediction(TimeModel,img)
    #print("TimePrediction: ",TimeModelPrediction)

    PhotoModelPrediction = PhotoGetClassPrediction(PhotoModel,img)
    #print("PhotoPrediction: ", PhotoModelPrediction)

    PeopleModelPrediction = PeopleGetClassPrediction(PeopleModel, img)
    #print("PeoplePrediction: ",PeopleModelPrediction)

    #MarePrediction,MontagnaPrediction,CittaPrediction=MareMontagnaCittaGetClassPrediction(MareMontagnaCittaModel,img)
    MarePrediction=MareGetClassPrediction(MareModel,img)
    #print("MarePrediction: ", MarePrediction)

    MontagnePrediction=MountainGetClassPrediction(MontagnaModel,img)
    #print("MontagnaPrediction: ", MontagnePrediction)

    CittaPrediction=CittaGetClassPrediction(CittaModel,img)
    #print("CittaPrediction: ", CittaPrediction)


    """imageType=PhotoGetClassPrediction(PhotoModel,img)
    peopleOrNot=PeopleGetClassPrediction(PeopleModel,img)
    time=TimeGetClassPrediction(TimeModel,img)
    isMare,isMontagna,isCitta=MareMontagnaCittaGetClassPrediction(MareMontagnaCittaModel,img)"""


    return PhotoModelPrediction,TimeModelPrediction,PeopleModelPrediction,MarePrediction,MontagnePrediction,CittaPrediction


from concurrent.futures import ThreadPoolExecutor, TimeoutError

def getPredictions(url, timeout_seconds=10):
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(getPredictions_noTimeout, url)
        return future.result(timeout=timeout_seconds)
        """
        try:
            # Wait for the result with a timeout
            return future.result(timeout=timeout_seconds)
        except TimeoutError:
            print(f"Timeout occurred for URL: {url}")
            return None  # Handle timeout (e.g., skip the URL)
    return None
    """

#print(getPredictions('https://thegetaway.mblycdn.com/uploads/tg/2022/01/GettyImages-938335974.jpg'))