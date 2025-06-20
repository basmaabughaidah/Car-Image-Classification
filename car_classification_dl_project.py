# -*- coding: utf-8 -*-
"""Car_Classification_DL_Project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1sNi4oPxvjsC6gEC1VK-1DWlXL_zWgjax
"""

from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/drive/MyDrive/deep_project/dataset

# Commented out IPython magic to ensure Python compatibility.
# %ls

from zipfile import ZipFile
import os

def get_all_file_paths(directory):

    # initializing empty file paths list
    file_paths = []

    # crawling through directory and subdirectories
    for root, directories, files in os.walk(directory):
        for filename in files:
            # join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

    # returning all file paths
    return file_paths

def main():
    # path to folder which needs to be zipped
    directory = '/content/drive/MyDrive/car-calssification/data.zip'

    # calling function to get all file paths in the directory
    file_paths = get_all_file_paths(directory)

    # printing the list of all files to be zipped
    #print('Following files will be zipped:')
    for file_name in file_paths:
        print(file_name)

    # writing files to a zipfile
    with ZipFile('data.zip','w') as zip:
        # writing each file one by one
        for file in file_paths:
            zip.write(file)

    print('All files zipped successfully!')


if __name__ == "__main__":
    main()

import shutil
shutil.make_archive('/content/drive/MyDrive/deep_project/dataset/data', 'zip', '/content/drive/MyDrive/deep_project/dataset')

# Commented out IPython magic to ensure Python compatibility.
# %cd DATA

# import the necessary packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow
import seaborn as sns
import pickle
import os
import glob as gb
import random
import cv2
from PIL import Image
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.preprocessing import image_dataset_from_directory
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras.utils import to_categorical
from keras.models import Sequential, Model
from tensorflow.keras.utils import get_file
from tensorflow.keras.layers import Conv2D, AveragePooling2D
from keras.layers import MaxPooling2D, Flatten, Dense, Dropout,Input, Add, Activation, ZeroPadding2D, BatchNormalization, AveragePooling2D, GlobalAveragePooling2D, GlobalMaxPooling2D

# Reading CSV File
df = pd.read_csv('/content/drive/MyDrive/deep_project/dataset/number_of_samples.csv')
df

# Number of Cars images per class
plt.figure(figsize=(20,5))
sns.barplot(y = df["Number of files"], x = df["Name of class"], palette = "inferno")
plt.title("Number of Cars images per class")
plt.show()

# Reading image dataset
dataset = '/content/drive/MyDrive/deep_project/dataset/DATA'

# Name of each directory
data = os.listdir(dataset)
data

# Generate random sample with title of class to visualise
plt.figure(figsize=(20, 20))
for i in range(10):
    px = plt.subplot(5, 5, i + 1)
    rand = random.randrange(1, 30)
    current_dir = os.listdir(dataset+'/'+str(data[i]))
    img = cv2.imread(dataset+'/'+str(data[i])+'/'+current_dir[rand])
    plt.imshow(img )
    plt.title(data[i])
    plt.axis("off")

plt.show()

# image size
img_path = r'/content/drive/MyDrive/deep_project/dataset/DATA/bmw serie 1/back1.jpg'
img = plt.imread(img_path)
print ('Input image shape is ',img.shape)
plt.axis('off')
imshow(img)

"""**2222 Data Pipeline**


"""

# Create an empty list to store the labels
labels = []

# Define the path to the image directory
image_dir = '/content/drive/MyDrive/deep_project/dataset/DATA'

# Get a list of all subdirectories in the image directory
folders = [f for f in os.listdir(image_dir) if os.path.isdir(os.path.join(image_dir, f))]

# Iterate through the subdirectories
for folder in folders:
    # Get the name of the folder
    label = folder
    # Append the label to the labels list
    labels.append(label)

# Create lists to store the filenames and labels
filenames = []
labels = []

# Define the path to the image directory
image_dir = '/content/drive/MyDrive/deep_project/dataset/DATA'

# Get a list of all subdirectories in the image directory
folders = [f for f in os.listdir(image_dir) if os.path.isdir(os.path.join(image_dir, f))]

# Iterate through the subdirectories
for folder in folders:
    # Get the name of the folder (label)
    label = folder
    # Get a list of all files in the subdirectory
    folder_path = os.path.join(image_dir, folder)
    files = os.listdir(folder_path)
    # Iterate through the files
    for file in files:
        # Get the full path of the file
        file_path = os.path.join(folder_path, file)
        # Append the file path and label to the lists
        filenames.append(file_path)
        labels.append(label)

# Create a dataframe with the filenames and labels
df = pd.DataFrame({'filename': filenames, 'label': labels})

# Shuffle the dataframe
df = df.sample(frac=1).reset_index(drop=True)

# Create empty lists to store the images and labels
X = []
y = []

# Load the images
for i, row in df.iterrows():
    # Open the image
    img = Image.open(row['filename'])
    # Resize the image
    img = img.resize((224, 224))
    # Convert the image to an array
    img_array = np.array(img)
    # Append the image to the images list
    X.append(img_array)
    # Append the label to the labels list
    y.append(row['label'])

# save the images and labels to a pickle file
file_x = open('/content/drive/MyDrive/deep_project/dataset/DATA/X.pickle', 'wb')
pickle.dump(X, file_x)
file_x.close()

file_y = open('/content/drive/MyDrive/deep_project/dataset/DATA/y.pickle', 'wb')
pickle.dump(y, file_y)
file_y.close()

X = pickle.load(open('/content/drive/MyDrive/deep_project/dataset/DATA/X.pickle', 'rb'))
y = pickle.load(open('/content/drive/MyDrive/deep_project/dataset/DATA/y.pickle', 'rb'))

# labe encoding the labels
encoder = LabelEncoder()
y = encoder.fit_transform(y)

# One-hot encode the labels
y = to_categorical(y, num_classes=20)

# Reshape the X array
X = np.reshape(X, (len(X), 224, 224, 3))

"""training and testing data"""

# split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# numbers of each part
print(X_train.shape)
print(y_train.shape)
print(X_test.shape)
print(y_test.shape)

"""Data augmentation"""

# Create an ImageDataGenerator
datagen = ImageDataGenerator(
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest')

# Create the model
model = Sequential()

# Add convolutional layers
model.add(Conv2D(64, (3, 3), activation='relu', input_shape=(224, 224, 3)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
#model.add(Dropout(0.25))

model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
#model.add(Dropout(0.25))

model.add(Conv2D(256, (3, 3), activation='relu'))
model.add(Conv2D(256, (3, 3), activation='relu'))
model.add(Conv2D(256, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
#model.add(Dropout(0.25))

model.add(Conv2D(512, (3, 3), activation='relu'))
model.add(Conv2D(512, (3, 3), activation='relu'))
model.add(Conv2D(512, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
#model.add(Dropout(0.25))

model.add(Conv2D(512, (3, 3), activation='relu'))
model.add(Conv2D(512, (3, 3), activation='relu'))
model.add(Conv2D(512, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Dropout(0.25))

# Add fully connected layers
model.add(Flatten())
model.add(Dense(4096, activation='relu'))
#model.add(Dropout(0.5))
model.add(Dense(4096, activation='relu'))
#model.add(Dropout(0.3))
# output layer
model.add(Dense(20, activation='softmax'))

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Model summary
model.summary()

model = Sequential()

model.add(Conv2D(32, (3, 3),input_shape=(224, 224, 3),strides = (1,1),  padding = 'same', activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
#model.add(AvgPool2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3),strides = (1,1),  padding = 'same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3),strides = (1,1),  padding = 'same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3),strides = (1,1),  padding = 'same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(units=128, activation='relu'))
model.add(Dense(units=20, activation='softmax'))

model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
model.summary()

# Fit the model on the batches generated by datagen.flow()
model.fit(datagen.flow(X_train, y_train, batch_size=64),
          steps_per_epoch=len(X_train) / 64, epochs=50,
          workers=-1,use_multiprocessing=True,
          validation_data = (X_test, y_test))

model.fit(X_train, y_train,
          epochs = 100, batch_size = 32,
          verbose=1,
          validation_data = (X_test, y_test))

scores = model.evaluate(test_generator)

# Use the generator to create augmented images
for x_batch, y_batch in datagen.flow(X_train, y_train, batch_size=32):
    # Use the augmented images for training
    model.fit(x_batch, y_batch)
    # Break the loop when the generator runs out of images
    if len(X_train) == 0:
        break

height=224
width=224
channels=3
seed=1337
batch_size = 64


# Training generator
train_datagen = ImageDataGenerator(rescale=1./255,rotation_range=40,width_shift_range=0.2,height_shift_range=0.2,
                                   shear_range=0.2,zoom_range=0.2,horizontal_flip=True,fill_mode='nearest')
train_generator = train_datagen.flow_from_directory(dataset, target_size=(height,width),batch_size=batch_size,
                                                    seed=seed,shuffle=True,class_mode='categorical')

# Testing generator
test_datagen = ImageDataGenerator(rescale=1./255)
test_generator = test_datagen.flow_from_directory(dataset,target_size=(height,width), batch_size=batch_size,
                                                  seed=seed,shuffle=True,class_mode='categorical')

training = image_dataset_from_directory(dataset,validation_split=0.2,subset='training',labels='inferred',label_mode='categorical',
    image_size=[224, 224],seed=123,interpolation='nearest',batch_size=64,shuffle=True,)

testing = image_dataset_from_directory(dataset,validation_split=0.2,subset='validation',labels='inferred',label_mode='categorical',
    image_size=[224, 224],seed=123,interpolation='nearest',batch_size=64,shuffle=False,)

def convert_to_float(image, label):
    image = tf.image.convert_image_dtype(image, dtype= tf.float32)
    return image, label

AUTOTUNE = tf.data.experimental.AUTOTUNE
data_train = (training.map(convert_to_float).cache().prefetch(buffer_size=AUTOTUNE))

data_test = (testing.map(convert_to_float).cache().prefetch(buffer_size=AUTOTUNE))

data_train

train_num = train_generator.samples
test_num = test_generator.samples

