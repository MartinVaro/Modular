# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 11:35:21 2023

@author: akava
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import customtkinter, tkinter
from retinaface import RetinaFace
import cv2
from gender_classification.gender_classifier_window import GenderClassifierWindow

class SinglePhotoDetectionPage:
    def __init__(self, Load, App, App_window, image1, options):
        self.App = App
        self.App_window = App_window
        self.Load = Load
        self.root = customtkinter.CTkToplevel()
        self.root.title("Pagina de Deteccion de Rostros de una Sola Foto")
        self.root.geometry("800x600")  # Tamaño de la ventana
        self.root.resizable(False, False)
        self.checkbox_vars = []
        
        # Configurar el evento de cierre de la ventana secundaria
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        # Variable de control para rastrear si se ha borrado alguna imagen
        self.images_deleted = False
        self.detected_faces = RetinaFace.extract_faces(image1, align = True)
        num_personas= len(self.detected_faces)
        self.scaled_image=image1
        self.Load.withdraw()
        
        main_frame = customtkinter.CTkFrame(self.root, fg_color=("transparent"))
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Crear un Frame para el mensaje
        message_frame = customtkinter.CTkFrame(main_frame, fg_color=("transparent"))
        message_frame.pack(side=tk.TOP, fill=tk.X)


        # Agregar una etiqueta para el mensaje "Selecciona las fotos que deseas eliminar"
        message_label = customtkinter.CTkLabel(message_frame, text="Selecciona las fotos que deseas eliminar:", font=('Calibri', 15),  fg_color="transparent", width=110)
        message_label.pack(padx=10, pady=5, anchor=tk.W)

        # Crear un Frame para las imágenes
        images_frame = customtkinter.CTkFrame(main_frame, fg_color=("transparent"))
        images_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Crear un Frame para los botones
        button_frame = customtkinter.CTkFrame(main_frame,  fg_color="transparent")
        button_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        face_count_image = customtkinter.CTkImage(Image.open("images/face.png"), size=(26, 26))
        self.face_count_label1 = customtkinter.CTkButton(button_frame, image=face_count_image, text_color="black", fg_color="transparent", text="", width=30)
        self.face_count_label1.pack(padx=10, pady=10, anchor=tk.W)

        # Botones para continuar y regresar en el Frame de los botones        
        home_image = customtkinter.CTkImage(Image.open("images/home.png"), size=(26, 26))
        home_button = customtkinter.CTkButton(
            button_frame,
            image=home_image,  
            fg_color="transparent", 
            text_color= "black", 
            text="Home", width=10, 
            command=self.return_to_main_menu)
        home_button.pack(pady=10)
        home_button.pack(padx=10, pady=10, anchor=tk.W) 
        
        continue_image = customtkinter.CTkImage(Image.open("images/aceptar.png"), size=(26, 26))
        continue_button = customtkinter.CTkButton(
            button_frame,
            text="Aceptar",
            width=20,
            command=self.continue_pressed,
            image=continue_image,
            text_color="black",
            fg_color="transparent"
        )
        continue_button.pack(padx=10, pady=10, anchor=tk.W)

        delete_image = customtkinter.CTkImage(Image.open("images/borrar.png"), size=(26, 26))
        delete_button = customtkinter.CTkButton(
            button_frame, 
            text="Borrar",
            width=20,
            command=self.delete_selected,
            image=delete_image,
            text_color="black",
            fg_color="transparent"
        )
        delete_button.pack(padx=10, pady=10, anchor=tk.W)
        
        back_image  = customtkinter.CTkImage(Image.open("images/volver.png"), size=(26, 26))
        back_button = customtkinter.CTkButton(
            button_frame, 
            text="Regresar",
            width=20,
            command=self.go_back,
            image=back_image,
            text_color="black",
            fg_color="transparent"
        )
        back_button.pack(padx=10, pady=10, anchor=tk.W)


        # Agregar una Scrollbar al Frame de las imágenes
        scroll_y = tk.Scrollbar(images_frame, orient=tk.VERTICAL)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Crear un Canvas para mostrar las imágenes con scrollbar en el Frame de las imágenes
        canvas = tk.Canvas(images_frame, yscrollcommand=scroll_y.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.config(command=canvas.yview)
        
        # Crear un Frame en el Canvas para mostrar las imágenes
        self.frame = customtkinter.CTkFrame(canvas, fg_color=("transparent"), width=650)
        canvas.create_window((0, 0), window=self.frame, anchor=tk.NW)
        
        self.display_detected_faces(self.frame , self.detected_faces, self.scaled_image )

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


        self.face_count_label1.configure(text="Rostros: {}".format(self.count_faces(self.detected_faces)))
        
        # Lista para mantener el estado de los checkboxes
        self.checkbox_vars = []
        
        # Contadores para controlar las columnas y filas de las imágenes
        col_count = 0
        row_count = 0
        
        self.person_images_tk = []
        style = ttk.Style()
        style.configure('TCheckbutton', font=('Calibri', 9))
        
        # Lista para mantener las imágenes personales

        for i, detection in enumerate(detected_faces):

            person_image = detection
            
            # Convertir la imagen de NumPy a imagen de PIL
            person_image_pil = Image.fromarray(cv2.cvtColor(person_image, cv2.COLOR_BGR2RGB))
            
            # Redimensionar la imagen
            person_image_pil = person_image_pil.resize((150, 150), Image.LANCZOS)
            
            # Redimensionar la imagen para mostrarla en tamaño más pequeño en la interfaz
            person_image_pil_small = person_image_pil.resize((80, 80), Image.LANCZOS)
                
            # Convertir la imagen de PIL a PhotoImage
            person_image_tk = ImageTk.PhotoImage(person_image_pil)  # Usar la imagen original aquí
            self.person_images_tk.append(person_image_tk)  # Agregar a la lista
                
            # Crear una variable para el estado del checkbox
            checkbox_var = tk.BooleanVar(value=False)
            self.checkbox_vars.append(checkbox_var)
            
            # Convertir la imagen de PIL a PhotoImage
            person_image_small_tk = ImageTk.PhotoImage(person_image_pil_small)
                
            # Mostrar la imagen en una etiqueta dentro del Frame
            label = customtkinter.CTkLabel(frame, image=person_image_small_tk, text="")
    
            # Agregar un checkbox para seleccionar la imagen
            checkbox = ttk.Checkbutton(frame, text="Seleccionar", variable=checkbox_var)

            
            # Colocar la etiqueta y el checkbox en la posición adecuada usando grid
            label.grid(row=row_count, column=col_count, padx=9, pady=5)
            checkbox.grid(row=row_count + 1, column=col_count, padx=9, pady=0)
            
            # Actualizar los contadores de columna y fila
            col_count += 1
                   
            # Si col_count es 0, significa que estamos en una nueva fila y necesitamos actualizar los contadores
            if col_count == 0:
                row_count += 2
            elif col_count >= 6:
                col_count = 0
                row_count += 2

       
        return self.person_images_tk


    def on_click(self, index):
        print(index)

    
    def continue_pressed(self):

        # Crear una nueva instancia de la ventana del Clasificador de género
        if self.images_deleted:
            self.root.withdraw()
            faces=self.extract_faces(self.scaled_image, self.updated_detected_faces)
            app = GenderClassifierWindow(self.root, self.App, self.App_window, faces)
            
        else:
            self.root.withdraw()
            faces=self.extract_faces(self.scaled_image, self.detected_faces)
            app = GenderClassifierWindow(self.root, self.App, self.App_window, faces)
           
   
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
            #x1, y1, width1, height1 = detection['box']
            #x1, y1, width1, height1 = int(x1), int(y1), int(width1), int(height1)
            #face_roi = scaled_image[y1:y1+height1, x1:x1+width1]
            #faces.append(face_roi)
            faces.append(detection)
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
        self.App_window.deiconify()
        
        # Cierra la ventana de PhotoLoadPage
        self.root.destroy()
        self.Load.destroy()
        
    def return_to_main_menu(self):
        # Restaura la ventana principal
        self.App_window.deiconify()
        # Cierra la ventana de PhotoLoadPage
        self.root.destroy()
        self.Load.destroy()