from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.optimizers import Adam
from sklearn.metrics import confusion_matrix, classification_report
import numpy as np

# Data augmentation for training
train_datagen = ImageDataGenerator(
    rescale=1./255,  # Normalize pixel values
    rotation_range=40,  # Random rotations
    width_shift_range=0.2,  # Random horizontal shifts
    height_shift_range=0.2,  # Random vertical shifts
    shear_range=0.2,  # Random shearing
    zoom_range=0.2,  # Random zoom
    horizontal_flip=True,  # Random horizontal flip
    fill_mode='nearest'  # Fill pixels after transformation
)

# Normalization for testing
test_datagen = ImageDataGenerator(rescale=1./255)

"""
# Load training data
train_generator = train_datagen.flow_from_directory(
    'Datasets/PhotoOrNotDataset2/train/',
    target_size=(244, 244),  # Resize images
    batch_size=32,
    class_mode='categorical',  # Multi-class classification
    shuffle=True
)

# Load testing data
test_generator = test_datagen.flow_from_directory(
    'Datasets/PhotoOrNotDataset2/test/',
    target_size=(244, 244),  # Resize images
    batch_size=32,
    class_mode='categorical',
    shuffle=False
)

#CNN

model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(244, 244, 3)),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    #Dense(4, activation='softmax')  # 6 classi: foto vere, disegni bianco e nero, disegnia  colori,  illustrazioni, mappe e charts
])

model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss='categorical_crossentropy',  # For multi-class classification
    metrics=['accuracy']
)"""


# Load training data
train_generator = train_datagen.flow_from_directory(
    'Datasets/PhotoOrNotDataset2/train/',
    target_size=(244, 244),  # Resize images
    batch_size=32,
    class_mode='binary',  # Multi-class classification
    shuffle=True
)

# Load testing data
test_generator = test_datagen.flow_from_directory(
    'Datasets/PhotoOrNotDataset2/test/',
    target_size=(244, 244),  # Resize images
    batch_size=32,
    class_mode='binary',
    shuffle=False
)


model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(244, 244, 3)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(1, activation='sigmoid')  # Output binario (0 o 1)
])


model.compile(
    optimizer='adam',
    loss='binary_crossentropy',  # Per classificazione binaria
    metrics=['accuracy']
)

history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // train_generator.batch_size,
    validation_data=test_generator,
    validation_steps=test_generator.samples // test_generator.batch_size,
    epochs=10  # Adjust based on your dataset and training time
)

model.save('photoOrNot2_classifier.h5')