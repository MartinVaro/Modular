# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 11:35:21 2023

@author: akava
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import models.MTCNN as mtcnn
import cv2
from gender_classification.gender_classifier_window import GenderClassifierWindow

class SinglePhotoDetectionPage:
    def __init__(self, Load, App, image1, options):
        self.App = App
        self.Load = Load
        self.root = tk.Toplevel()
        self.root.title("Pagina de Deteccion de Rostros de una Sola Foto")
        self.root.geometry("800x600")  # Tamaño de la ventana
        self.root.resizable(False, False)
        self.checkbox_vars = []
        
        
        # Configurar el evento de cierre de la ventana secundaria
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Variable de control para rastrear si se ha borrado alguna imagen
        self.images_deleted = False

        label_style = ttk.Style()
        label_style.configure("Custom.TLabel", foreground="white", background="#007ACC", font=("Helvetica", 8), padding=5, borderwidth=2, relief="solid")

        # Llamar a la función de detección de rostros aquí con la ruta de la imagen
        num_personas, self.scaled_image, self.detected_faces = mtcnn.detect_faces_and_display(image1)

        self.Load.withdraw()
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Crear un Frame para el mensaje
        message_frame = ttk.Frame(main_frame)
        message_frame.pack(side=tk.TOP, fill=tk.X)


        # Agregar una etiqueta para el mensaje "Selecciona las fotos que deseas eliminar"
        message_label = ttk.Label(message_frame, text="Selecciona las fotos que deseas eliminar:", style="Custom.TLabel", width=110)
        message_label.pack(padx=10, pady=5, anchor=tk.W)

        # Crear un Frame para las imágenes
        images_frame = ttk.Frame(main_frame)
        images_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Crear un Frame para los botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y)

        
        # Agregar una Scrollbar al Frame de las imágenes
        scroll_y = tk.Scrollbar(images_frame, orient=tk.VERTICAL)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Crear un Canvas para mostrar las imágenes con scrollbar en el Frame de las imágenes
        canvas = tk.Canvas(images_frame, yscrollcommand=scroll_y.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.config(command=canvas.yview)

        # Crear un Frame en el Canvas para mostrar las imágenes
        self.frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=self.frame, anchor=tk.NW)

        self.face_count_label1 = ttk.Label(button_frame, text="", style="Custom.TLabel", width=10)
        self.face_count_label1.pack(padx=10, pady=10, anchor=tk.NW)

        
        self.display_detected_faces(self.frame , self.detected_faces, self.scaled_image )

        # Botones para continuar y regresar en el Frame de los botones
        continue_button = ttk.Button(button_frame, text="Continuar", command=lambda: self.continue_pressed())
        continue_button.pack(padx=10, pady=10, anchor=tk.E)

        delete_button = ttk.Button(button_frame, text="Borrar", command=self.delete_selected)
        delete_button.pack(padx=10, pady=10, anchor=tk.E)

        back_button = ttk.Button(button_frame, text="Regresar", command=self.go_back)
        back_button.pack(padx=10, pady=10, anchor=tk.E)

        # Configurar el Canvas para que pueda desplazarse
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))   
   
        
    # Función para eliminar imágenes seleccionadas
    def delete_selected(self):

        self.detected_faces = self.delete_selected_images(self.scaled_image, self.detected_faces, self.checkbox_vars)
        # Actualizar la variable de control
        self.images_deleted = True
        self.display_detected_faces(self.frame, self.detected_faces, self.scaled_image)
    

    def display_detected_faces(self, frame, detected_faces, scaled_image):
        
        for widget in frame.winfo_children():
            widget.destroy()


        self.face_count_label1.config(text="Rostros:{}".format(self.count_faces(self.detected_faces)))
        
        # Lista para mantener el estado de los checkboxes
        self.checkbox_vars = []
        
        # Contadores para controlar las columnas y filas de las imágenes
        col_count = 0
        row_count = 0
        
        # Lista para mantener las imágenes personales
        self.person_images_tk = []
        

        for i, detection in enumerate(detected_faces):
            x, y, w, h = detection['box']
            x, y, w, h = int(x), int(y), int(w), int(h)
            person_image = scaled_image[y:y+h, x:x+w]
            
            # Convertir la imagen de NumPy a imagen de PIL
            person_image_pil = Image.fromarray(cv2.cvtColor(person_image, cv2.COLOR_BGR2RGB))
            
            # Redimensionar la imagen
            person_image_pil = person_image_pil.resize((150, 150), Image.LANCZOS)
            
            # Redimensionar la imagen para mostrarla en tamaño más pequeño en la interfaz
            person_image_pil_small = person_image_pil.resize((90, 90), Image.LANCZOS)
                
            # Convertir la imagen de PIL a PhotoImage
            person_image_tk = ImageTk.PhotoImage(person_image_pil)  # Usar la imagen original aquí
            self.person_images_tk.append(person_image_tk)  # Agregar a la lista
                
            # Crear una variable para el estado del checkbox
            checkbox_var = tk.BooleanVar(value=False)
            self.checkbox_vars.append(checkbox_var)
            
            # Convertir la imagen de PIL a PhotoImage
            person_image_small_tk = ImageTk.PhotoImage(person_image_pil_small)
                
            # Mostrar la imagen en una etiqueta dentro del Frame
            label = ttk.Label(frame, image=person_image_small_tk, text="Rostro {}".format(i + 1), compound=tk.TOP)
            label.image = person_image_small_tk
            
            # Agregar un checkbox para seleccionar la imagen
            checkbox = ttk.Checkbutton(frame, text="Seleccionar", variable=checkbox_var)
            
            # Colocar la etiqueta y el checkbox en la posición adecuada usando grid
            label.grid(row=row_count, column=col_count, padx=10, pady=10)
            checkbox.grid(row=row_count + 1, column=col_count, padx=10, pady=0)
            
            # Actualizar los contadores de columna y fila
            col_count += 1
                   
            # Si col_count es 0, significa que estamos en una nueva fila y necesitamos actualizar los contadores
            if col_count == 0:
                row_count += 2
            elif col_count >= 6:
                col_count = 0
                row_count += 2

       
        return self.person_images_tk
    
    def continue_pressed(self):

        # Crear una nueva instancia de la ventana del Clasificador de género
        if self.images_deleted:
            self.root.withdraw()
            faces=self.extract_faces(self.scaled_image, self.updated_detected_faces)
            app = GenderClassifierWindow(self.root, self.App, faces)
            
        else:
            self.root.withdraw()
            faces=self.extract_faces(self.scaled_image, self.detected_faces)
            app = GenderClassifierWindow(self.root, self.App, faces)
           
   
    def count_faces(self, detected_faces):
        return len(detected_faces)     
        
    def go_back(self):
        # Hacer que la ventana anterior vuelva a ser visible
        self.Load.deiconify()
        # Cerrar la ventana actual
        self.root.destroy()
        
    def extract_faces(self, scaled_image, detected_faces):
        faces = []  # Lista para almacenar los rostros extraídos
        # Iterar sobre las detecciones de rostros
        for detection in detected_faces:
            x1, y1, width1, height1 = detection['box']
            x1, y1, width1, height1 = int(x1), int(y1), int(width1), int(height1)
            face_roi = scaled_image[y1:y1+height1, x1:x1+width1]
            faces.append(face_roi)
        return faces

    def delete_selected_images(self, scaled_image, detected_faces, checkbox_vars):
        # Eliminar las imágenes seleccionadas de detected_faces
        updated_detected_faces = []
        for detection, checkbox_var in zip(detected_faces, checkbox_vars):
            if not checkbox_var.get():
                updated_detected_faces.append(detection)

        self.updated_detected_faces = updated_detected_faces
        return updated_detected_faces


    def on_closing(self):
        # Restaura la ventana principal
        self.App.deiconify()
        
        # Cierra la ventana de PhotoLoadPage
        self.root.destroy()
        self.Load.destroy()