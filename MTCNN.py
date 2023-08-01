# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 13:56:08 2023

@author: akava
"""


import cv2
from mtcnn import MTCNN

# Cargar la imagen que deseas analizar
image_path = "normal.jpg"
image = cv2.imread(image_path)

# Crear una instancia del detector MTCNN
detector = MTCNN()

# Detectar rostros en la imagen
detections = detector.detect_faces(image)

# Mostrar a cada persona por separado y contar el número de personas
num_personas = 0


# Mostrar a cada persona por separado
for i, detection in enumerate(detections):
    x, y, w, h = detection['box']
    x, y, w, h = int(x), int(y), int(w), int(h)
    person_image = image[y:y+h, x:x+w]
    # Dibujar un rectángulo alrededor del rostro detectado en la imagen original
    cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 5)
    num_personas += 1

# Mostrar la imagen original con todas las detecciones de forma más pequeña
cv2.namedWindow('Detected Faces', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Detected Faces', 800, 600)
cv2.imshow('Detected Faces', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
print("Número de personas detectadas:", num_personas)





"""
import cv2
import numpy as np
from mtcnn import MTCNN
import modelGenderDetection as mu
import matplotlib.pyplot as plt

# Crear el modelo
gender_model = mu.create_gender_model()

# Cargar los pesos del modelo entrenado
gender_model.load_weights("gender_model_weights.h5")

# Cargar la imagen que deseas analizar
image_path = "comparar2.jpg"
image = cv2.imread(image_path)

# Crear una instancia del detector MTCNN
detector = MTCNN()

# Detectar rostros en la imagen
detections = detector.detect_faces(image)

# Mostrar a cada persona por separado
for i, detection in enumerate(detections):
    x, y, w, h = detection['box']
    x, y, w, h = int(x), int(y), int(w), int(h)
    person_image = image[y:y+h, x:x+w]

    # Preprocesar la imagen para la predicción del género
    person_image = cv2.resize(person_image, (96, 96))  # Redimensionar a 96x96 píxeles
    person_image = person_image.astype('float32') / 255
    person_image = np.expand_dims(person_image, axis=0)

    # Realizar la predicción del género
    prediction = gender_model.predict(person_image)
    if prediction[0][0] > 0.5:
        gender = 'Mujer'
        color = (0, 0, 255)  # Rojo
    else:
        gender = 'Hombre'
        color = (255, 0, 0)  # Azul
    percentage = prediction[0][0] * 100

    # Dibujar un rectángulo alrededor del rostro detectado en la imagen original
    cv2.rectangle(image, (x, y), (x+w, y+h), color, 1)

    # Mostrar el género predicho encima del rectángulo
    cv2.putText(image, f'{gender}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, color, 1)

# Mostrar la imagen original con todas las detecciones
cv2.imshow('Detected Faces', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
plt.show()
"""








