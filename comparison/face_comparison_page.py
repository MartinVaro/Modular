# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 11:31:06 2023

@author: akava
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import detectionComparador as detect
from gender_classification.gender_classifier_window import GenderClassifierWindow

class FaceComparison:
    def __init__(self, Detection, scaled_image1, detected_faces_image1, scaled_image2, detected_faces_image2, selected_option):
        self.Detection = Detection
        self.root = tk.Toplevel()
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
        

        label_style = ttk.Style()
        label_style.configure("Custom.TLabel", foreground="white", background="#007ACC", font=("Helvetica", 8), padding=5, borderwidth=2, relief="solid")
        

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
        app = GenderClassifierWindow(self.root, faces)
        
        
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
        return self.unique_faces

    def go_back(self):
        # Hacer que la ventana anterior vuelva a ser visible
        self.Detection.deiconify()
        # Cerrar la ventana actual
        self.root.destroy()






"""

class FaceComparison:
    def __init__(self, root, scaled_image1, detected_faces_image1, scaled_image2, detected_faces_image2, selected_option):
        self.root = root
        self.root.title("Pagina de Comparación de Rostros")
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
        

        # Realizar la comparación de rostros y obtener la lista faces_to_show
        self.faces_to_show, self.unique_faces = detect.CompareFaces(scaled_image1, detected_faces_image1, scaled_image2, detected_faces_image2, selected_option)

        # Llamar a la función show_detected_faces para mostrar los rostros emparejados
        self.show_detected_faces(self.faces_to_show, self.checkbox_vars)  # Pasar checkbox_vars al método
        
        # Mostrar los botones "Regresar" y "Reclasificar"
        self.show_buttons()
        
        # Iniciar el loop principal de la interfaz
        self.root.mainloop()

    def show_detected_faces(self, faces_to_show, checkbox_vars):

        # Crear un marco para mostrar los rostros emparejados en la ventana principal
        faces_frame = ttk.Frame(self.root)
        faces_frame.pack(padx=10, pady=10)

        # Lista para almacenar los checkbox seleccionados
        selected_faces = []

        def on_checkbox_change(i):
            if checkbox_vars[i].get():
                selected_faces.append(faces_to_show[i])
            else:
                if faces_to_show[i] in selected_faces:
                    selected_faces.remove(faces_to_show[i])
        
            # Verificar si al menos un checkbox está seleccionado
            if any(checkbox_var.get() for checkbox_var in checkbox_vars):
                self.reclassify_button.config(state=tk.NORMAL)
            else:
                self.reclassify_button.config(state=tk.DISABLED)


        # Recorrer la lista de rostros emparejados y mostrar cada rostro en el marco
        for i, (face1, face2) in enumerate(faces_to_show):
            # Convertir la imagen de NumPy a imagen de PIL
            face1_pil = Image.fromarray(cv2.cvtColor(face1, cv2.COLOR_BGR2RGB))
            face2_pil = Image.fromarray(cv2.cvtColor(face2, cv2.COLOR_BGR2RGB))

            # Redimensionar las imágenes
            face1_pil = face1_pil.resize((150, 150), Image.LANCZOS)
            face2_pil = face2_pil.resize((150, 150), Image.LANCZOS)

            # Convertir las imágenes de PIL a PhotoImage
            face1_tk = ImageTk.PhotoImage(face1_pil)
            face2_tk = ImageTk.PhotoImage(face2_pil)

            # Crear un marco para contener cada pareja de rostros y checkbox
            face_pair_frame = ttk.Frame(faces_frame)
            face_pair_frame.pack(fill=tk.X, padx=5, pady=5)

            # Mostrar las imágenes en etiquetas dentro del marco
            label1 = ttk.Label(face_pair_frame, image=face1_tk, text="Rostro {} (Imagen 1)".format(i + 1), compound=tk.TOP)
            label1.image = face1_tk
            label1.pack(side=tk.LEFT)

            label2 = ttk.Label(face_pair_frame, image=face2_tk, text="Rostro {} (Imagen 2)".format(i + 1), compound=tk.TOP)
            label2.image = face2_tk
            label2.pack(side=tk.LEFT)

            # Crear una variable para el estado del checkbox
            checkbox_var = tk.BooleanVar(value=False)
            checkbox_vars.append(checkbox_var)

            # Agregar un checkbox para seleccionar la pareja de rostros
            checkbox = ttk.Checkbutton(face_pair_frame, text="Seleccionar", variable=checkbox_var, command=lambda i=i: on_checkbox_change(i))
            checkbox.pack(side=tk.LEFT)
        


    def show_buttons(self):
        # Mostrar el botón "Regresar"
        return_button = ttk.Button(self.root, text="Regresar", command=self.return_pressed)
        return_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Mostrar el botón "Reclasificar"
        self.reclassify_button = ttk.Button(self.root, text="Reclasificar", command=self.reclassify_pressed, state=tk.DISABLED)
        self.reclassify_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Mostrar el botón "Continuar"
        continue_button = ttk.Button(self.root, text="Continuar", command=self.continue_pressed)
        continue_button.pack(side=tk.LEFT, padx=10, pady=10)


    def continue_pressed(self):
        gender_classifier_window = tk.Toplevel(self.root)
        faces=self.merge_faces_to_unique()
        self.root.withdraw()
        app = GenderClassifierWindow(gender_classifier_window, faces)

    def return_pressed(self):
        # Agregar aquí la lógica para regresar a la ventana anterior
        pass

    def reclassify_pressed(self):
        if self.reclassify_count < 2:  # Verificar si el botón aún puede ser presionado
            self.reclassify_count += 1
            
            self.reclassify_button.config(state=tk.DISABLED)
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
    
            # Ocultar los widgets actuales en el marco de los rostros emparejados
            for widget in self.root.winfo_children():
                widget.pack_forget()
            
            
           
            
            print(len(marked_pairs))  # Imprime la cantidad de elementos en marked_pairs
            if len(marked_pairs) > 0:
                print("marked_pairs tiene información")
            else:
                print("marked_pairs está vacío")
            
            #selected_faces_image1.extend(self.unique_faces)
            #Llamar a la función CompareFaces para reclasificar las caras seleccionadas
            self.faces_to_show, self.unique_faces = detect.ReclassifyFaces(selected_faces_image1, selected_faces_image2, self.unique_faces, marked_pairs)
    
            # Llamar a la función show_detected_faces para mostrar los rostros emparejados reclasificados
            self.show_detected_faces(self.faces_to_show, self.checkbox_vars)  # Pasar checkbox_vars al método
    
            # Mostrar los botones "Regresar" y "Reclasificar"
            self.show_buttons()
            
            
        # Actualizar el estado del botón si ya se ha presionado dos veces
        if self.reclassify_count == 2:
            self.unique_faces.extend([face2 for _, face2 in self.faces_to_show])
            #self.unique_faces.extend([face1 for face1, face2 in self.faces_to_show])
            self.reclassify_button.config(state=tk.DISABLED)
            self.root.after(100, self.continue_pressed)            
            
        
    def merge_faces_to_unique(self):
        for face1, _ in self.faces_to_show:
            self.unique_faces.append(face1)
        return self.unique_faces








"""











