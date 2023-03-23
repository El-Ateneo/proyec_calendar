import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkcalendar import Calendar
from tkinter.ttk import Combobox
from tkinter import messagebox
from datetime import datetime, timedelta
import json




class Calend(ttk.Frame):
    def __init__(self, master= None):
        self.master = master
        #self.master.geometry()
         #Título de la ventana
        self.master.title("MI CALENDARIO PERSONAL")
        
        
        #cuadros frame 1
        self.frame1= tk.Frame(self.master, bg= "lemon chiffon",  border=2, relief= "groove")
        self.titt= tk.Label(self.frame1, text= "Vista Mensual", fg='red', bg='cyan').pack(padx=20, pady=20)

        # Add Calendar
        #self.desabilitar_campos()
        
        self.cal = Calendar(self.frame1, selectmode = 'day',
                    year = 2023, month = 5,
                    day = 22, borderwidth= 5,
                    firstweekday= 'sunday', font= 'Arial 15 bold', bordercolor= 'red',background= 'PURPLE',
                    headersforeground= '#330033', headersbackground= '#CCCC99', othermonthforeground= '#00CCFF',
                    othermonthweforeground= '#00CCFF')
        
        self.cal.pack(padx=20, pady=20)
        self.cal.bind("<<CalendarSelected>>",self.seleccion)
        
        self.date_entry= self.cal.get_date()
                
        #self.date_entry= Label(root, text = "")
        #self.date_entry.pack(pady = 20)

        self.create_button = tk.Button(self.frame1, text=" Eventos del Dia ", command= self.create_ventana)
        self.create_button.pack(padx=20, pady=20)
        self.create_button.config(cursor= 'hand2')

        # Cerrar la ventana de eventos
          
        self.quit_button = tk.Button(self.frame1, text="Salir", command=self.master.quit)
        self.quit_button.pack(padx=10, pady=10)
        self.quit_button.config(cursor= 'hand2')

        self.frame1.config(width="300", height="800")
        self.frame1.pack(expand=True, fill='both',side=LEFT)
        self.frame1.config(cursor= "circle")


        #frame 2
        self.frame2= tk.Frame(self.master, bg= "SpringGreen2", border=2, relief= "groove")
        self.tit= tk.Label(self.frame2, text= "Vista semanal",fg='red4', bg='orange').pack(padx=20,pady=20)

        #Eventos de la semana

        self.columnas = ('dom', 'lun', 'mar', 'mier', 'jue', 'vier','sab')
        self.tab_sem= ttk.Treeview(self.frame2, columns=self.columnas, show= 'headings', height= '10')
        
        self.tab_sem.column('dom', width=80,anchor=CENTER)
        self.tab_sem.column('lun', width=80,anchor=CENTER)
        self.tab_sem.column('mar', width=80,anchor=CENTER)
        self.tab_sem.column('mier', width=80,anchor=CENTER)
        self.tab_sem.column('jue', width=80,anchor=CENTER)
        self.tab_sem.column('vier', width=80,anchor=CENTER)
        self.tab_sem.column('sab', width=80,anchor=CENTER)

        self.tab_sem.heading('dom', tex= 'Domingo',anchor=CENTER)
        self.tab_sem.heading('lun', tex= 'Lunes',anchor=CENTER)
        self.tab_sem.heading('mar', tex= 'Martes',anchor=CENTER)
        self.tab_sem.heading('mier', tex= 'Miercoles',anchor=CENTER)
        self.tab_sem.heading('jue', tex= 'Jueves',anchor=CENTER)
        self.tab_sem.heading('vier', tex= 'Viernes',anchor=CENTER)
        self.tab_sem.heading('sab', tex= 'Sabado',anchor=CENTER)
        self.tab_sem.pack(padx=20, pady=20)
        self.tab_sem.config(cursor= 'hand2')

       
        

        self.frame2.pack(expand=True, fill='both', side=RIGHT)
        self.frame2.config(cursor= "gumby")
        self.frame2.config(width="500", height="800")

    def seleccion(self, event):
        self.date_entry= self.cal.get_date()
        print(self.date_entry)
    
#ventan del evento semanal
    def create_ventana(self):
        self.event_window = Toplevel(self.frame1)
        
        self.event_window.geometry("850x500")
        self.event_window.title("Eventos del Dia: " + self.date_entry)
         # Crear un Entry para ingresar el nuevo evento
        self.event_entry = Entry(self.event_window)

        #tabla de eventos del día
        
        self.tabla= ttk.Treeview(self.event_window, columns=('hora','evento', 'importancia', 'etiqueta'), show= 'headings', height= '5')
        self.tabla.grid(row=1, column=1, pady=10, padx=10)
        self.tabla.heading('hora', tex= 'Horario')
        self.tabla.heading('evento', tex= 'Evento')
        self.tabla.heading('importancia', tex= 'Importancia')
        self.tabla.heading('etiqueta', tex= 'Etiqueta')
        self.tabla.config(cursor= 'hand2')
        self.tabla.bind("<Double-Button-1>",self.doubleClickTabla)
        self.tabla.bind("<<TreeviewSelect>>", self.habilitar_campos)


        #Llama a las funcione creada  para leer el archivo JSON y mostrar los datos en el Treeview:
        
        self.mostrar_datos(self.tabla)

        
        # Crear un botón para crear el nuevo evento
        self.save_button = Button(self.event_window, text="Crear Nuevo Evento", command=self.vent_create__event)
        self.save_button.grid(row=2, column=1, pady=10, padx=10)
        self.save_button.config(cursor= 'hand2')

        # Crear un mensaje indicando como editar el evento
        
        self.edit_button= tk.Label(self.event_window, text= "Haga Doble Click sobre el evento para Editar", fg='red', bg='cyan')
        self.edit_button.grid(row=3, column= 1, pady=10, padx=10)
        self.edit_button.config(cursor= 'question_arrow')
        
        self.delete_button = tk.Button(self.event_window, text="Eliminar Evento", state="disabled", command=self.eliminar_evento)
        self.delete_button.grid(row=4, column=1, pady=10, padx=10)
        self.delete_button.config(cursor= 'hand2')

        self.cerrar_button = tk.Button(self.event_window, text="Cerrar", command=self.event_window.destroy)
        self.cerrar_button.grid(row=5, column=1, pady=10, padx=10)
        self.cerrar_button.config(cursor= 'hand2')
        
        
    def vent_create__event(self):
        self.evento_window = tk.Toplevel(self.master)
        self.evento_window.title("Agregar Evento")
        self.evento_window.geometry("300x400")
        

         # Crear campos de entrada
        self.title_label = tk.Label(self.evento_window, text="Título:")
        self.title_entry = tk.Entry(self.evento_window)
        
        self.fecha_label = tk.Label(self.evento_window, text="Fecha:")
        self.fech_entry = tk.Entry(self.evento_window)
        self.fech_entry.insert(0,self.date_entry)
        self.fech_entry.config(state= 'disable')

        self.date_label = tk.Label(self.evento_window, text="Hora:")
        self.date_enty = tk.Entry(self.evento_window)
        hora= ["00:00", "00:30", "01:00", "01:30", "02:00", "02:30", "03:00", "03:30", "04:00", "04:30", 
                "05:00", "05:30", "06:00", "06:30", "07:00", "07:30", "08:00","08:30", "09:00", "09:30", "10:00", 
                "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", 
                "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30", "20:00", "20:30", "21:00",
                "21:30", "22:00","22:30", "23:00", "23:30"]
        self.date_menu = Combobox(self.evento_window,values= hora, state= "readonly") 
        self.date_menu.set('17:30')

        self.duration_label = tk.Label(self.evento_window, text="Duración:")
        self.duration_entry = tk.Entry(self.evento_window)
        self.duration_entry.insert(0, "1")

        self.description_label = tk.Label(self.evento_window, text="Descripción:")
        self.description_entry = tk.Text(self.evento_window, width=20, height=4)

        self.importance_label = tk.Label(self.evento_window, text="Importancia:")
        self.importance_entry = tk.StringVar(self.evento_window)
        self.importance_entry.set("normal")
        self.importance_menu = tk.OptionMenu(self.evento_window, self.importance_entry, "normal", "importante")

        self.reminder_label = tk.Label(self.evento_window, text="Recordatorio:")
        self.reminder_entry = tk.Entry(self.evento_window)

        self.tags_label = tk.Label(self.evento_window, text="Etiquetas:")
        self.tags_entry = tk.Entry(self.evento_window)

        # Crear botones
        self.create_button = tk.Button(self.evento_window, text="Guardar", command=self.save_event)
        self.create_button.config( cursor= 'hand2')
        
        self.quit_button = tk.Button(self.evento_window, text="Salir", command=self.evento_window.destroy)
        self.quit_button.config(cursor= 'hand2')

        # Posicionar elementos en la ventana
        self.title_label.grid(row=0, column=0)
        self.title_entry.grid(row=0, column=1)

        self.fecha_label.grid(row=1, column=0)
        self.fech_entry.grid(row=1, column=1)
        
        self.date_label.grid(row=2, column=0)
        self.date_menu.grid(row=2, column=1)

        self.duration_label.grid(row=3, column=0)
        self.duration_entry.grid(row=3, column=1)

        self.description_label.grid(row=4, column=0)
        self.description_entry.grid(row=4, column=1)

        self.importance_label.grid(row=5, column=0)
        self.importance_menu.grid(row=5, column=1)

        self.reminder_label.grid(row=6, column=0)
        self.reminder_entry.grid(row=6, column=1)

        self.tags_label.grid(row=7, column=0)
        self.tags_entry.grid(row=7, column=1)

        self.create_button.grid(row=8, column=0)
        self.quit_button.grid(row=8, column=1)

          
        # Obtener la fecha del usuario (puede ser a través de un Entry)
        date = self.date_entry

        # Cargar los eventos del archivo json (si ya existen)
        with open('datos.json', 'r') as f:
            events = json.load(f)

            # Obtener los eventos del día seleccionado
            self.day_events = events[date] if date in events else []

         

    
    def save_event(self):
        # Obtener el evento ingresado por el usuario

        event = { # Crear campos de entrada
            "titulo": self.title_entry.get(),
            "fecha":self.date_entry,
            "hora":self.date_menu.get(),
            "duracion": self.duration_entry.get(),
            "descripcion":self.description_entry.get("1.0", "end"),
            "importancia":self.importance_entry.get(),
            "recordatorio":self.reminder_entry.get(),
            "etiquetas":self.tags_entry.get()

               }

        # Obtener la fecha del usuario
        date = self.date_entry
        datos = self.leer_archivo_json()

        if date not in datos:
            # Agregar el nuevo evento al día seleccionado
            datos.append(event)

        #extrae el diccionario a partir de la clave "fecha seleccionada" del evento
        self.datos_filtrados = [dato for dato in datos if dato['fecha'] == self.date_entry]

        #extrae la lista del diccionario a partir de la "Hora" del evento
        self.hora_selec= event["hora"]
        
        for dat in self.datos_filtrados:
            if self.hora_selec == dat['hora']:
                if messagebox.askyesno(message="Ya existe un evento a esa hora, ¿desea reemplazarlo?" ,title="Evento")==True:
                    # Guardar los eventos actualizados en el archivo json
                    datos.remove(dat)
                    
      
        if date not in datos:
            # Agregar el nuevo evento al día seleccionado
            datos.append(event)

        with open('datos.json', 'w') as f:
            json.dump(datos, f, indent=2)
            
        #actualiza el Treeview

        self.mostrar_datos(self.tabla)

        # Cerrar la ventana de eventos
        self.evento_window.destroy()

        # Muestra la ventana principal nuevamente
        self.event_window.deiconify()

    def habilitar_campos(self,event):
        item = self.tabla.item(self.tabla.focus())["values"][0]
        if item:
            self.delete_button.config(state="normal")
        else:
            self.delete_button.config(state="disabled")

    def desabilitar_campos(self):
        self.create_button.config(state='disabled')
        self.edit_button.config(state='disabled')
        self.delete_button.config(state='disabled')


    def leer_archivo_json(self):
        with open('datos.json', 'r') as f:
            arch_datos = json.load(f)
        return arch_datos
    
    
    def mostrar_datos(self, tree):
        #Crear una función que tome el diccionario de Python y lo muestre en un Treeview:
    
        datos = self.leer_archivo_json()
        
        datos_filtrados = [dato for dato in datos if dato['fecha'] == self.date_entry]
        #ordeno la lista
        datos_ordenados = sorted(datos_filtrados, key=lambda x: x['hora'])
        
       
        #pregunto si hay lineas en la tabla y si es asi la borra
        if len(tree.get_children()) > 0:
            tree.delete(*tree.get_children())

           
        for dato in datos_ordenados:
            tree.insert('', 'end', text=dato['hora'], 
                        values=(dato['hora'],dato['titulo'], dato['importancia'], dato['etiquetas']))                       
            
        
     
    def modificar_evento(self):
                
        # Obtener el evento ingresado por el usuario
        event = {
            "titulo": self.di_title_entry.get(),
            "fecha":self.date_entry,
            "hora":self.di_date_menu.get(),
            "duracion": self.di_duration_entry.get(),
            "descripcion":self.di_description_entry.get("1.0", "end"),
            "importancia":self.di_importance_entry.get(),
            "recordatorio":self.di_reminder_entry.get(),
            "etiquetas":self.di_tags_entry.get()

               }

        # Obteneos la fecha del usuario
        date = self.date_entry

        self.claveVieja= str(self.tabla.item(self.tabla.selection())["values"][0])

        datos = self.leer_archivo_json()

        #extrae el diccionario a partir de la clave "fecha seleccionada" del evento
        datos_filtrados = [dato for dato in datos if dato['fecha'] == self.date_entry]

        #extrae la lista del diccionario a partir de la "Hora" del evento
        self.datos_hora = [dato for dato in datos_filtrados if dato['hora'] == self.tabla.item(self.tabla.selection())["values"][0]]
        #print(self.datos_hora)
        #hora_seleccionada = self.tabla.item(self.tabla.selection())["values"][0]

        datos.remove(self.datos_hora[0])

                        
        # Agregamos el nuevo evento al día seleccionado
        if date not in datos:
            datos.append(event)

        # Guardar los eventos actualizados en el archivo json
        with open('datos.json', 'w') as f:
            json.dump(datos, f, indent=2)

        #actualiza el Treeview
        self.mostrar_datos(self.tabla)

        # Cerrar la ventana de eventos
        self.evento_window.destroy()
        

    def doubleClickTabla(self,event):
        self.claveVieja= str(self.tabla.item(self.tabla.selection())["values"][0])

        datos = self.leer_archivo_json()

        #extrae el diccionario a partir de la clave "fecha seleccionada" del evento
        datos_filtrados = [dato for dato in datos if dato['fecha'] == self.date_entry]

        #extrae la lista del diccionario a partir de la "Hora" del evento
        self.datos_hora = [dato for dato in datos_filtrados if dato['hora'] == self.tabla.item(self.tabla.selection())["values"][0]]
        
        self.evento_window = tk.Toplevel(self.master)
        self.evento_window.title("Editar Evento")
        self.evento_window.geometry("300x400")
        

        # Crear campos de entrada
        self.di_title_label = tk.Label(self.evento_window, text="Título:")
        self.di_title_entry = tk.Entry(self.evento_window)
        self.di_title_entry.insert(0,str(self.datos_hora[0]['titulo']))
        
        
        self.di_fecha_label = tk.Label(self.evento_window, text="Fecha:")
        self.di_fech_entry = tk.Entry(self.evento_window)
        self.di_fech_entry.insert(0,self.date_entry)
        self.di_fech_entry.config(state= 'disable')

        self.di_date_label = tk.Label(self.evento_window, text="Hora:")
        self.di_date_enty = tk.Entry(self.evento_window)
        
        hora= ["00:00", "00:30", "01:00", "01:30", "02:00", "02:30", "03:00", "03:30", "04:00", "04:30", 
                "05:00", "05:30", "06:00", "06:30", "07:00", "07:30", "08:00","08:30", "09:00", "09:30", "10:00", 
                "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", 
                "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30", "20:00", "20:30", "21:00",
                "21:30", "22:00","22:30", "23:00", "23:30"]
        self.di_date_menu = Combobox(self.evento_window,values= hora, state= "readonly" ) 
        self.di_date_menu.set(str(self.datos_hora[0]['hora']))

        self.di_duration_label = tk.Label(self.evento_window, text="Duración:")
        self.di_duration_entry = tk.Entry(self.evento_window)
        
        self.di_duration_entry.insert(0,str(self.datos_hora[0]['duracion']))

        self.di_description_label = tk.Label(self.evento_window, text="Descripción:")
        self.di_description_entry = tk.Text(self.evento_window, width=20, height=4)
        self.di_description_entry.insert(END,str(self.datos_hora[0]['descripcion']))

        self.di_importance_label = tk.Label(self.evento_window, text="Importancia:")
        self.di_importance_entry = tk.StringVar(self.evento_window)
        self.di_importance_entry.set(str(self.datos_hora[0]['importancia']))
        self.di_importance_menu = tk.OptionMenu(self.evento_window, self.di_importance_entry, "normal", "importante")
        

        self.di_reminder_label = tk.Label(self.evento_window, text="Recordatorio:")
        self.di_reminder_entry = tk.Entry(self.evento_window)
        self.di_reminder_entry.insert(0,str(self.datos_hora[0]['recordatorio']))

        self.di_tags_label = tk.Label(self.evento_window, text="Etiquetas:")
        self.di_tags_entry = tk.Entry(self.evento_window)
        self.di_tags_entry.insert(0,str(self.datos_hora[0]['etiquetas']))

        # Crear botones
        self.di_create_button = tk.Button(self.evento_window, text="actualizar", 
                                       command=self.modificar_evento)
        self.di_create_button.config( cursor= 'hand2')
        
        self.di_quit_button = tk.Button(self.evento_window, text="Cancelar", 
                                     command=self.evento_window.destroy)
        self.di_quit_button.config(cursor= 'hand2')

        # Posicionar elementos en la ventana
        self.di_title_label.grid(row=0, column=0)
        self.di_title_entry.grid(row=0, column=1)

        self.di_fecha_label.grid(row=1, column=0)
        self.di_fech_entry.grid(row=1, column=1)
        
        self.di_date_label.grid(row=2, column=0)
        self.di_date_menu.grid(row=2, column=1)

        self.di_duration_label.grid(row=3, column=0)
        self.di_duration_entry.grid(row=3, column=1)

        self.di_description_label.grid(row=4, column=0)
        self.di_description_entry.grid(row=4, column=1)

        self.di_importance_label.grid(row=5, column=0)
        self.di_importance_menu.grid(row=5, column=1)

        self.di_reminder_label.grid(row=6, column=0)
        self.di_reminder_entry.grid(row=6, column=1)

        self.di_tags_label.grid(row=7, column=0)
        self.di_tags_entry.grid(row=7, column=1)

        self.di_create_button.grid(row=8, column=0)
        self.di_quit_button.grid(row=8, column=1)

          
        # Obtener la fecha del usuario (puede ser a través de un Entry)
        date = self.date_entry

        # Cargar los eventos del archivo json (si ya existen)
        with open('datos.json', 'r') as f:
            events = json.load(f)

            # Obtener los eventos del día seleccionado
            self.day_events = events[date] if date in events else []

         

    def eliminar_evento(self):
        if messagebox.askyesno(message="¿Seguro que deseas eliminar el Evento?" ,title="Borar Evento")== True:
            # Obteneos la fecha del usuario
            date = self.date_entry
            datos = self.leer_archivo_json()
            self.dat_selec= self.tabla.focus()

            #extrae el diccionario a partir de la clave "fecha seleccionada" del evento
            datos_filtrados = [dato for dato in datos if dato['fecha'] == self.date_entry]

            #extrae la lista del diccionario a partir de la "Hora" del evento
            self.datos_hora = [dato for dato in datos_filtrados if dato['hora'] == self.tabla.item(self.tabla.focus())["values"][0]]
            #self.datos_hora = [dato for dato in datos_filtrados if dato['hora'] == self.tabla.item(self.tabla.selection())["values"][0]]
            print(self.datos_hora)
            
           
            datos.remove(self.datos_hora[0])

            # Guardar los eventos actualizados en el archivo json
            with open('datos.json', 'w') as f:
                json.dump(datos, f, indent=2)

            #actualiza el Treeview
            self.mostrar_datos(self.tabla)

        # Muestra la ventana principal nuevamente
        self.event_window.deiconify()
           
   
root = tk.Tk()
Calend(root)
root.mainloop()
