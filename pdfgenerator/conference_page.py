# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 11:34:20 2023

@author: akava
"""

import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Image, Spacer, Table, TableStyle, Paragraph
from tkinter import filedialog
import matplotlib.pyplot as plt
from io import BytesIO
import re
from tkcalendar import DateEntry
import sqlite3
import openpyxl

class ConferenceWindow:
    def __init__(self, num_men, num_women):
        #self.Gender = Gender
        self.root = tk.Toplevel()
        self.root.title("Registro de Evento")
        self.root.resizable(False, False)
        self.nuevo_id = 0
        #self.root.geometry("800x600")  # Tamaño de la ventana
      
        
        self.num_men = num_men
        self.num_women = num_women
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear un Frame para los labels y entrys
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Crear un Frame para los botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=20, pady=20)
        
        self.name_label = tk.Label(input_frame, text="Evento o conferencia:")
        self.name_label.grid(row=0, column=0, sticky="w", pady=10)
        self.name_entry = tk.Entry(input_frame, width=50)
        self.name_entry.grid(row=0, column=1, sticky="w", pady=10)

        self.speakers_label = tk.Label(input_frame, text="Nombre del exponente:")
        self.speakers_label.grid(row=1, column=0, sticky="w", pady=10)
        self.speakers_entry = tk.Entry(input_frame, width=50)
        self.speakers_entry.grid(row=1, column=1, sticky="w", pady=10)

        self.location_label = tk.Label(input_frame, text="Localización del evento:")
        self.location_label.grid(row=2, column=0, sticky="w", pady=10)
        self.location_entry = tk.Entry(input_frame, width=50)
        self.location_entry.grid(row=2, column=1, sticky="w", pady=10)

        self.date_label = tk.Label(input_frame, text="Fecha del evento:")
        self.date_label.grid(row=3, column=0, sticky="w", pady=10)

        self.date_cal =DateEntry(input_frame, date_pattern="yy/MM/dd")
        self.date_cal.grid(row=3, column=1, sticky="w", pady=10)
        
        # Botones para Guardar y regresar en el Frame de los botones
        save_button = ttk.Button(button_frame, text="Guardar", command=self.create_button_clicked, width=15)
        save_button.pack(padx=10, pady=10, anchor=tk.E)
        
        back_button = ttk.Button(button_frame, text="Regresar", command=self.go_back, width=15)
        back_button.pack(padx=10, pady=10, anchor=tk.E)
 
        
    def create_button_clicked(self):
        
        conference_name = self.name_entry.get()
        speakers_names = self.speakers_entry.get()
        location = self.location_entry.get()
        date = self.date_cal.get_date() 
        asistentes_hombres = self.num_men  
        asistentes_mujeres = self.num_women  

        missing_fields = []
    
        if not conference_name:
            missing_fields.append("Nombre del evento o conferencia")
        if not speakers_names:
            missing_fields.append("Nombre del exponente")
        if not location:
            missing_fields.append("Localización del evento")
        if not date:
            missing_fields.append("Fecha del evento")
        
        if missing_fields:
            # Mostrar un mensaje de error si hay campos obligatorios vacíos
            messagebox.showerror("Campos Faltantes", f"Los siguientes campos son obligatorios:\n\n{', '.join(missing_fields)}")
        else:
            try:
                # Conectar a la base de datos
                #conn = sqlite3.connect("database/eventos.db")
                conn = sqlite3.connect("C:/Users/akava/OneDrive/Desktop/NuevoModular/database/eventos.db")
    
                cursor = conn.cursor()
    
                # Realizar la inserción de datos en la tabla "eventos"
                cursor.execute("INSERT INTO eventos (nombre_evento, nombres_exponentes, lugar_evento, fecha_evento, asistentes_hombres, asistentes_mujeres) VALUES (?, ?, ?, ?, ?, ?)",
                               (conference_name, speakers_names, location, date, asistentes_hombres, asistentes_mujeres))
                
                
                # Obtener el ID del elemento recién insertado
                self.nuevo_id = cursor.lastrowid
                
                # Confirmar la inserción y cerrar la conexión a la base de datos
                conn.commit()
                conn.close()
    
                # Mostrar un mensaje de éxito
                #messagebox.showinfo("Éxito", "Dato guardado correctamente en la base de datos.")
                self.show_confirmation_window()
    
            except sqlite3.Error as e:
                # Si ocurre un error al conectar o insertar datos, se capturará aquí
                print("Error al conectar a la base de datos o insertar datos:", e)
 
  
    def go_back(self):
        # Hacer que la ventana anterior vuelva a ser visible
        #self.Gender.deiconify()
        # Cerrar la ventana actual
        self.root.destroy()
    


    def show_confirmation_window(self):
        self.root.destroy()
        confirmation_window = tk.Toplevel()
        confirmation_window.title("EventAI")
    
        # Add a message label
        message_label = ttk.Label(confirmation_window, text="Datos almacenados correctamente.")
        message_label.pack(padx=20, pady=20)
    
        # Add a label for the buttons
        option_label = ttk.Label(confirmation_window, text="Crear archivo:")
        option_label.pack(padx=20, pady=10)
    
        # Add buttons
        pdf_button = ttk.Button(confirmation_window, text="PDF", command=lambda:self.create_pdf_report(self.nuevo_id))
        pdf_button.pack(pady=10)
        excel_button = ttk.Button(confirmation_window, text="Excel", command=lambda:self.create_excel_report(self.nuevo_id))
        excel_button.pack(pady=10)
    
  
        tk.Label(confirmation_window, text="").pack()
    
        # Add a button to return to the main menu
        return_to_main_menu_button = ttk.Button(confirmation_window, text="Menú principal", command=self.return_to_main_menu)
        return_to_main_menu_button.pack(pady=10)
    
        # Show the confirmation window
        confirmation_window.mainloop()
    
    

    def create_excel_report(self, evento_id):
        self.evento_id=evento_id
        # Preguntar al usuario la ubicación y nombre del archivo
        
        try:
            # Conectar a la base de datos y obtener información del evento por su ID
            conn = sqlite3.connect("C:/Users/akava/OneDrive/Desktop/NuevoModular/database/eventos.db")
            cursor = conn.cursor()

            # Realizar una consulta para obtener información del evento por su ID
            query =" SELECT nombre_evento, fecha_evento, asistentes_hombres, asistentes_mujeres FROM eventos WHERE id = ?"
            cursor.execute(query, (evento_id,))
            event_data = cursor.fetchone()

            # Cerrar la conexión a la base de datos
            conn.close()

            if not event_data:
                # El evento con el ID especificado no existe
                messagebox.showerror("Error", "El evento no existe.")
                return

            # Desempaquetar los datos del evento
            conference_name, date, num_men, num_women = event_data
                    

            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], initialfile="EventAI")
        
            if not file_path:  # El usuario canceló la selección
                return
        
            # Crear un nuevo libro de trabajo de Excel
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            
            # Configurar los encabezados
            headers = ["Evento", "Fecha", "Asistentes", "Hombres", "Mujeres"]
            sheet.append(headers)
            
            asistentes = event_data[2]+event_data[3]
            row = [event_data[0], event_data[1], asistentes, event_data[2],event_data[3]]
            sheet.append(row)
            
            # Guardar el archivo de Excel en la ubicación proporcionada
            workbook.save(file_path)
            
            tk.messagebox.showinfo("Excel Exportado", f"Los datos se han exportado a '{file_path}'")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error al exportar a Excel: {str(e)}")
    
    def return_to_main_menu(self):
        pass


    def create_pdf_report(self, evento_id):
        self.evento_id=evento_id
        try:
            # Conectar a la base de datos y obtener información del evento por su ID
            conn = sqlite3.connect("C:/Users/akava/OneDrive/Desktop/NuevoModular/database/eventos.db")
            cursor = conn.cursor()

            # Realizar una consulta para obtener información del evento por su ID
            query =" SELECT nombre_evento, nombres_exponentes, lugar_evento, fecha_evento, asistentes_hombres, asistentes_mujeres FROM eventos WHERE id = ?"
            cursor.execute(query, (evento_id,))
            #cursor.execute("SELECT nombre_evento, nombres_exponentes, lugar_evento, fecha_evento, asistentes_hombres, asistentes_mujeres FROM eventos")
            event_data = cursor.fetchone()

            # Cerrar la conexión a la base de datos
            conn.close()

            if not event_data:
                # El evento con el ID especificado no existe
                messagebox.showerror("Error", "El evento no existe.")
                return

            # Desempaquetar los datos del evento
            conference_name, speakers_names, location, date, num_men, num_women = event_data
            
            
            
            conference_filename = conference_name.replace(" ", "_").lower()
            doc = SimpleDocTemplate(conference_filename, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=54, bottomMargin=54)

            # Usar filedialog para que el usuario seleccione la ubicación y el nombre del archivo
            output_filepath = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile=conference_filename, title="Guardar PDF")

            if not output_filepath:  # El usuario canceló la selección
                return

            doc = SimpleDocTemplate(output_filepath, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=54, bottomMargin=54)
            story = []
            styles = getSampleStyleSheet()
            title_style = styles["Title"]

            # Crear un estilo centrado para el subtítulo
            center_subtitle_style = styles["Normal"].clone("center_subtitle_style")
            center_subtitle_style.alignment = 1  # Center alignment
            center_subtitle_style.fontName = "Helvetica-Bold"  # Cambia la fuente a negritas
            center_subtitle_style.fontSize = 14
                 
            university_logo = "logo_udg.jpg"
            department_logo = "logo_cucei.png"
        
            university_image = Image(university_logo, width=90, height=90)
            department_image = Image(department_logo, width=70, height=90)
        
            # Create a table to align the logos
            logo_table = Table([[university_image, department_image]], colWidths=[150, 380])
            logo_table.setStyle(TableStyle([('ALIGN', (0, 0), (0, 0), 'LEFT'),
                                            ('ALIGN', (1, 0), (1, 0), 'RIGHT')]))
        
            title = "UNIVERSIDAD DE GUADALAJARA"
            subtitle = "CENTRO UNIVERSITARIO DE CIENCIAS EXACTAS E INGENIERÍAS"
        
            # Define el estilo para la primera columna (negritas y tamaño 14)
            first_column_style = styles["Normal"].clone("first_column_style")
            first_column_style.fontName = "Helvetica-Bold"  # Cambia la fuente a negritas
            first_column_style.fontSize = 12  # Cambia el tamaño de la fuente
            first_column_style.alignment = 0  # Alineación a la izquierdable_style.leading = 16  # Espacio entre líneas
    
        
            event_table = Table([
                [],
                [Paragraph("<b>Evento:</b>", first_column_style), conference_name],
                [Paragraph("<b>Exponente:</b>", first_column_style), speakers_names],
                [Paragraph("<b>Lugar del evento:</b>", first_column_style),  location],
                [Paragraph("<b>Total de asistentes:</b>", first_column_style), num_men+num_women],
                [Paragraph("<b>Fecha del evento:</b>", first_column_style),  date],
            ], colWidths=[150, 200])
        
            event_table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente negrita para la primera fila
                ('FONT', (0, 1), (-1, -1), 'Helvetica', 12),  # Fuente tamaño 14 para las otras celdas
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Alineación a la izquierda
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alineación vertical al centro
            ]))

            # Crear la gráfica de pastel con Matplotlib
            data = [num_men, num_women]
            labels = ["Hombres", "Mujeres"]
            colors = ['#4C8FD6', '#FF8EB0']

            plt.figure(figsize=(6, 6))  # Aumentar el tamaño de la gráfica
            wedges, texts, autotexts = plt.pie(data, labels=labels, colors=colors, autopct=lambda p: '{:.0f} ({:.1f}%)'.format(p * sum(data) / 100, p))
            plt.title('Distribución de Asistentes', fontsize=14, fontweight='bold')

            for autotext in autotexts:
                autotext.set_fontsize(12)  # Tamaño de fuente para los porcentajes
                autotext.set_color('white')  # Color de fuente en blanco

            # Guardar la gráfica en un objeto BytesIO
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()

            # Crear la imagen a partir del contenido del objeto BytesIO
            pie_chart_image = Image(buffer, width=350, height=350)  # Aumentar el tamaño de la imagen

            content = [
                logo_table,
                Paragraph(title, title_style),
                Paragraph(subtitle, center_subtitle_style),
                Spacer(1, 24),
                event_table,
                Spacer(1, 36),  # Espacio antes de la gráfica de pastel
                pie_chart_image,  # Agregar la gráfica de pastel
            ]

            story.extend(content)
            doc.build(story)
            messagebox.showinfo("Archivo Creado", "El archivo PDF se ha creado exitosamente.")

        except sqlite3.Error as e:
            # Si ocurre un error al conectar o insertar datos, se capturará aquí
            print("Error al conectar a la base de datos o insertar datos:", e)












    
"""
        
    def generate_report(self):
        conference_name = self.name_entry.get()
        speakers_names = self.speakers_entry.get()
        location = self.location_entry.get()
        date = self.date_cal.get_date()
        
        missing_fields = []
    
        if not conference_name:
            missing_fields.append("Nombre del evento o conferencia")
        if not speakers_names:
            missing_fields.append("Nombre del exponente")
        if not location:
            missing_fields.append("Localización del evento")
        if not date:
            missing_fields.append("Fecha del evento")
        
        if missing_fields:
            # Mostrar un mensaje de error si hay campos obligatorios vacíos
            messagebox.showerror("Campos Faltantes", f"Los siguientes campos son obligatorios:\n\n{', '.join(missing_fields)}")
        else:
            # Llamar a la función para crear el informe solo si todos los campos están completos
            self.create_pdf_report(conference_name, speakers_names, location, date, self.num_men, self.num_women)

 
    

    def create_pdf_report():
        
        conference_filename = conference_name.replace(" ", "_").lower() + ".pdf"
        doc = SimpleDocTemplate(conference_filename, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=54, bottomMargin=54)
        
        # Usar filedialog para que el usuario seleccione la ubicación y el nombre del archivo
        output_filepath = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile=conference_filename, title="Guardar PDF")
        
        if not output_filepath:  # El usuario canceló la selección
            return
        
        doc = SimpleDocTemplate(output_filepath, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=54, bottomMargin=54)
        story = []
        styles = getSampleStyleSheet()
        title_style = styles["Title"]
        
        # Crear un estilo centrado para el subtítulo
        center_subtitle_style = styles["Normal"].clone("center_subtitle_style")
        center_subtitle_style.alignment = 1  # Center alignment
        center_subtitle_style.fontName = "Helvetica-Bold"  # Cambia la fuente a negritas
        center_subtitle_style.fontSize = 14
             
        university_logo = "logo_udg.jpg"
        department_logo = "logo_cucei.png"
    
        university_image = Image(university_logo, width=90, height=90)
        department_image = Image(department_logo, width=70, height=90)
    
        # Create a table to align the logos
        logo_table = Table([[university_image, department_image]], colWidths=[150, 380])
        logo_table.setStyle(TableStyle([('ALIGN', (0, 0), (0, 0), 'LEFT'),
                                        ('ALIGN', (1, 0), (1, 0), 'RIGHT')]))
    
        title = "UNIVERSIDAD DE GUADALAJARA"
        subtitle = "CENTRO UNIVERSITARIO DE CIENCIAS EXACTAS E INGENIERÍAS"
    
        # Define el estilo para la primera columna (negritas y tamaño 14)
        first_column_style = styles["Normal"].clone("first_column_style")
        first_column_style.fontName = "Helvetica-Bold"  # Cambia la fuente a negritas
        first_column_style.fontSize = 12  # Cambia el tamaño de la fuente
        first_column_style.alignment = 0  # Alineación a la izquierdable_style.leading = 16  # Espacio entre líneas

    
        event_table = Table([
            [],
            [Paragraph("<b>Evento:</b>", first_column_style), conference_name],
            [Paragraph("<b>Exponente:</b>", first_column_style), speakers_names],
            [Paragraph("<b>Lugar del evento:</b>", first_column_style),  location],
            [Paragraph("<b>Total de asistentes:</b>", first_column_style), num_men+num_women],
            [Paragraph("<b>Fecha del evento:</b>", first_column_style),  date],
        ], colWidths=[150, 200])
    
        event_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente negrita para la primera fila
            ('FONT', (0, 1), (-1, -1), 'Helvetica', 12),  # Fuente tamaño 14 para las otras celdas
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Alineación a la izquierda
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alineación vertical al centro
        ]))
    
        # Crear la gráfica de pastel con Matplotlib
        data = [num_men, num_women]
        labels = ["Hombres", "Mujeres"]
        colors = ['#4C8FD6', '#FF8EB0']
        
        plt.figure(figsize=(6, 6))  # Aumentar el tamaño de la gráfica
        wedges, texts, autotexts = plt.pie(data, labels=labels, colors=colors, autopct=lambda p: '{:.0f} ({:.1f}%)'.format(p * sum(data) / 100, p))
        plt.title('Distribución de Asistentes', fontsize=14, fontweight='bold')
        
        for autotext in autotexts:
            autotext.set_fontsize(12)  # Tamaño de fuente para los porcentajes
            autotext.set_color('white')  # Color de fuente en blanco
            #autotext.set_weight('bold')  # Fuente en negritas
        
        # Guardar la gráfica en un objeto BytesIO
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()
        
        # Crear la imagen a partir del contenido del objeto BytesIO
        pie_chart_image = Image(buffer, width=350, height=350)  # Aumentar el tamaño de la imagen
    
        content = [
            logo_table,
            Paragraph(title, title_style),
            Paragraph(subtitle, center_subtitle_style),
            Spacer(1, 24),
            event_table,
            Spacer(1, 36),  # Espacio antes de la gráfica de pastel
            pie_chart_image,  # Agregar la gráfica de pastel
        ]
    
        story.extend(content)
        doc.build(story)
        messagebox.showinfo("Archivo Creado", "El archivo PDF se ha creado exitosamente.")

"""
if __name__ == "__main__":
    # Crea una instancia de la clase ConferenceWindow
    app = ConferenceWindow(50, 50)
    # Inicia el bucle principal de la aplicación tkinter
    app.root.mainloop()