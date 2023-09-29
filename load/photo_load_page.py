# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 11:37:27 2023

@author: akava
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from detection.two_photos_detection_page import TwoPhotosDetectionPage
from detection.single_photo_detection_page import SinglePhotoDetectionPage

class PhotoLoadPage:
    def __init__(self, App):
        self.App = App
        self.root = tk.Toplevel()
        self.root.title("Pagina de Carga de Fotos")
        self.root.resizable(False, False)
        #self.root.geometry("800x600")  # Tamaño de la ventana

        # Variables para las imágenes
        self.image1_path = tk.StringVar()
        self.image2_path = tk.StringVar()
        self.show_additional_elements = tk.BooleanVar()

        # Crear una variable para almacenar la opción seleccionada
        self.selected_option = tk.StringVar(self.root)
        self.selected_option.set("alto")  # Valor predeterminado

        # Etiqueta y botón para cargar la imagen
        load_label = tk.Label(self.root, text="Cargar imagen 1:")
        load_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        self.image_label = tk.Label(self.root, textvariable=self.image1_path, relief="groove", width=50)
        self.image_label.grid(row=0, column=1, padx=10, pady=20, sticky="w")

        # Elemento para cargar una imagen
        self.load_image_button = ttk.Button(self.root, text="Cargar", command=self.load_image)
        self.load_image_button.grid(row=0, column=2, padx=10, pady=20)

        # Checkbox para mostrar opciones adicionales
        self.show_options_checkbox = ttk.Checkbutton(self.root, text="Mostrar opciones adicionales", variable=self.show_additional_elements, command=self.toggle_options)
        self.show_options_checkbox.grid(row=1, columnspan=3, padx=20, pady=10, sticky="w")

        # Etiqueta y botón para cargar la segunda imagen (ocultos inicialmente)
        self.load_label2 = tk.Label(self.root, text="Cargar imagen 2:")
        self.image2_label = tk.Label(self.root, textvariable=self.image2_path, relief="groove", width=50)
        self.load_image2_button = ttk.Button(self.root, text="Cargar", command=self.load_image2)

        # Botones Cerrar y Continuar
        self.button_frame = tk.Frame(self.root)
        self.button_frame.grid(row=3, column=1, columnspan=3, padx=0, pady=20, sticky="e")

        self.continue_button = ttk.Button(self.button_frame, text="Continuar", command=self.continue_pressed)
        self.continue_button.pack(side="right", padx=10)

        self.close_button = ttk.Button(self.button_frame, text="Cerrar", command=self.close_window)
        self.close_button.pack(side="right")

    def toggle_options(self):
        if self.show_additional_elements.get():
            self.load_label2.grid(row=2, column=0, padx=20, pady=10, sticky="w")
            self.image2_label.grid(row=2, column=1, padx=10, pady=10, sticky="w", columnspan=2)
            self.load_image2_button.grid(row=2, column=2, padx=10, pady=10, sticky="w")
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
                app = TwoPhotosDetectionPage(self.root, self.image1_path.get(), self.image2_path.get(), options)
                #self.root.withdraw()
            else:
                messagebox.showerror("Error", "Por favor, carga ambas imágenes antes de continuar.")
        else:
            if self.image1_path.get():
                #self.root.withdraw()
                options = self.selected_option.get()
                #second_window = tk.Toplevel(self.root)
                app = SinglePhotoDetectionPage(self.root, self.image1_path.get(), options)
            else:
                messagebox.showerror("Error", "Por favor, carga al menos una imagen antes de continuar.")
                
              
    def close_window(self):
        # Cierra la ventana de PhotoLoadPage
        self.root.destroy()

        # Restaura la ventana principal
        self.App.deiconify()