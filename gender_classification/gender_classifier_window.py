# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 11:32:54 2023

@author: akava
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import modelGenderDetection as mu
import numpy as np
from pdfgenerator.conference_page import ConferenceWindow


class GenderClassifierWindow:
    def __init__(self, root, detected_faces):
        self.root = root
        self.root.title("Clasificador de Género")    
        self.root.geometry("800x600")  # Tamaño de la ventana
        self.root.resizable(False, False)
        self.detected_faces = detected_faces
        self.gender_model = mu.create_gender_model()
        self.gender_model.load_weights("gender_model_weights.h5")
        self.face_data = []  # Almacenar información de las caras (imagen, género, selección)
        self.face_info_images = []  # Lista para almacenar las referencias a las imágenes de Tkinter
        self.checkbox_vars = []
        self.face_train = []
        
        label_style = ttk.Style()
        label_style.configure("Custom.TLabel", foreground="white", background="#007ACC", font=("Helvetica", 8), padding=5, borderwidth=2, relief="solid")

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Crear un Frame para el mensaje
        message_frame = ttk.Frame(main_frame)
        message_frame.pack(side=tk.TOP, fill=tk.X)

        # Agregar una etiqueta para el mensaje "Selecciona las fotos que deseas eliminar"
        message_label = ttk.Label(message_frame, text="Selecciona las fotos que estan mal clasificadas:", style="Custom.TLabel", width=110)
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

        # Definir las etiquetas de recuento de rostros en el segundo Frame
        self.face_count_men = ttk.Label(button_frame, text="", style="Custom.TLabel", width=10)
        self.face_count_men.pack(padx=10, pady=10, anchor=tk.NW)
        
        self.face_count_women = ttk.Label(button_frame, text="", style="Custom.TLabel", width=10)
        self.face_count_women.pack(padx=10, pady=10, anchor=tk.NW)

              
        self.display_detected_faces(self.frame , self.detected_faces)


        # Botones para continuar y regresar en el Frame de los botones
        continue_button = ttk.Button(button_frame, text="Continuar", command=lambda: self.continue_pressed())
        continue_button.pack(padx=10, pady=10, anchor=tk.E)

        self.reclassify_button = ttk.Button(button_frame, text="Reclasificar", command=self.reclassify_faces)
        self.reclassify_button.pack(padx=10, pady=10, anchor=tk.E)

        back_button = ttk.Button(button_frame, text="Regresar", command=self.go_back)
        back_button.pack(padx=10, pady=10, anchor=tk.E)

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
            face1_pil_resized = face1_pil.resize((85, 85), Image.LANCZOS)
            
            
            #Aqui servia
            # Add a colored border based on gender
            border_color = (255, 105, 180) if face_info['gender'] == "Mujer" else "blue"
            # Crear Tkinter image with border
            border_size = 90
            face1_pil_resized_with_border = Image.new('RGBA', (border_size, border_size), border_color)
            face1_pil_resized_with_border.paste(face1_pil_resized, (int((border_size - 85) / 2), int((border_size - 85) / 2)))
    
            # Crear una referencia persistente a la imagen de Tkinter
            face1_tk = ImageTk.PhotoImage(face1_pil_resized_with_border)
            self.face_info_images.append(face1_tk)
    
            # Mostrar la imagen en una etiqueta dentro del Frame
            label = ttk.Label(frame, image=face1_tk, compound=tk.TOP)
            label.image = face1_tk  # Guardar la referencia a la imagen
    
            #gender_label = ttk.Label(frame, text="Género: {}".format(face_info['gender']))
    
            checkbox = ttk.Checkbutton(frame, text="Seleccionar", variable=checkbox_var)
    
            label.grid(row=row_count, column=col_count, padx=10, pady=10)
            #gender_label.grid(row=row_count + 1, column=col_count, padx=10, pady=0)
            checkbox.grid(row=row_count + 1, column=col_count, padx=10, pady=5)
    
            col_count += 1
            if col_count >= 6:
                col_count = 0
                row_count += 3
    
        num_men, num_women, total_people = self.count_genders()
        self.face_count_men.config(text="Hombres:{}".format(num_men))
        self.face_count_women.config(text="Mujeres:{}".format(num_women), background="#FF69B4")



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
        conference_page = tk.Toplevel(self.root)
        app = ConferenceWindow(conference_page, num_men, num_women)
        self.root.withdraw()
        
        """
        ruta_mujeres = "faces/woman/"
        ruta_hombres = "faces/man/"
        
        for i, face_info in enumerate(self.face_data):      
            face_image = face_info['image']
            face_gender = face_info['gender']
        
            if face_gender == 'Mujer':
                file_path = ruta_mujeres + f"cucei_mujer_{i+323}.jpg"
            else:
                file_path = ruta_hombres + f"cucei_hombre_{i+323}.jpg"
        
            self.save_image(face_image, file_path)     
        """
               

    def go_back(self):
        # Hacer que la ventana anterior vuelva a ser visible
        self.root.deiconify()
        # Cerrar la ventana actual
        self.root.destroy()
            





































"""
class GenderClassifierWindow:
    def __init__(self, root, detected_faces):
        self.root = root
        self.root.title("Clasificador de Género")    
        self.root.geometry("800x600")  # Tamaño de la ventana
        self.root.resizable(False, False)
        self.detected_faces = detected_faces
        self.gender_model = mu.create_gender_model()
        self.gender_model.load_weights("gender_model_weights.h5")
        self.face_data = []  # Almacenar información de las caras (imagen, género, selección)
        self.face_info_images = []  # Lista para almacenar las referencias a las imágenes de Tkinter
        self.checkbox_vars = []

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
        
        self.display_detected_faces(self.frame , self.detected_faces)


    def display_detected_faces(self, frame, detected_faces):
        for widget in frame.winfo_children():
            widget.destroy()
    
        # Lista para mantener el estado de los checkboxes
        self.checkbox_vars = []
        
        # Contadores para controlar las columnas y filas de las imágenes
        col_count = 0
        row_count = 0
        
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
            face1_pil_resized = face1_pil.resize((90, 90), Image.LANCZOS)
            
            # Crear una referencia persistente a la imagen de Tkinter
            face1_tk = ImageTk.PhotoImage(face1_pil_resized)
            self.face_info_images.append(face1_tk) 
            
            # Mostrar la imagen en una etiqueta dentro del Frame
            label = ttk.Label(frame, image=face1_tk, compound=tk.TOP)
            label.image = face1_tk  # Guardar la referencia a la imagen
            
            # Etiqueta para mostrar la predicción de género
            gender_label = ttk.Label(frame, text="Género: {}".format(face_info['gender']))
            
            # Agregar un checkbox para seleccionar la imagen
            checkbox = ttk.Checkbutton(frame, text="Seleccionar", variable=checkbox_var)
            
            label.grid(row=row_count, column=col_count, padx=10, pady=10)
            gender_label.grid(row=row_count + 1, column=col_count, padx=10, pady=0)
            checkbox.grid(row=row_count + 2, column=col_count, padx=10, pady=5)
            
            # Actualizar los contadores de columna y fila
            col_count += 1
            
            if col_count >= 6:
                col_count = 0
                row_count += 3

        # Frame para los botones
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=0, column=6, padx=0, sticky="ns")  

        num_men, num_women, total_people = self.count_genders()

        # Botones para continuar y regresar
        continue_button = ttk.Button(button_frame, text="Continuar", command=lambda: self.continue_pressed())
        continue_button.grid(row=5, column=0, padx=0, pady=10, sticky="w")
        
        delete_button = ttk.Button(button_frame, text="Reclasificar", command=self.reclassify_faces)
        delete_button.grid(row=7, column=0, padx=0, pady=10, sticky="w")
        
        back_button = ttk.Button(button_frame, text="Regresar", command=self.go_back)
        back_button.grid(row=9, column=0, padx=0, pady=10, sticky="w")

        # Mostrar el número de personas detectadas
        label_women = ttk.Label(button_frame, text="Mujeres: {}".format(num_women), foreground="green")
        label_women.grid(row=11, column=0, padx=0, pady=10, sticky="w")

        label_men = ttk.Label(button_frame, text="Hombres: {}".format(num_men), foreground="blue")
        label_men.grid(row=13, column=0, padx=0, pady=10, sticky="w")

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

        
    def continue_pressed(self):
                
        # Contar y mostrar los géneros
        #num_men, num_women, total_people = self.count_genders()
        #print(f"Hombres: {num_men}, Mujeres: {num_women}, Total: {total_people}")
        pass

    def go_back(self):
        pass
            
"""