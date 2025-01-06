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

from Models.PeopleModel.PgetPredictionClass import PeopleGetClassPrediction
from Models.TimeModel.TgetClassPrediction import TimeGetClassPrediction
from Models.PhotoOrNotModel.PHgetClassPrediction import PhotoGetClassPrediction
from Models.MareMontagnaCittaModel.MMCgetPredictionClass import MareMontagnaCittaGetClassPrediction

TimeModel = load_model(os.path.abspath('Models/TimeModel/DaySunsetNight_classifier.h5').replace('\interfaccia',''))
PhotoModel = load_model(os.path.abspath('Models/PhotoOrNotModel/PhotoOrNot_classifier.h5').replace('\interfaccia',''))
PeopleModel=load_model(os.path.abspath('Models/PeopleModel/PeopleOrNot_classifier.h5').replace('\interfaccia',''))
MareMontagnaCittaModel=load_model(os.path.abspath('Models/MareMontagnaCittaModel/MareMontagnaCitta_classifier.h5').replace('\interfaccia',''))

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
    imageType=PhotoGetClassPrediction(PhotoModel,img)
    peopleOrNot=PeopleGetClassPrediction(PeopleModel,img)
    time=TimeGetClassPrediction(TimeModel,img)
    isMare,isMontagna,isCitta=MareMontagnaCittaGetClassPrediction(MareMontagnaCittaModel,img)
    return imageType,peopleOrNot,time,isMare,isMontagna,isCitta


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
