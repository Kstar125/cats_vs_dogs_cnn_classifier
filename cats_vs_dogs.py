# -*- coding: utf-8 -*-

import tensorflow as tf
import keras

from keras import datasets, layers, models, utils

import tensorflow_datasets as tfds
import numpy as np

"""Loading Dataset"""

test_ds, test_dataset_info = tfds.load('cats_vs_dogs', as_supervised=True, with_info=True, shuffle_files=True, split = 'train[70%:100%]')
train_ds, train_dataset_info = tfds.load('cats_vs_dogs', as_supervised=True, with_info=True, shuffle_files=True, split = 'train[:70%]')

print("Train Split Length: {}".format(len(train_ds)))

print("Test Split Length: {}".format(len(test_ds)))
#x_data = list(train_ds)

"""Dataset Info"""

class_names = ['cat', 'dog']

BATCH_SIZE = 126

x_data = []
x_labels = []

for image, label in train_ds:
  #print(image.shape)
  x_data.append(tf.image.resize(image, [200, 200])/255)
  x_labels.append(label)
  #print(resized_images[0].shape)
  #break

x_data = np.array(x_data)
x_labels = np.array(x_labels)

y_data = []
y_labels = []

for image, label in test_ds:
  #print(image.shape)
  y_data.append(tf.image.resize(image, [200, 200])/255)
  y_labels.append(label)
  #break

y_data = np.array(y_data)
y_labels = np.array(y_labels)

  #print(image[0])

"""CNN"""

model = models.Sequential()
model.add(layers.Input(shape = (200, 200, 3))),
model.add(layers.RandomFlip("horizontal_and_vertical")),
model.add(layers.RandomRotation(0.2)),
model.add(layers.Conv2D(32, (3, 3), activation='relu')),
model.add(layers.Conv2D(32, (3, 3), activation='relu')), 
model.add(layers.MaxPooling2D(3, 3)),
model.add(layers.Dropout(0.2)),
model.add(layers.Conv2D(64, (3, 3), activation='relu')), #32
model.add(layers.Conv2D(64, (3, 3), activation='relu')), #New layer 32
model.add(layers.Flatten()),
model.add(keras.layers.BatchNormalization()),
model.add(layers.Dense((16), activation = 'relu')), 
model.add(layers.Dense(2)),
model.add(keras.layers.BatchNormalization()),
model.add(keras.layers.Activation('sigmoid'))

model.summary()

print("Shape of resized_images:", x_data.shape)
print("Shape of x_labels:", x_labels.shape)


print("Shape of resized_images:", y_data.shape)
print("Shape of y_labels:", y_labels.shape)

#model.compile(optimizer=keras.optimizers.Adam(),
#              loss=keras.losses.BinaryCrossentropy(from_logits=True),
#              metrics=[keras.metrics.BinaryAccuracy()])



model.compile(optimizer = 'Adam', loss = 'sparse_categorical_crossentropy', metrics=['accuracy'])


#model.fit(x_data, x_labels, epochs=12, batch_size = BATCH_SIZE)

history = model.fit(x_data, x_labels, epochs=20, batch_size = BATCH_SIZE, validation_split = 0.2)

test_loss, test_acc = model.evaluate(y_data, y_labels)

print("Test Accuracy: {}".format(test_acc))
print("Test Loss: {}".format(test_loss))

