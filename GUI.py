# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 15:39:22 2023

@author: akava
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import MTCNN as mtcnn
import cv2
import modelGenderDetection as mu
import numpy as np
import matplotlib.pyplot as plt


class PhotoLoadPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Pagina de Carga de Fotos")
        
        # Crear una variable para almacenar la opción seleccionada
        self.selected_option = tk.StringVar(root)
        self.selected_option.set("mucho")  # Valor predeterminado
        
        # Elemento para cargar una imagen
        self.load_image_button = ttk.Button(root, text="Cargar Imagen", command=self.load_image)
        self.load_image_button.pack(pady=10)
        
        # Checkbox para mostrar opciones adicionales
        self.show_options = tk.BooleanVar()
        self.show_options_checkbox = ttk.Checkbutton(root, text="Mostrar Opciones", variable=self.show_options, command=self.toggle_options)
        self.show_options_checkbox.pack()
        
        # Elementos adicionales para opciones
        self.additional_elements_frame = None
        self.additional_elements = []
        
        # Botones de Continuar y Cancelar
        self.continue_button = ttk.Button(root, text="Continuar", command=self.continue_pressed)
        self.continue_button.pack(pady=10)
        
        self.cancel_button = ttk.Button(root, text="Cancelar", command=self.root.quit)
        self.cancel_button.pack(pady=10)
        
        # Botón para cerrar la aplicación
        #self.quit_button = ttk.Button(root, text="Cerrar Aplicación", command=root.quit)
        #self.quit_button.pack(pady=10)
                
        
        
        # Variables para las imágenes
        self.image1 = None
        self.image2 = None

    def toggle_options(self):
        if self.show_options.get():
            # Crear y mostrar elementos adicionales para opciones
            self.additional_elements_frame = ttk.Frame(self.root)
            self.additional_elements_frame.pack()
            
            # Elemento para cargar una imagen adicional
            load_additional_image_button = ttk.Button(self.additional_elements_frame, text="Cargar Imagen Adicional", command=self.load_additional_image)
            load_additional_image_button.pack(pady=10)
            
            # Crear un widget para seleccionar opciones
            ttk.Label(self.additional_elements_frame, text="Selecciona una opción:").pack()
            ttk.OptionMenu(self.additional_elements_frame, self.selected_option, "mucho", "poco", "nada").pack()
            
        else:
            # Eliminar elementos adicionales
            if self.additional_elements_frame:
                self.additional_elements_frame.destroy()
                self.additional_elements_frame = None
        
    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Imagenes", "*.jpg *.png")])
        if file_path:
            print("Imagen cargada:", file_path)
            self.image1 = file_path
    
    def load_additional_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Imagenes", "*.jpg *.png")])
        if file_path:
            print("Imagen adicional cargada:", file_path)
            self.image2 = file_path

    def continue_pressed(self):
        if self.show_options.get():
            if self.image1 and self.image2:
                self.root.withdraw()
                options = self.selected_option.get()
                third_window = tk.Toplevel(self.root)
                app = TwoPhotosDetectionPage(third_window, self.image1, self.image2, options)
            else:
                print("Por favor, carga ambas imágenes antes de continuar.")
        else:
            if self.image1:
                self.root.withdraw()
                options = self.selected_option.get()
                second_window = tk.Toplevel(self.root)
                app = SinglePhotoDetectionPage(second_window, self.image1, options)
            else:
                print("Por favor, carga al menos una imagen antes de continuar.")




class SinglePhotoDetectionPage:
    def __init__(self, root, image1, options):
        self.root = root
        self.root.title("Pagina de Deteccion de Rostros de una Sola Foto")

        
        # Variable de control para rastrear si se ha borrado alguna imagen
        self.images_deleted = False

        # Llamar a la función de detección de rostros aquí con la ruta de la imagen
        image_path = image1  # Actualiza con la ruta correcta
        num_personas, scaled_image, detected_faces = mtcnn.detect_faces_and_display(image_path)

        # Mostrar el número de personas detectadas
        ttk.Label(root, text="Número de personas detectadas: {}".format(num_personas)).pack()

        # Crear un Canvas para mostrar las imágenes con scrollbar
        canvas = tk.Canvas(self.root)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Agregar una Scrollbar al Canvas
        scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Crear un Frame en el Canvas para mostrar las imágenes
        frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor=tk.NW)

        
        # Función para eliminar imágenes seleccionadas
        def delete_selected():
            updated_detected_faces = self.delete_selected_images(scaled_image, detected_faces, checkbox_vars)
            # Actualizar la variable de control
            self.images_deleted = True



        # Lista para mantener el estado de los checkboxes
        checkbox_vars = []

        # Mostrar las imágenes de los rostros detectados en etiquetas dentro del Frame
        for i, detection in enumerate(detected_faces):
            x, y, w, h = detection['box']
            x, y, w, h = int(x), int(y), int(w), int(h)
            person_image = scaled_image[y:y+h, x:x+w]

            # Convertir la imagen de NumPy a imagen de PIL
            person_image_pil = Image.fromarray(cv2.cvtColor(person_image, cv2.COLOR_BGR2RGB))

            # Redimensionar la imagen
            person_image_pil = person_image_pil.resize((150, 150), Image.LANCZOS)

            # Convertir la imagen de PIL a PhotoImage
            person_image_tk = ImageTk.PhotoImage(person_image_pil)

            # Crear una variable para el estado del checkbox
            checkbox_var = tk.BooleanVar(value=False)
            checkbox_vars.append(checkbox_var)

            # Mostrar la imagen en una etiqueta dentro del Frame
            label = ttk.Label(frame, image=person_image_tk, text="Rostro {}".format(i + 1), compound=tk.TOP)
            label.image = person_image_tk

            # Agregar un checkbox para seleccionar la imagen
            checkbox = ttk.Checkbutton(frame, text="Seleccionar", variable=checkbox_var)
            checkbox.pack()

            label.pack(pady=10)
            
            
        # Agregar un botón para eliminar las imágenes seleccionadas
        delete_button = ttk.Button(frame, text="Eliminar Seleccionadas", command=delete_selected)
        delete_button.pack()

        # Agregar botones para continuar y regresar
        continue_button = ttk.Button(frame, text="Continuar", command=lambda: self.continue_pressed(detected_faces, scaled_image))
        continue_button.pack()

        back_button = ttk.Button(frame, text="Regresar", command=self.go_back)
        back_button.pack()
        
        
        # Configurar el Canvas para que pueda desplazarse
        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def delete_selected_images(self, scaled_image, detected_faces, checkbox_vars):
        # Eliminar las imágenes seleccionadas de detected_faces
        updated_detected_faces = []

        # Mostrar la imagen original con las detecciones actualizadas
        scaled_image_updated = scaled_image.copy()
        for detection, checkbox_var in zip(detected_faces, checkbox_vars):
            if not checkbox_var.get():
                x, y, w, h = detection['box']
                x, y, w, h = int(x), int(y), int(w), int(h)
                cv2.rectangle(scaled_image_updated, (x, y), (x + w, y + h), (255, 0, 0), 5)
                updated_detected_faces.append(detection)

        self.updated_detected_faces = updated_detected_faces
        cv2.namedWindow('Detected Faces', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Detected Faces', 800, 600)
        cv2.imshow('Detected Faces', scaled_image_updated)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return updated_detected_faces
    
    
    def continue_pressed(self, detected_faces, scaled_image):
        # Crear una nueva instancia de la ventana del Clasificador de género
        gender_classifier_window = tk.Toplevel(self.root)
        if self.images_deleted:
            self.root.withdraw()
            app = GenderClassifierWindow(gender_classifier_window, self.updated_detected_faces, scaled_image)
        else:
            self.root.withdraw()
            app = GenderClassifierWindow(gender_classifier_window, detected_faces, scaled_image)


    def go_back(self):
        # Crear una nueva instancia de FirstWindow
        root = tk.Tk()
        app = PhotoLoadPage(root)
        self.root.destroy()  # Cerrar la ventana actual
        root.mainloop()



class TwoPhotosDetectionPage:
    def __init__(self, root, image1, image2, options):
        self.root = root
        self.root.title("Pagina de Deteccion de Rostros de Dos Fotos")

        # Llamar a la función de detección de rostros aquí con la ruta de la imagen 1
        image_path = image1  # Actualiza con la ruta correcta
        mtcnn.detect_faces_and_display(image_path)
        
        # Llamar a la función de detección de rostros aquí con la ruta de la imagen 2
        image_path2 = image2  # Actualiza con la ruta correcta
        mtcnn.detect_faces_and_display(image_path2)





class GenderClassifierWindow:
    def __init__(self, root, detected_faces, scaled_image):
        self.root = root
        self.root.title("Clasificador de Género")
        self.detected_faces = detected_faces
        self.scaled_image = scaled_image
        self.gender_model = mu.create_gender_model()
        self.gender_model.load_weights("gender_model_weights.h5")
        self.face_data = []  # Almacenar información de las caras (imagen, género, selección)

        # Crear un Canvas para mostrar las imágenes con scrollbar
        canvas = tk.Canvas(self.root)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Agregar una Scrollbar al Canvas
        scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Crear un Frame en el Canvas para mostrar las imágenes
        self.frame = ttk.Frame(canvas)  # Define self.frame como variable de instancia
        canvas.create_window((0, 0), window=self.frame, anchor=tk.NW)

        # Lista para almacenar las variables de control de los checkboxes
        self.checkbox_vars = []

        # Mostrar las imágenes de los rostros detectados en etiquetas dentro del Frame
        for i, detection in enumerate(detected_faces):
            x, y, w, h = detection['box']
            x, y, w, h = int(x), int(y), int(w), int(h)
            person_image = scaled_image[y:y+h, x:x+w]

            # Convertir la imagen de NumPy a imagen de PIL en formato BGR
            person_image_pil_bgr = Image.fromarray(cv2.cvtColor(person_image, cv2.COLOR_BGR2RGB))

            # Redimensionar la imagen
            person_image_pil_bgr = person_image_pil_bgr.resize((96, 96), Image.LANCZOS)  # Ajustar al tamaño esperado por el modelo

            # Convertir la imagen de PIL a NumPy array y escalar los valores
            person_image_array = np.array(person_image_pil_bgr) / 255.0

            # Realizar la predicción de género
            prediction = self.gender_model.predict(np.expand_dims(person_image_array, axis=0))

            # Convertir la imagen de NumPy a objeto PhotoImage de Tkinter en formato RGB
            person_image_tk_rgb = ImageTk.PhotoImage(person_image_pil_bgr)

            # Variable de control para el checkbox
            checkbox_var = tk.BooleanVar(value=False)
            self.checkbox_vars.append(checkbox_var)

            # Almacenar la información de la cara
            face_info = {
                'image': person_image_tk_rgb,
                'gender': 'Mujer' if prediction > 0.5 else 'Hombre',
                'selected': checkbox_var
            }
            self.face_data.append(face_info)

            # Mostrar la imagen en una etiqueta dentro del Frame
            label = ttk.Label(self.frame, image=person_image_tk_rgb, text="Rostro {}".format(i + 1), compound=tk.TOP)
            label.image = person_image_tk_rgb
            label.pack(pady=10)

            # Etiqueta para mostrar la predicción de género
            gender_label = ttk.Label(self.frame, text="Género: {}".format(face_info['gender']))
            gender_label.pack()

            # Checkbox para seleccionar la imagen
            checkbox = ttk.Checkbutton(self.frame, text="Seleccionar", variable=checkbox_var)
            checkbox.pack()

        # Botón para continuar y manejo de la acción
        continue_button = ttk.Button(self.frame, text="Continuar", command=self.continue_pressed)
        continue_button.pack()


    def count_genders(self):
        num_men = sum(1 for face_info in self.face_data if face_info['gender'] == 'Hombre')
        num_women = sum(1 for face_info in self.face_data if face_info['gender'] == 'Mujer')
        total_people = len(self.face_data)
        return num_men, num_women, total_people


    def continue_pressed(self):
        selected_faces = [i for i, var in enumerate(self.checkbox_vars) if var.get()]
        print("Rostros seleccionados:", selected_faces)

        # Cambiar género y mostrar información de las caras seleccionadas y almacenadas
        for i, face_info in enumerate(self.face_data):
            if i in selected_faces:
                face_info['gender'] = 'Mujer' if face_info['gender'] == 'Hombre' else 'Hombre'
                selected = "Seleccionado" if face_info['selected'].get() else "No seleccionado"
                print(f"Rostro {i + 1}: Género: {face_info['gender']}, {selected}")
                if selected:
                    corrected_image = self.correct_image_gender(face_info['image'], face_info['gender'])
                    face_info['image'] = corrected_image
            else:
                print(f"Rostro {i + 1}: Género: {face_info['gender']}, No seleccionado")

        # Actualizar visualización de imágenes
        self.update_image_display()
        
        # Contar y mostrar los géneros
        num_men, num_women, total_people = self.count_genders()
        print(f"Hombres: {num_men}, Mujeres: {num_women}, Total: {total_people}")
        

    def correct_image_gender(self, image, gender):
        # Implementa tu lógica para corregir el género de la imagen
        # Puedes cargar una nueva imagen con el género corregido o aplicar transformaciones
        # Retorna la imagen corregida
        return image  # Por defecto, no se realiza ninguna corrección

    def update_image_display(self):
        # Borrar contenido anterior del frame
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Mostrar las imágenes con género actualizado
        for i, face_info in enumerate(self.face_data):
            # Obtener la PhotoImage existente
            person_image_tk_rgb = face_info['image']

            # Mostrar la imagen en una etiqueta dentro del Frame
            label = ttk.Label(self.frame, image=person_image_tk_rgb, text="Rostro {}".format(i + 1), compound=tk.TOP)
            label.image = person_image_tk_rgb
            label.pack(pady=10)

            # Etiqueta para mostrar el nuevo género
            gender_label = ttk.Label(self.frame, text="Género: {}".format(face_info['gender']))
            gender_label.pack()

            # Checkbox para seleccionar la imagen
            checkbox = ttk.Checkbutton(self.frame, text="Seleccionar", variable=face_info['selected'])
            checkbox.pack()




 








if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoLoadPage(root)
    root.mainloop()







