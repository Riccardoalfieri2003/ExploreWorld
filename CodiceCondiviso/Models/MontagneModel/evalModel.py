from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import confusion_matrix, classification_report
import numpy as np

#from TimeModel.TgetClassPrediction import TimeGetClassPrediction


def manipulate_probabilities(predictions, threshold=0.3):
    manipulated_predictions = []
    for pred in predictions:
        # Apply the threshold logic
        if pred[0] > threshold:
            manipulated_predictions.append(1)  # Class 1 (positive)
        else:
            manipulated_predictions.append(0)  # Class 0 (negative)
    return np.array(manipulated_predictions)


PhotoOrNotModel = load_model('Models/MontagneModel/Montagne_classifier.h5')

# Normalization for testing
test_datagen = ImageDataGenerator(rescale=1./255)
# Load testing data
test_generator = test_datagen.flow_from_directory(
    'Datasets/MontagneDataset/test/',
    target_size=(244, 244),  # Resize images
    batch_size=32,
    class_mode='binary',
    shuffle=False
)




# Ottieni le predizioni
test_pred = PhotoOrNotModel.predict(test_generator, steps=test_generator.samples // test_generator.batch_size, verbose=1)

# Calcola le classi predette
#test_pred_classes = (test_pred > 0.5).astype(int).flatten()

test_pred_classes = manipulate_probabilities(test_pred)

# Get true classes
#test_true_classes = test_generator.classes[:len(test_pred_classes)]  # Align lengths


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