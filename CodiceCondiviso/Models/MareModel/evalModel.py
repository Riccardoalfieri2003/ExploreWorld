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


PhotoOrNotModel = load_model('Models/MareModel/Mare_classifier.h5')

# Normalization for testing
test_datagen = ImageDataGenerator(rescale=1./255)
# Load testing data
test_generator = test_datagen.flow_from_directory(
    'Datasets/MareDataset/test/',
    target_size=(244, 244),  # Resize images
    batch_size=32,
    class_mode='binary',
    shuffle=False
)




# Ottieni le predizioni
test_pred = PhotoOrNotModel.predict(test_generator, steps=test_generator.samples // test_generator.batch_size, verbose=1)

# Calcola le classi predette
test_pred_classes = (test_pred > 0.5).astype(int).flatten()

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