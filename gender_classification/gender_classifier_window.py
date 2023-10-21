# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 11:32:54 2023

@author: akava
"""

import tkinter as tk
from tkinter import ttk
import customtkinter, tkinter
from PIL import Image, ImageTk
import cv2
import models.modelGenderDetection as mu
import numpy as np
from conference_window.conference_page import ConferenceWindow


class GenderClassifierWindow:
    def __init__(self, Detection, App, App_window, detected_faces):
        self.App = App
        self.App_window = App_window
        self.Detection = Detection
        self.root = customtkinter.CTkToplevel()
        self.root.title("Clasificador de Género")    
        self.root.geometry("800x600")  # Tamaño de la ventana
        self.root.resizable(False, False)
        self.detected_faces = detected_faces
        self.gender_model = mu.create_gender_model()
        self.gender_model.load_weights("models/gender_model_weights.h5")
        self.face_data = []  # Almacenar información de las caras (imagen, género, selección)
        self.face_info_images = []  # Lista para almacenar las referencias a las imágenes de Tkinter
        self.checkbox_vars = []
        self.face_train = []

        # Configurar el evento de cierre de la ventana secundaria
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        main_frame = customtkinter.CTkFrame(self.root, fg_color=("transparent"))
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Crear un Frame para el mensaje
        message_frame = customtkinter.CTkFrame(main_frame, fg_color=("transparent"))
        message_frame.pack(side=tk.TOP, fill=tk.X)

        # Agregar una etiqueta para el mensaje "Selecciona las fotos que deseas eliminar"
        message_label = customtkinter.CTkLabel(message_frame, text="Selecciona las fotos que estan mal clasificadas:", font=('Calibri', 15),  fg_color="transparent", width=110)
        message_label.pack(padx=10, pady=5, anchor=tk.W)
        
        # Crear un Frame para las imágenes
        images_frame = customtkinter.CTkFrame(main_frame, fg_color=("transparent"))
        images_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Crear un Frame para los botones
        button_frame = customtkinter.CTkFrame(main_frame,  fg_color="transparent")
        button_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Definir las etiquetas de recuento de rostros en el segundo Frame
        hombres_image = customtkinter.CTkImage(Image.open("images/hombre.png"), size=(26, 26))
        self.face_count_men = customtkinter.CTkButton(button_frame, image=hombres_image, text_color="black", fg_color="transparent", text="", width=10)
        self.face_count_men.pack(padx=10, pady=10, anchor=tk.NW)
        
        mujeres_image = customtkinter.CTkImage(Image.open("images/mujer.png"), size=(26, 26))
        self.face_count_women =  customtkinter.CTkButton(button_frame, image=mujeres_image, text_color="black", fg_color="transparent", text="", width=10)
        self.face_count_women.pack(padx=10, pady=10, anchor=tk.NW)

        
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
        
        clasificar_image = customtkinter.CTkImage(Image.open("images/clasificar.png"), size=(26, 26))
        reclassify_button = customtkinter.CTkButton(
            button_frame, 
            text="Reclasificar",
            width=20,
            command=self.reclassify_faces,
            image=clasificar_image,
            text_color="black",
            fg_color="transparent"
        )
        reclassify_button.pack(padx=10, pady=10, anchor=tk.W)        
        
        
        back_image = customtkinter.CTkImage(Image.open("images/volver.png"), size=(26, 26))
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
        self.frame = customtkinter.CTkFrame(canvas, fg_color=("transparent"))
        canvas.create_window((0, 0), window=self.frame, anchor=tk.NW)

        self.display_detected_faces(self.frame , self.detected_faces)

        # Configurar el Canvas para que pueda desplazarse
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))   
        
        

    def display_detected_faces(self, frame, detected_faces):
        for widget in frame.winfo_children():
            widget.destroy()
            
        
        # Lista para mantener el estado de los checkboxes
        self.checkbox_vars = []
        
        # Contadores para controlar las columnas y filas de las imágenes
        col_count = 0
        row_count = 0
        
        self.person_images_tk = []
        style = ttk.Style()
        style.configure('TCheckbutton', font=('Calibri', 9))
        
        for i, detection in enumerate(detected_faces):
            
            # Crear una variable para el estado del checkbox
            checkbox_var = tk.BooleanVar(value=False)
            self.checkbox_vars.append(checkbox_var)
            
            if i < len(self.face_data):
                face_info = self.face_data[i]
                face1_pil = face_info['image']
                face_info = {
                    'image': face_info['image'],
                    'gender': face_info['gender'],
                    'selected': checkbox_var
                }
            else:
                face1_pil = Image.fromarray(cv2.cvtColor(detection, cv2.COLOR_BGR2RGB))
                face1_pil = face1_pil.resize((96, 96), Image.LANCZOS)  # Redimensionar a 96x96
                face1_np = np.array(face1_pil) / 255.0  # Escalar los valores
                
                # Realizar la predicción de género solo si no hay información previa
                prediction = self.gender_model.predict(np.expand_dims(face1_np, axis=0))
                
                # Almacenar la información de la cara
                face_info = {
                    'image': face1_pil,
                    'gender': 'Mujer' if prediction > 0.5 else 'Hombre',
                    'selected': checkbox_var
                }
                self.face_data.append(face_info)
    
            # Redimensionar la imagen para mostrarla en tamaño más pequeño en la interfaz
            face1_pil_resized = face1_pil.resize((80, 80), Image.LANCZOS)
            
            
            #Aqui servia
            # Add a colored border based on gender
            border_color = (255, 105, 180) if face_info['gender'] == "Mujer" else "blue"
            # Crear Tkinter image with border
            border_size = 90
            face1_pil_resized_with_border = Image.new('RGBA', (border_size, border_size), border_color)
            face1_pil_resized_with_border.paste(face1_pil_resized, (int((border_size - 80) / 2), int((border_size - 80) / 2)))
    
            # Crear una referencia persistente a la imagen de Tkinter
            face1_tk = ImageTk.PhotoImage(face1_pil_resized_with_border)
            self.face_info_images.append(face1_tk)
    
            # Mostrar la imagen en una etiqueta dentro del Frame
            label = customtkinter.CTkLabel(frame, image=face1_tk, text="", compound=tk.TOP)
            label.image = face1_tk  # Guardar la referencia a la imagen
    
            #gender_label = ttk.Label(frame, text="Género: {}".format(face_info['gender']))
    
            checkbox = ttk.Checkbutton(frame, text="Seleccionar", variable=checkbox_var)
    
            label.grid(row=row_count, column=col_count, padx=9, pady=5)
            #gender_label.grid(row=row_count + 1, column=col_count, padx=10, pady=0)
            checkbox.grid(row=row_count + 1, column=col_count, padx=9, pady=0)
    
            col_count += 1
            if col_count >= 6:
                col_count = 0
                row_count += 3
    
        num_men, num_women, total_people = self.count_genders()
        self.face_count_men.configure(text="Hombres: {}".format(num_men))
        self.face_count_women.configure(text="Mujeres: {}".format(num_women))



    def count_genders(self):
        num_men = sum(1 for face_info in self.face_data if face_info['gender'] == 'Hombre')
        num_women = sum(1 for face_info in self.face_data if face_info['gender'] == 'Mujer')
        total_people = len(self.face_data)
        return num_men, num_women, total_people

    def reclassify_faces(self):

        selected_faces = [i for i, var in enumerate(self.checkbox_vars) if var.get()]
        # Cambiar género y mostrar información de las caras seleccionadas y almacenadas
        for i, face_info in enumerate(self.face_data):
            if i in selected_faces:
                face_info['gender'] = 'Mujer' if face_info['gender'] == 'Hombre' else 'Hombre'
                selected = "Seleccionado" if face_info['selected'].get() else "No seleccionado"

        # Actualizar visualización de imágenes
        self.display_detected_faces(self.frame, self.face_data)


    def save_image(self, image, file_path):
        image.save(file_path)
        
    def continue_pressed(self):
        num_men, num_women, total_people = self.count_genders()
        self.root.withdraw()
        app = ConferenceWindow(self.root, self.App, self.App_window, num_men, num_women)
        
               
    def go_back(self):
        # Hacer que la ventana anterior vuelva a ser visible
        self.Detection.deiconify()
        # Cerrar la ventana actual
        self.root.destroy()
            
    def return_to_main_menu(self):
        # Restaura la ventana principal
        self.App_window.deiconify()
        # Cierra la ventana de PhotoLoadPage
        self.root.destroy()
        self.Detection.destroy()

    def on_closing(self):
        # Restaura la ventana principal
        self.App_window.deiconify()
        # Cierra la ventana de PhotoLoadPage
        self.root.destroy()
        self.Detection.destroy()

