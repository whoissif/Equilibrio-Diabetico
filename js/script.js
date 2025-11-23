document.addEventListener('DOMContentLoaded', () => {
  // Variables globales
  let lastSimulation = null;
  
  // Elementos del DOM para el simulador
  const carbsSlider = document.getElementById('carbs');
  const walkSlider = document.getElementById('walk');
  const sleepSlider = document.getElementById('sleep');
  const carbsVal = document.getElementById('carbs-val');
  const walkVal = document.getElementById('walk-val');
  const sleepVal = document.getElementById('sleep-val');
  const glucoseOut = document.getElementById('glucose-output');
  const carbsEffectEl = document.getElementById('carbs-effect');
  const walkEffectEl = document.getElementById('walk-effect');
  const sleepEffectEl = document.getElementById('sleep-effect');
  const simulateBtn = document.getElementById('simulate');
  const exportSection = document.getElementById('export-section');
  const exportCsvBtn = document.getElementById('export-csv');
  const exportJsonBtn = document.getElementById('export-json');
  
  // Elementos para análisis avanzado
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');
  const downloadPythonBtn = document.getElementById('download-python');
  
  // Inicializar sliders
  carbsVal.textContent = carbsSlider.value;
  walkVal.textContent = walkSlider.value;
  sleepVal.textContent = sleepSlider.value;
  
  // Eventos para tabs
  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const tabId = btn.getAttribute('data-tab');
      
      // Actualizar botones activos
      tabBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      
      // Mostrar contenido correspondiente
      tabContents.forEach(content => {
        content.classList.remove('active');
        if (content.id === `${tabId}-tab`) {
          content.classList.add('active');
        }
      });
    });
  });
  
  // Eventos para sliders
  carbsSlider.addEventListener('input', () => carbsVal.textContent = carbsSlider.value);
  walkSlider.addEventListener('input', () => walkVal.textContent = walkSlider.value);
  sleepSlider.addEventListener('input', () => sleepVal.textContent = sleepSlider.value);
  
  // Simulación
  simulateBtn.addEventListener('click', simulateGlucose);
  
  // Exportación
  exportCsvBtn.addEventListener('click', exportToCSV);
  exportJsonBtn.addEventListener('click', exportToJSON);
  
  // Descarga de script Python
  if (downloadPythonBtn) {
    downloadPythonBtn.addEventListener('click', downloadPythonScript);
  }
  
  // Simulación inicial
  setTimeout(simulateGlucose, 300);
  
  // Función principal de simulación
  function simulateGlucose() {
    const carbs = parseFloat(carbsSlider.value);
    const walk = parseFloat(walkSlider.value);
    const sleep = parseFloat(sleepSlider.value);
    
    // Cálculos fisiológicos simplificados
    const glucosa_base = 90;
    const incremento_por_hc = carbs * 1.2;
    const descuento_por_caminar = Math.min(walk * 0.8, 30);
    
    // Efecto del sueño
    let sleepAdjustment = 0;
    let sleepText = "";
    if (sleep < 7) {
      sleepAdjustment = (7 - sleep) * 2.5;
      sleepText = `+${sleepAdjustment.toFixed(1)} por <7h sueño`;
      sleepEffectEl.style.color = "#e74c3c";
    } else if (sleep > 8) {
      sleepAdjustment = Math.max(-5, (sleep - 8) * -0.7);
      sleepText = `${sleepAdjustment.toFixed(1)} por >8h sueño`;
      sleepEffectEl.style.color = "#2ecc71";
    } else {
      sleepText = "0 por sueño óptimo";
      sleepEffectEl.style.color = "#27ae60";
    }
    
    // Cálculo final
    let glucosa = glucosa_base + incremento_por_hc - descuento_por_caminar + sleepAdjustment;
    glucosa = Math.max(70, Math.min(200, glucosa));
    
    // Guardar resultados
    lastSimulation = {
      timestamp: new Date().toISOString(),
      carbs: carbs,
      walk: walk,
      sleep: sleep,
      glucose: Math.round(glucosa),
      carbsEffect: Math.round(incremento_por_hc),
      walkEffect: Math.round(descuento_por_caminar),
      sleepEffect: sleepAdjustment.toFixed(1),
      sleepText: sleepText
    };
    
    // Actualizar interfaz
    glucoseOut.innerHTML = `<span style="color: ${getGlucoseColor(glucosa)}">${Math.round(glucosa)}</span> mg/dL`;
    carbsEffectEl.textContent = Math.round(incremento_por_hc);
    walkEffectEl.textContent = Math.round(descuento_por_caminar);
    sleepEffectEl.innerHTML = sleepText;
    
    // Mostrar sección de exportación
    exportSection.classList.remove('hidden');
  }
  
  // Función para colores según nivel de glucosa
  function getGlucoseColor(value) {
    if (value > 140) return '#e74c3c';
    if (value < 80) return '#f39c12';
    return '#2ecc71';
  }
  
  // Exportar como CSV
  function exportToCSV() {
    if (!lastSimulation) return;
    
    const date = new Date(lastSimulation.timestamp);
    const formattedDate = date.toLocaleDateString('es-ES');
    const formattedTime = date.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
    
    // Encabezados y datos
    const csvContent = [
      ["Fecha", "Hora", "Hidratos (g)", "Caminata (min)", "Sueño (h)", "Glucosa (mg/dL)", "Efecto HC", "Efecto Caminar", "Efecto Sueño"],
      [
        formattedDate,
        formattedTime,
        lastSimulation.carbs,
        lastSimulation.walk,
        lastSimulation.sleep,
        lastSimulation.glucose,
        `+${lastSimulation.carbsEffect}`,
        `-${lastSimulation.walkEffect}`,
        lastSimulation.sleepText
      ]
    ].map(e => e.map(field => 
      typeof field === 'string' ? `"${field.replace(/"/g, '""')}"` : field
    ).join(",")).join("\n");
    
    // Crear enlace de descarga
    downloadFile(
      csvContent, 
      `simulacion_diabetes_${formattedDate.replace(/\//g, '-')}.csv`,
      'text/csv;charset=utf-8;'
    );
  }
  
  // Exportar como JSON
  function exportToJSON() {
    if (!lastSimulation) return;
    
    const date = new Date(lastSimulation.timestamp);
    const formattedDate = date.toLocaleDateString('es-ES');
    
    // Preparar datos para exportar
    const exportData = {
      tipo: "Simulación Educativa Diabetes Tipo 2",
      fecha: formattedDate,
      hora: date.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' }),
      parametros: {
        hidratos_carbono_gramos: lastSimulation.carbs,
        minutos_caminando: lastSimulation.walk,
        horas_sueño: lastSimulation.sleep
      },
      resultados: {
        glucosa_estimada_mg_dl: lastSimulation.glucose,
        efecto_hidratos: `+${lastSimulation.carbsEffect} mg/dL`,
        efecto_caminata: `-${lastSimulation.walkEffect} mg/dL`,
        efecto_sueño: lastSimulation.sleepText
      },
      recomendaciones: generarRecomendaciones(lastSimulation),
      notas: "Esta simulación es educativa. Consulta siempre con tu médico para tu manejo personalizado."
    };
    
    // Convertir a JSON formateado
    const jsonContent = JSON.stringify(exportData, null, 2);
    
    // Crear enlace de descarga
    downloadFile(
      jsonContent,
      `simulacion_diabetes_${formattedDate.replace(/\//g, '-')}.json`,
      'application/json;charset=utf-8;'
    );
  }
  
  // Función genérica para descargar archivos
  function downloadFile(content, filename, mimeType) {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    
    const link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", filename);
    link.style.visibility = 'hidden';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    // Liberar memoria
    setTimeout(() => URL.revokeObjectURL(url), 100);
  }
  
  // Generar recomendaciones personalizadas
  function generarRecomendaciones(sim) {
    const recomendaciones = [];
    
    if (sim.glucose > 140) {
      recomendaciones.push("⚠️ Glucosa alta: Reduce hidratos de carbono en la próxima comida");
      recomendaciones.push("💡 Aumenta el tiempo de caminata a 30-40 minutos para mejorar el control");
    } else if (sim.glucose < 80) {
      recomendaciones.push("⚠️ Glucosa baja: Asegúrate de consumir hidratos suficientes");
      recomendaciones.push("💡 Reduce el tiempo de caminata si es muy intenso");
    } else {
      recomendaciones.push("✅ ¡Excelente equilibrio! Mantén estos hábitos");
    }
    
    if (sim.sleep < 7) {
      recomendaciones.push("💤 Prioriza dormir 7-8 horas para mejorar la sensibilidad a la insulina");
    } else if (sim.sleep > 8) {
      recomendaciones.push("💤 El sueño excesivo puede afectar el metabolismo. 7-8 horas es ideal");
    }
    
    if (sim.walk < 30) {
      recomendaciones.push("🚶‍♂️ Intenta caminar al menos 30 minutos diarios para un mejor control glucémico");
    }
    
    return recomendaciones;
  }
  
  // Descargar script Python
  function downloadPythonScript() {
    const pythonScript = `#!/usr/bin/env python3
"""
Analizador de Simulaciones Diabéticas
======================================

Script para procesar archivos CSV exportados por la app educativa
'Equilibrio Diabético' y generar informes resumen con visualizaciones.

Uso:
    python analisis_simulaciones.py /ruta/a/tus/archivos_csv/

Requisitos:
    pip install pandas matplotlib seaborn jinja2

Características:
    - Analiza múltiples archivos CSV de simulaciones
    - Genera gráficos de tendencias (glucosa vs tiempo)
    - Crea un informe HTML interactivo
    - Detecta patrones en hidratos, ejercicio y sueño
"""

import os
import sys
import glob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from jinja2 import Template
import base64
from io import BytesIO

# Configuración de estilos para gráficos
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.family'] = 'Segoe UI'
plt.rcParams['axes.titleweight'] = 'bold'

def cargar_simulaciones(ruta_csv):
    """
    Carga todos los archivos CSV de simulaciones en una carpeta
    """
    archivos = glob.glob(os.path.join(ruta_csv, "*.csv"))
    if not archivos:
        print(f"❌ No se encontraron archivos CSV en: {ruta_csv}")
        sys.exit(1)
    
    dfs = []
    for archivo in archivos:
        try:
            df = pd.read_csv(archivo)
            df['archivo_origen'] = os.path.basename(archivo)
            dfs.append(df)
        except Exception as e:
            print(f"⚠️ Error al leer {archivo}: {str(e)}")
    
    if not dfs:
        print("❌ No se pudieron cargar datos válidos de ningún archivo")
        sys.exit(1)
    
    return pd.concat(dfs, ignore_index=True)

def generar_grafico_tendencia(df):
    """
    Genera un gráfico de tendencia de glucosa a lo largo del tiempo
    """
    plt.figure(figsize=(12, 6))
    
    # Convertir fecha y hora a datetime
    df['datetime'] = pd.to_datetime(df['Fecha'] + ' ' + df['Hora'], dayfirst=True, errors='coerce')
    df = df.sort_values('datetime').dropna(subset=['datetime'])
    
    if not df.empty:
        # Gráfico principal
        sns.lineplot(data=df, x='datetime', y='Glucosa (mg/dL)', 
                    marker='o', linewidth=2.5, markersize=10,
                    color='#2980b9', label='Glucosa medida')
        
        # Líneas de referencia
        plt.axhline(y=140, color='#e74c3c', linestyle='--', alpha=0.7, label='Límite alto (>140 mg/dL)')
        plt.axhline(y=80, color='#2ecc71', linestyle='--', alpha=0.7, label='Límite bajo (<80 mg/dL)')
        
        plt.title('📈 Tendencia de Glucosa en Sangre', fontsize=16, pad=20)
        plt.xlabel('Fecha y Hora', fontsize=12)
        plt.ylabel('Glucosa (mg/dL)', fontsize=12)
        plt.legend(loc='best')
        plt.tight_layout()
        
        # Formato del eje X
        plt.gcf().autofmt_xdate()
    
    # Guardar en buffer
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    plt.close()
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"

def generar_grafico_factores(df):
    """
    Genera un gráfico comparando los factores que afectan la glucosa
    """
    plt.figure(figsize=(12, 6))
    
    # Preparar datos
    factores = pd.DataFrame({
        'Factor': ['Hidratos de carbono', 'Minutos caminando', 'Horas de sueño'],
        'Valor': [df['Hidratos (g)'].mean(), df['Caminata (min)'].mean(), df['Sueño (h)'].mean()],
        'Unidad': ['gramos', 'minutos', 'horas'],
        'Color': ['#c2185b', '#1976d2', '#2e7d32']
    })
    
    # Gráfico de barras
    bars = plt.bar(factores['Factor'], factores['Valor'], 
                  color=factores['Color'], alpha=0.85,
                  edgecolor='white', linewidth=2)
    
    # Añadir valores en las barras
    for bar, valor, unidad in zip(bars, factores['Valor'], factores['Unidad']):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{valor:.1f} {unidad}', 
                ha='center', va='bottom', fontweight='bold')
    
    plt.title('📊 Factores que Influyen en la Glucosa', fontsize=16, pad=20)
    plt.ylabel('Valor Promedio', fontsize=12)
    plt.ylim(0, max(factores['Valor']) * 1.3)
    plt.tight_layout()
    
    # Guardar en buffer
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    plt.close()
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"

def generar_informe_html(df, grafico_tendencia, grafico_factores):
    """
    Genera un informe HTML interactivo con los resultados del análisis
    """
    # Calcular estadísticas clave
    glucosa_promedio = df['Glucosa (mg/dL)'].mean()
    hc_promedio = df['Hidratos (g)'].mean()
    caminata_promedio = df['Caminata (min)'].mean()
    sueño_promedio = df['Sueño (h)'].mean()
    
    # Determinar estado general
    if glucosa_promedio > 140:
        estado = "⚠️ ALTO - Requiere atención"
        color_estado = "#e74c3c"
    elif glucosa_promedio < 80:
        estado = "⚠️ BAJO - Riesgo de hipoglucemia"
        color_estado = "#f39c12"
    else:
        estado = "✅ ÓPTIMO - Buen control"
        color_estado = "#2ecc71"
    
    # Plantilla HTML
    template = Template("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>📊 Informe de Simulaciones Diabéticas</title>
        <style>
            :root {
                --primary: #2980b9;
                --success: #2ecc71;
                --warning: #f39c12;
                --danger: #e74c3c;
                --light: #f9fbfd;
                --dark: #2c3742;
            }
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }
            body {
                font-family: 'Segoe UI', system-ui, sans-serif;
                background: var(--light);
                color: var(--dark);
                line-height: 1.6;
                padding: 1rem;
                max-width: 1200px;
                margin: 0 auto;
            }
            header {
                text-align: center;
                padding: 2rem 0;
                background: white;
                border-radius: 16px;
                margin-bottom: 2rem;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            }
            h1 {
                color: var(--primary);
                font-size: 2.2rem;
                margin-bottom: 0.5rem;
            }
            .subtitle {
                color: #7f8c8d;
                font-size: 1.2rem;
            }
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 1.5rem;
                margin-bottom: 2rem;
            }
            .stat-card {
                background: white;
                border-radius: 16px;
                padding: 1.5rem;
                text-align: center;
                box-shadow: 0 4px 8px rgba(0,0,0,0.08);
                border: 2px solid #e0e6ed;
                transition: all 0.3s ease;
            }
            .stat-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 6px 15px rgba(0,0,0,0.12);
            }
            .stat-value {
                font-size: 2.5rem;
                font-weight: bold;
                margin: 0.5rem 0;
            }
            .stat-label {
                color: #7f8c8d;
                font-size: 1.1rem;
            }
            .estado {
                padding: 0.8rem;
                border-radius: 12px;
                font-weight: bold;
                font-size: 1.3rem;
                text-align: center;
                margin: 1.5rem 0;
            }
            .graficos {
                display: grid;
                grid-template-columns: 1fr;
                gap: 2rem;
                margin: 2rem 0;
            }
            .grafico-container {
                background: white;
                border-radius: 16px;
                padding: 1.5rem;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            }
            .recomendaciones {
                background: #e8f4fc;
                border-radius: 16px;
                padding: 2rem;
                margin: 2rem 0;
                border-left: 4px solid #3498db;
            }
            .recomendaciones h2 {
                color: #2980b9;
                margin-bottom: 1rem;
            }
            .recomendaciones ul {
                margin-left: 1.5rem;
                margin-top: 0.8rem;
            }
            .recomendaciones li {
                margin-bottom: 0.7rem;
                line-height: 1.5;
            }
            footer {
                text-align: center;
                margin-top: 3rem;
                padding: 1.5rem;
                color: #7f8c8d;
                font-size: 0.95rem;
                border-top: 1px solid #eee;
            }
            @media (max-width: 768px) {
                .stats-grid {
                    grid-template-columns: 1fr;
                }
                .stat-value {
                    font-size: 2rem;
                }
            }
        </style>
    </head>
    <body>
        <header>
            <h1>⚕️ Informe de Simulaciones Diabéticas</h1>
            <p class="subtitle">Análisis de datos educativos - Generado el {{ fecha_actual }}</p>
        </header>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Glucosa Promedio</div>
                <div class="stat-value" style="color: {{ color_glucosa }};">{{ glucosa_promedio }} mg/dL</div>
                <div>{{ num_simulaciones }} simulaciones analizadas</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Hidratos de Carbono</div>
                <div class="stat-value">{{ hc_promedio }} g</div>
                <div>Por comida</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Actividad Física</div>
                <div class="stat-value">{{ caminata_promedio }} min</div>
                <div>Caminata diaria promedio</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Sueño</div>
                <div class="stat-value">{{ sueño_promedio }} h</div>
                <div>Horas por noche</div>
            </div>
        </div>
        
        <div class="estado" style="background: {{ color_estado }}15; border-color: {{ color_estado }};">
            Estado General: {{ estado }}
        </div>
        
        <div class="graficos">
            <div class="grafico-container">
                <h2 style="color: var(--primary); margin-bottom: 1.5rem;">Tendencia de Glucosa en el Tiempo</h2>
                <img src="{{ grafico_tendencia }}" alt="Gráfico de tendencia de glucosa" style="max-width: 100%; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            </div>
            
            <div class="grafico-container">
                <h2 style="color: var(--primary); margin-bottom: 1.5rem;">Factores que Influyen en la Glucosa</h2>
                <img src="{{ grafico_factores }}" alt="Gráfico de factores" style="max-width: 100%; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            </div>
        </div>
        
        <div class="recomendaciones">
            <h2>💡 Recomendaciones Personalizadas</h2>
            <ul>
                {% if glucosa_promedio > 140 %}
                <li>🔴 <strong>Glucosa alta:</strong> Considera reducir hidratos de carbono a 45-50g por comida y aumentar caminata a 30-40 minutos diarios.</li>
                {% elif glucosa_promedio < 80 %}
                <li>🟡 <strong>Glucosa baja:</strong> Asegúrate de consumir al menos 40g de hidratos por comida y reduce la intensidad de la caminata si es muy prolongada.</li>
                {% else %}
                <li>🟢 <strong>Buen control:</strong> Mantén estos hábitos. Pequeños ajustes en el sueño (7-8 horas) pueden mejorar aún más el control.</li>
                {% endif %}
                
                {% if sueño_promedio < 7 %}
                <li>💤 <strong>Sueño insuficiente:</strong> Prioriza dormir 7-8 horas. La falta de sueño aumenta la resistencia a la insulina un 25-30%.</li>
                {% endif %}
                
                {% if caminata_promedio < 30 %}
                <li>🚶‍♂️ <strong>Actividad reducida:</strong> Caminar 30 minutos diarios puede reducir la glucosa en un 15-20%.</li>
                {% endif %}
                
                <li>📊 <strong>Siguiente paso:</strong> Exporta más simulaciones de diferentes momentos del día para ver patrones completos.</li>
            </ul>
        </div>
        
        <footer>
            <p>Informe generado automáticamente por el Analizador de Simulaciones Diabéticas</p>
            <p>Basado en datos educativos de la app 'Equilibrio Diabético' • MIT License © 2025</p>
            <p style="margin-top: 0.5rem; font-size: 0.9rem; color: #e74c3c;">
                *Este informe es con fines educativos. Consulta siempre con tu médico para tu manejo personalizado.
            </p>
        </footer>
    </body>
    </html>
    """)
    
    # Determinar color según glucosa promedio
    if glucosa_promedio > 140:
        color_glucosa = "#e74c3c"
    elif glucosa_promedio < 80:
        color_glucosa = "#f39c12"
    else:
        color_glucosa = "#2ecc71"
    
    # Renderizar HTML
    html_content = template.render(
        fecha_actual=datetime.now().strftime("%d de %B de %Y a las %H:%M"),
        glucosa_promedio=round(glucosa_promedio, 1),
        hc_promedio=round(hc_promedio, 1),
        caminata_promedio=round(caminata_promedio, 1),
        sueño_promedio=round(sueño_promedio, 1),
        num_simulaciones=len(df),
        estado=estado,
        color_estado=color_estado,
        color_glucosa=color_glucosa,
        grafico_tendencia=grafico_tendencia,
        grafico_factores=grafico_factores
    )
    
    # Guardar informe
    nombre_informe = f"informe_diabetes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(nombre_informe, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Informe generado: {nombre_informe}")
    print(f"   - Glucosa promedio: {glucosa_promedio:.1f} mg/dL")
    print(f"   - {len(df)} simulaciones analizadas")
    return nombre_informe

def main():
    """Función principal del script"""
    if len(sys.argv) != 2:
        print("❌ Uso incorrecto. Debes especificar la ruta de los archivos CSV:")
        print("   python analisis_simulaciones.py /ruta/a/tus/csv/")
        sys.exit(1)
    
    ruta_csv = sys.argv[1]
    
    if not os.path.exists(ruta_csv):
        print(f"❌ La ruta no existe: {ruta_csv}")
        sys.exit(1)
    
    print("🚀 Iniciando análisis de simulaciones diabéticas...")
    print(f"📂 Analizando archivos en: {ruta_csv}")
    
    # Cargar datos
    df = cargar_simulaciones(ruta_csv)
    
    # Generar gráficos
    print("📊 Generando gráficos de tendencias...")
    grafico_tendencia = generar_grafico_tendencia(df)
    grafico_factores = generar_grafico_factores(df)
    
    # Generar informe
    print("📝 Creando informe HTML interactivo...")
    informe = generar_informe_html(df, grafico_tendencia, grafico_factores)
    
    print("\\n🎉 ¡Análisis completado!")
    print(f"   🔗 Abre el informe en tu navegador: {os.path.abspath(informe)}")
    print("\\n💡 Consejos para usar este informe:")
    print("   - Comparte el HTML con tus estudiantes o pacientes")
    print("   - Usa los gráficos para discutir patrones en clase")
    print("   - Exporta más simulaciones para actualizar el análisis")

if __name__ == "__main__":
    main()
`;
    
    // Crear blob con el script
    const blob = new Blob([pythonScript], { type: 'text/x-python' });
    const url = URL.createObjectURL(blob);
    
    const link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", "analisis_simulaciones.py");
    link.style.visibility = 'hidden';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    // Liberar memoria
    setTimeout(() => URL.revokeObjectURL(url), 100);
    
    // Mensaje de confirmación
    alert("¡Script Python descargado!\\n\\nInstrucciones:\\n1. Guarda el archivo en una carpeta llamada 'tools'\\n2. Exporta tus simulaciones como CSV\\n3. Ejecuta: python tools/analisis_simulaciones.py /tu/carpeta/con/csvs/");
  }
});