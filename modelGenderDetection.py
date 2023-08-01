# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 15:34:06 2023

@author: akava
"""

import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization

def create_gender_model(input_shape=(96, 96, 3)):
    # Definir la arquitectura del modelo
    inputs = Input(shape=input_shape)

    # Capas convolucionales y de MaxPooling con Dropout
    x = Conv2D(32, (3, 3), activation='relu')(inputs)
    x = BatchNormalization()(x)
    x = MaxPooling2D((3, 3))(x)
    x = Dropout(0.25)(x)

    x = Conv2D(64, (3, 3), activation='relu')(x)
    x = BatchNormalization()(x)
    x = MaxPooling2D((2, 2))(x)
    x = Dropout(0.25)(x)

    x = Conv2D(64, (3, 3), activation='relu')(x)
    x = BatchNormalization()(x)
    x = MaxPooling2D((2, 2))(x)
    x = Dropout(0.25)(x)

    x = Conv2D(128, (3, 3), activation='relu')(x)
    x = BatchNormalization()(x)
    x = MaxPooling2D((2, 2))(x)
    x = Dropout(0.25)(x)

    # Capa de aplanado (Flatten)
    x = Flatten()(x)

    # Capa Fully Connected con ReLU y Dropout
    x = Dense(1024, activation='relu')(x)
    x = Dropout(0.5)(x)

    # Capa de salida con Sigmoid
    outputs = Dense(1, activation='sigmoid')(x)

    # Crear el modelo
    model = Model(inputs=inputs, outputs=outputs)

    # Compilar el modelo
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    return model