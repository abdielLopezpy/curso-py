#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║           💪 SISTEMA DE GESTIÓN DE GIMNASIO - VERSIÓN GUI           ║
║                                                                      ║
║  Interfaz gráfica moderna para gestionar miembros, entrenadores     ║
║  y clases del gimnasio.                                              ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from pathlib import Path
import sys
from datetime import datetime

# Agregar la carpeta framework al path
sys.path.insert(0, str(Path(__file__).parent.parent / "framework"))

from models import Miembro, Entrenador, Clase
from sistema_gimnasio import SistemaGimnasio


class GimnasioGUI:
    """
    Interfaz gráfica principal del sistema de gimnasio.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("💪 Sistema de Gestión de Gimnasio")
        self.root.geometry("1200x800")

        # Crear el sistema
        self.sistema = SistemaGimnasio()

        # Configurar estilo
        self.configurar_estilo()

        # Crear interfaz
        self.crear_widgets()

        # Cargar datos iniciales
        self.actualizar_listas()

    def configurar_estilo(self):
        """Configura el estilo visual de la aplicación."""
        style = ttk.Style()
        style.theme_use('clam')

        # Colores del tema
        self.color_primario = "#2C3E50"
        self.color_secundario = "#3498DB"
        self.color_exito = "#27AE60"
        self.color_peligro = "#E74C3C"
        self.color_fondo = "#ECF0F1"

        # Configurar estilos personalizados
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'),
                       foreground=self.color_primario)
        style.configure('Subtitle.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Primary.TButton', font=('Arial', 10, 'bold'))

    def crear_widgets(self):
        """Crea todos los widgets de la interfaz."""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Título
        titulo = ttk.Label(main_frame, text="💪 Sistema de Gestión de Gimnasio",
                          style='Title.TLabel')
        titulo.grid(row=0, column=0, pady=10)

        # Notebook (pestañas)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Crear pestañas
        self.crear_pestaña_miembros()
        self.crear_pestaña_entrenadores()
        self.crear_pestaña_clases()
        self.crear_pestaña_reportes()

    def crear_pestaña_miembros(self):
        """Crea la pestaña de gestión de miembros."""
        tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab, text="👥 Miembros")

        # Frame izquierdo - Formulario
        form_frame = ttk.LabelFrame(tab, text="Agregar Miembro", padding="10")
        form_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)

        # Campos del formulario
        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.miembro_nombre = ttk.Entry(form_frame, width=30)
        self.miembro_nombre.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Edad:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.miembro_edad = ttk.Entry(form_frame, width=30)
        self.miembro_edad.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.miembro_email = ttk.Entry(form_frame, width=30)
        self.miembro_email.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Teléfono:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.miembro_telefono = ttk.Entry(form_frame, width=30)
        self.miembro_telefono.grid(row=3, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Cédula:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.miembro_cedula = ttk.Entry(form_frame, width=30)
        self.miembro_cedula.grid(row=4, column=1, pady=5, padx=5)
        ttk.Label(form_frame, text="(Formato: X-XXX-XXX-X)", font=('Arial', 8)).grid(
            row=5, column=1, sticky=tk.W)

        ttk.Label(form_frame, text="Membresía Activa:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.miembro_activa = tk.BooleanVar(value=True)
        ttk.Checkbutton(form_frame, variable=self.miembro_activa).grid(
            row=6, column=1, sticky=tk.W, pady=5)

        # Botón agregar
        ttk.Button(form_frame, text="✅ Agregar Miembro",
                  command=self.agregar_miembro).grid(row=7, column=0, columnspan=2, pady=10)

        # Frame derecho - Lista
        list_frame = ttk.LabelFrame(tab, text="Miembros Registrados", padding="10")
        list_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)

        # Configurar grid
        tab.columnconfigure(1, weight=1)
        tab.rowconfigure(0, weight=1)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        # Treeview para miembros
        columns = ('ID', 'Nombre', 'Edad', 'Email', 'Membresía')
        self.miembros_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=20)

        for col in columns:
            self.miembros_tree.heading(col, text=col)
            self.miembros_tree.column(col, width=100)

        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL,
                                 command=self.miembros_tree.yview)
        self.miembros_tree.configure(yscroll=scrollbar.set)

        self.miembros_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Botones de acción
        btn_frame = ttk.Frame(list_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=5)

        ttk.Button(btn_frame, text="🔄 Actualizar",
                  command=self.actualizar_lista_miembros).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="✅ Activar Membresía",
                  command=self.activar_membresia).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="❌ Desactivar Membresía",
                  command=self.desactivar_membresia).pack(side=tk.LEFT, padx=5)

    def crear_pestaña_entrenadores(self):
        """Crea la pestaña de gestión de entrenadores."""
        tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab, text="👨‍🏫 Entrenadores")

        # Frame izquierdo - Formulario
        form_frame = ttk.LabelFrame(tab, text="Agregar Entrenador", padding="10")
        form_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)

        # Campos
        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entrenador_nombre = ttk.Entry(form_frame, width=30)
        self.entrenador_nombre.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Especialidad:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entrenador_especialidad = ttk.Entry(form_frame, width=30)
        self.entrenador_especialidad.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Años Experiencia:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entrenador_experiencia = ttk.Entry(form_frame, width=30)
        self.entrenador_experiencia.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Certificaciones:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.entrenador_certificaciones = ttk.Entry(form_frame, width=30)
        self.entrenador_certificaciones.grid(row=3, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Email:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.entrenador_email = ttk.Entry(form_frame, width=30)
        self.entrenador_email.grid(row=4, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Disponible:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.entrenador_disponible = tk.BooleanVar(value=True)
        ttk.Checkbutton(form_frame, variable=self.entrenador_disponible).grid(
            row=5, column=1, sticky=tk.W, pady=5)

        ttk.Button(form_frame, text="✅ Agregar Entrenador",
                  command=self.agregar_entrenador).grid(row=6, column=0, columnspan=2, pady=10)

        # Frame derecho - Lista
        list_frame = ttk.LabelFrame(tab, text="Entrenadores Registrados", padding="10")
        list_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)

        tab.columnconfigure(1, weight=1)
        tab.rowconfigure(0, weight=1)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        # Treeview
        columns = ('ID', 'Nombre', 'Especialidad', 'Experiencia', 'Disponible')
        self.entrenadores_tree = ttk.Treeview(list_frame, columns=columns,
                                             show='headings', height=20)

        for col in columns:
            self.entrenadores_tree.heading(col, text=col)
            self.entrenadores_tree.column(col, width=100)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL,
                                 command=self.entrenadores_tree.yview)
        self.entrenadores_tree.configure(yscroll=scrollbar.set)

        self.entrenadores_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Botones
        btn_frame = ttk.Frame(list_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=5)

        ttk.Button(btn_frame, text="🔄 Actualizar",
                  command=self.actualizar_lista_entrenadores).pack(side=tk.LEFT, padx=5)

    def crear_pestaña_clases(self):
        """Crea la pestaña de gestión de clases."""
        tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab, text="📚 Clases")

        # Frame superior - Formulario
        form_frame = ttk.LabelFrame(tab, text="Programar Clase", padding="10")
        form_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        # Campos
        ttk.Label(form_frame, text="Nombre Clase:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.clase_nombre = ttk.Entry(form_frame, width=25)
        self.clase_nombre.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="ID Miembro:").grid(row=0, column=2, sticky=tk.W, pady=5)
        self.clase_miembro_id = ttk.Entry(form_frame, width=10)
        self.clase_miembro_id.grid(row=0, column=3, pady=5, padx=5)

        ttk.Label(form_frame, text="ID Entrenador:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.clase_entrenador_id = ttk.Entry(form_frame, width=10)
        self.clase_entrenador_id.grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)

        ttk.Label(form_frame, text="Fecha (AAAA-MM-DD):").grid(row=1, column=2, sticky=tk.W, pady=5)
        self.clase_fecha = ttk.Entry(form_frame, width=15)
        self.clase_fecha.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.clase_fecha.grid(row=1, column=3, pady=5, padx=5)

        ttk.Label(form_frame, text="Hora (HH:MM):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.clase_hora = ttk.Entry(form_frame, width=10)
        self.clase_hora.grid(row=2, column=1, sticky=tk.W, pady=5, padx=5)

        ttk.Label(form_frame, text="Duración (min):").grid(row=2, column=2, sticky=tk.W, pady=5)
        self.clase_duracion = ttk.Entry(form_frame, width=10)
        self.clase_duracion.grid(row=2, column=3, sticky=tk.W, pady=5, padx=5)

        ttk.Label(form_frame, text="Salón:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.clase_salon = ttk.Entry(form_frame, width=25)
        self.clase_salon.grid(row=3, column=1, pady=5, padx=5)

        ttk.Button(form_frame, text="✅ Programar Clase",
                  command=self.programar_clase).grid(row=3, column=2, columnspan=2, pady=5, padx=5)

        # Frame inferior - Lista
        list_frame = ttk.LabelFrame(tab, text="Clases Programadas", padding="10")
        list_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(1, weight=1)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        # Treeview
        columns = ('ID', 'Clase', 'Miembro', 'Entrenador', 'Fecha', 'Hora', 'Estado')
        self.clases_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)

        for col in columns:
            self.clases_tree.heading(col, text=col)
            self.clases_tree.column(col, width=100)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL,
                                 command=self.clases_tree.yview)
        self.clases_tree.configure(yscroll=scrollbar.set)

        self.clases_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Botones
        btn_frame = ttk.Frame(list_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=5)

        ttk.Button(btn_frame, text="🔄 Actualizar",
                  command=self.actualizar_lista_clases).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="✅ Completar",
                  command=self.completar_clase).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="❌ Cancelar",
                  command=self.cancelar_clase).pack(side=tk.LEFT, padx=5)

    def crear_pestaña_reportes(self):
        """Crea la pestaña de reportes y estadísticas."""
        tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab, text="📊 Reportes")

        # Frame de botones
        btn_frame = ttk.Frame(tab)
        btn_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=10)

        ttk.Button(btn_frame, text="📊 Resumen General",
                  command=self.mostrar_resumen).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="👥 Estadísticas Miembros",
                  command=self.estadisticas_miembros).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="👨‍🏫 Estadísticas Entrenadores",
                  command=self.estadisticas_entrenadores).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="📚 Estadísticas Clases",
                  command=self.estadisticas_clases).pack(side=tk.LEFT, padx=5)

        # Área de texto para reportes
        self.reporte_text = scrolledtext.ScrolledText(tab, width=100, height=35,
                                                      font=('Courier', 10))
        self.reporte_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(1, weight=1)

    # ══════════════════════════════════════════════════════════════
    #                     MÉTODOS DE MIEMBROS
    # ══════════════════════════════════════════════════════════════

    def agregar_miembro(self):
        """Agrega un nuevo miembro."""
        try:
            # Obtener siguiente ID
            nuevo_id = self.sistema.miembros.contar() + 1

            miembro = Miembro(
                id=nuevo_id,
                nombre=self.miembro_nombre.get(),
                edad=int(self.miembro_edad.get()),
                email=self.miembro_email.get(),
                telefono=self.miembro_telefono.get(),
                cedula=self.miembro_cedula.get(),
                membresia_activa=self.miembro_activa.get(),
                fecha_registro=datetime.now().strftime("%Y-%m-%d")
            )

            if self.sistema.agregar_miembro(miembro):
                messagebox.showinfo("Éxito", f"Miembro {miembro.nombre} agregado correctamente")
                self.limpiar_formulario_miembro()
                self.actualizar_lista_miembros()
        except ValueError as e:
            messagebox.showerror("Error", f"Error en los datos: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar miembro: {str(e)}")

    def limpiar_formulario_miembro(self):
        """Limpia el formulario de miembros."""
        self.miembro_nombre.delete(0, tk.END)
        self.miembro_edad.delete(0, tk.END)
        self.miembro_email.delete(0, tk.END)
        self.miembro_telefono.delete(0, tk.END)
        self.miembro_cedula.delete(0, tk.END)
        self.miembro_activa.set(True)

    def actualizar_lista_miembros(self):
        """Actualiza la lista de miembros."""
        # Limpiar árbol
        for item in self.miembros_tree.get_children():
            self.miembros_tree.delete(item)

        # Agregar miembros
        for miembro in self.sistema.listar_miembros():
            estado = "✅ Activa" if miembro.membresia_activa else "❌ Inactiva"
            self.miembros_tree.insert('', tk.END, values=(
                miembro.id, miembro.nombre, miembro.edad,
                miembro.email, estado
            ))

    def activar_membresia(self):
        """Activa la membresía del miembro seleccionado."""
        seleccion = self.miembros_tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un miembro")
            return

        item = self.miembros_tree.item(seleccion[0])
        miembro_id = item['values'][0]

        if self.sistema.activar_membresia(miembro_id):
            messagebox.showinfo("Éxito", "Membresía activada")
            self.actualizar_lista_miembros()

    def desactivar_membresia(self):
        """Desactiva la membresía del miembro seleccionado."""
        seleccion = self.miembros_tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un miembro")
            return

        item = self.miembros_tree.item(seleccion[0])
        miembro_id = item['values'][0]

        if self.sistema.desactivar_membresia(miembro_id):
            messagebox.showinfo("Éxito", "Membresía desactivada")
            self.actualizar_lista_miembros()

    # ══════════════════════════════════════════════════════════════
    #                   MÉTODOS DE ENTRENADORES
    # ══════════════════════════════════════════════════════════════

    def agregar_entrenador(self):
        """Agrega un nuevo entrenador."""
        try:
            nuevo_id = self.sistema.entrenadores.contar() + 1

            entrenador = Entrenador(
                id=nuevo_id,
                nombre=self.entrenador_nombre.get(),
                especialidad=self.entrenador_especialidad.get(),
                años_experiencia=int(self.entrenador_experiencia.get()),
                certificaciones=self.entrenador_certificaciones.get(),
                email=self.entrenador_email.get(),
                disponible=self.entrenador_disponible.get()
            )

            if self.sistema.agregar_entrenador(entrenador):
                messagebox.showinfo("Éxito", f"Entrenador {entrenador.nombre} agregado correctamente")
                self.limpiar_formulario_entrenador()
                self.actualizar_lista_entrenadores()
        except ValueError as e:
            messagebox.showerror("Error", f"Error en los datos: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar entrenador: {str(e)}")

    def limpiar_formulario_entrenador(self):
        """Limpia el formulario de entrenadores."""
        self.entrenador_nombre.delete(0, tk.END)
        self.entrenador_especialidad.delete(0, tk.END)
        self.entrenador_experiencia.delete(0, tk.END)
        self.entrenador_certificaciones.delete(0, tk.END)
        self.entrenador_email.delete(0, tk.END)
        self.entrenador_disponible.set(True)

    def actualizar_lista_entrenadores(self):
        """Actualiza la lista de entrenadores."""
        for item in self.entrenadores_tree.get_children():
            self.entrenadores_tree.delete(item)

        for entrenador in self.sistema.listar_entrenadores():
            disponible = "✅ Sí" if entrenador.disponible else "❌ No"
            self.entrenadores_tree.insert('', tk.END, values=(
                entrenador.id, entrenador.nombre, entrenador.especialidad,
                f"{entrenador.años_experiencia} años", disponible
            ))

    # ══════════════════════════════════════════════════════════════
    #                      MÉTODOS DE CLASES
    # ══════════════════════════════════════════════════════════════

    def programar_clase(self):
        """Programa una nueva clase."""
        try:
            resultado = self.sistema.programar_clase(
                nombre_clase=self.clase_nombre.get(),
                miembro_id=int(self.clase_miembro_id.get()),
                entrenador_id=int(self.clase_entrenador_id.get()),
                fecha=self.clase_fecha.get(),
                hora=self.clase_hora.get(),
                duracion_minutos=int(self.clase_duracion.get()),
                salon=self.clase_salon.get()
            )

            if resultado:
                messagebox.showinfo("Éxito", "Clase programada correctamente")
                self.limpiar_formulario_clase()
                self.actualizar_lista_clases()
        except ValueError as e:
            messagebox.showerror("Error", f"Error en los datos: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al programar clase: {str(e)}")

    def limpiar_formulario_clase(self):
        """Limpia el formulario de clases."""
        self.clase_nombre.delete(0, tk.END)
        self.clase_miembro_id.delete(0, tk.END)
        self.clase_entrenador_id.delete(0, tk.END)
        self.clase_hora.delete(0, tk.END)
        self.clase_duracion.delete(0, tk.END)
        self.clase_salon.delete(0, tk.END)

    def actualizar_lista_clases(self):
        """Actualiza la lista de clases."""
        for item in self.clases_tree.get_children():
            self.clases_tree.delete(item)

        for clase in self.sistema.listar_clases():
            miembro = self.sistema.buscar_miembro(clase.miembro_id)
            entrenador = self.sistema.buscar_entrenador(clase.entrenador_id)

            nombre_miembro = miembro.nombre if miembro else "Desconocido"
            nombre_entrenador = entrenador.nombre if entrenador else "Desconocido"

            self.clases_tree.insert('', tk.END, values=(
                clase.id, clase.nombre_clase, nombre_miembro,
                nombre_entrenador, clase.fecha, clase.hora,
                clase.estado.upper()
            ))

    def completar_clase(self):
        """Completa la clase seleccionada."""
        seleccion = self.clases_tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una clase")
            return

        item = self.clases_tree.item(seleccion[0])
        clase_id = item['values'][0]

        if self.sistema.completar_clase(clase_id):
            messagebox.showinfo("Éxito", "Clase completada")
            self.actualizar_lista_clases()

    def cancelar_clase(self):
        """Cancela la clase seleccionada."""
        seleccion = self.clases_tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una clase")
            return

        item = self.clases_tree.item(seleccion[0])
        clase_id = item['values'][0]

        if self.sistema.cancelar_clase(clase_id):
            messagebox.showinfo("Éxito", "Clase cancelada")
            self.actualizar_lista_clases()

    # ══════════════════════════════════════════════════════════════
    #                      MÉTODOS DE REPORTES
    # ══════════════════════════════════════════════════════════════

    def mostrar_resumen(self):
        """Muestra el resumen general del sistema."""
        self.reporte_text.delete(1.0, tk.END)

        total_miembros = self.sistema.miembros.contar()
        miembros_activos = sum(1 for m in self.sistema.listar_miembros()
                              if m.membresia_activa)

        total_entrenadores = self.sistema.entrenadores.contar()
        entrenadores_disponibles = sum(1 for e in self.sistema.listar_entrenadores()
                                      if e.disponible)

        clases = self.sistema.listar_clases()
        clases_programadas = sum(1 for c in clases if c.estado == "programada")
        clases_completadas = sum(1 for c in clases if c.estado == "completada")
        clases_canceladas = sum(1 for c in clases if c.estado == "cancelada")

        reporte = f"""
{'='*70}
            📊 RESUMEN GENERAL DEL GIMNASIO
{'='*70}

👥 MIEMBROS:
   • Total: {total_miembros}
   • Activos: {miembros_activos}
   • Inactivos: {total_miembros - miembros_activos}

👨‍🏫 ENTRENADORES:
   • Total: {total_entrenadores}
   • Disponibles: {entrenadores_disponibles}
   • No disponibles: {total_entrenadores - entrenadores_disponibles}

📚 CLASES:
   • Total: {len(clases)}
   • Programadas: {clases_programadas}
   • Completadas: {clases_completadas}
   • Canceladas: {clases_canceladas}

{'='*70}
        """

        self.reporte_text.insert(1.0, reporte)

    def estadisticas_miembros(self):
        """Muestra estadísticas de miembros."""
        self.reporte_text.delete(1.0, tk.END)

        reporte = "📊 ESTADÍSTICAS DE MIEMBROS\n\n"

        for miembro in self.sistema.listar_miembros():
            clases = self.sistema.obtener_clases_de_miembro(miembro.id)
            estado = "✅ Activa" if miembro.membresia_activa else "❌ Inactiva"

            reporte += f"\n{'='*70}\n"
            reporte += f"👤 {miembro.nombre} (ID: {miembro.id})\n"
            reporte += f"   Email: {miembro.email}\n"
            reporte += f"   Membresía: {estado}\n"
            reporte += f"   Clases inscritas: {len(clases)}\n"

            if clases:
                reporte += f"   Clases:\n"
                for clase in clases:
                    reporte += f"      • {clase.nombre_clase} - {clase.fecha} ({clase.estado})\n"

        self.reporte_text.insert(1.0, reporte)

    def estadisticas_entrenadores(self):
        """Muestra estadísticas de entrenadores."""
        self.reporte_text.delete(1.0, tk.END)

        reporte = "📊 ESTADÍSTICAS DE ENTRENADORES\n\n"

        for entrenador in self.sistema.listar_entrenadores():
            clases = self.sistema.obtener_clases_de_entrenador(entrenador.id)
            disponible = "✅ Sí" if entrenador.disponible else "❌ No"

            reporte += f"\n{'='*70}\n"
            reporte += f"👨‍🏫 {entrenador.nombre} (ID: {entrenador.id})\n"
            reporte += f"   Especialidad: {entrenador.especialidad}\n"
            reporte += f"   Experiencia: {entrenador.años_experiencia} años\n"
            reporte += f"   Disponible: {disponible}\n"
            reporte += f"   Clases asignadas: {len(clases)}\n"

            if clases:
                reporte += f"   Clases:\n"
                for clase in clases:
                    miembro = self.sistema.buscar_miembro(clase.miembro_id)
                    nombre_miembro = miembro.nombre if miembro else "Desconocido"
                    reporte += f"      • {clase.nombre_clase} con {nombre_miembro} - {clase.fecha}\n"

        self.reporte_text.insert(1.0, reporte)

    def estadisticas_clases(self):
        """Muestra estadísticas de clases."""
        self.reporte_text.delete(1.0, tk.END)

        reporte = "📊 ESTADÍSTICAS DE CLASES\n\n"

        for clase in self.sistema.listar_clases():
            miembro = self.sistema.buscar_miembro(clase.miembro_id)
            entrenador = self.sistema.buscar_entrenador(clase.entrenador_id)

            nombre_miembro = miembro.nombre if miembro else "Desconocido"
            nombre_entrenador = entrenador.nombre if entrenador else "Desconocido"

            reporte += f"\n{'='*70}\n"
            reporte += f"📚 {clase.nombre_clase} (ID: {clase.id})\n"
            reporte += f"   Miembro: {nombre_miembro}\n"
            reporte += f"   Entrenador: {nombre_entrenador}\n"
            reporte += f"   Fecha: {clase.fecha} a las {clase.hora}\n"
            reporte += f"   Duración: {clase.duracion_minutos} minutos\n"
            reporte += f"   Salón: {clase.salon}\n"
            reporte += f"   Estado: {clase.estado.upper()}\n"

        self.reporte_text.insert(1.0, reporte)

    def actualizar_listas(self):
        """Actualiza todas las listas."""
        self.actualizar_lista_miembros()
        self.actualizar_lista_entrenadores()
        self.actualizar_lista_clases()


def main():
    """Función principal."""
    root = tk.Tk()
    app = GimnasioGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
