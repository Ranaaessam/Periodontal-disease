# -*- coding: utf-8 -*-
"""Periodontal_ModelVGG19.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Qx4PJxPXJEn9H8RJ18sZF0t9SlLAQryt
"""

# -*- coding: utf-8 -*-
"""VGG_GP.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KPHjt6bzNjQKH7QWWAjc5X_dlqL1h9Kc
"""

import os
import numpy as np
import cv2
from keras.layers import Input, Conv2D, Activation, MaxPool2D, Dense, Dropout, Flatten, BatchNormalization
from keras.models import Sequential, Model
import matplotlib
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import itertools
from sklearn.model_selection  import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn import preprocessing
import keras,os
import numpy as np
import tensorflow as tf
import pandas as pd
import matplotlib, cv2
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import itertools
from keras.applications.vgg19 import VGG19
from keras.applications.densenet import DenseNet121
from keras.applications.inception_resnet_v2 import InceptionResNetV2
from keras.applications.inception_resnet_v2 import preprocess_input, decode_predictions
from keras.applications.vgg16 import VGG16
from tensorflow import keras
from tensorflow.keras.utils import plot_model,to_categorical
from tensorflow.keras.layers import Input, Conv2D, Activation, MaxPool2D, Dense, Dropout, Flatten, BatchNormalization, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam,RMSprop
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.callbacks import EarlyStopping,ReduceLROnPlateau
from tensorflow.keras.metrics import categorical_crossentropy
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img, array_to_img
from sklearn.metrics import classification_report,confusion_matrix,accuracy_score
from  matplotlib import pyplot as plt

from tensorflow.keras.layers import Input, Conv2D, BatchNormalization, Dense
from tensorflow.keras.layers import AvgPool2D, GlobalAveragePooling2D, MaxPool2D
from tensorflow.keras.models import Model
from tensorflow.keras.layers import ReLU, concatenate
import tensorflow.keras.backend as K
from keras.layers import GlobalMaxPooling2D
from keras.datasets import mnist
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout

from google.colab import drive
drive.mount('/content/drive')
#Dataset Path
image_dir ='/content/drive/MyDrive/IDental/Dataset/drivetest'
non_periodontal_path = '/content/drive/MyDrive/IDental/Dataset/drivetest/Non-periodontal'
periodontal_path ='/content/drive/MyDrive/IDental/Dataset/drivetest/Periodontal'
unrecogonized_path ='/content/drive/MyDrive/IDental/Dataset/drivetest/unrecognized'
base_path ='/content/drive/MyDrive/VGG_weights'

image_list=[]
label_list=[]

size = 224,224 #image size
batch_size = 25
epochs=40

def get_path(image_dir):
  element_path = os.listdir(image_dir)
  allpics = list()
  for element in element_path:
    fullpath = os.path.join(image_dir, element)
    if os.path.isdir(fullpath):
      allpics = allpics + get_path(fullpath)
    else:
      allpics.append(fullpath)
  return allpics

files = get_path(image_dir)

#cleaning the two lists
image_list.clear()
label_list.clear()


def load_pics():
    for file in get_path(image_dir):
        img = load_image(file)
        if img is not None:
            image_list.append(img)
            label_list.append(os.path.basename(os.path.dirname(file)))
        else:
            continue
    return image_list,label_list

def load_image(file) :
    try:
        img = cv2.imread(file)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img,size)
        return img
    except:
        return None

imageList,labelList = load_pics()


def overview(total_rows):
        fig = plt.figure(figsize=(10,10))
        idx = 0
        while idx < total_rows:
            ax = fig.add_subplot(10,10,idx+1)
            ax.imshow(image_list[idx], cmap=plt.cm.get_cmap('gray'))
            plt.xticks(np.array([]))
            plt.yticks(np.array([]))
            plt.tight_layout()
            idx += 1
        plt.show()

overview(20)
# Getting the Classes Numbers
def getClassesNum():
    classes=set(label_list)
    return classes.__len__()

c = getClassesNum()

print("classes number")
print(c)
'''######################## Encoding images classes labels ########################'''

def categorizeLables(label_list):

    le = preprocessing.LabelEncoder()
    encoding = le.fit_transform(label_list)
    le_name_mapping = dict(zip(le.classes_, le.transform(le.classes_))) #mapping between classes and numbers
    print(le_name_mapping)
    return encoding

'''######################## Loading the dataset ########################'''
def split_dataset():
    imgs = np.asarray(image_list)


    lbls = categorizeLables(label_list) # Zeros and Ones
    lbls = np.asarray(lbls) # Converting list to array
    lbls = to_categorical(lbls, num_classes=getClassesNum())

    x_train, x_test, y_train, y_test = train_test_split(imgs, lbls, test_size=0.3, random_state=0)
    x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.2, random_state=0)

    return x_train, x_val, x_test, y_train, y_val, y_test, lbls

x_train, x_val, x_test, y_train, y_val, y_test, lbls = split_dataset()


# print('labels',len(y_train))
print(len(y_train))
print(len(y_test))
print('length labels',len(lbls))
# print(lbls)

print(len(image_list))
print(len(label_list))
# print(len(files))

#MODELS


def construct_model(type):
    if type == 'CNN':
      print('CNN not implemented')
      # Creating Densenet121
    elif type == 'DenseNet121':


        base_model = DenseNet121(include_top=False)
        print('----------------------------- ',len(base_model.layers),'---------------------------')
        x = base_model.output
        x = GlobalMaxPooling2D()(x)
        x = Dense(1024, activation='relu')(x)
        predictions = Dense(getClassesNum(), activation='softmax')(x)
        model = Model(inputs=base_model.input, outputs=predictions)
        for layer in base_model.layers[0:425]:
            layer.trainable = False
        for layer in base_model.layers[425:]:
            layer.trainable = True
       #Creating VGG19
    elif type == 'VGG19':

      from keras.layers import GlobalMaxPooling2D

      base_model = VGG19(include_top=False,input_shape = (224,224,3))
      print('----------------------------- ',len(base_model.layers),'---------------------------')
      x = base_model.output
      x = GlobalMaxPooling2D()(x)
      x = Dense(1024, activation='relu')(x)
      predictions = Dense(getClassesNum(), activation='softmax')(x)
      model = Model(inputs=base_model.input, outputs=predictions)
      for layer in base_model.layers[0:20]:
        layer.trainable = False
      for layer in base_model.layers[20:]:
        layer.trainable = True


    model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
    model.summary()


    return model


# model = construct_model('DenseNet121')
model = construct_model('VGG19')

def init_callbacks():
    from keras.callbacks import CSVLogger, ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
    #weights folder
    trained_models_path = base_path + 'model_weights'
    #h5 file type contain (epochs , loss , accuracy)
    model_names = trained_models_path + '.{epoch:04d}--{val_loss:.4f}--{val_accuracy:.4f}.h5'
    #verbos how progess is vosualized in h file (Training progress) ,  choose the best epoch
    model_checkpoint = ModelCheckpoint(model_names, monitor = 'val_accuracy', verbose=1,save_best_only=True)
    callbacks = [model_checkpoint]
    return callbacks

def plot_history(history):
  #store data history , loss , acc
    loss_list = [s for s in history.history.keys() if 'loss' in s and 'val' not in s]
    val_loss_list = [s for s in history.history.keys() if 'loss' in s and 'val' in s]
    acc_list = [s for s in history.history.keys() if 'acc' in s and 'val' not in s]
    val_acc_list = [s for s in history.history.keys() if 'acc' in s and 'val' in s]

    if len(loss_list) == 0:
        print('Loss is missing in history')
        return

            ## As loss always exists
    epochs = range(1, len(history.history[loss_list[0]]) + 1)

        ## Loss
    plt.figure(1)
    for l in loss_list:
        plt.plot(epochs, history.history[l], 'b',
                     label='Training loss (' + str(str(format(history.history[l][-1], '.5f')) + ')'))
    for l in val_loss_list:
        plt.plot(epochs, history.history[l], 'g',
                     label='Validation loss (' + str(str(format(history.history[l][-1], '.5f')) + ')'))

    plt.title('Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    # all elements by default
    plt.legend()

        ## Accuracy
    plt.figure(2)
    for l in acc_list:
        plt.plot(epochs, history.history[l], 'b',
                    label='Training accuracy (' + str(format(history.history[l][-1], '.5f')) + ')')
    for l in val_acc_list:
        plt.plot(epochs, history.history[l], 'g',
                     label='Validation accuracy (' + str(format(history.history[l][-1], '.5f')) + ')')

    plt.title('Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.show()

from keras.preprocessing.image import ImageDataGenerator
  train_datagen = ImageDataGenerator(featurewise_center=False, samplewise_center=False, featurewise_std_normalization=False,
        samplewise_std_normalization=False, zca_whitening=False, rotation_range=10, zoom_range = 0.1, width_shift_range=0.1,
        height_shift_range=0.1, horizontal_flip=False, vertical_flip=False)
  #Model Training
  history = model.fit(train_datagen.flow(x_train, y_train, batch_size),  steps_per_epoch=len(x_train) / batch_size,  epochs=25, verbose=1, callbacks= init_callbacks(), validation_data=(x_val, y_val))
  test_loss,test_acc= model.evaluate(x_test, y_test)
  print("\nTest accuracy: ",test_acc)
  print("\nTest loss: ",test_loss)

  plot_history(history)
  plot_model
  saved_model_dir = ''
  tf.saved_model.save(model, saved_model_dir)
   #constructing tflite file
  converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
  tflite_model = converter.convert()

  with open('modelFinaal.tflite', 'wb') as f:
   f.write(tflite_model)

def load_image(file) :
    try:
        img = cv2.imread(file)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img,size)
        train_images = np.zeros((x_train,size,size,3), dtype='uint8')
        train_labels = np.zeros((x_train,1), dtype='uint8')

        test_images = np.zeros((x_test, size, size, size,3),dtype='uint8')
        test_labels = np.zeros((x_test,  1),dtype='uint8')

        for i in range(x_train):
          if i % 2 == 0:
            original_image = cv2.imread(periodontal_path +"periodontal-"+str(i+1)+".png")
            train_images[i] = 1
          else:
            original_image = cv2.imread(non_periodontal_path +"Non-periodontal-"+str(i+1)+".png")
            train_labels[i] = 0
          resized_image = cv2.resize(original_image,(size,size))
          train_images[i] = resized_image

        for i in range(x_test):
          if i % 2 == 0:
            original_image = cv2.imread(periodontal_path + "periodontal-"+str(i + 1 + x_train)+".png")
            test_labels[i] = 1
          else:
            original_image = cv2.imread(non_periodontal_path  + "Normal-" + str(i + 1 + x_train) + ".png")
            test_labels[i] = 0
          resized_image = cv2.resize(original_image, (size, size))
          test_images[i] = resized_image

        return img
    except:
        return None

import cv2
from google.colab.patches import cv2_imshow


def classify_teeth():

    image = tf.keras.preprocessing.image.load_img("/content/drive/MyDrive/IDental/Periodontal_dataset/penyakit-non-periodontal/non_periodontal_15.png", target_size=(224, 224))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])  # Convert single image to a batch.

    predictions = model.predict(input_arr)


    prediction = model.predict(input_arr)
    print(prediction)
    max_pred = tf.argmax(prediction,axis=1)
    print('sum test: ',sum(sum(prediction)))
    print('max pred',max_pred)
    return np.argmax(model.predict(input_arr), axis=-1)


cls = classify_teeth()
if cls == 0:
  print("The patient is healthy!!",cls)
elif cls == 1:
  print("unfortunately the patient have Periodontitis!",cls)
else:
  print("Try again")