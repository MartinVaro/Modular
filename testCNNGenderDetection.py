# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 16:10:56 2023

@author: akava
"""

import tensorflow as tf
import glob
import numpy as np
import matplotlib.pyplot as plt
import modelGenderDetection as mu


# Función para cargar y preprocesar las imágenes
def load_and_preprocess_image(filepath):
    img = tf.keras.preprocessing.image.load_img(filepath, target_size=(96, 96))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = img_array / 255.0  # Normalizar los valores de píxeles al rango [0, 1]
    return img_array

# Obtener las rutas de las imágenes de prueba
test_photos = glob.glob("faces/predicts/*")

# Crear el modelo
gender_model = mu.create_gender_model()

# Cargar los pesos del modelo entrenado
gender_model.load_weights("gender_model_weights.h5")

# Configurar la visualización de las imágenes y predicciones
rows = 10
cols = 10
num_images = rows * cols
plt.figure(figsize=(2 * 2 * cols, 2 * rows))

for i, photo in enumerate(test_photos[:num_images]):
    img = load_and_preprocess_image(photo)
    img = np.expand_dims(img, axis=0)  # Añadir una dimensión extra para que sea una lista de imágenes
    prediction = gender_model.predict(img)[0][0]

    plt.subplot(rows, 2 * cols, 2 * i + 1)
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(img[0])

    etiqueta_prediccion = 1 if prediction > 0.5 else 0
    etiqueta_real = None  # No tenemos etiquetas reales para las imágenes de prueba
    if etiqueta_prediccion == 1:
        color = 'red'
    else:
        color = 'blue'

    plt.xlabel("Predicción: {} ({:.2f}%)\nReal: {}".format(
        'Mujer' if etiqueta_prediccion == 1 else 'Hombre',
        100 * prediction,
        'Desconocido'),
        color=color)

    plt.subplot(rows, 2 * cols, 2 * i + 2)
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    thisplot = plt.bar(range(1), prediction, color="#777777")
    plt.ylim([0, 1])

    if etiqueta_prediccion == 1:
        thisplot[0].set_color('red')
    else:
        thisplot[0].set_color('blue')

plt.tight_layout()
plt.show()