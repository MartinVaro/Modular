# -*- coding: utf-8 -*-
"""
Created on Sun Jul 30 17:13:18 2023

@author: akava
"""


import cv2
import numpy as np
from deepface import DeepFace
import matplotlib.pyplot as plt



def CompareFaces(scaled_image1, detected_faces_image1, scaled_image2, detected_faces_image2, selected_option):
    
    detections1 = detected_faces_image1
    detections2 = detected_faces_image2
    image1 = scaled_image1
    image2 = scaled_image2

    # Obtener las coordenadas de los rostros en cada imagen
    faces1 = [detection['box'] for detection in detections1]
    faces2 = [detection['box'] for detection in detections2]

    # Lista para almacenar los rostros emparejados aprobados
    approved_faces = []
    unique_faces = []

    # Definir los umbrales a utilizar
    if selected_option == "alto":
        thresholds = [0.15, 0.2, 0.25, 0.3]
    elif selected_option == "medio":
        thresholds = [0.1, 0.2, 0.3]
    elif selected_option == "bajo":
        thresholds = [0.3]

    # Calcular todas las distancias de antemano
    distances = []
    for i, face1_coords in enumerate(faces1):
        distances_row = []
        matches = 0
        x1, y1, width1, height1 = face1_coords
        face_roi1 = image1[y1:y1 + height1, x1:x1 + width1]
        
        print("Rostro:", i+1)
        for j, face2_coords in enumerate(faces2):
           
            x2, y2, width2, height2 = face2_coords
            face_roi2 = image2[y2:y2 + height2, x2:x2 + width2]
            # Realizar la comparación de rostros con enforce_detection=False
            distance = DeepFace.verify(img1_path=face_roi1, img2_path=face_roi2, enforce_detection=False)
            
            # Si la distancia es menor a 0.3, aumentar el contador de coincidencias
            if distance < 0.3:
                distances_row.append(distance)
                matches += 1
            
            # Si el contador de coincidencias es mayor o igual a 3, detener la iteración
            if matches >= 3:
                print("aqui hubo break :", j)
                break
            
            distances_row.append(None)
        distances.append(distances_row)



    compared_indices_faces1 = set()
    compared_indices_faces2 = set()  # Conjunto para almacenar los índices de rostros comparados
    # Realizar la comparación de rostros utilizando DeepFace
    for threshold in thresholds:
               
       # compared_indices = set()  # Conjunto para almacenar los índices de rostros comparados

        for i, face1_coords in enumerate(faces1):
           
            print("Cara numero:", i + 1)
            if i in compared_indices_faces1:
                continue
            for j, face2_coords in enumerate(faces2):
                if j in compared_indices_faces2:
                    continue

                # Recortar el rostro de cada imagen
                x1, y1, width1, height1 = face1_coords
                x2, y2, width2, height2 = face2_coords
                face_roi1 = image1[y1:y1+height1, x1:x1+width1]
                face_roi2 = image2[y2:y2+height2, x2:x2+width2]

                distance = distances[i][j]
                if distance < threshold:
                   
                    print(f"El rostro {i+1} en la imagen 1 y el rostro {j+1} en la imagen 2 pertenecen a la misma persona.")
                    # Agregar el índice de rostro en faces2 como comparado
                    compared_indices_faces1.add(i)
                    compared_indices_faces2.add(j)
                    # Redimensionar el segundo rostro para que tenga la misma altura que el primero
                    face_roi2_resized = cv2.resize(face_roi2, (face_roi1.shape[1], face_roi1.shape[0]))      
                    # Agregar el rostro emparejado aprobado a la lista
                    approved_faces.append([face_roi1, face_roi2_resized])      
                    break     # No es necesario comparar con otros rostros en faces2 para este rostro en faces1
    
 
    # Ahora agregar los rostros restantes de faces1 que no tuvieron semejanza con ningún rostro en faces2
    for i, face1_coords in enumerate(faces1):
        if i not in compared_indices_faces1:
            x, y, w, h = face1_coords
            unique_faces.append(image1[y:y+h, x:x+w])
    
    # Ahora agregar los rostros restantes de faces2 que no tuvieron semejanza con ningún rostro en faces1
    for j, face2_coords in enumerate(faces2):
        if j not in compared_indices_faces2:
            x, y, w, h = face2_coords
            unique_faces.append(image2[y:y+h, x:x+w])
    
    return approved_faces, unique_faces   
    




def ReclassifyFaces(detected_faces_image1, detected_faces_image2, unique_faces, marked_pairs):
    # Obtener las coordenadas de los rostros en cada imagen
    faces1 = detected_faces_image1
    faces2 = detected_faces_image2

    # Lista para almacenar los rostros emparejados aprobados
    approved_faces = []
    
    compared_indices = set()  # Conjunto para almacenar los índices de rostros comparados

    threshold = 0.1  # Umbral para la comparación de rostros

    for i, face1 in enumerate(faces1):
        is_compared = False  # Indicador para controlar si se comparó el rostro
        
        for j, face2 in enumerate(faces2):
            # Verificar si el par de índices ya fue comparado
            if j in compared_indices:
                continue

            if (i, j) not in marked_pairs:
                # Realizar la comparación de rostros con enforce_detection=False
                distance = DeepFace.verify(img1_path=face1, img2_path=face2, enforce_detection=False)


                # Comparar la distancia con el umbral
                if distance < threshold:
                    is_compared = True
                    print(f"El rostro {i+1} en la imagen 1 y el rostro {j+1} en la imagen 2 pertenecen a la misma persona.")
                    # Agregar el índice de rostro en faces2 como comparado
                    compared_indices.add(j)
                    # Agregar el rostro emparejado aprobado a la lista
                    approved_faces.append([face1, face2])
                    break

        if not is_compared:
            unique_faces.append(face1)

    # Agregar los rostros restantes de faces2 que no tuvieron semejanza con ningún rostro en faces1
    unique_faces.extend(face2 for j, face2 in enumerate(faces2) if j not in compared_indices)
    
    print("rostros unicos:", len(unique_faces))
    return approved_faces, unique_faces









    

"""VERsion con duplicacion pero funciona en parte


    compared_indices_faces1 = set()
    compared_indices_faces2 = set()  # Conjunto para almacenar los índices de rostros comparados
    # Realizar la comparación de rostros utilizando DeepFace
    for threshold in thresholds:
               
       # compared_indices = set()  # Conjunto para almacenar los índices de rostros comparados

        for i, face1_coords in enumerate(faces1):
           
            print("Cara numero:", i + 1)
            if i in compared_indices_faces1:
                continue
            for j, face2_coords in enumerate(faces2):
                if j in compared_indices_faces2:
                    continue

                # Recortar el rostro de cada imagen
                x1, y1, width1, height1 = face1_coords
                x2, y2, width2, height2 = face2_coords
                face_roi1 = image1[y1:y1+height1, x1:x1+width1]
                face_roi2 = image2[y2:y2+height2, x2:x2+width2]

                distance = distances[i][j]
                if distance < threshold:
                   
                    print(f"El rostro {i+1} en la imagen 1 y el rostro {j+1} en la imagen 2 pertenecen a la misma persona.")
                    # Agregar el índice de rostro en faces2 como comparado
                    compared_indices_faces1.add(i)
                    compared_indices_faces2.add(j)
                    # Redimensionar el segundo rostro para que tenga la misma altura que el primero
                    face_roi2_resized = cv2.resize(face_roi2, (face_roi1.shape[1], face_roi1.shape[0]))      
                    # Agregar el rostro emparejado aprobado a la lista
                    approved_faces.append([face_roi1, face_roi2_resized])      
                    break     # No es necesario comparar con otros rostros en faces2 para este rostro en faces1
    
 
    
    
    # Ahora agregar los rostros restantes de faces1 que no tuvieron semejanza con ningún rostro en faces2
    unique_faces.extend(image1[y:y+h, x:x+w] for x, y, w, h in faces1)
    
    # Ahora agregar los rostros restantes de faces2 que no tuvieron semejanza con ningún rostro en faces1
    unique_faces.extend(image2[y:y+h, x:x+w] for x, y, w, h in faces2)
    
    return approved_faces, unique_faces   
"""

"""
def CompareFaces(scaled_image1, detected_faces_image1, scaled_image2, detected_faces_image2, selected_option):
    
    
    detections1 = detected_faces_image1
    detections2 = detected_faces_image2
    
    image1 = scaled_image1
    image2 = scaled_image2
    
    # Obtener las coordenadas de los rostros en cada imagen
    faces1 = [detection['box'] for detection in detections1]
    faces2 = [detection['box'] for detection in detections2]
    
    
    # Lista para almacenar los rostros únicos
    unique_faces = []
    thresholds = []

    selected_option = "alto"
    # Definir los umbrales a utilizar
    if selected_option == "alto":
        thresholds = [0.15, 0.2, 0.25, 0.3]
    elif selected_option == "medio":
        thresholds = [0.1, 0.2, 0.3]
    elif selected_option == "bajo":
        thresholds = [0.3]
    
    # Lista para almacenar los rostros emparejados aprobados
    approved_faces = []
    
    # Realizar la comparación de rostros utilizando DeepFace
    for threshold in thresholds:
        
        # Crear listas para almacenar los rostros aún no comparados
        new_faces1 = []
        new_faces2 = []
        compared_indices = set()  # Conjunto para almacenar los índices de rostros comparados
    
        for i, face1_coords in enumerate(faces1):
            is_compared = False
            print("Cara numero: ", i+1)
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
                distance = DeepFace.verify(img1_path=face_roi1, img2_path=face_roi2, enforce_detection=False)
    
                # Comparar la distancia con el umbral
                if distance < threshold:
                    is_compared = True
                    print(f"El rostro {i+1} en la imagen 1 y el rostro {j+1} en la imagen 2 pertenecen a la misma persona.")
                    # Agregar el índice de rostro en faces2 como comparado
                    compared_indices.add(j)
                    # Redimensionar el segundo rostro para que tenga la misma altura que el primero
                    face_roi2_resized = cv2.resize(face_roi2, (face_roi1.shape[1], face_roi1.shape[0]))      
                    # Agregar el rostro emparejado aprobado a la lista
                    approved_faces.append([face_roi1, face_roi2_resized])      
                    break     # No es necesario comparar con otros rostros en faces2 para este rostro en faces1
    
            # Si el rostro actual no fue comparado, agregarlo a las nuevas listas
            if not is_compared:
                new_faces1.append(face1_coords)
    
        # Agregar los rostros restantes de faces2 que no tuvieron semejanza con ningún rostro en faces1
        # Agregar los rostros restantes de faces2 que no tuvieron semejanza con ningún rostro en faces1
        new_faces2.extend(face2_coords for j, face2_coords in enumerate(faces2) if j not in compared_indices)
    
        # Actualizar las listas faces1 y faces2 para el próximo ciclo
        faces1 = new_faces1
        faces2 = new_faces2
    
    
    # Ahora agregar los rostros restantes de faces1 que no tuvieron semejanza con ningún rostro en faces2
    unique_faces.extend(image1[y:y+h, x:x+w] for x, y, w, h in faces1)
    
    # Ahora agregar los rostros restantes de faces2 que no tuvieron semejanza con ningún rostro en faces1
    unique_faces.extend(image2[y:y+h, x:x+w] for x, y, w, h in faces2)
    
    return approved_faces, unique_faces   
    

    
"""
  
    
"""   
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
                    #unique_faces.append(face_roi2)
                    # Redimensionar el segundo rostro para que tenga la misma altura que el primero
                    face_roi2_resized = cv2.resize(face_roi2, (face_roi1.shape[1], face_roi1.shape[0]))      
                    # Agregar el rostro emparejado aprobado a la lista
                    approved_faces.append([face_roi1, face_roi2_resized])      
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

    print("Aqui estoy dentro de la primera clasificacion de rostros", len(unique_faces))
    return approved_faces, unique_faces
    """













"""
def ReclassifyFaces(detected_faces_image1, detected_faces_image2, unique_faces, marked_pairs):
    # Obtener las coordenadas de los rostros en cada imagen
    faces1 = detected_faces_image1
    faces2 = detected_faces_image2
    
    
    print(len(faces1))
    print(len(faces2))

    thresholds = [0.1]

    # Lista para almacenar los rostros emparejados aprobados
    approved_faces = []
    
    compared_indices = set()  # Conjunto para almacenar los índices de rostros comparados
    
    # Realizar la comparación de rostros utilizando DeepFace
    for threshold in thresholds:
        # Crear listas para almacenar los rostros aún no comparados
        new_faces1 = []
        new_faces2 = []
        
        for i, face1 in enumerate(faces1):
            for j, face2 in enumerate(faces2):
                # Verificar si el par de índices ya fue comparado
                if j in compared_indices:
                    continue
     
                if (i, j) not in marked_pairs:

                    # Realizar la comparación de rostros con enforce_detection=False
                    result = DeepFace.verify(img1_path=face1, img2_path=face1, enforce_detection=False)
                   
                    # Verificar si se detectaron rostros en ambas imágenes
                    if "message" in result and "No face" in result["message"]:
                        print(f"No se detectaron rostros en el par {i+1} - {j+1}.")
                        continue
        
                    # Obtener la distancia entre los rostros
                    distance = result["distance"]
                    print(distance)
                    # Comparar la distancia con el umbral
                    if distance < threshold:
                        print(f"El rostro {i+1} en la imagen 1 y el rostro {j+1} en la imagen 2 pertenecen a la misma persona.")
                        # Agregar el índice de rostro en faces2 como comparado
                        compared_indices.add(j)
                        # Agregar el rostro emparejado aprobado a la lista
                        approved_faces.append([face1, face2])      
                        break     # No es necesario comparar con otros rostros en faces2 para este rostro en faces1
    
            # Si el rostro actual no fue comparado, agregarlo a las nuevas listas
            if j not in compared_indices:
                new_faces1.append(face1)
    
        # Agregar los rostros restantes de faces2 que no tuvieron semejanza con ningún rostro en faces1
        for j, face2 in enumerate(faces2):
            if j not in compared_indices:
                new_faces2.append(face2)
    
        # Actualizar las listas faces1 y faces2 para el próximo ciclo
        faces1 = new_faces1
        faces2 = new_faces2
    
    # Ahora agregar los rostros restantes de faces2 que no tuvieron semejanza con ningún rostro en faces1
    for face1_coords in faces1:
        unique_faces.append(face1)
        
    # Ahora agregar los rostros restantes de faces2 que no tuvieron semejanza con ningún rostro en faces1
    for face2_coords in faces2:
        unique_faces.append(face2)    

    print("rostros unicos: ", len(unique_faces))
    return approved_faces, unique_faces

"""






    
"""    
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


"""

"""
import cv2
import numpy as np
from mtcnn import MTCNN
from deepface import DeepFace
import matplotlib.pyplot as plt

# El codigo funciona mejor cuando en el path1 ingresamos la foto con menor cantidad rostros

# Cargar la imagen que deseas analizar
image1_path = "testimagenes/bycent2.jpg"  #Menos rostros
image2_path = "testimagenes/bycent1.jpg"  #Mas rostros
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
thresholds = [0.15, 0.2, 0.25, 0.3] #muchas personas
#thresholds = [0.15, 0.2] #pocas personas

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





"""









