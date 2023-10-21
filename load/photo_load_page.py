# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 11:37:27 2023

@author: akava
"""

import tkinter as tk
from tkinter import ttk
import customtkinter
from tkinter import filedialog
from tkinter import messagebox
from detection.two_photos_detection_page import TwoPhotosDetectionPage
from detection.single_photo_detection_page import SinglePhotoDetectionPage
from PIL import Image

class PhotoLoadPage:
    def __init__(self, App, root):
        self.App = App
        self.App_window = root
        self.root = customtkinter.CTkToplevel()
        self.root.title("Pagina de Carga de Fotos")
        self.root.resizable(False, False)
        #self.root.geometry("800x600")  # Tamaño de la ventana
        
        # Configurar el evento de cierre de la ventana secundaria
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        # Variables para las imágenes
        self.image1_path = tk.StringVar()
        self.image2_path = tk.StringVar()
        self.show_additional_elements = tk.BooleanVar()

        # Crear una variable para almacenar la opción seleccionada
        self.selected_option = tk.StringVar(self.root)
        self.selected_option.set("alto")  # Valor predeterminado

        # Etiqueta y botón para cargar la imagen
        load_image = customtkinter.CTkImage(Image.open("images/imagen.png"), size=(26, 26))
        load_label = customtkinter.CTkLabel(self.root, text="  Imagen 1:", font=('Calibri', 15), image=load_image, compound=tk.LEFT)
        load_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        self.image_label = customtkinter.CTkLabel(self.root, textvariable=self.image1_path, width=450, font=('Calibri', 15),  fg_color="white", corner_radius= 8)
        self.image_label.grid(row=0, column=1, padx=10, pady=10,)

        # Elemento para cargar una imagen
        cargar_image = customtkinter.CTkImage(Image.open("images/imagen.png"), size=(26, 26))
        self.load_image_button = customtkinter.CTkButton(self.root, text="Cargar", command=self.load_image, image= cargar_image, text_color= "black", fg_color="transparent")
        self.load_image_button.grid(row=0, column=2, padx=10, pady=10)


        # Checkbox para mostrar opciones adicionales
        self.show_options_checkbox = customtkinter.CTkCheckBox(self.root, text="Opciones adicionales", font=('Calibri', 15), variable=self.show_additional_elements, command=self.toggle_options)
        self.show_options_checkbox.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        # Etiqueta y botón para cargar la segunda imagen (ocultos inicialmente)
        self.load_label2 = customtkinter.CTkLabel(self.root, text="  Imagen 2:", font=('Calibri', 15), image=load_image, compound=tk.LEFT)
        self.image2_label = customtkinter.CTkLabel(self.root, textvariable=self.image2_path, width=450, font=('Calibri', 15),  fg_color="white", corner_radius= 8)
        self.load_image2_button = customtkinter.CTkButton(self.root, text="Cargar", command=self.load_image2, image= cargar_image, text_color= "black", fg_color="transparent")

        # Botones Cerrar y Continuar
        self.button_frame = customtkinter.CTkFrame(self.root, fg_color="transparent")
        self.button_frame.grid(row=3, column=1, columnspan=3, padx=0, pady=20, sticky="e")

        close_image = customtkinter.CTkImage(Image.open("images/volver.png"), size=(26, 26))
        self.close_button = customtkinter.CTkButton(self.button_frame, text="Regresar", command=self.close_window, image= close_image, text_color= "black", fg_color="transparent")
        self.close_button.pack(side="right")
        
        continue_image = customtkinter.CTkImage(Image.open("images/aceptar.png"), size=(26, 26))
        self.continue_button = customtkinter.CTkButton(self.button_frame, text="Aceptar", command=self.continue_pressed, image= continue_image, text_color= "black", fg_color="transparent")
        self.continue_button.pack(side="right")

    def toggle_options(self):
        if self.show_additional_elements.get():
            self.load_label2.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
            self.image2_label.grid(row=2, column=1, padx=10, pady=10)
            self.load_image2_button.grid(row=2, column=2, padx=10, pady=10)
        else:
            self.load_label2.grid_forget()
            self.image2_label.grid_forget()
            self.load_image2_button.grid_forget()

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Imagenes", "*.jpg *.png *.jpeg")])
        if file_path:
            self.image1_path.set(file_path)

    def load_image2(self):
        file_path = filedialog.askopenfilename(filetypes=[("Imagenes", "*.jpg *.png *.jpeg")])
        if file_path:
            self.image2_path.set(file_path)
    
    def continue_pressed(self):
        pass

        if self.show_additional_elements.get():
            if self.image1_path.get() and self.image2_path.get():
                
                options = self.selected_option.get()
                app = TwoPhotosDetectionPage(self.root, self.App, self.App_window, self.image1_path.get(), self.image2_path.get(), options)
                #self.root.withdraw()
            else:
                messagebox.showerror("Error", "Por favor, carga ambas imágenes antes de continuar.")
        else:
            if self.image1_path.get():
                #self.root.withdraw()
                options = self.selected_option.get()
                #second_window = tk.Toplevel(self.root)
                app = SinglePhotoDetectionPage(self.root, self.App, self.App_window, self.image1_path.get(), options)
            else:
                messagebox.showerror("Error", "Por favor, carga al menos una imagen antes de continuar.")
                
              
    def close_window(self):
        # Cierra la ventana de PhotoLoadPage
        self.root.destroy()
        # Restaura la ventana principal
        self.App_window.deiconify()
        
    def on_closing(self):
        # Restaura la ventana principal
        self.App_window.deiconify()
        
        # Cierra la ventana de PhotoLoadPage
        self.root.destroy()
        