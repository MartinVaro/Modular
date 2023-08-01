# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 15:45:41 2023

@author: akava
"""

import modelGenderDetection as mu
import glob
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split

# Función para cargar y preprocesar las imágenes
def load_and_preprocess_image(filepath):
    img = tf.keras.preprocessing.image.load_img(filepath, target_size=(96, 96))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = img_array / 255.0  # Normalizar los valores de píxeles al rango [0, 1]
    return img_array

# Crear DataFrame con las rutas de las imágenes y las etiquetas (género)
men = glob.glob("faces/man/*")
women = glob.glob("faces/woman/*")

men_df = pd.DataFrame({'filepath': men, 'gender': 0})
women_df = pd.DataFrame({'filepath': women, 'gender': 1})

df_raw = pd.concat([men_df, women_df], ignore_index=True)

# Preprocesar las imágenes y añadir al DataFrame
df_raw['image_data'] = df_raw['filepath'].apply(load_and_preprocess_image)

# Dividir los datos en conjuntos de entrenamiento y prueba (80% para entrenamiento, 20% para prueba)
train_df, test_df = train_test_split(df_raw, test_size=0.1, random_state=42)

# Crear generadores de datos
batch_size = 32

train_generator = tf.data.Dataset.from_tensor_slices((train_df['image_data'].to_list(), train_df['gender'].to_numpy()))
train_generator = train_generator.batch(batch_size)

test_generator = tf.data.Dataset.from_tensor_slices((test_df['image_data'].to_list(), test_df['gender'].to_numpy()))
test_generator = test_generator.batch(batch_size)

# Función para entrenar el modelo y guardar los pesos
def train_and_save_model(model, train_generator, test_generator, epochs, save_path):

    history = model.fit(train_generator, epochs=epochs, validation_data=test_generator)
    model.save_weights(save_path)
    return history

# Crear el modelo
gender_model = mu.create_gender_model()



# Cargar los pesos preentrenados
weights_save_path = "gender_model_weights.h5"
gender_model.load_weights(weights_save_path)



# Especificar el número de épocas y el path para guardar los pesos
epochs = 200
weights_save_path = "gender_model_weights.h5"

# Entrenar el modelo y guardar los pesos
history = train_and_save_model(gender_model, train_generator, test_generator, epochs, weights_save_path)


import matplotlib.pyplot as plt

# Función para graficar las métricas de entrenamiento
def plot_training_metrics(history):
    # Obtener las métricas de entrenamiento
    training_loss = history.history['loss']
    training_accuracy = history.history['accuracy']

    # Obtener las métricas de validación (prueba)
    validation_loss = history.history['val_loss']
    validation_accuracy = history.history['val_accuracy']

    # Graficar la pérdida
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(training_loss, label='Training Loss')
    plt.plot(validation_loss, label='Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()

    # Graficar la precisión (accuracy)
    plt.subplot(1, 2, 2)
    plt.plot(training_accuracy, label='Training Accuracy')
    plt.plot(validation_accuracy, label='Validation Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()

    plt.tight_layout()
    plt.show()

# Graficar las métricas de entrenamiento
plot_training_metrics(history)