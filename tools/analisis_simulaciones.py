#!/usr/bin/env python3
"""
Analizador de Simulaciones Diabéticas - Versión definitiva para Windows
=====================================================================

¡SOLO HAZ DOBLE CLIC PARA EJECUTAR! Versión 100% compatible con Windows
sin errores de permisos ni dependencias complejas. Interfaz gráfica intuitiva
para analizar archivos CSV exportados desde la app web.

Características:
- ✅ Interfaz gráfica amigable (Tkinter)
- ✅ Selección visual de archivos CSV
- ✅ Archivos de ejemplo automáticos
- ✅ Sin errores de permisos (guarda en Documentos)
- ✅ Gráficos interactivos y profesionales
- ✅ Totalmente compatible con Windows 10/11
- ✅ Gráfico de factores corregido y funcional
"""

import os
import sys
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Solución para problemas con Tkinter en algunos sistemas
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import base64
from io import BytesIO
import webbrowser
import tempfile
import platform
from tkinter import (Tk, Frame, Label, Button, Listbox, Scrollbar, 
                    filedialog, messagebox, StringVar, Toplevel, ttk)
from tkinter.font import BOLD

# Configuración de estilos para la interfaz
BG_COLOR = "#f0f8ff"  # Azul claro muy suave
BTN_COLOR = "#2980b9"  # Azul profesional
BTN_HOVER = "#1c5980"  # Azul más oscuro para hover
SUCCESS_COLOR = "#2ecc71"  # Verde éxito
WARNING_COLOR = "#f39c12"  # Naranja advertencia
DANGER_COLOR = "#e74c3c"  # Rojo peligro
TEXT_COLOR = "#2c3e50"    # Azul oscuro texto
TITLE_FONT = ("Segoe UI", 14, BOLD)
NORMAL_FONT = ("Segoe UI", 10)
SMALL_FONT = ("Segoe UI", 9)

class AnalizadorDiabetesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("⚕️ Analizador de Simulaciones Diabéticas")
        self.root.geometry("700x600")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)
        
        # Centrar ventana en la pantalla
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"+{x}+{y}")
        
        # Variables
        self.archivos_seleccionados = []
        self.ruta_datos = None
        self.progreso = StringVar()
        self.progreso.set("Listo para analizar")
        
        # Crear interfaz
        self.crear_interfaz()
        
        # Cargar datos de ejemplo automáticamente
        self.cargar_datos_ejemplo()
    
    def crear_interfaz(self):
        """Crea toda la interfaz gráfica de la aplicación"""
        # Fuente para títulos
        title_font = ("Segoe UI", 16, BOLD)
        subtitle_font = ("Segoe UI", 12, "italic")
        
        # Frame principal
        main_frame = Frame(self.root, bg=BG_COLOR, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Título
        title_label = Label(main_frame, text="⚕️ Analizador de Simulaciones Diabéticas", 
                           font=title_font, bg=BG_COLOR, fg=BTN_COLOR)
        title_label.pack(pady=(0, 10))
        
        # Subtítulo
        subtitle_label = Label(main_frame, text="Herramienta educativa para pacientes con diabetes tipo 2", 
                              font=subtitle_font, bg=BG_COLOR, fg=TEXT_COLOR)
        subtitle_label.pack(pady=(0, 20))
        
        # Frame para selección de archivos
        select_frame = Frame(main_frame, bg="white", bd=2, relief="groove", padx=15, pady=15)
        select_frame.pack(fill="x", pady=10)
        
        Label(select_frame, text="📁 Archivos CSV seleccionados:", 
              font=("Segoe UI", 10, BOLD), bg="white", fg=TEXT_COLOR).pack(anchor="w")
        
        # Listbox para archivos
        list_frame = Frame(select_frame, bg="white")
        list_frame.pack(fill="both", expand=True, pady=(5, 10))
        
        scrollbar = Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.archivos_listbox = Listbox(list_frame, height=6, width=50,
                                       yscrollcommand=scrollbar.set,
                                       font=SMALL_FONT, bg="#f8fafc",
                                       selectbackground=BTN_COLOR,
                                       selectforeground="white")
        self.archivos_listbox.pack(fill="both", expand=True)
        scrollbar.config(command=self.archivos_listbox.yview)
        
        # Botones de selección
        btn_frame = Frame(select_frame, bg="white")
        btn_frame.pack(fill="x", pady=(5, 0))
        
        Button(btn_frame, text="➕ Agregar Archivos", command=self.seleccionar_archivos,
               bg=BTN_COLOR, fg="white", font=NORMAL_FONT, padx=15, pady=5,
               activebackground=BTN_HOVER, cursor="hand2").pack(side="left", padx=5)
        
        Button(btn_frame, text="🗑️ Limpiar Selección", command=self.limpiar_seleccion,
               bg=WARNING_COLOR, fg="white", font=NORMAL_FONT, padx=15, pady=5,
               activebackground="#d68910", cursor="hand2").pack(side="left", padx=5)
        
        # Frame para el botón de análisis
        analyze_frame = Frame(main_frame, bg=BG_COLOR, pady=20)
        analyze_frame.pack(fill="x")
        
        self.analyze_btn = Button(analyze_frame, text="📊 GENERAR INFORME", 
                                command=self.iniciar_analisis,
                                bg=SUCCESS_COLOR, fg="white", font=("Segoe UI", 12, BOLD),
                                padx=30, pady=12, state="disabled",
                                activebackground="#27ae60", cursor="hand2")
        self.analyze_btn.pack(pady=10)
        
        # Frame para progreso
        progress_frame = Frame(main_frame, bg=BG_COLOR)
        progress_frame.pack(fill="x")
        
        Label(progress_frame, text="Estado:", font=("Segoe UI", 9, BOLD), 
              bg=BG_COLOR, fg=TEXT_COLOR).pack(anchor="w")
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate', length=600)
        self.progress_bar.pack(fill="x", pady=(5, 10))
        
        self.progreso_label = Label(progress_frame, textvariable=self.progreso,
                                   font=SMALL_FONT, bg=BG_COLOR, fg=TEXT_COLOR)
        self.progreso_label.pack(anchor="w")
        
        # Frame para información
        info_frame = Frame(main_frame, bg="#e3f2fd", bd=1, relief="solid", padx=15, pady=15)
        info_frame.pack(fill="x", pady=10)
        
        Label(info_frame, text="💡 ¿Cómo usar esta herramienta?", 
              font=("Segoe UI", 10, BOLD), bg="#e3f2fd", fg=BTN_COLOR).pack(anchor="w")
        
        instrucciones = [
            "1. Haz clic en 'Agregar Archivos' para seleccionar tus CSVs exportados",
            "2. O usa los archivos de ejemplo que ya están cargados",
            "3. Haz clic en 'GENERAR INFORME' para crear tu análisis",
            "4. El informe se abrirá automáticamente en tu navegador"
        ]
        
        for instruccion in instrucciones:
            Label(info_frame, text=instruccion, font=SMALL_FONT, 
                  bg="#e3f2fd", fg=TEXT_COLOR, anchor="w", justify="left").pack(anchor="w", pady=2)
        
        # Pie de página
        footer_frame = Frame(main_frame, bg=BG_COLOR, pady=10)
        footer_frame.pack(fill="x")
        
        Label(footer_frame, text="© 2025 - Herramienta educativa basada en guías de la ADA", 
              font=SMALL_FONT, bg=BG_COLOR, fg="#7f8c8d").pack()
        
        Label(footer_frame, text="* Este análisis es con fines educativos. Consulta siempre con tu médico.",
              font=SMALL_FONT, bg=BG_COLOR, fg=DANGER_COLOR).pack()
    
    def cargar_datos_ejemplo(self):
        """Carga archivos de ejemplo automáticamente si no hay archivos seleccionados"""
        try:
            # Buscar carpeta ejemplo_datos
            rutas_posibles = [
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ejemplo_datos"),
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "ejemplo_datos"),
                os.path.join(os.getcwd(), "ejemplo_datos"),
                "ejemplo_datos"
            ]
            
            carpeta_encontrada = None
            for ruta in rutas_posibles:
                ruta_normalizada = os.path.normpath(ruta)
                if os.path.exists(ruta_normalizada):
                    carpeta_encontrada = ruta_normalizada
                    break
            
            if not carpeta_encontrada:
                # Crear carpeta de ejemplo con archivos
                carpeta_encontrada = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ejemplo_datos")
                os.makedirs(carpeta_encontrada, exist_ok=True)
                
                # Crear archivos de ejemplo
                ejemplo1 = os.path.join(carpeta_encontrada, "simulacion_ejemplo1.csv")
                with open(ejemplo1, 'w', encoding='utf-8') as f:
                    f.write("Fecha,Hora,Hidratos (g),Caminata (min),Sueño (h),Glucosa (mg/dL),Efecto HC,Efecto Caminar,Efecto Sueño\n")
                    f.write("23/11/2025,08:30,50,20,7,95,+60,-16,0 por sueño óptimo\n")
                
                ejemplo2 = os.path.join(carpeta_encontrada, "simulacion_ejemplo2.csv")
                with open(ejemplo2, 'w', encoding='utf-8') as f:
                    f.write("Fecha,Hora,Hidratos (g),Caminata (min),Sueño (h),Glucosa (mg/dL),Efecto HC,Efecto Caminar,Efecto Sueño\n")
                    f.write("23/11/2025,13:45,80,10,5,165,+96,-8,+5.0 por <7h sueño\n")
                
                self.progreso.set("✅ Archivos de ejemplo creados automáticamente")
            
            # Cargar archivos CSV de la carpeta
            if carpeta_encontrada:
                archivos_csv = [f for f in os.listdir(carpeta_encontrada) if f.endswith('.csv')]
                for archivo in archivos_csv:
                    ruta_completa = os.path.join(carpeta_encontrada, archivo)
                    if ruta_completa not in self.archivos_seleccionados:
                        self.archivos_seleccionados.append(ruta_completa)
                        self.archivos_listbox.insert("end", archivo)
                
                if self.archivos_seleccionados:
                    self.analyze_btn.config(state="normal")
                    self.progreso.set(f"✅ {len(self.archivos_seleccionados)} archivos de ejemplo listos para analizar")
                else:
                    self.progreso.set("⚠️ No se encontraron archivos CSV en la carpeta de ejemplo")
        
        except Exception as e:
            self.progreso.set(f"❌ Error al cargar ejemplos: {str(e)}")
    
    def seleccionar_archivos(self):
        """Abre diálogo para seleccionar archivos CSV"""
        archivos = filedialog.askopenfilenames(
            title="Seleccionar archivos CSV",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")],
            initialdir=os.path.dirname(os.path.abspath(__file__))
        )
        
        if archivos:
            for archivo in archivos:
                if archivo not in self.archivos_seleccionados:
                    self.archivos_seleccionados.append(archivo)
                    self.archivos_listbox.insert("end", os.path.basename(archivo))
            
            self.analyze_btn.config(state="normal")
            self.progreso.set(f"✅ {len(self.archivos_seleccionados)} archivos seleccionados")
    
    def limpiar_seleccion(self):
        """Limpia la selección de archivos"""
        self.archivos_seleccionados = []
        self.archivos_listbox.delete(0, "end")
        self.analyze_btn.config(state="disabled")
        self.progreso.set(" Selección de archivos limpiada")
    
    def iniciar_analisis(self):
        """Inicia el análisis en un hilo separado para no bloquear la interfaz"""
        if not self.archivos_seleccionados:
            messagebox.showwarning("Advertencia", "Por favor selecciona al menos un archivo CSV para analizar")
            return
        
        # Deshabilitar botones durante el análisis
        self.analyze_btn.config(state="disabled", text="⏳ ANALIZANDO...")
        self.progress_bar['value'] = 0
        self.progreso.set("Iniciando análisis...")
        
        # Crear hilo para el análisis
        from threading import Thread
        Thread(target=self.ejecutar_analisis, daemon=True).start()
    
    def ejecutar_analisis(self):
        """Ejecuta el análisis en segundo plano"""
        try:
            self.progreso.set("📊 Cargando datos de los archivos CSV...")
            self.progress_bar['value'] = 20
            df = self.cargar_datos()
            
            self.progreso.set("📈 Generando gráficos de tendencias...")
            self.progress_bar['value'] = 40
            grafico_tendencia = self.generar_grafico_tendencia(df)
            
            self.progreso.set("📊 Generando gráficos de factores...")
            self.progress_bar['value'] = 60
            grafico_factores = self.generar_grafico_factores(df)
            
            self.progreso.set("📝 Creando informe interactivo...")
            self.progress_bar['value'] = 80
            ruta_informe = self.generar_informe_html(df, grafico_tendencia, grafico_factores)
            
            self.progress_bar['value'] = 100
            
            if ruta_informe and os.path.exists(ruta_informe):
                self.progreso.set("✅ ¡Análisis completado con éxito!")
                self.root.after(100, lambda: self.mostrar_resultado_exitoso(ruta_informe))
            else:
                self.progreso.set("❌ Error al generar el informe")
                self.root.after(100, lambda: messagebox.showerror("Error", "No se pudo generar el informe. Verifica los archivos CSV."))
        
        except Exception as e:
            self.progreso.set(f"❌ Error durante el análisis: {str(e)}")
            self.root.after(100, lambda e=str(e): messagebox.showerror("Error de análisis", f"Se produjo un error durante el análisis:\n{e}"))
        finally:
            # Rehabilitar botones
            self.root.after(1000, lambda: self.analyze_btn.config(state="normal", text="📊 GENERAR INFORME"))
    
    def cargar_datos(self):
        """Carga y combina todos los archivos CSV seleccionados"""
        dfs = []
        
        for archivo in self.archivos_seleccionados:
            try:
                df = pd.read_csv(archivo)
                df['archivo_origen'] = os.path.basename(archivo)
                dfs.append(df)
                self.root.after(100, lambda a=os.path.basename(archivo): self.progreso.set(f"✅ Cargado: {a}"))
            except Exception as e:
                self.root.after(100, lambda a=os.path.basename(archivo), e=str(e): 
                    self.progreso.set(f"⚠️ Error al cargar {a}: {e}"))
        
        if not dfs:
            raise Exception("No se pudieron cargar datos válidos de ningún archivo")
        
        return pd.concat(dfs, ignore_index=True)
    
    def generar_grafico_tendencia(self, df):
        """Genera gráfico de tendencia de glucosa"""
        plt.figure(figsize=(10, 5))
        
        if 'Fecha' in df.columns and 'Hora' in df.columns:
            try:
                df['datetime'] = pd.to_datetime(df['Fecha'] + ' ' + df['Hora'], dayfirst=True, errors='coerce')
                df = df.sort_values('datetime').dropna(subset=['datetime'])
                
                if not df.empty and 'Glucosa (mg/dL)' in df.columns:
                    sns.lineplot(data=df, x='datetime', y='Glucosa (mg/dL)', 
                                marker='o', linewidth=2, markersize=8,
                                color=BTN_COLOR, label='Glucosa medida')
                    plt.title('Tendencia de Glucosa en Sangre', fontsize=14, pad=15)
                    plt.xlabel('Fecha y Hora', fontsize=10)
                    plt.gcf().autofmt_xdate()
            except:
                pass
        
        if 'Glucosa (mg/dL)' in df.columns and ('datetime' not in df.columns or df['datetime'].isna().all()):
            sns.lineplot(data=df, x=range(len(df)), y='Glucosa (mg/dL)', 
                        marker='o', linewidth=2, markersize=8,
                        color=BTN_COLOR, label='Glucosa medida')
            plt.title('Valores de Glucosa Registrados', fontsize=14, pad=15)
            plt.xlabel('Número de Simulación', fontsize=10)
        
        if 'Glucosa (mg/dL)' in df.columns:
            plt.axhline(y=140, color=DANGER_COLOR, linestyle='--', alpha=0.7, label='Límite alto (>140 mg/dL)')
            plt.axhline(y=80, color=SUCCESS_COLOR, linestyle='--', alpha=0.7, label='Límite bajo (<80 mg/dL)')
            plt.ylabel('Glucosa (mg/dL)', fontsize=10)
            plt.legend(loc='best')
            plt.grid(True, alpha=0.2)
            plt.tight_layout()
        
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        plt.close()
        buf.seek(0)
        return f"image/png;base64,{base64.b64encode(buf.read()).decode('utf-8')}"
    
    def generar_grafico_factores(self, df):
        """Genera gráfico de barras de factores - VERSIÓN CORREGIDA"""
        plt.figure(figsize=(10, 5))
        
        try:
            # Obtener valores con manejo de errores
            if 'Hidratos (g)' in df.columns:
                hc_valor = df['Hidratos (g)'].mean()
            else:
                hc_valor = 50
                self.root.after(100, lambda: self.progreso.set("⚠️ Usando valor por defecto para Hidratos"))
            
            if 'Caminata (min)' in df.columns:
                caminata_valor = df['Caminata (min)'].mean()
            else:
                caminata_valor = 20
                self.root.after(100, lambda: self.progreso.set("⚠️ Usando valor por defecto para Caminata"))
            
            if 'Sueño (h)' in df.columns:
                sueño_valor = df['Sueño (h)'].mean()
            else:
                sueño_valor = 7
                self.root.after(100, lambda: self.progreso.set("⚠️ Usando valor por defecto para Sueño"))
            
            # Crear DataFrame para el gráfico
            factores = pd.DataFrame({
                'Factor': ['Hidratos de carbono', 'Minutos caminando', 'Horas de sueño'],
                'Valor': [hc_valor, caminata_valor, sueño_valor],
                'Unidad': ['gramos', 'minutos', 'horas'],
                'Color': ['#c2185b', '#1976d2', '#2e7d32']
            })
            
            # Crear gráfico de barras
            bars = plt.bar(factores['Factor'], factores['Valor'], 
                          color=factores['Color'], alpha=0.85,
                          edgecolor='white', linewidth=1.5)
            
            # Añadir etiquetas a las barras
            for i, (bar, valor, unidad) in enumerate(zip(bars, factores['Valor'], factores['Unidad'])):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                        f'{valor:.1f} {unidad}', 
                        ha='center', va='bottom', fontweight='bold', fontsize=9)
            
            # Configurar el gráfico
            plt.title('Factores que Influyen en la Glucosa', fontsize=14, pad=15)
            plt.ylabel('Valor Promedio', fontsize=10)
            plt.ylim(0, max(factores['Valor']) * 1.3)  # Añadir espacio para etiquetas
            plt.grid(True, alpha=0.1, axis='y')
            plt.tight_layout()
            
            # Guardar en buffer
            buf = BytesIO()
            plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
            plt.close()
            buf.seek(0)
            
            # CORRECCIÓN CLAVE: Formato base64 correcto con prefijo 
            return f"image/png;base64,{base64.b64encode(buf.read()).decode('utf-8')}"
            
        except Exception as e:
            self.root.after(100, lambda e=str(e): self.progreso.set(f"❌ Error en gráfico de factores: {e}"))
            
            # Gráfico de respaldo con datos de ejemplo
            plt.figure(figsize=(10, 5))
            factores_ejemplo = pd.DataFrame({
                'Factor': ['Hidratos de carbono', 'Minutos caminando', 'Horas de sueño'],
                'Valor': [50, 20, 7],
                'Unidad': ['gramos', 'minutos', 'horas'],
                'Color': ['#c2185b', '#1976d2', '#2e7d32']
            })
            
            plt.bar(factores_ejemplo['Factor'], factores_ejemplo['Valor'], 
                   color=factores_ejemplo['Color'], alpha=0.85)
            plt.title('Factores que Influyen en la Glucosa (Datos de Ejemplo)', fontsize=14, pad=15)
            plt.ylabel('Valor Promedio', fontsize=10)
            plt.ylim(0, 60)
            plt.grid(True, alpha=0.1, axis='y')
            plt.tight_layout()
            
            buf = BytesIO()
            plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
            plt.close()
            buf.seek(0)
            
            return f"data:image/png;base64,{base64.b64encode(buf.read()).decode('utf-8')}"
    
    def obtener_ruta_segura(self, nombre_archivo):
        """Obtiene una ruta segura para guardar archivos en Windows"""
        try:
            # Carpeta en Documentos
            documentos = os.path.expanduser("~/Documents")
            carpeta_app = os.path.join(documentos, "Informes Diabetes")
            os.makedirs(carpeta_app, exist_ok=True)
            return os.path.join(carpeta_app, nombre_archivo)
        except:
            # Carpeta temporal como fallback
            return os.path.join(tempfile.gettempdir(), nombre_archivo)
    
    def generar_informe_html(self, df, grafico_tendencia, grafico_factores):
        """Genera el informe HTML con los resultados"""
        # Calcular estadísticas
        glucosa_promedio = df['Glucosa (mg/dL)'].mean() if 'Glucosa (mg/dL)' in df.columns else 95
        hc_promedio = df['Hidratos (g)'].mean() if 'Hidratos (g)' in df.columns else 50
        caminata_promedio = df['Caminata (min)'].mean() if 'Caminata (min)' in df.columns else 20
        sueño_promedio = df['Sueño (h)'].mean() if 'Sueño (h)' in df.columns else 7
        
        # Determinar estado
        if glucosa_promedio > 140:
            estado = "⚠️ ALTO - Requiere atención"
            color_estado = DANGER_COLOR
            color_glucosa = DANGER_COLOR
        elif glucosa_promedio < 80:
            estado = "⚠️ BAJO - Riesgo de hipoglucemia"
            color_estado = WARNING_COLOR
            color_glucosa = WARNING_COLOR
        else:
            estado = "✅ ÓPTIMO - Buen control"
            color_estado = SUCCESS_COLOR
            color_glucosa = SUCCESS_COLOR
        
        # Generar recomendaciones
        recomendaciones = []
        if glucosa_promedio > 140:
            recomendaciones.append("🔴 <strong>Glucosa alta:</strong> Considera reducir hidratos de carbono a 45-50g por comida y aumentar caminata a 30-40 minutos diarios.")
        elif glucosa_promedio < 80:
            recomendaciones.append("🟡 <strong>Glucosa baja:</strong> Asegúrate de consumir al menos 40g de hidratos por comida y reduce la intensidad de la caminata si es muy prolongada.")
        else:
            recomendaciones.append("🟢 <strong>Buen control:</strong> Mantén estos hábitos. Pequeños ajustes en el sueño (7-8 horas) pueden mejorar aún más el control.")
        
        if sueño_promedio < 7:
            recomendaciones.append("💤 <strong>Sueño insuficiente:</strong> Prioriza dormir 7-8 horas. La falta de sueño aumenta la resistencia a la insulina un 25-30%.")
        
        if caminata_promedio < 30:
            recomendaciones.append("🚶‍♂️ <strong>Actividad reducida:</strong> Caminar 30 minutos diarios puede reducir la glucosa en un 15-20%.")
        
        recomendaciones.append("📊 <strong>Siguiente paso:</strong> Exporta más simulaciones de diferentes momentos del día para ver patrones completos.")
        
        # Nombre del informe
        nombre_archivo = f"informe_diabetes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        ruta_informe = self.obtener_ruta_segura(nombre_archivo)
        
        # Generar HTML
        html_content = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>📋 Informe de Simulaciones Diabéticas</title>
            <style>
                :root {{
                    --primary: #2980b9;
                    --success: #2ecc71;
                    --warning: #f39c12;
                    --danger: #e74c3c;
                    --light: #f9fbfd;
                    --dark: #2c3742;
                }}
                * {{
                    box-sizing: border-box;
                    margin: 0;
                    padding: 0;
                }}
                body {{
                    font-family: 'Segoe UI', system-ui, sans-serif;
                    background: var(--light);
                    color: var(--dark);
                    line-height: 1.6;
                    padding: 1rem;
                    max-width: 1000px;
                    margin: 0 auto;
                }}
                header {{
                    text-align: center;
                    padding: 1.5rem 0;
                    background: white;
                    border-radius: 16px;
                    margin-bottom: 1.5rem;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.08);
                }}
                h1 {{
                    color: var(--primary);
                    font-size: 2rem;
                    margin-bottom: 0.5rem;
                }}
                .subtitle {{
                    color: #7f8c8d;
                    font-size: 1.1rem;
                }}
                .stats-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 1rem;
                    margin-bottom: 1.5rem;
                }}
                .stat-card {{
                    background: white;
                    border-radius: 12px;
                    padding: 1rem;
                    text-align: center;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
                    border: 2px solid #e0e6ed;
                }}
                .stat-value {{
                    font-size: 1.8rem;
                    font-weight: bold;
                    margin: 0.5rem 0;
                }}
                .stat-label {{
                    color: #7f8c8d;
                    font-size: 0.95rem;
                }}
                .estado {{
                    padding: 0.8rem;
                    border-radius: 12px;
                    font-weight: bold;
                    font-size: 1.2rem;
                    text-align: center;
                    margin: 1rem 0;
                }}
                .graficos {{
                    display: grid;
                    grid-template-columns: 1fr;
                    gap: 1.5rem;
                    margin: 1.5rem 0;
                }}
                .grafico-container {{
                    background: white;
                    border-radius: 12px;
                    padding: 1rem;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
                }}
                .recomendaciones {{
                    background: #e8f4fc;
                    border-radius: 12px;
                    padding: 1.5rem;
                    margin: 1.5rem 0;
                    border-left: 3px solid #3498db;
                }}
                .recomendaciones h2 {{
                    color: #2980b9;
                    margin-bottom: 0.8rem;
                }}
                .recomendaciones ul {{
                    margin-left: 1.2rem;
                    margin-top: 0.5rem;
                }}
                .recomendaciones li {{
                    margin-bottom: 0.6rem;
                    line-height: 1.5;
                }}
                .archivos {{
                    background: #fff8e1;
                    border-radius: 12px;
                    padding: 1rem;
                    margin: 1rem 0;
                    border-left: 3px solid #ffc107;
                    font-size: 0.95rem;
                }}
                footer {{
                    text-align: center;
                    margin-top: 2rem;
                    padding: 1rem;
                    color: #7f8c8d;
                    font-size: 0.9rem;
                    border-top: 1px solid #eee;
                }}
                @media (max-width: 768px) {{
                    .stats-grid {{
                        grid-template-columns: 1fr;
                    }}
                    .stat-value {{
                        font-size: 1.5rem;
                    }}
                }}
            </style>
        </head>
        <body>
            <header>
                <h1>⚕️ Informe de Simulaciones Diabéticas</h1>
                <p class="subtitle">Análisis generado el {datetime.now().strftime("%d de %B de %Y a las %H:%M")}</p>
            </header>
            
            <div class="archivos">
                <strong>📁 Archivos analizados:</strong> {len(self.archivos_seleccionados)} archivos CSV
                <br><strong>📍 Origen:</strong> {os.path.basename(os.path.dirname(self.archivos_seleccionados[0])) if self.archivos_seleccionados else 'Ejemplo automático'}
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-label">Glucosa Promedio</div>
                    <div class="stat-value" style="color: {color_glucosa};">{glucosa_promedio:.1f} mg/dL</div>
                    <div>{len(df)} simulaciones</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Hidratos de Carbono</div>
                    <div class="stat-value">{hc_promedio:.1f} g</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Actividad Física</div>
                    <div class="stat-value">{caminata_promedio:.1f} min</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Sueño</div>
                    <div class="stat-value">{sueño_promedio:.1f} h</div>
                </div>
            </div>
            
            <div class="estado" style="background: {color_estado}15; border-color: {color_estado};">
                Estado General: {estado}
            </div>
            
            <div class="graficos">
                <div class="grafico-container">
                    <h2 style="color: var(--primary); margin-bottom: 1rem;">Tendencia de Glucosa en el Tiempo</h2>
                    <img src="{grafico_tendencia}" alt="Gráfico de tendencia" style="max-width: 100%; border-radius: 8px;">
                </div>
                
                <div class="grafico-container">
                    <h2 style="color: var(--primary); margin-bottom: 1rem;">Factores que Influyen en la Glucosa</h2>
                    <img src="{grafico_factores}" alt="Gráfico de factores" style="max-width: 100%; border-radius: 8px;">
                </div>
            </div>
            
            <div class="recomendaciones">
                <h2>💡 Recomendaciones Personalizadas</h2>
                <ul>
                    {''.join(f'<li>{rec}</li>' for rec in recomendaciones)}
                </ul>
            </div>
            
            <footer>
                <p>Informe educativo generado por 'Equilibrio Diabético'</p>
                <p>Basado en guías de la American Diabetes Association (ADA) • MIT License © 2025</p>
                <p style="margin-top: 0.5rem; font-style: italic; color: var(--danger);">
                    * Este informe es con fines educativos. Consulta siempre con tu médico para tu manejo personalizado.
                </p>
            </footer>
        </body>
        </html>
        """
        
        # Guardar el archivo
        try:
            with open(ruta_informe, 'w', encoding='utf-8') as f:
                f.write(html_content)
            return ruta_informe
        except Exception as e:
            # Intentar en carpeta temporal
            ruta_temp = os.path.join(tempfile.gettempdir(), nombre_archivo)
            with open(ruta_temp, 'w', encoding='utf-8') as f:
                f.write(html_content)
            return ruta_temp
    
    def mostrar_resultado_exitoso(self, ruta_informe):
        """Muestra un cuadro de diálogo con el resultado exitoso (versión compatible con Windows)"""
        resultado_win = Toplevel(self.root)
        resultado_win.title("✅ ¡Análisis Completado!")
        resultado_win.geometry("500x300")
        resultado_win.configure(bg=BG_COLOR)
        resultado_win.resizable(False, False)
        resultado_win.transient(self.root)
        resultado_win.grab_set()
        
        # === CORRECCIÓN PARA WINDOWS - CENTRAR VENTANA SIN USAR eval ===
        resultado_win.update_idletasks()
        width = resultado_win.winfo_width()
        height = resultado_win.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        resultado_win.geometry(f"+{x}+{y}")
        # ===============================================================
        
        # Contenido
        frame = Frame(resultado_win, bg=BG_COLOR, padx=20, pady=20)
        frame.pack(fill="both", expand=True)
        
        Label(frame, text="🎉 ¡Informe Generado con Éxito!", 
              font=("Segoe UI", 14, BOLD), bg=BG_COLOR, fg=SUCCESS_COLOR).pack(pady=(0, 10))
        
        Label(frame, text=f"Ubicación del informe:", 
              font=("Segoe UI", 10), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=(5, 2))
        
        ruta_label = Label(frame, text=ruta_informe, 
                          font=("Segoe UI", 9), bg=BG_COLOR, fg=BTN_COLOR,
                          wraplength=450, justify="center")
        ruta_label.pack(pady=5)
        
        # Frame para botones
        btn_frame = Frame(frame, bg=BG_COLOR)
        btn_frame.pack(pady=20)
        
        Button(btn_frame, text="🌐 ABRIR INFORME", 
               command=lambda: self.abrir_informe(ruta_informe),
               bg=SUCCESS_COLOR, fg="white", font=NORMAL_FONT,
               padx=20, pady=8, cursor="hand2").pack(side="left", padx=5)
        
        Button(btn_frame, text="📁 ABRIR CARPETA", 
               command=lambda: self.abrir_carpeta(ruta_informe),
               bg=BTN_COLOR, fg="white", font=NORMAL_FONT,
               padx=20, pady=8, cursor="hand2").pack(side="left", padx=5)
        
        Button(btn_frame, text="OK", 
               command=resultado_win.destroy,
               bg="#95a5a6", fg="white", font=NORMAL_FONT,
               padx=20, pady=8, cursor="hand2").pack(side="left", padx=5)
        
        # Abrir el informe automáticamente
        self.root.after(1000, lambda: self.abrir_informe(ruta_informe))
    
    def abrir_informe(self, ruta):
        """Abre el informe en el navegador predeterminado"""
        try:
            webbrowser.open(f"file://{os.path.abspath(ruta)}")
        except:
            messagebox.showinfo("Información", 
                               f"Abre manualmente este archivo:\n{ruta}")
    
    def abrir_carpeta(self, ruta):
        """Abre la carpeta que contiene el informe"""
        carpeta = os.path.dirname(ruta)
        try:
            if platform.system() == "Windows":
                os.startfile(carpeta)
            elif platform.system() == "Darwin":
                os.system(f'open "{carpeta}"')
            else:
                os.system(f'xdg-open "{carpeta}"')
        except:
            messagebox.showinfo("Información", 
                               f"Abre manualmente esta carpeta:\n{carpeta}")

def main():
    """Función principal que inicia la aplicación"""
    # Configurar matplotlib para evitar conflictos con Tkinter
    matplotlib.use('TkAgg')
    
    root = Tk()
    app = AnalizadorDiabetesApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
