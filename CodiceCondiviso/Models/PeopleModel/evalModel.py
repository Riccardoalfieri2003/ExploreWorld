from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import confusion_matrix, classification_report
import numpy as np


def manipulate_probabilities(predictions, threshold=0.4):
    manipulated_predictions = []
    for pred in predictions:
        # Apply the threshold logic
        if pred[0] > threshold:
            manipulated_predictions.append(1)  # Class 1 (positive)
        else:
            manipulated_predictions.append(0)  # Class 0 (negative)
    return np.array(manipulated_predictions)

PeopleModel = load_model('Models/PeopleModel/People_classifier.h5')


# Normalization for testing
test_datagen = ImageDataGenerator(rescale=1./255)
# Load testing data
test_generator = test_datagen.flow_from_directory(
    'Datasets/PeopleDataset/test/',
    target_size=(244, 244),  # Resize images
    batch_size=32,
    class_mode='binary',
    shuffle=False
)


# Get predictions
test_pred = PeopleModel.predict(test_generator, steps=test_generator.samples // test_generator.batch_size, verbose=1)
#print(test_pred*10)
# Manipulate predictions using the custom logic
test_pred_classes = manipulate_probabilities(test_pred)

# Get true classes
test_true_classes = test_generator.classes[:len(test_pred_classes)]  # Align lengths

# Confusion Matrix
cm = confusion_matrix(test_true_classes, test_pred_classes)
print("Confusion Matrix:")
print(cm)

# Classification Report
report = classification_report(test_true_classes, test_pred_classes, target_names=['No people', 'People'])
print("Classification Report:")
print(report)
