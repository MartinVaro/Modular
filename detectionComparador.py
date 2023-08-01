# -*- coding: utf-8 -*-
"""
Created on Sun Jul 30 17:13:18 2023

@author: akava
"""

import cv2
import numpy as np
from mtcnn import MTCNN
from deepface import DeepFace
import matplotlib.pyplot as plt

# El codigo funciona mejor cuando en el path1 ingresamos la foto con menor cantidad rostros

# Cargar la imagen que deseas analizar
image1_path = "bycent2.jpg"  #Menos rostros
image2_path = "bycent1.jpg"  #Mas rostros
image1 = cv2.imread(image1_path)
image2 = cv2.imread(image2_path)

# Crear una instancia del detector MTCNN
detector = MTCNN()

# Detectar rostros en ambas imágenes
detections1 = detector.detect_faces(image1)
detections2 = detector.detect_faces(image2)

# Obtener las coordenadas de los rostros en cada imagen
faces1 = [detection['box'] for detection in detections1]
faces2 = [detection['box'] for detection in detections2]

# Lista para almacenar los rostros únicos
unique_faces = []

# Definir los umbrales a utilizar
thresholds = [0.15, 0.2, 0.25, 0.3]


# Definir el tamaño de la imagen de destino que muestra las caras emparejadas
destination_width = 300
destination_height = 150

# Crear la imagen de destino
destination_image = np.zeros((destination_height, destination_width, 3), dtype=np.uint8)

#
print("Voy a entrar al for")

# Realizar la comparación de rostros utilizando DeepFace
for threshold in thresholds:
    # Crear listas para almacenar los rostros aún no comparados
    new_faces1 = []
    new_faces2 = []
    compared_indices = set()  # Conjunto para almacenar los índices de rostros comparados

    for i, face1_coords in enumerate(faces1):
        print("Cara numero: ", i)
        for j, face2_coords in enumerate(faces2):
            # Verificar si el índice de rostro en faces2 ya fue comparado
            if j in compared_indices:
                continue

            # Recortar el rostro de cada imagen
            x1, y1, width1, height1 = face1_coords
            x2, y2, width2, height2 = face2_coords
            face_roi1 = image1[y1:y1+height1, x1:x1+width1]
            face_roi2 = image2[y2:y2+height2, x2:x2+width2]

            # Realizar la comparación de rostros con enforce_detection=False
            result = DeepFace.verify(img1_path=face_roi1, img2_path=face_roi2, enforce_detection=False)

            # Verificar si se detectaron rostros en ambas imágenes
            if "message" in result and "No face" in result["message"]:
                print(f"No se detectaron rostros en el par {i+1} - {j+1}.")
                continue

            # Obtener la distancia entre los rostros
            distance = result["distance"]

            # Comparar la distancia con el umbral
            if distance < threshold:
                print(f"El rostro {i+1} en la imagen 1 y el rostro {j+1} en la imagen 2 pertenecen a la misma persona.")
    
                # Agregar el índice de rostro en faces2 como comparado
                compared_indices.add(j)
                # Agregar el rostro a la lista de rostros únicos
                unique_faces.append(face_roi2)
    
                # Redimensionar el segundo rostro para que tenga la misma altura que el primero
                face_roi2_resized = cv2.resize(face_roi2, (face_roi1.shape[1], face_roi1.shape[0]))
    
                # Mostrar los rostros emparejados en una sola imagen
                combined_face = np.hstack((face_roi1, face_roi2_resized))
                combined_face = cv2.resize(combined_face, (destination_width, destination_height))
                destination_image[:] = combined_face
    
                # Agregar la distancia encontrada en la imagen
                cv2.putText(destination_image, f"Distancia: {distance:.4f}", (10, destination_height - 20),
                            cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
    
                # Mostrar la imagen con ambos rostros y la distancia
                plt.imshow(cv2.cvtColor(destination_image, cv2.COLOR_BGR2RGB))
                plt.axis('off')
                plt.show()
                break     # No es necesario comparar con otros rostros en faces2 para este rostro en faces1

        # Si el rostro actual no fue comparado, agregarlo a las nuevas listas
        if j not in compared_indices:
            new_faces1.append(face1_coords)

    # Agregar los rostros restantes de faces2 que no tuvieron semejanza con ningún rostro en faces1
    for j, face2_coords in enumerate(faces2):
        if j not in compared_indices:
            new_faces2.append(face2_coords)

    # Actualizar las listas faces1 y faces2 para el próximo ciclo
    faces1 = new_faces1
    faces2 = new_faces2


# Ahora agregar los rostros restantes de faces2 que no tuvieron semejanza con ningún rostro en faces1
for face1_coords in faces1:
    print("si hay faces en el 1")
    x2, y2, width2, height2 = face1_coords
    face_roi1 = image1[y2:y2+height2, x2:x2+width2]
    unique_faces.append(face_roi1)
    
# Ahora agregar los rostros restantes de faces2 que no tuvieron semejanza con ningún rostro en faces1
for face2_coords in faces2:
    print("si hay faces en el 2")
    x2, y2, width2, height2 = face2_coords
    face_roi2 = image2[y2:y2+height2, x2:x2+width2]
    unique_faces.append(face_roi2)    

# Definir el tamaño deseado de los rostros en la imagen de destino
face_size = 150

# Calcular el número de columnas en la cuadrícula
num_cols = 10

# Calcular el número de filas en la cuadrícula
num_rows = (len(unique_faces) - 1) // num_cols + 1

# Calcular el tamaño de cada celda en la cuadrícula
cell_width = face_size
cell_height = face_size

# Calcular el tamaño de la imagen de destino
destination_width = num_cols * cell_width
destination_height = num_rows * cell_height

# Crear la imagen de destino
destination_image = np.zeros((destination_height, destination_width, 3), dtype=np.uint8)

# Visualizar los rostros únicos en la imagen de destino
for i, face_roi in enumerate(unique_faces):
    face_roi = cv2.resize(face_roi, (cell_width, cell_height))  # Redimensionar para que todos los rostros tengan el mismo tamaño
    row = i // num_cols
    col = i % num_cols
    destination_image[row*cell_height:(row+1)*cell_height, col*cell_width:(col+1)*cell_width] = face_roi

# Guardar la imagen de destino con los rostros únicos
cv2.imwrite("rostros_unicos.jpg", destination_image)

# Mostrar la imagen de destino con los rostros únicos
plt.imshow(cv2.cvtColor(destination_image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
















