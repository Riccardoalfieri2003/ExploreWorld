from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import confusion_matrix, classification_report
import numpy as np

#from TimeModel.TgetClassPrediction import TimeGetClassPrediction


# Define the proportionate function
def proportionate(num1, num2, num3):
    numSum = num1 + num2 + num3
    perc1 = num1 / numSum
    perc2 = num2 / numSum
    perc3 = num3 / numSum
    return perc1, perc2, perc3

# Define the manipulation function for batch predictions
def manipulate_probabilities(predictions):
    manipulated_predictions = []
    for pred in predictions:
        # Normalize the predictions
        perc1, perc2, perc3 = proportionate(pred[0], pred[1], pred[2])

        # Apply the custom logic
        perc1 *= 5  # Amplify sea class probability
        perc3 /= 2  # Reduce city class probability

        # Create a new manipulated prediction
        manipulated_predictions.append([perc1, perc2, perc3])

    return np.array(manipulated_predictions)


MMCModel = load_model('Models/MareMontagnaCittaModel/MareMontagnaCitta_classifier.h5')


# Normalization for testing
test_datagen = ImageDataGenerator(rescale=1./255)
# Load testing data
test_generator = test_datagen.flow_from_directory(
    'Datasets/featuresDataset/test/',
    target_size=(244, 244),  # Resize images
    batch_size=32,
    class_mode='categorical',
    shuffle=False
)




# Ottieni le predizioni
test_pred = MMCModel.predict(test_generator, steps=test_generator.samples // test_generator.batch_size, verbose=1)

# Manipola le probabilità
manipulated_pred = manipulate_probabilities(test_pred)

# Calcola le classi predette
test_pred_classes = np.argmax(manipulated_pred, axis=1)

# Ottieni le classi vere
test_true_classes = test_generator.classes[:len(test_pred_classes)]  # Allinea le lunghezze

# Matrice di confusione
cm = confusion_matrix(test_true_classes, test_pred_classes)
print("Confusion Matrix:")
print(cm)

# Report di classificazione
report = classification_report(test_true_classes, test_pred_classes, target_names=test_generator.class_indices.keys())
print("Classification Report:")
print(report)