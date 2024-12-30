import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten
from keras.preprocessing.image import ImageDataGenerator


# Data augmentation per il training
train_datagen = ImageDataGenerator(
    rescale=1.0/255,  # Normalizza i valori dei pixel tra 0 e 1
    rotation_range=10,  # Rotazioni casuali
    width_shift_range=0.2,  # Traslazioni orizzontali
    height_shift_range=0.2,  # Traslazioni verticali
    shear_range=0.2,  # Trasformazioni angolari
    zoom_range=(0.5,1.2),  # Zoom casuale
    horizontal_flip=True,  # Ribaltamenti orizzontali
    brightness_range=[0.3, 1.5]  # Random brightness adjustment between 0.5 and 1.5 times the original brightness
)


# Solo rescaling per il test
test_datagen = ImageDataGenerator(rescale=1.0/255)

# Caricamento delle immagini
train_generator = train_datagen.flow_from_directory(
    "Datasets/PeopleDataset/train",
    target_size=(244, 244),  # Dimensioni uniformi per le immagini
    batch_size=16,
    class_mode='binary'  # Classificazione binaria
)

test_generator = test_datagen.flow_from_directory(
    #"PeopleDataset/test",
    "Datasets/PeopleDataset/test",
    target_size=(244, 244),
    batch_size=32,
    class_mode='binary'
)

print("Class indices:", train_generator.class_indices)
print("Class indices:", test_generator.class_indices)


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
    epochs=20,  # Puoi regolare il numero di epoche
    validation_data=test_generator
)

model.save('PeopleOrNot2_classifier.h5')


#persone in posizioni strane, parzialmente ricoperte OPPURE cose che possono ricordare umani, dovuto a causa della compressione delle immagini