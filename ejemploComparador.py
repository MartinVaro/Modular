# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 16:40:49 2023

@author: akava
"""

from deepface import DeepFace

# Cargar las dos imágenes
image_path1 = "faces/predicts/profe2.jpeg"
image_path2 = "faces/predicts/profe9.jpg"

# Realizar la verificación facial con enforce_detection=False
result = DeepFace.verify(img1_path=image_path1, img2_path=image_path2, enforce_detection=False)

# Obtener la distancia entre los rostros
distance = result["distance"]

print(distance)
# Definir un umbral para determinar si los rostros pertenecen a la misma persona
threshold = 0.5

# Comparar la distancia con el umbral
if distance < threshold:
    print("Los rostros pertenecen a la misma persona.")
else:
    print("Los rostros pertenecen a diferentes personas.")





"""


import cv2
import torch
import numpy as np
from facenet_pytorch import InceptionResnetV1
from mtcnn import MTCNN

# Cargar el modelo FaceNet
facenet = InceptionResnetV1(pretrained='vggface2').eval()

# Cargar el detector MTCNN
detector = MTCNN()

# Cargar las dos imágenes
image_path1 = "faces/predicts/profe2.jpeg"
image_path2 = "faces/predicts/profe1.jpeg"

# Cargar las imágenes usando OpenCV
image1 = cv2.imread(image_path1)
image2 = cv2.imread(image_path2)

# Convertir las imágenes de BGR (OpenCV) a RGB (facenet-pytorch)
image1_rgb = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
image2_rgb = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)

# Detectar rostros en cada imagen usando MTCNN
faces1 = detector.detect_faces(image1_rgb)
faces2 = detector.detect_faces(image2_rgb)

# Verificar si se detectaron rostros en ambas imágenes
if len(faces1) > 0 and len(faces2) > 0:
    # Suponemos que solo hay un rostro en cada imagen, por lo que tomamos el primero
    face1 = faces1[0]
    face2 = faces2[0]

    # Obtener las coordenadas del recuadro del rostro
    x1, y1, width1, height1 = face1['box']
    x2, y2, width2, height2 = face2['box']

    # Recortar la región de interés (rostro) de las imágenes
    face_roi1 = image1_rgb[y1:y1+height1, x1:x1+width1]
    face_roi2 = image2_rgb[y2:y2+height2, x2:x2+width2]

    # Preprocesar las imágenes para la predicción de FaceNet
    face_roi1 = cv2.resize(face_roi1, (160, 160))  # Redimensionar a 160x160 píxeles (tamaño requerido por FaceNet)
    face_roi1 = face_roi1.astype('float32') / 255.0  # Normalizar a rango [0, 1]
    face_roi1 = np.transpose(face_roi1, (2, 0, 1))  # Cambiar el orden de los canales (de HxWxC a CxHxW)
    face_roi1 = np.expand_dims(face_roi1, axis=0)  # Agregar una dimensión adicional para representar el lote (batch)

    face_roi2 = cv2.resize(face_roi2, (160, 160))
    face_roi2 = face_roi2.astype('float32') / 255.0
    face_roi2 = np.transpose(face_roi2, (2, 0, 1))
    face_roi2 = np.expand_dims(face_roi2, axis=0)

    # Obtener los embeddings de los rostros utilizando FaceNet
    embeddings1 = facenet(torch.tensor(face_roi1)).detach().numpy()
    embeddings2 = facenet(torch.tensor(face_roi2)).detach().numpy()

    # Calcular la distancia euclidiana entre los embeddings
    distance = np.linalg.norm(embeddings1 - embeddings2)

    print(distance)
    # Definir un umbral para determinar si los rostros pertenecen a la misma persona
    threshold = 1

    # Comparar la distancia con el umbral
    if distance < threshold:
        print("Los rostros pertenecen a la misma persona.")
    else:
        print("Los rostros pertenecen a diferentes personas.")
else:
    print("No se detectaron rostros en ambas imágenes.")
"""



""" FALLA CON PROFE 3 y 4, atina 1 y 2
import cv2
import numpy as np

# Cargar las dos imágenes
image_path1 = "faces/predicts/profe3.jpg"
image_path2 = "faces/predicts/profe4.jpg"

# Cargar las imágenes en escala de grises
image1 = cv2.imread(image_path1, cv2.IMREAD_GRAYSCALE)
image2 = cv2.imread(image_path2, cv2.IMREAD_GRAYSCALE)

# Redimensionar las imágenes para que tengan el mismo tamaño
image1_resized = cv2.resize(image1, (128, 128))
image2_resized = cv2.resize(image2, (128, 128))

# Calcular la diferencia absoluta entre las dos imágenes
difference = cv2.absdiff(image1_resized, image2_resized)

# Calcular el porcentaje de similitud entre las imágenes
similarity = 1.0 - np.mean(difference) / 255.0

# Definir un umbral para determinar si las imágenes son similares o no
threshold = 0.8

# Comparar el porcentaje de similitud con el umbral
if similarity > threshold:
    print("Las imágenes pertenecen a la misma persona.")
else:
    print("Las imágenes pertenecen a diferentes personas.")
"""

"""
import cv2
import numpy as np
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Lambda
import tensorflow.keras.backend as K
from tensorflow.keras.utils import normalize

def create_siamese_model(input_shape):
    # Definir la red Siamesa
    input_1 = Input(shape=input_shape)
    input_2 = Input(shape=input_shape)

    convnet = create_convnet(input_shape)
    embeddings_1 = convnet(input_1)
    embeddings_2 = convnet(input_2)

    distance = Lambda(euclidean_distance)([embeddings_1, embeddings_2])

    siamese_model = Model(inputs=[input_1, input_2], outputs=distance)

    return siamese_model

def create_convnet(input_shape):
    # Definir la arquitectura de la red convolucional
    model = Sequential()
    model.add(Conv2D(64, (3, 3), activation='relu', input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(128, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dense(128, activation='relu'))
    
    return model

def euclidean_distance(vectors):
    vector1, vector2 = vectors
    sum_square = K.sum(K.square(vector1 - vector2), axis=1, keepdims=True)
    return K.sqrt(K.maximum(sum_square, K.epsilon()))

# Cargar las dos imágenes
image_path1 = "faces/predicts/soy4.png"
image_path2 = "faces/predicts/soy5.png"

# Cargar las imágenes usando OpenCV
image1 = cv2.imread(image_path1)
image2 = cv2.imread(image_path2)

# Preprocesar las imágenes para la red Siamesa
input_shape = (160, 160, 3)  # Asegúrate de que las imágenes tengan el mismo tamaño y canales
face_roi1 = cv2.resize(image1, (input_shape[0], input_shape[1]))
face_roi2 = cv2.resize(image2, (input_shape[0], input_shape[1]))

# Agregar una dimensión adicional para representar el lote (batch)
face_roi1 = np.expand_dims(face_roi1, axis=0)
face_roi2 = np.expand_dims(face_roi2, axis=0)

# Normalizar las imágenes para la red Siamesa
face_roi1 = normalize(face_roi1.astype(float), axis=1)
face_roi2 = normalize(face_roi2.astype(float), axis=1)

# Crear el modelo Siamesa
siamese_model = create_siamese_model(input_shape)

# Cargar los pesos del modelo entrenado (ajusta la ruta al archivo de pesos)
siamese_model.load_weights('path_to_weights.h5')

# Obtener la distancia entre los embeddings de las imágenes
distance = siamese_model.predict([face_roi1, face_roi2])[0][0]

# Definir un umbral para determinar si los rostros pertenecen a la misma persona
threshold = 0.7

# Comparar la distancia con el umbral
if distance < threshold:
    print("Los rostros pertenecen a la misma persona.")
else:
    print("Los rostros pertenecen a diferentes personas.")


"""
