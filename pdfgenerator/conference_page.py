# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 11:34:20 2023

@author: akava
"""

import tkinter as tk
from tkinter import ttk
#from tkcalendar import Calendar
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Image, Spacer, Table, TableStyle, Paragraph
from tkinter import filedialog
import matplotlib.pyplot as plt
from io import BytesIO


class ConferenceWindow:
    def __init__(self, Gender, num_men, num_women):
        self.Gender = Gender
        self.root = tk.Toplevel()
        self.root.title("Registro de Evento")
        self.root.resizable(False, False)
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

        self.date_entry = tk.Entry(input_frame)
        self.date_entry.grid(row=3, column=1, sticky="w", pady=10)
        #self.date_entry.bind("<Button-1>", self.show_calendar)

        #self.date_cal = Calendar(input_frame, selectmode="day")
        #self.date_cal.grid(row=3, column=1, sticky="w", pady=10)
        #self.date_cal.grid_remove()
        #self.date_cal.bind("<<CalendarSelected>>", self.update_date_entry)

        self.time_label = tk.Label(input_frame, text="Hora de inicio (hh:mm):")
        self.time_label.grid(row=4, column=0, sticky="w", pady=10)

        self.time_entry = tk.Entry(input_frame)
        self.time_entry.grid(row=4, column=1, sticky="w", pady=10)
        #self.time_entry.bind("<KeyRelease>", self.validate_time_entry)

        # Botones para continuar y regresar en el Frame de los botones
        continue_button = ttk.Button(button_frame, text="Generar Reporte", command=self.generate_report, width=15)
        continue_button.pack(padx=10, pady=10, anchor=tk.E)

        back_button = ttk.Button(button_frame, text="Regresar", command=self.go_back, width=15)
        back_button.pack(padx=10, pady=10, anchor=tk.E)
        
        
        
    def generate_report(self):
  
        
        conference_name = self.name_entry.get()
        speakers_names = self.speakers_entry.get()
        location = self.location_entry.get()
        date = self.date_entry.get()
        time = self.time_entry.get()
        
        """
        missing_fields = []

        if not conference_name:
            missing_fields.append("Nombre del evento o conferencia")
        if not speakers_names:
            missing_fields.append("Nombre del exponente")
        if not location:
            missing_fields.append("Localización del evento")
        if not date:
            missing_fields.append("Fecha del evento")
        if not time:
            missing_fields.append("Hora de inicio")

        if missing_fields:
            messagebox.showerror("Campos Faltantes", f"Los siguientes campos son obligatorios:\n\n{', '.join(missing_fields)}")
        else:
            """
        self.create_pdf_report(conference_name, speakers_names, location, date, time, self.num_men, self.num_women)
       
 

    
    def go_back(self):
        # Hacer que la ventana anterior vuelva a ser visible
        self.Gender.deiconify()
        # Cerrar la ventana actual
        self.root.destroy()
    """
    def show_calendar(self, event):
        if not self.date_cal.winfo_ismapped():  # Check if the calendar is not shown
            self.date_cal.grid()  # Show the calendar
    """
    def update_date_entry(self, event):
        selected_date = self.date_cal.get_date()
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, selected_date)
        self.date_cal.grid_remove()  # Hide the calendar after selection

    def validate_time_entry(self, event):
        input_text = self.time_entry.get()
        valid_format = len(input_text) <= 5 and input_text.count(':') == 1
        if valid_format:
            hours, minutes = map(int, input_text.split(':'))
            valid_values = 0 <= hours <= 23 and 0 <= minutes <= 59
            if valid_values:
                self.time_entry.config(foreground="black")
            else:
                self.time_entry.config(foreground="red")
        else:
            self.time_entry.config(foreground="red")

    def create_pdf_report(self, conference_name, speakers_names, location, date, time, num_men, num_women):
        
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
            [Paragraph("<b>Hora de inicio:</b>", first_column_style), time]
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
            Spacer(1, 12),  # Espacio antes de la gráfica de pastel
            pie_chart_image,  # Agregar la gráfica de pastel
            # Agrega más contenido aquí...
        ]
    
        story.extend(content)
        doc.build(story)
        messagebox.showinfo("Archivo Creado", "El archivo PDF se ha creado exitosamente.")


