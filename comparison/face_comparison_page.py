# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 11:31:06 2023

@author: akava
"""

import tkinter as tk
from tkinter import ttk
import customtkinter, tkinter
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import models.detectionComparador as detect
from gender_classification.gender_classifier_window import GenderClassifierWindow

class FaceComparison:
    def __init__(self, Detection, App, App_window, scaled_image1, detected_faces_image1, scaled_image2, detected_faces_image2, selected_option):
        self.App = App
        self.App_window = App_window
        self.Detection = Detection
        self.root = customtkinter.CTkToplevel()
        self.root.title("Pagina de Comparación de Rostros")
        self.root.geometry("800x600")  # Tamaño de la ventana
        self.root.resizable(False, False)
        self.scaled_image1 = scaled_image1
        self.detected_faces_image1 = detected_faces_image1
        self.scaled_image2 = scaled_image2
        self.detected_faces_image2 = detected_faces_image2
        self.selected_option = selected_option
        self.updated_detected_faces_image1 = []
        self.updated_detected_faces_image2 = []
        self.checkbox_vars = []  
        self.faces_to_show = []  
        self.unique_faces = []
        self.at_least_one_selected = False  # Variable de control
        self.reclassify_count = 0  # Variable para llevar un registro de las veces que se ha presionado el botón
        
        # Configurar el evento de cierre de la ventana secundaria
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  

        main_frame = customtkinter.CTkFrame(self.root, fg_color=("transparent"))
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Crear un Frame para el mensaje
        message_frame = customtkinter.CTkFrame(main_frame, fg_color=("transparent"))
        message_frame.pack(side=tk.TOP, fill=tk.X)

        # Agregar una etiqueta para el mensaje "Selecciona las fotos que deseas eliminar"
        message_label = customtkinter.CTkLabel(message_frame, text="Selecciona las fotos que que estan mal emparejadas:", font=('Calibri', 15),  fg_color="transparent", width=110)
        message_label.pack(padx=10, pady=5, anchor=tk.W)

        # Crear un Frame para las imágenes
        images_frame = customtkinter.CTkFrame(main_frame, fg_color=("transparent"))
        images_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Crear un Frame para los botones
        button_frame = customtkinter.CTkFrame(main_frame,  fg_color="transparent")
        button_frame.pack(side=tk.RIGHT, fill=tk.Y)


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
        self.reclassify_button = customtkinter.CTkButton(
            button_frame, 
            text="Reemparejar",
            width=20,
            command=self.reclassify_pressed,
            image=clasificar_image,
            text_color="black",
            fg_color="transparent"
        )
        self.reclassify_button.pack(padx=10, pady=10, anchor=tk.W)  
        
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

        # Realizar la comparación de rostros y obtener la lista faces_to_show
        self.faces_to_show, self.unique_faces = detect.CompareFaces(scaled_image1, detected_faces_image1, scaled_image2, detected_faces_image2, selected_option)

        self.Detection.withdraw()

        # Verificar si no hay rostros emparejados
        if len(self.faces_to_show) == 0:
            self.continue_pressed()

        # Llamar a la función show_detected_faces para mostrar los rostros emparejados
        self.show_detected_faces(self.frame, self.faces_to_show) 
        
        # Configurar el Canvas para que pueda desplazarse
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))        


    def show_detected_faces(self, frame, faces_to_show):
    
        # Ocultar los widgets actuales en el marco de los rostros emparejados
        for widget in self.frame.winfo_children():
            widget.destroy()
            
        col_count = 0
        row_count = 0
        
        checkbox_vars=[]
        
        self.person_images_tk = []
        style = ttk.Style()
        style.configure('TCheckbutton', font=('Calibri', 9))
        
        # Recorrer la lista de rostros emparejados y mostrar cada rostro en el marco
        for i, (face1, face2) in enumerate(faces_to_show):
            # Convertir la imagen de NumPy a imagen de PIL
            face1_pil = Image.fromarray(cv2.cvtColor(face1, cv2.COLOR_BGR2RGB))
            face2_pil = Image.fromarray(cv2.cvtColor(face2, cv2.COLOR_BGR2RGB))
    
            # Redimensionar las imágenes
            face1_pil = face1_pil.resize((80, 80), Image.LANCZOS)
            face2_pil = face2_pil.resize((80, 80), Image.LANCZOS)
    
            # Convertir las imágenes de PIL a PhotoImage
            face1_tk = ImageTk.PhotoImage(face1_pil)
            face2_tk = ImageTk.PhotoImage(face2_pil)
    
            # Mostrar las imágenes en etiquetas dentro del marco
            label1 = customtkinter.CTkLabel(frame, image=face1_tk, text="", compound=tk.TOP)
            label1.grid(row=row_count, column=col_count, padx=10, pady=5)
    
            label2 = customtkinter.CTkLabel(frame, image=face2_tk, text="", compound=tk.TOP)
            label2.grid(row=row_count, column=col_count + 1, padx=10, pady=5)
    
            # Crear una variable para el estado del checkbox
            checkbox_var = tk.BooleanVar(value=False)
            checkbox_vars.append(checkbox_var)
    
            # Agregar un checkbox para seleccionar la pareja de rostros
            checkbox = ttk.Checkbutton(frame, text="Seleccionar", variable=checkbox_var)
            checkbox.grid(row=row_count + 1, column=col_count, columnspan=2, padx=10, pady=5, sticky="n")
    
            # Actualizar los contadores de columna y fila
            col_count += 2
                   
            # Si col_count es 0, significa que estamos en una nueva fila y necesitamos actualizar los contadores
            if col_count >= 6:
                col_count = 0
                row_count += 2   
        self.checkbox_vars.extend(checkbox_vars) 

    def continue_pressed(self):
        self.root.withdraw()
        faces=self.merge_faces_to_unique()
        app = GenderClassifierWindow(self.root, self.App, self.App_window, faces)
        
        
    def reclassify_pressed(self):
        
        if self.reclassify_count < 1:  # Verificar si el botón aún puede ser presionado
            self.reclassify_count += 1
            
            selected_faces_image1 = []
            selected_faces_image2 = []
            marked_pairs = set()  # Usar un conjunto en lugar de una lista para marked_pairs
        
            # Recorrer las variables de los checkboxes y las caras emparejadas
            for i, (checkbox_var, (face1, face2)) in enumerate(zip(self.checkbox_vars, self.faces_to_show)):
                if checkbox_var.get():
                    selected_faces_image1.append(face1)
                    selected_faces_image2.append(face2)
                    marked_pairs.add((i, i))
                    
                else:
                    self.unique_faces.append(face1)

            self.checkbox_vars = [] 
            #Llamar a la función CompareFaces para reclasificar las caras seleccionadas
            self.faces_to_show, self.unique_faces = detect.ReclassifyFaces(selected_faces_image1, selected_faces_image2, self.unique_faces, marked_pairs)

            # Verificar si no hay rostros emparejados
            if len(self.faces_to_show) == 0:
                self.continue_pressed()
                
            # Llamar a la función show_detected_faces para mostrar los rostros emparejados reclasificados
            self.show_detected_faces(self.frame, self.faces_to_show) 
            
        # Actualizar el estado del botón si ya se ha presionado dos veces
        else:
            self.unique_faces.extend([face2 for _, face2 in self.faces_to_show])
            self.reclassify_button.configure(state=tk.DISABLED)
            self.continue_pressed()

            
    def merge_faces_to_unique(self):
        for face1, _ in self.faces_to_show:
            self.unique_faces.append(face1)
        self.faces_to_show=[] #Esta linea evita que existan duplicados al regresar y avanzar
        return self.unique_faces

    def go_back(self):
        # Hacer que la ventana anterior vuelva a ser visible
        self.Detection.deiconify()
        # Cerrar la ventana actual
        self.root.destroy()

    def on_closing(self):
        # Restaura la ventana principal
        self.App_window.deiconify()
        
        # Cierra la ventana de PhotoLoadPage
        self.root.destroy()
        self.Detection.destroy()

    def return_to_main_menu(self):
        # Restaura la ventana principal
        self.App_window.deiconify()
        # Cierra la ventana de PhotoLoadPage
        self.root.destroy()
        self.Detection.destroy()  


"""

class FaceComparison:
    def __init__(self, Detection, App, App_window, scaled_image1, detected_faces_image1, scaled_image2, detected_faces_image2, selected_option):
        self.App = App
        self.App_window = App_window
        self.Detection = Detection
        self.root = customtkinter.CTkToplevel()
        self.root.title("Pagina de Comparación de Rostros")
        self.root.geometry("800x600")  # Tamaño de la ventana
        self.root.resizable(False, False)
        self.scaled_image1 = scaled_image1
        self.detected_faces_image1 = detected_faces_image1
        self.scaled_image2 = scaled_image2
        self.detected_faces_image2 = detected_faces_image2
        self.selected_option = selected_option
        self.updated_detected_faces_image1 = []
        self.updated_detected_faces_image2 = []
        self.checkbox_vars = []  
        self.faces_to_show = []  
        self.unique_faces = []
        self.at_least_one_selected = False  # Variable de control
        self.reclassify_count = 0  # Variable para llevar un registro de las veces que se ha presionado el botón
        
        # Configurar el evento de cierre de la ventana secundaria
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Crear un Frame para el mensaje
        message_frame = ttk.Frame(main_frame)
        message_frame.pack(side=tk.TOP, fill=tk.X)

        # Agregar una etiqueta para el mensaje "Selecciona las fotos que deseas eliminar"
        message_label = ttk.Label(message_frame, text="Selecciona las fotos que que estan mal emparejadas:", style="Custom.TLabel", width=110)
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


        # Realizar la comparación de rostros y obtener la lista faces_to_show
        self.faces_to_show, self.unique_faces = detect.CompareFaces(scaled_image1, detected_faces_image1, scaled_image2, detected_faces_image2, selected_option)

        self.Detection.withdraw()

        # Verificar si no hay rostros emparejados
        if len(self.faces_to_show) == 0:
            self.continue_pressed()


        # Llamar a la función show_detected_faces para mostrar los rostros emparejados
        self.show_detected_faces(self.frame, self.faces_to_show) 
        

        # Botones para continuar y regresar en el Frame de los botones
        continue_button = ttk.Button(button_frame, text="Continuar", command=lambda: self.continue_pressed())
        continue_button.pack(padx=10, pady=10, anchor=tk.E)

        self.reclassify_button = ttk.Button(button_frame, text="Reemparejar", command=self.reclassify_pressed)
        self.reclassify_button.pack(padx=10, pady=10, anchor=tk.E)

        back_button = ttk.Button(button_frame, text="Regresar", command=self.go_back)
        back_button.pack(padx=10, pady=10, anchor=tk.E)

        # Configurar el Canvas para que pueda desplazarse
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))        


    def show_detected_faces(self, frame, faces_to_show):
    
        # Ocultar los widgets actuales en el marco de los rostros emparejados
        for widget in self.frame.winfo_children():
            widget.destroy()
            
        col_count = 0
        row_count = 0
        
        checkbox_vars=[]
        
        
        # Recorrer la lista de rostros emparejados y mostrar cada rostro en el marco
        for i, (face1, face2) in enumerate(faces_to_show):
            # Convertir la imagen de NumPy a imagen de PIL
            face1_pil = Image.fromarray(cv2.cvtColor(face1, cv2.COLOR_BGR2RGB))
            face2_pil = Image.fromarray(cv2.cvtColor(face2, cv2.COLOR_BGR2RGB))
    
            # Redimensionar las imágenes
            face1_pil = face1_pil.resize((90, 90), Image.LANCZOS)
            face2_pil = face2_pil.resize((90, 90), Image.LANCZOS)
    
            # Convertir las imágenes de PIL a PhotoImage
            face1_tk = ImageTk.PhotoImage(face1_pil)
            face2_tk = ImageTk.PhotoImage(face2_pil)
    
            # Mostrar las imágenes en etiquetas dentro del marco
            label1 = ttk.Label(frame, image=face1_tk, text="Imagen 1", compound=tk.TOP)
            label1.image = face1_tk
            label1.grid(row=row_count, column=col_count, padx=0, pady=5, sticky="n")
    
            label2 = ttk.Label(frame, image=face2_tk, text="Imagen 2", compound=tk.TOP)
            label2.image = face2_tk
            label2.grid(row=row_count, column=col_count + 1, padx=10, pady=5, sticky="n")
    
            # Crear una variable para el estado del checkbox
            checkbox_var = tk.BooleanVar(value=False)
            checkbox_vars.append(checkbox_var)
    
            # Agregar un checkbox para seleccionar la pareja de rostros
            checkbox = ttk.Checkbutton(frame, text="Seleccionar", variable=checkbox_var)
            checkbox.grid(row=row_count + 1, column=col_count, columnspan=2, padx=10, pady=5, sticky="n")
    
            # Actualizar los contadores de columna y fila
            col_count += 2
                   
            # Si col_count es 0, significa que estamos en una nueva fila y necesitamos actualizar los contadores
            if col_count >= 6:
                col_count = 0
                row_count += 2   
        self.checkbox_vars.extend(checkbox_vars) 

    def continue_pressed(self):
        self.root.withdraw()
        faces=self.merge_faces_to_unique()
        app = GenderClassifierWindow(self.root, self.App, faces)
        
        
    def reclassify_pressed(self):
        
        if self.reclassify_count < 1:  # Verificar si el botón aún puede ser presionado
            self.reclassify_count += 1
            
            selected_faces_image1 = []
            selected_faces_image2 = []
            marked_pairs = set()  # Usar un conjunto en lugar de una lista para marked_pairs
        
            # Recorrer las variables de los checkboxes y las caras emparejadas
            for i, (checkbox_var, (face1, face2)) in enumerate(zip(self.checkbox_vars, self.faces_to_show)):
                if checkbox_var.get():
                    selected_faces_image1.append(face1)
                    selected_faces_image2.append(face2)
                    marked_pairs.add((i, i))
                    
                else:
                    self.unique_faces.append(face1)

            self.checkbox_vars = [] 
            #Llamar a la función CompareFaces para reclasificar las caras seleccionadas
            self.faces_to_show, self.unique_faces = detect.ReclassifyFaces(selected_faces_image1, selected_faces_image2, self.unique_faces, marked_pairs)

            # Verificar si no hay rostros emparejados
            if len(self.faces_to_show) == 0:
                self.continue_pressed()
                
            # Llamar a la función show_detected_faces para mostrar los rostros emparejados reclasificados
            self.show_detected_faces(self.frame, self.faces_to_show) 
            
        # Actualizar el estado del botón si ya se ha presionado dos veces
        else:
            self.unique_faces.extend([face2 for _, face2 in self.faces_to_show])
            self.reclassify_button.config(state=tk.DISABLED)
            self.continue_pressed()

            
    def merge_faces_to_unique(self):
        for face1, _ in self.faces_to_show:
            self.unique_faces.append(face1)
        self.faces_to_show=[] #Esta linea evita que existan duplicados al regresar y avanzar
        return self.unique_faces

    def go_back(self):
        # Hacer que la ventana anterior vuelva a ser visible
        self.Detection.deiconify()
        # Cerrar la ventana actual
        self.root.destroy()

    def on_closing(self):
        # Restaura la ventana principal
        self.App.deiconify()
        
        # Cierra la ventana de PhotoLoadPage
        self.root.destroy()
        self.Detection.destroy()







"""











