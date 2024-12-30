from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import confusion_matrix, classification_report
import numpy as np

#from TimeModel.TgetClassPrediction import TimeGetClassPrediction


def proportionate(num1, num2, num3, num4):
    numSum = num1 + num2 + num3
    perc1 = num1 / numSum
    perc2 = num2 / numSum
    perc3 = num3 / numSum
    perc4 = num4 / numSum
    return perc1, perc2, perc3, perc4

def manipulate_probabilities(predictions):
    for i in range(len(predictions)):
        # Applica la proporzione
        predictions[i] = proportionate(predictions[i][0], predictions[i][1], predictions[i][2], predictions[i][3])
        
        # Controllo aggiuntivo per classi
        if np.argmax(predictions[i]) == 1 and predictions[i][0] * 5 >= predictions[i][1]:
            predictions[i][1] = 0  # Forza la probabilità della classe 1 a 0
        predictions[i] = np.array(predictions[i])  # Riconverti in array
    return predictions



PhotoOrNotModel = load_model('Models/PhotoOrNotModel/PhotoOrNot_classifier.h5')


# Normalization for testing
test_datagen = ImageDataGenerator(rescale=1./255)
# Load testing data
test_generator = test_datagen.flow_from_directory(
    'Datasets/PhotoOrNotDataset/test/',
    target_size=(244, 244),  # Resize images
    batch_size=32,
    class_mode='categorical',
    shuffle=False
)




# Ottieni le predizioni
test_pred = PhotoOrNotModel.predict(test_generator, steps=test_generator.samples // test_generator.batch_size, verbose=1)

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