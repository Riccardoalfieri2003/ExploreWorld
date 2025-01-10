from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import confusion_matrix, classification_report
import numpy as np

#from TimeModel.TgetClassPrediction import TimeGetClassPrediction

#TimeModel = load_model('Models/TimeModel/DaySunsetNight_classifier.h5')
TimeModel = load_model('Models/TimeModel/Time_classifier.h5')


# Normalization for testing
test_datagen = ImageDataGenerator(rescale=1./255)
# Load testing data
test_generator = test_datagen.flow_from_directory(
    'Datasets/TimeDataset2/test/',
    target_size=(244, 244),  # Resize images
    batch_size=32,
    class_mode='categorical',
    shuffle=False
)

# Get the predictions for the test set
test_pred = TimeModel.predict(test_generator, steps=test_generator.samples // test_generator.batch_size, verbose=1)
test_pred_classes = np.argmax(test_pred, axis=1)  # Convert predictions to class labels

# Get the true labels from the test generator
test_true_classes = test_generator.classes

# Ensure both arrays have the same length by trimming or padding
test_true_classes = test_true_classes[:len(test_pred_classes)]

# Confusion Matrix
cm = confusion_matrix(test_true_classes, test_pred_classes)
print("Confusion Matrix:")
print(cm)

# Classification Report (Precision, Recall, F1-Score)
report = classification_report(test_true_classes, test_pred_classes, target_names=test_generator.class_indices.keys())
print("Classification Report:")
print(report)