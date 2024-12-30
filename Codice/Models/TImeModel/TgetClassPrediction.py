import numpy as np

def TimeGetClassPrediction(model, img):
    predictions=model.predict(img)
    predicted_class=np.argmax(predictions[0])
    return predicted_class