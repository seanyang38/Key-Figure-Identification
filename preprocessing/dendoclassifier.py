'''This script goes along the blog post
"Building powerful image classification models using very little data"
from blog.keras.io.
It uses data that can be downloaded at:
https://www.kaggle.com/c/dogs-vs-cats/data
In our setup, we:
- created a data/ folder
- created train/ and validation/ subfolders inside data/
- created cats/ and dogs/ subfolders inside train/ and validation/
- put the cat pictures index 0-999 in data/train/cats
- put the cat pictures index 1000-1400 in data/validation/cats
- put the dogs pictures index 12500-13499 in data/train/dogs
- put the dog pictures index 13500-13900 in data/validation/dogs
So that we have 1000 training examples for each class, and 400 validation examples for each class.
In summary, this is our directory structure:
```
data/
    train/
        dogs/
            dog001.jpg
            dog002.jpg
            ...
        cats/
            cat001.jpg
            cat002.jpg
            ...
    validation/
        dogs/
            dog001.jpg
            dog002.jpg
            ...
        cats/
            cat001.jpg
            cat002.jpg
            ...
```
'''
import numpy as np
import os
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from keras import applications



# dimensions of our images.
img_width, img_height = 224, 224

top_model_weights_path = 'bottleneck_fc_model.h5'
train_data_dir = './data/train'
validation_data_dir = './data/val'
eval_data_dir = './data/eval'
nb_train_samples = 1146
nb_validation_samples = 140
nb_eval_samples = 140
epochs = 100
batch_size = 20


def save_bottlebeck_features():
    datagen = ImageDataGenerator(rescale=1. / 255)

    # build the ResNet50 network
    model = applications.ResNet50(include_top=False, weights='imagenet', input_shape=(224,224,3))

    generator = datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode=None,
        shuffle=False)
    bottleneck_features_train = model.predict_generator(
        generator, nb_train_samples // batch_size, verbose=1)

    #print(bottleneck_features_train)

    np.save(open('bottleneck_features_train.npy', 'wb'),
            bottleneck_features_train)

    generator = datagen.flow_from_directory(
        validation_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode=None,
        shuffle=False)
    bottleneck_features_validation = model.predict_generator(
        generator, nb_validation_samples // batch_size, verbose=1)
    np.save(open('bottleneck_features_validation.npy', 'wb'),
            bottleneck_features_validation)
    
    generator = datagen.flow_from_directory(
        eval_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode=None,
        shuffle=False)
    bottleneck_features_eval = model.predict_generator(
        generator, nb_eval_samples // batch_size)
    np.save(open('bottleneck_features_eval.npy', 'wb'),
            bottleneck_features_eval)


def train_top_model():
    train_data = np.load(open('bottleneck_features_train.npy'))
    train_labels = np.array(
        [0] * (nb_train_samples / 2) + [1] * (nb_train_samples / 2))

    validation_data = np.load(open('bottleneck_features_validation.npy'))
    validation_labels = np.array(
        [0] * (nb_validation_samples / 2) + [1] * (nb_validation_samples / 2))

    model = Sequential()
    model.add(Flatten(input_shape=train_data.shape[1:]))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='rmsprop',
                  loss='binary_crossentropy', metrics=['accuracy'])

    model.fit(train_data, train_labels,
              epochs=epochs,
              batch_size=batch_size,
              validation_data=(validation_data, validation_labels)
              )
    model.save_weights(top_model_weights_path)


def evaluate_model():
    eval_data = np.load(open('bottleneck_features_eval.npy'))
    eval_labels = np.array(
        [0] * (nb_eval_samples / 2) + [1] * (nb_eval_samples / 2))

    model = Sequential()
    model.add(Flatten(input_shape=eval_data.shape[1:]))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='rmsprop',
                  loss='binary_crossentropy', metrics=['accuracy'])
    
    model.load_weights(top_model_weights_path)

    
    model.evaluate(eval_data, eval_labels,
                   batch_size=batch_size)



os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
#save_bottlebeck_features()
#train_top_model()
evaluate_model()
