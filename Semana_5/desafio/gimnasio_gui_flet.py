#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════╗
║         💪 POWERZONE - Sistema de Gestión de Gimnasio               ║
║                      Flet Edition v2.0                               ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import flet as ft
from pathlib import Path
import sys
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent / "framework"))

from models import Miembro, Entrenador, Clase
from sistema_gimnasio import SistemaGimnasio


# ═══════════════════════════════════════════════════════════════════════
#                         TEMA Y COLORES
# ═══════════════════════════════════════════════════════════════════════

class Theme:
    # Fondos
    BG = "#0a0a0a"
    SURFACE = "#141414"
    CARD = "#1c1c1c"
    INPUT = "#252525"
    
    # Colores principales
    PRIMARY = "#ef4444"      # Rojo
    SECONDARY = "#3b82f6"    # Azul
    SUCCESS = "#22c55e"      # Verde
    WARNING = "#f59e0b"      # Amarillo
    ERROR = "#ef4444"        # Rojo
    INFO = "#3b82f6"         # Azul
    
    # Acentos
    PURPLE = "#a855f7"
    CYAN = "#06b6d4"
    GOLD = "#eab308"
    
    # Texto
    TEXT = "#ffffff"
    TEXT_SECONDARY = "#a1a1aa"
    TEXT_MUTED = "#52525b"
    BORDER = "#27272a"


def main(page: ft.Page):
    # ═══════════════════════════════════════════════════════════════════
    #                    CONFIGURACIÓN DE PÁGINA
    # ═══════════════════════════════════════════════════════════════════
    
    page.title = "Gym"
    page.bgcolor = Theme.BG
    page.padding = 0
    page.spacing = 0
    page.window.width = 1400
    page.window.height = 900
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = None
    
    # Sistema
    sistema = SistemaGimnasio()
    
    # Estado
    state = {"miembro_id": None, "clase_id": None}
    
    # ═══════════════════════════════════════════════════════════════════
    #                      COMPONENTES UI
    # ═══════════════════════════════════════════════════════════════════
    
    def snack(msg: str, color: str = Theme.INFO):
        page.snack_bar = ft.SnackBar(
            ft.Row([
                ft.Icon(ft.Icons.INFO_OUTLINE, color=color, size=20),
                ft.Text(msg, color=Theme.TEXT, size=14),
            ], spacing=10),
            bgcolor=Theme.CARD,
            duration=3000,
        )
        page.snack_bar.open = True
        page.update()
    
    def text_field(label: str, icon=None, expand: bool = False, col: dict = None):
        tf = ft.TextField(
            label=label,
            prefix_icon=icon,
            bgcolor=Theme.INPUT,
            border_color=Theme.BORDER,
            focused_border_color=Theme.PRIMARY,
            border_radius=8,
            text_size=14,
            label_style=ft.TextStyle(size=12, color=Theme.TEXT_SECONDARY),
            cursor_color=Theme.PRIMARY,
            color=Theme.TEXT,
            height=50,
        )
        if expand:
            tf.expand = True
        if col:
            tf.col = col
        return tf
    
    def btn_primary(text: str, icon=None, on_click=None, color: str = Theme.PRIMARY):
        return ft.ElevatedButton(
            text=text,
            icon=icon,
            on_click=on_click,
            bgcolor=color,
            color=Theme.TEXT,
            height=45,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        )
    
    def btn_outline(text: str, icon=None, on_click=None, color: str = Theme.SECONDARY):
        return ft.OutlinedButton(
            text=text,
            icon=icon,
            on_click=on_click,
            height=40,
            style=ft.ButtonStyle(
                color=color,
                side=ft.BorderSide(1, color),
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
        )
    
    def card(content, col: dict = None):
        c = ft.Container(
            content=content,
            bgcolor=Theme.CARD,
            border_radius=12,
            border=ft.border.all(1, Theme.BORDER),
            padding=20,
        )
        if col:
            c.col = col
        return c
    
    def section_title(icon, title: str, color: str = Theme.PRIMARY):
        return ft.Row([
            ft.Icon(icon, color=color, size=22),
            ft.Text(title, size=16, weight=ft.FontWeight.W_600, color=Theme.TEXT),
        ], spacing=10)
    
    def stat_card(icon, value: str, label: str, color: str):
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    ft.Icon(icon, size=24, color=color),
                    bgcolor=ft.Colors.with_opacity(0.1, color),
                    padding=12,
                    border_radius=10,
                ),
                ft.Text(value, size=28, weight=ft.FontWeight.BOLD, color=Theme.TEXT),
                ft.Text(label, size=11, color=Theme.TEXT_SECONDARY),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
            bgcolor=Theme.CARD,
            border_radius=12,
            border=ft.border.all(1, Theme.BORDER),
            padding=20,
            col={"xs": 6, "md": 3},
        )
    
    # ═══════════════════════════════════════════════════════════════════
    #                         DASHBOARD
    # ═══════════════════════════════════════════════════════════════════
    
    def build_dashboard():
        total_m = sistema.miembros.contar()
        activos = sum(1 for m in sistema.listar_miembros() if m.membresia_activa)
        total_e = sistema.entrenadores.contar()
        total_c = len(list(sistema.listar_clases()))
        
        # Stats
        stats = ft.ResponsiveRow([
            stat_card(ft.Icons.PEOPLE, str(total_m), "Miembros", Theme.SECONDARY),
            stat_card(ft.Icons.VERIFIED_USER, str(activos), "Activos", Theme.SUCCESS),
            stat_card(ft.Icons.SPORTS_GYMNASTICS, str(total_e), "Entrenadores", Theme.PURPLE),
            stat_card(ft.Icons.EVENT, str(total_c), "Clases", Theme.GOLD),
        ], spacing=15, run_spacing=15)
        
        # Clases recientes
        clases_list = []
        for c in list(sistema.listar_clases())[:6]:
            color = Theme.SUCCESS if c.estado == "completada" else (
                Theme.WARNING if c.estado == "programada" else Theme.ERROR)
            clases_list.append(
                ft.Container(
                    ft.Row([
                        ft.Icon(ft.Icons.FITNESS_CENTER, color=Theme.SECONDARY, size=18),
                        ft.Column([
                            ft.Text(c.nombre_clase, size=13, weight=ft.FontWeight.W_500, color=Theme.TEXT),
                            ft.Text(f"{c.fecha} • {c.hora}", size=11, color=Theme.TEXT_MUTED),
                        ], spacing=2, expand=True),
                        ft.Container(
                            ft.Text(c.estado.upper(), size=9, weight=ft.FontWeight.BOLD, color=color),
                            bgcolor=ft.Colors.with_opacity(0.1, color),
                            padding=ft.padding.symmetric(8, 4),
                            border_radius=4,
                        ),
                    ]),
                    bgcolor=Theme.SURFACE,
                    padding=12,
                    border_radius=8,
                )
            )
        
        if not clases_list:
            clases_list = [ft.Text("Sin clases registradas", color=Theme.TEXT_MUTED, size=13)]
        
        recientes = card(ft.Column([
            section_title(ft.Icons.HISTORY, "Actividad Reciente"),
            ft.Divider(height=20, color=Theme.BORDER),
            ft.Column(clases_list, spacing=8),
        ]))
        
        # Acciones rápidas
        acciones = card(ft.Column([
            section_title(ft.Icons.BOLT, "Acciones Rápidas", Theme.GOLD),
            ft.Divider(height=20, color=Theme.BORDER),
            btn_outline("Nuevo Miembro", ft.Icons.PERSON_ADD, lambda e: nav_change(1), Theme.SUCCESS),
            btn_outline("Nueva Clase", ft.Icons.ADD_TASK, lambda e: nav_change(3), Theme.PURPLE),
            btn_outline("Ver Reportes", ft.Icons.ANALYTICS, lambda e: nav_change(4), Theme.CYAN),
        ], spacing=10), col={"xs": 12, "md": 4})
        
        return ft.Container(
            ft.Column([
                ft.Text("Dashboard", size=26, weight=ft.FontWeight.BOLD, color=Theme.TEXT),
                ft.Text(datetime.now().strftime("%A, %d de %B %Y"), size=13, color=Theme.TEXT_SECONDARY),
                ft.Container(height=20),
                stats,
                ft.Container(height=20),
                ft.ResponsiveRow([
                    ft.Container(recientes, col={"xs": 12, "md": 8}),
                    acciones,
                ], spacing=15),
            ], scroll=ft.ScrollMode.AUTO),
            padding=30,
            expand=True,
        )
    
    # ═══════════════════════════════════════════════════════════════════
    #                          MIEMBROS
    # ═══════════════════════════════════════════════════════════════════
    
    m_nombre = text_field("Nombre completo", ft.Icons.PERSON)
    m_edad = text_field("Edad", ft.Icons.CAKE, col={"xs": 6})
    m_telefono = text_field("Teléfono", ft.Icons.PHONE, col={"xs": 6})
    m_email = text_field("Email", ft.Icons.EMAIL)
    m_cedula = text_field("Cédula", ft.Icons.BADGE)
    m_activa = ft.Checkbox(label="Membresía activa", value=True, active_color=Theme.SUCCESS)
    
    m_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", size=12, color=Theme.TEXT_SECONDARY)),
            ft.DataColumn(ft.Text("Nombre", size=12, color=Theme.TEXT_SECONDARY)),
            ft.DataColumn(ft.Text("Email", size=12, color=Theme.TEXT_SECONDARY)),
            ft.DataColumn(ft.Text("Estado", size=12, color=Theme.TEXT_SECONDARY)),
        ],
        rows=[],
        border_radius=8,
        heading_row_color=Theme.SURFACE,
        data_row_max_height=50,
        column_spacing=30,
    )
    
    def refresh_miembros():
        m_table.rows.clear()
        for m in sistema.listar_miembros():
            color = Theme.SUCCESS if m.membresia_activa else Theme.ERROR
            m_table.rows.append(ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(m.id), size=13, color=Theme.TEXT)),
                    ft.DataCell(ft.Text(m.nombre, size=13, color=Theme.TEXT)),
                    ft.DataCell(ft.Text(m.email, size=13, color=Theme.TEXT_SECONDARY)),
                    ft.DataCell(ft.Text("Activo" if m.membresia_activa else "Inactivo", 
                                       size=12, color=color, weight=ft.FontWeight.W_500)),
                ],
                on_select_changed=lambda e, mid=m.id: select_miembro(mid),
            ))
    
    def select_miembro(mid):
        state["miembro_id"] = mid
        m = sistema.buscar_miembro(mid)
        snack(f"Seleccionado: {m.nombre}" if m else "Error")
    
    def add_miembro(e):
        try:
            m = Miembro(
                id=sistema.miembros.contar() + 1,
                nombre=m_nombre.value or "",
                edad=int(m_edad.value or 0),
                email=m_email.value or "",
                telefono=m_telefono.value or "",
                cedula=m_cedula.value or "",
                membresia_activa=m_activa.value,
                fecha_registro=datetime.now().strftime("%Y-%m-%d")
            )
            if sistema.agregar_miembro(m):
                snack(f"✓ {m.nombre} agregado", Theme.SUCCESS)
                m_nombre.value = m_edad.value = m_email.value = m_telefono.value = m_cedula.value = ""
                refresh_miembros()
                page.update()
        except Exception as ex:
            snack(f"Error: {ex}", Theme.ERROR)
    
    def toggle_membresia(activar: bool):
        if not state["miembro_id"]:
            snack("Selecciona un miembro", Theme.WARNING)
            return
        fn = sistema.activar_membresia if activar else sistema.desactivar_membresia
        if fn(state["miembro_id"]):
            snack("Membresía " + ("activada" if activar else "desactivada"), Theme.SUCCESS if activar else Theme.WARNING)
            refresh_miembros()
            page.update()
    
    def build_miembros():
        refresh_miembros()
        
        form = card(ft.Column([
            section_title(ft.Icons.PERSON_ADD, "Nuevo Miembro"),
            ft.Divider(height=15, color=Theme.BORDER),
            m_nombre,
            ft.ResponsiveRow([m_edad, m_telefono], spacing=10),
            m_email,
            m_cedula,
            m_activa,
            ft.Container(height=5),
            btn_primary("Agregar Miembro", ft.Icons.ADD, add_miembro),
        ], spacing=12), col={"xs": 12, "lg": 4})
        
        tabla = card(ft.Column([
            ft.Row([
                section_title(ft.Icons.PEOPLE, "Miembros Registrados", Theme.SECONDARY),
                ft.Container(expand=True),
                btn_outline("Refrescar", ft.Icons.REFRESH, lambda e: (refresh_miembros(), page.update())),
            ]),
            ft.Divider(height=15, color=Theme.BORDER),
            ft.Container(
                content=ft.Column([m_table], scroll=ft.ScrollMode.AUTO),
                expand=True,
            ),
            ft.Container(height=10),
            ft.Row([
                btn_outline("Activar", ft.Icons.CHECK_CIRCLE, lambda e: toggle_membresia(True), Theme.SUCCESS),
                btn_outline("Desactivar", ft.Icons.CANCEL, lambda e: toggle_membresia(False), Theme.ERROR),
            ], spacing=10),
        ], expand=True), col={"xs": 12, "lg": 8})
        
        return ft.Container(
            ft.Column([
                ft.Text("Gestión de Miembros", size=26, weight=ft.FontWeight.BOLD, color=Theme.TEXT),
                ft.Container(height=20),
                ft.ResponsiveRow([form, tabla], spacing=20, run_spacing=20),
            ], expand=True),
            padding=30,
            expand=True,
        )
    
    # ═══════════════════════════════════════════════════════════════════
    #                        ENTRENADORES
    # ═══════════════════════════════════════════════════════════════════
    
    e_nombre = text_field("Nombre", ft.Icons.PERSON)
    e_especialidad = text_field("Especialidad", ft.Icons.SPORTS_MARTIAL_ARTS)
    e_experiencia = text_field("Años exp.", ft.Icons.TIMELINE, col={"xs": 6})
    e_email = text_field("Email", ft.Icons.EMAIL, col={"xs": 6})
    e_cert = text_field("Certificaciones", ft.Icons.VERIFIED)
    e_disp = ft.Checkbox(label="Disponible", value=True, active_color=Theme.SUCCESS)
    
    e_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", size=12, color=Theme.TEXT_SECONDARY)),
            ft.DataColumn(ft.Text("Nombre", size=12, color=Theme.TEXT_SECONDARY)),
            ft.DataColumn(ft.Text("Especialidad", size=12, color=Theme.TEXT_SECONDARY)),
            ft.DataColumn(ft.Text("Exp.", size=12, color=Theme.TEXT_SECONDARY)),
            ft.DataColumn(ft.Text("Estado", size=12, color=Theme.TEXT_SECONDARY)),
        ],
        rows=[],
        border_radius=8,
        heading_row_color=Theme.SURFACE,
        data_row_max_height=50,
    )
    
    def refresh_entrenadores():
        e_table.rows.clear()
        for ent in sistema.listar_entrenadores():
            color = Theme.SUCCESS if ent.disponible else Theme.ERROR
            e_table.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(str(ent.id), size=13, color=Theme.TEXT)),
                ft.DataCell(ft.Text(ent.nombre, size=13, color=Theme.TEXT)),
                ft.DataCell(ft.Text(ent.especialidad, size=13, color=Theme.TEXT_SECONDARY)),
                ft.DataCell(ft.Text(f"{ent.años_experiencia}a", size=13, color=Theme.TEXT_SECONDARY)),
                ft.DataCell(ft.Text("✓" if ent.disponible else "✗", size=14, color=color)),
            ]))
    
    def add_entrenador(e):
        try:
            ent = Entrenador(
                id=sistema.entrenadores.contar() + 1,
                nombre=e_nombre.value or "",
                especialidad=e_especialidad.value or "",
                años_experiencia=int(e_experiencia.value or 0),
                certificaciones=e_cert.value or "",
                email=e_email.value or "",
                disponible=e_disp.value
            )
            if sistema.agregar_entrenador(ent):
                snack(f"✓ {ent.nombre} agregado", Theme.SUCCESS)
                e_nombre.value = e_especialidad.value = e_experiencia.value = e_email.value = e_cert.value = ""
                refresh_entrenadores()
                page.update()
        except Exception as ex:
            snack(f"Error: {ex}", Theme.ERROR)
    
    def build_entrenadores():
        refresh_entrenadores()
        
        form = card(ft.Column([
            section_title(ft.Icons.SPORTS_GYMNASTICS, "Nuevo Entrenador", Theme.PURPLE),
            ft.Divider(height=15, color=Theme.BORDER),
            e_nombre,
            e_especialidad,
            ft.ResponsiveRow([e_experiencia, e_email], spacing=10),
            e_cert,
            e_disp,
            ft.Container(height=5),
            btn_primary("Agregar Entrenador", ft.Icons.ADD, add_entrenador, Theme.PURPLE),
        ], spacing=12), col={"xs": 12, "lg": 4})
        
        tabla = card(ft.Column([
            ft.Row([
                section_title(ft.Icons.GROUP, "Entrenadores", Theme.PURPLE),
                ft.Container(expand=True),
                btn_outline("Refrescar", ft.Icons.REFRESH, lambda e: (refresh_entrenadores(), page.update()), Theme.PURPLE),
            ]),
            ft.Divider(height=15, color=Theme.BORDER),
            ft.Container(
                content=ft.Column([e_table], scroll=ft.ScrollMode.AUTO),
                expand=True,
            ),
        ], expand=True), col={"xs": 12, "lg": 8})
        
        return ft.Container(
            ft.Column([
                ft.Text("Gestión de Entrenadores", size=26, weight=ft.FontWeight.BOLD, color=Theme.TEXT),
                ft.Container(height=20),
                ft.ResponsiveRow([form, tabla], spacing=20, run_spacing=20),
            ], expand=True),
            padding=30,
            expand=True,
        )
    
    # ═══════════════════════════════════════════════════════════════════
    #                           CLASES
    # ═══════════════════════════════════════════════════════════════════
    
    c_nombre = text_field("Nombre de la clase", ft.Icons.FITNESS_CENTER)
    c_miembro = text_field("ID Miembro", ft.Icons.PERSON, col={"xs": 6})
    c_entrenador = text_field("ID Entrenador", ft.Icons.SPORTS, col={"xs": 6})
    c_fecha = text_field("Fecha", ft.Icons.CALENDAR_TODAY, col={"xs": 6})
    c_fecha.value = datetime.now().strftime("%Y-%m-%d")
    c_hora = text_field("Hora", ft.Icons.ACCESS_TIME, col={"xs": 6})
    c_duracion = text_field("Duración (min)", ft.Icons.TIMER, col={"xs": 6})
    c_salon = text_field("Salón", ft.Icons.ROOM, col={"xs": 6})
    
    c_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", size=12, color=Theme.TEXT_SECONDARY)),
            ft.DataColumn(ft.Text("Clase", size=12, color=Theme.TEXT_SECONDARY)),
            ft.DataColumn(ft.Text("Miembro", size=12, color=Theme.TEXT_SECONDARY)),
            ft.DataColumn(ft.Text("Fecha", size=12, color=Theme.TEXT_SECONDARY)),
            ft.DataColumn(ft.Text("Estado", size=12, color=Theme.TEXT_SECONDARY)),
        ],
        rows=[],
        border_radius=8,
        heading_row_color=Theme.SURFACE,
        data_row_max_height=50,
    )
    
    def refresh_clases():
        c_table.rows.clear()
        for c in sistema.listar_clases():
            m = sistema.buscar_miembro(c.miembro_id)
            color = Theme.SUCCESS if c.estado == "completada" else (
                Theme.WARNING if c.estado == "programada" else Theme.ERROR)
            c_table.rows.append(ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(c.id), size=13, color=Theme.TEXT)),
                    ft.DataCell(ft.Text(c.nombre_clase, size=13, color=Theme.TEXT)),
                    ft.DataCell(ft.Text(m.nombre if m else "?", size=13, color=Theme.TEXT_SECONDARY)),
                    ft.DataCell(ft.Text(c.fecha, size=13, color=Theme.TEXT_SECONDARY)),
                    ft.DataCell(ft.Text(c.estado.upper(), size=11, color=color, weight=ft.FontWeight.W_600)),
                ],
                on_select_changed=lambda e, cid=c.id: select_clase(cid),
            ))
    
    def select_clase(cid):
        state["clase_id"] = cid
        snack(f"Clase {cid} seleccionada")
    
    def add_clase(e):
        try:
            if sistema.programar_clase(
                nombre_clase=c_nombre.value or "",
                miembro_id=int(c_miembro.value or 0),
                entrenador_id=int(c_entrenador.value or 0),
                fecha=c_fecha.value or "",
                hora=c_hora.value or "",
                duracion_minutos=int(c_duracion.value or 0),
                salon=c_salon.value or ""
            ):
                snack("✓ Clase programada", Theme.SUCCESS)
                c_nombre.value = c_miembro.value = c_entrenador.value = c_hora.value = c_duracion.value = c_salon.value = ""
                refresh_clases()
                page.update()
        except Exception as ex:
            snack(f"Error: {ex}", Theme.ERROR)
    
    def cambiar_estado_clase(completar: bool):
        if not state["clase_id"]:
            snack("Selecciona una clase", Theme.WARNING)
            return
        fn = sistema.completar_clase if completar else sistema.cancelar_clase
        if fn(state["clase_id"]):
            snack("Clase " + ("completada" if completar else "cancelada"), Theme.SUCCESS if completar else Theme.WARNING)
            refresh_clases()
            page.update()
    
    def build_clases():
        refresh_clases()
        
        form = card(ft.Column([
            section_title(ft.Icons.ADD_TASK, "Programar Clase", Theme.GOLD),
            ft.Divider(height=15, color=Theme.BORDER),
            c_nombre,
            ft.ResponsiveRow([c_miembro, c_entrenador], spacing=10),
            ft.ResponsiveRow([c_fecha, c_hora], spacing=10),
            ft.ResponsiveRow([c_duracion, c_salon], spacing=10),
            ft.Container(height=5),
            btn_primary("Programar", ft.Icons.EVENT_AVAILABLE, add_clase, Theme.GOLD),
        ], spacing=12), col={"xs": 12, "lg": 4})
        
        tabla = card(ft.Column([
            ft.Row([
                section_title(ft.Icons.EVENT_NOTE, "Clases", Theme.GOLD),
                ft.Container(expand=True),
                btn_outline("Refrescar", ft.Icons.REFRESH, lambda e: (refresh_clases(), page.update()), Theme.GOLD),
            ]),
            ft.Divider(height=15, color=Theme.BORDER),
            ft.Container(
                content=ft.Column([c_table], scroll=ft.ScrollMode.AUTO),
                expand=True,
            ),
            ft.Container(height=10),
            ft.Row([
                btn_outline("Completar", ft.Icons.CHECK_CIRCLE, lambda e: cambiar_estado_clase(True), Theme.SUCCESS),
                btn_outline("Cancelar", ft.Icons.CANCEL, lambda e: cambiar_estado_clase(False), Theme.ERROR),
            ], spacing=10),
        ], expand=True), col={"xs": 12, "lg": 8})
        
        return ft.Container(
            ft.Column([
                ft.Text("Gestión de Clases", size=26, weight=ft.FontWeight.BOLD, color=Theme.TEXT),
                ft.Container(height=20),
                ft.ResponsiveRow([form, tabla], spacing=20, run_spacing=20),
            ], expand=True),
            padding=30,
            expand=True,
        )
    
    # ═══════════════════════════════════════════════════════════════════
    #                          REPORTES
    # ═══════════════════════════════════════════════════════════════════
    
    report_output = ft.Text("Selecciona un reporte...", color=Theme.TEXT_SECONDARY, selectable=True, size=13)
    
    def gen_resumen(e):
        tm = sistema.miembros.contar()
        ta = sum(1 for m in sistema.listar_miembros() if m.membresia_activa)
        te = sistema.entrenadores.contar()
        tc = list(sistema.listar_clases())
        report_output.value = f"""
══════════════════════════════════════════
        📊 RESUMEN GENERAL
══════════════════════════════════════════

👥 MIEMBROS
   Total: {tm}  |  Activos: {ta}  |  Inactivos: {tm-ta}

👨‍🏫 ENTRENADORES
   Total: {te}

📚 CLASES
   Total: {len(tc)}
   Programadas: {sum(1 for c in tc if c.estado=='programada')}
   Completadas: {sum(1 for c in tc if c.estado=='completada')}
   Canceladas: {sum(1 for c in tc if c.estado=='cancelada')}
══════════════════════════════════════════
"""
        report_output.color = Theme.TEXT
        page.update()
    
    def gen_miembros(e):
        lines = ["📊 DETALLE DE MIEMBROS\n" + "═"*40 + "\n"]
        for m in sistema.listar_miembros():
            cls = sistema.obtener_clases_de_miembro(m.id)
            lines.append(f"• {m.nombre} | {'✓' if m.membresia_activa else '✗'} | Clases: {len(cls)}")
        report_output.value = "\n".join(lines)
        report_output.color = Theme.TEXT
        page.update()
    
    def gen_entrenadores(e):
        lines = ["📊 DETALLE DE ENTRENADORES\n" + "═"*40 + "\n"]
        for ent in sistema.listar_entrenadores():
            cls = sistema.obtener_clases_de_entrenador(ent.id)
            lines.append(f"• {ent.nombre} | {ent.especialidad} | {'✓' if ent.disponible else '✗'} | Clases: {len(cls)}")
        report_output.value = "\n".join(lines)
        report_output.color = Theme.TEXT
        page.update()
    
    def gen_clases(e):
        lines = ["📊 DETALLE DE CLASES\n" + "═"*40 + "\n"]
        for c in sistema.listar_clases():
            m = sistema.buscar_miembro(c.miembro_id)
            lines.append(f"• {c.nombre_clase} | {m.nombre if m else '?'} | {c.fecha} | {c.estado.upper()}")
        report_output.value = "\n".join(lines)
        report_output.color = Theme.TEXT
        page.update()
    
    def build_reportes():
        return ft.Container(
            ft.Column([
                ft.Text("Reportes", size=26, weight=ft.FontWeight.BOLD, color=Theme.TEXT),
                ft.Container(height=20),
                card(ft.Column([
                    section_title(ft.Icons.ANALYTICS, "Generar Reportes", Theme.CYAN),
                    ft.Divider(height=15, color=Theme.BORDER),
                    ft.Row([
                        btn_outline("Resumen", ft.Icons.DASHBOARD, gen_resumen, Theme.SECONDARY),
                        btn_outline("Miembros", ft.Icons.PEOPLE, gen_miembros, Theme.SUCCESS),
                        btn_outline("Entrenadores", ft.Icons.SPORTS_GYMNASTICS, gen_entrenadores, Theme.PURPLE),
                        btn_outline("Clases", ft.Icons.EVENT, gen_clases, Theme.GOLD),
                    ], spacing=10, wrap=True),
                    ft.Container(height=15),
                    ft.Container(
                        content=report_output,
                        bgcolor=Theme.SURFACE,
                        padding=20,
                        border_radius=8,
                        expand=True,
                    ),
                ], expand=True)),
            ], expand=True),
            padding=30,
            expand=True,
        )
    
    # ═══════════════════════════════════════════════════════════════════
    #                        NAVEGACIÓN
    # ═══════════════════════════════════════════════════════════════════
    
    content = ft.Container(expand=True)
    views = [build_dashboard, build_miembros, build_entrenadores, build_clases, build_reportes]
    
    def nav_change(idx):
        rail.selected_index = idx
        content.content = views[idx]()
        page.update()
    
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        extended=True,
        min_extended_width=200,
        bgcolor=Theme.SURFACE,
        indicator_color=ft.Colors.with_opacity(0.15, Theme.PRIMARY),
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.DASHBOARD_OUTLINED, selected_icon=ft.Icons.DASHBOARD, label="Dashboard"),
            ft.NavigationRailDestination(icon=ft.Icons.PEOPLE_OUTLINE, selected_icon=ft.Icons.PEOPLE, label="Miembros"),
            ft.NavigationRailDestination(icon=ft.Icons.SPORTS_GYMNASTICS, label="Entrenadores"),
            ft.NavigationRailDestination(icon=ft.Icons.EVENT_NOTE_OUTLINED, selected_icon=ft.Icons.EVENT_NOTE, label="Clases"),
            ft.NavigationRailDestination(icon=ft.Icons.ANALYTICS_OUTLINED, selected_icon=ft.Icons.ANALYTICS, label="Reportes"),
        ],
        on_change=lambda e: nav_change(e.control.selected_index),
        leading=ft.Container(
            ft.Column([
                ft.Icon(ft.Icons.FITNESS_CENTER, size=32, color=Theme.PRIMARY),
                ft.Text("POWERZONE", size=15, weight=ft.FontWeight.BOLD, color=Theme.TEXT),
                ft.Text("Gym Manager", size=10, color=Theme.TEXT_MUTED),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
            padding=ft.padding.only(top=25, bottom=30),
        ),
    )
    
    # Layout
    page.add(
        ft.Row([
            rail,
            ft.VerticalDivider(width=1, color=Theme.BORDER),
            content,
        ], expand=True, spacing=0)
    )
    
    content.content = build_dashboard()
    page.update()


if __name__ == "__main__":
    ft.app(target=main)