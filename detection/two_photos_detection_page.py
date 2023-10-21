# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 11:29:22 2023

@author: akava
"""



import tkinter as tk
from tkinter import ttk
import customtkinter, tkinter
from PIL import Image, ImageTk
from retinaface import RetinaFace
import cv2
from comparison.face_comparison_page import FaceComparison

class TwoPhotosDetectionPage:
       
    def __init__(self, Load, App, App_window, image1, image2, options):
        self.App = App
        self.App_window = App_window
        self.Load = Load
        self.root = customtkinter.CTkToplevel()
        self.root.title("Pagina de Deteccion de Rostros de Dos Fotos")
        self.root.geometry("800x600")  # Tamaño de la ventana
        self.root.resizable(False, False)
        self.checkbox_vars = []
        self.checkbox_vars_image1 = [] 
        self.checkbox_vars_image2 = []  
        self.selected_option = options

        # Configurar el evento de cierre de la ventana secundaria
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.detected_faces_image1 = RetinaFace.extract_faces(image1, align = True)
        self.scaled_image1=image1

        self.detected_faces_image2 = RetinaFace.extract_faces(image2, align = True)
        self.scaled_image2=image2
         
        self.Load.withdraw()

        main_frame = customtkinter.CTkFrame(self.root, fg_color=("transparent"))
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Crear un Frame para el mensaje
        message_frame = customtkinter.CTkFrame(main_frame, fg_color=("transparent"))
        message_frame.pack(side=tk.TOP, fill=tk.X)

        # Agregar una etiqueta para el mensaje "Selecciona las fotos que deseas eliminar"
        message_label = customtkinter.CTkLabel(message_frame, text="Selecciona las fotos que deseas eliminar:", font=('Calibri', 15),  fg_color="transparent", width=110)
        message_label.pack(padx=10, pady=5, anchor=tk.W)
        
                
        face_count_image = customtkinter.CTkImage(Image.open("images/face.png"), size=(26, 26))
        self.face_count_label1 = customtkinter.CTkButton(
            message_frame, 
            image=face_count_image, 
            border_width=2,
            corner_radius=8,
            text_color="black", 
            fg_color="transparent", 
            text="", 
            width=300)
        self.face_count_label1.pack(padx=10, side=tk.LEFT)
 
        self.face_count_label2 = customtkinter.CTkButton(
            message_frame, 
            image=face_count_image, 
            border_width=2,
            corner_radius=8,
            text_color="black", 
            fg_color="transparent", 
            text="", 
            width=300)
        self.face_count_label2.pack(padx=10, side=tk.LEFT)
        

        # Crear un Frame para las imágenes
        images_frame = customtkinter.CTkFrame(main_frame, fg_color=("transparent"))
        images_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Crear un Frame para los botones
        button_frame = customtkinter.CTkFrame(main_frame,  fg_color="transparent")
        button_frame.pack(side=tk.RIGHT, fill=tk.Y)

        
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
        self.frame = customtkinter.CTkFrame(canvas, fg_color="transparent")
        canvas.create_window((0, 0), window=self.frame, anchor=tk.NW)



        for i in range(2):
            detected_faces = self.detected_faces_image1 if i == 0 else self.detected_faces_image2
            scaled_image = self.scaled_image1 if i == 0 else self.scaled_image2
            checkbox_vars = self.checkbox_vars_image1 if i == 0 else self.checkbox_vars_image2
            self.show_detected_faces(self.frame, detected_faces, scaled_image, checkbox_vars, i)

        # Configurar el Canvas para que pueda desplazarse
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))




    def show_detected_faces(self, frame, detected_faces, scaled_image, checkbox_vars, section):
        
        self.face_count_label1.configure(text="Foto 1:  {}".format(self.count_faces(self.detected_faces_image1)))
        self.face_count_label2.configure(text="Foto 2:  {}".format(self.count_faces(self.detected_faces_image2)))
        
        if section == 0:
            col_count = 0
            row_count = 0
        else:
            col_count = 3
            row_count = 0
    
        # Lista para mantener las imágenes personales
        self.person_images_tk = []
    
        self.person_images_tk = []
        style = ttk.Style()
        style.configure('TCheckbutton', font=('Calibri', 9))
        
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
            checkbox_vars.append(checkbox_var)
    
            # Convertir la imagen de PIL a PhotoImage
            person_image_small_tk = ImageTk.PhotoImage(person_image_pil_small)
    
            # Mostrar la imagen en una etiqueta dentro del Frame
            label = customtkinter.CTkLabel(frame, image=person_image_small_tk, text="")
            
            # Agregar un checkbox para seleccionar la imagen
            checkbox = ttk.Checkbutton(frame, text="Seleccionar", variable=checkbox_var)

            if section == 0:
                # Colocar la etiqueta y el checkbox en la posición adecuada usando grid
                label.grid(row=row_count, column=col_count, padx=10, pady=10, sticky="n")
                checkbox.grid(row=row_count + 1, column=col_count, padx=10, pady=5, sticky="s")
            else:
                # Colocar la etiqueta y el checkbox en la posición adecuada usando grid
                label.grid(row=row_count, column=col_count+5, padx=10, pady=10, sticky="n")
                checkbox.grid(row=row_count + 1, column=col_count+5, padx=10, pady=5, sticky="s")

            # Actualizar los contadores de columna y fila
            col_count += 1
    
            if section == 0:
                if col_count >= 3:
                    col_count = 0
                    row_count += 2
            else:
                if col_count >= 6:
                    col_count = 3
                    row_count += 2
            
            
        self.checkbox_vars.extend(checkbox_vars)  # Agregar las variables a la lista general

    def go_back(self):
        # Hacer que la ventana anterior vuelva a ser visible
        self.Load.deiconify()
        # Cerrar la ventana actual
        self.root.destroy()

    def count_faces(self, detected_faces):
        return len(detected_faces)       

    def continue_pressed(self):
        # Crear una nueva instancia de la ventana FaceComparison
        app = FaceComparison(self.root, self.App, self.App_window, self.scaled_image1, self.detected_faces_image1, self.scaled_image2, self.detected_faces_image2, self.selected_option)
        #self.root.withdraw()

    def delete_selected(self):
        
        self.detected_faces_image1 = self.delete_selected_images(self.detected_faces_image1, self.checkbox_vars_image1)
        self.detected_faces_image2 = self.delete_selected_images(self.detected_faces_image2, self.checkbox_vars_image2)

        for widget in self.frame.winfo_children():
            widget.destroy()
        self.checkbox_vars = []
        self.checkbox_vars_image1 = [] 
        self.checkbox_vars_image2 = [] 
        
        for i in range(2):
            detected_faces = self.detected_faces_image1 if i == 0 else self.detected_faces_image2
            scaled_image = self.scaled_image1 if i == 0 else self.scaled_image2
            checkbox_vars = self.checkbox_vars_image1 if i == 0 else self.checkbox_vars_image2
            self.show_detected_faces(self.frame, detected_faces, scaled_image, checkbox_vars, i)

    def delete_selected_images(self, detected_faces, checkbox_vars):
        updated_detected_faces = [detection for detection, checkbox_var in zip(detected_faces, checkbox_vars) if not checkbox_var.get()]
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
        
        
        
        
        
        
        
"""

class TwoPhotosDetectionPage:
       
    def __init__(self, Load, App, App_window, image1, image2, options):
        self.App = App
        self.App_window = App_window
        self.Load = Load
        self.root = customtkinter.CTkToplevel()
        self.root.title("Pagina de Deteccion de Rostros de Dos Fotos")
        self.root.geometry("800x600")  # Tamaño de la ventana
        self.root.resizable(False, False)
        self.checkbox_vars = []
        self.checkbox_vars_image1 = [] 
        self.checkbox_vars_image2 = []  
        self.selected_option = options

        # Configurar el evento de cierre de la ventana secundaria
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        label_style = ttk.Style()
        label_style.configure("Custom.TLabel", foreground="white", background="#007ACC", font=("Helvetica", 8), padding=5, borderwidth=2, relief="solid")

        # Llamar a la función de detección de rostros aquí con la ruta de la imagen
        #num_personas_image1, self.scaled_image1, self.detected_faces_image1 = mtcnn.detect_faces_and_display(image1)
        #num_personas_image2, self.scaled_image2, self.detected_faces_image2 = mtcnn.detect_faces_and_display(image2)


        self.detected_faces_image1 = RetinaFace.extract_faces(image1, align = True)
        num_personas_image1= len(self.detected_faces_image1)
        self.scaled_image1=image1

        self.detected_faces_image2 = RetinaFace.extract_faces(image2, align = True)
        num_personas_image2= len(self.detected_faces_image2)
        self.scaled_image2=image2
         
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


        # Definir las etiquetas de recuento de rostros
        self.face_count_label1 = ttk.Label(button_frame, text="", style="Custom.TLabel", width=10)
        self.face_count_label1.pack(padx=10, pady=10, anchor=tk.NW)
        
        self.face_count_label2 = ttk.Label(button_frame, text="", style="Custom.TLabel", width=10)
        self.face_count_label2.pack(padx=10, pady=10, anchor=tk.NW)



        for i in range(2):
            detected_faces = self.detected_faces_image1 if i == 0 else self.detected_faces_image2
            scaled_image = self.scaled_image1 if i == 0 else self.scaled_image2
            checkbox_vars = self.checkbox_vars_image1 if i == 0 else self.checkbox_vars_image2
            self.show_detected_faces(self.frame, detected_faces, scaled_image, checkbox_vars, i)


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


    def show_detected_faces(self, frame, detected_faces, scaled_image, checkbox_vars, section):
        
        self.face_count_label1.config(text="Foto 1:  {}".format(self.count_faces(self.detected_faces_image1)))
        self.face_count_label2.config(text="Foto 2:  {}".format(self.count_faces(self.detected_faces_image2)))
        
        if section == 0:
            col_count = 0
            row_count = 0
        else:
            col_count = 3
            row_count = 0
    
        # Lista para mantener las imágenes personales
        self.person_images_tk = []
    
        for i, detection in enumerate(detected_faces):
            #x, y, w, h = detection['box']
            #x, y, w, h = int(x), int(y), int(w), int(h)
            #person_image = scaled_image[y:y + h, x:x + w]
            person_image = detection
    
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
            checkbox_vars.append(checkbox_var)
    
            # Convertir la imagen de PIL a PhotoImage
            person_image_small_tk = ImageTk.PhotoImage(person_image_pil_small)
    
            # Mostrar la imagen en una etiqueta dentro del Frame
            label = ttk.Label(frame, image=person_image_small_tk, compound=tk.TOP)
            label.image = person_image_small_tk
    
            # Agregar un checkbox para seleccionar la imagen
            checkbox = ttk.Checkbutton(frame, text="Seleccionar", variable=checkbox_var)

            if section == 0:
                # Colocar la etiqueta y el checkbox en la posición adecuada usando grid
                label.grid(row=row_count, column=col_count, padx=10, pady=10, sticky="n")
                checkbox.grid(row=row_count + 1, column=col_count, padx=10, pady=5, sticky="s")
            else:
                # Colocar la etiqueta y el checkbox en la posición adecuada usando grid
                label.grid(row=row_count, column=col_count+5, padx=10, pady=10, sticky="n")
                checkbox.grid(row=row_count + 1, column=col_count+5, padx=10, pady=5, sticky="s")

            # Actualizar los contadores de columna y fila
            col_count += 1
    
            if section == 0:
                if col_count >= 3:
                    col_count = 0
                    row_count += 2
            else:
                if col_count >= 6:
                    col_count = 3
                    row_count += 2
        self.checkbox_vars.extend(checkbox_vars)  # Agregar las variables a la lista general

    def go_back(self):
        # Hacer que la ventana anterior vuelva a ser visible
        self.Load.deiconify()
        # Cerrar la ventana actual
        self.root.destroy()

    def count_faces(self, detected_faces):
        return len(detected_faces)       

    def continue_pressed(self):
        # Crear una nueva instancia de la ventana FaceComparison
        app = FaceComparison(self.root, self.App, self.scaled_image1, self.detected_faces_image1, self.scaled_image2, self.detected_faces_image2, self.selected_option)
        #self.root.withdraw()

    def delete_selected(self):
        
        self.detected_faces_image1 = self.delete_selected_images(self.detected_faces_image1, self.checkbox_vars_image1)
        self.detected_faces_image2 = self.delete_selected_images(self.detected_faces_image2, self.checkbox_vars_image2)

        for widget in self.frame.winfo_children():
            widget.destroy()
        self.checkbox_vars = []
        self.checkbox_vars_image1 = [] 
        self.checkbox_vars_image2 = [] 
        
        for i in range(2):
            detected_faces = self.detected_faces_image1 if i == 0 else self.detected_faces_image2
            scaled_image = self.scaled_image1 if i == 0 else self.scaled_image2
            checkbox_vars = self.checkbox_vars_image1 if i == 0 else self.checkbox_vars_image2
            self.show_detected_faces(self.frame, detected_faces, scaled_image, checkbox_vars, i)

    def delete_selected_images(self, detected_faces, checkbox_vars):
        updated_detected_faces = [detection for detection, checkbox_var in zip(detected_faces, checkbox_vars) if not checkbox_var.get()]
        return updated_detected_faces

    def on_closing(self):
        # Restaura la ventana principal
        self.App.deiconify()
        
        # Cierra la ventana de PhotoLoadPage
        self.root.destroy()
        self.Load.destroy()
        
"""