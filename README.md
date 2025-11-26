# ⚖️ Equilibrio Diabético - Simulador Educativo

![Preview de la aplicación](https://via.placeholder.com/800x400/e3f2fd/2980b9?text=Simulador+Diabetes+Interactivo)

Una aplicación web educativa **100% offline** que ayuda a pacientes diabéticos tipo 2 (sin insulina) a entender cómo los hidratos de carbono, el ejercicio y el sueño afectan sus niveles de glucosa en sangre.

## ✨ Características

- **Simulador básico**: Interfaz intuitiva para ajustar parámetros y ver resultados
- **Exportación de datos**: Guarda resultados como CSV o JSON
- **Análisis avanzado**: Script Python para generar informes con gráficos interactivos
- **Totalmente offline**: Funciona sin conexión a internet
- **Diseño responsivo**: Perfecto para móviles, tablets y escritorios
- **Educación médica**: Basado en guías de la American Diabetes Association (ADA)

## 🚀 Cómo usarlo

### Versión web (recomendado)
1. Visita: [https://whoissif.github.io/equilibrio-diabetes](https://whoissif.github.io/Equilibrio-Diabetico/)
2. Ajusta los parámetros usando los deslizadores
3. Haz clic en "Calcular glucosa" para ver los resultados
4. Exporta tus simulaciones como CSV o JSON si lo deseas

### Versión local
```bash
# Clona el repositorio
git clone https://github.com/tuusuario/equilibrio-diabetes.git

# Abre el archivo index.html en tu navegador
open equilibrio-diabetes/index.html
```

## 📊 Análisis Avanzado con Python

Para un análisis profundo de tus simulaciones:

### Requisitos
- Python 3.8 o superior
- Paquetes: `pandas matplotlib seaborn jinja2`
  ```bash
  pip install pandas matplotlib seaborn jinja2
  ```

### Pasos
1. **Exporta tus simulaciones** desde la app web como CSV
2. **Descarga el script** de análisis:
   - En la app web, ve a la pestaña "Análisis Avanzado"
   - Haz clic en "Descargar script Python"
   - Guarda el archivo en una carpeta llamada `tools/`
3. **Ejecuta el análisis**:
   ```bash
   python tools/analisis_simulaciones.py /tu/carpeta/con/csvs/
   ```
4. **Abre el informe** generado:
   - Se creará un archivo `informe_diabetes_YYYYMMDD_HHMMSS.html`
   - Ábrelo en cualquier navegador para ver gráficos y recomendaciones

### Ejemplo de uso
```bash
# Estructura de carpetas
tu_proyecto/
├── tools/
│   └── analisis_simulaciones.py
└── mis_simulaciones/
    ├── simulacion1.csv
    ├── simulacion2.csv
    └── simulacion3.csv

# Comando de análisis
python tools/analisis_simulaciones.py mis_simulaciones/
```

## 🎓 Para educadores y profesionales médicos

Esta herramienta es ideal para:
- **Clases de nutrición y diabetes**: Demuestra visualmente el impacto de los factores
- **Consultas médicas**: Ayuda a pacientes a entender su manejo
- **Talleres educativos**: Genera informes personalizados para cada paciente
- **Material didáctico**: Exporta simulaciones como material de estudio

### Consejos para usar en clase
1. Pide a los estudiantes que exporten 3-5 simulaciones diferentes
2. Ejecuta el análisis avanzado con todos los archivos
3. Muestra el informe HTML en clase para discutir patrones
4. Pide a los estudiantes que comparen sus resultados con las recomendaciones

## 🛠️ Tecnologías utilizadas

- **Frontend**: HTML5, CSS3, JavaScript puro
- **Backend (opcional)**: Python 3 con pandas, matplotlib, seaborn, jinja2
- **Diseño**: Responsive, accesible, con paleta de colores médica
- **Arquitectura**: 100% funcional offline + análisis avanzado opcional

## 📜 Licencia

MIT License © 2025 - Código abierto para uso educativo y sin fines de lucro.

> **Nota importante**: Esta es una herramienta educativa. Los resultados son estimaciones y no sustituyen el consejo médico profesional.

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Por favor abre un issue o pull request para:
- Mejorar los algoritmos de simulación
- Añadir más factores (estrés, medicación oral, etc.)
- Traducciones a otros idiomas
- Nuevas características educativas
- Optimización de la interfaz

---

## 🙏 Agradecimientos

Desarrollado con ❤️ para:
- Pacientes diabéticos tipo 2 que buscan entender su condición
- Educadores médicos que enseñan manejo no farmacológico
- Familias que apoyan a seres queridos con diabetes

Basado en evidencia médica de la [American Diabetes Association](https://www.diabetes.org/).

---

**MIT License** - Código abierto para educación médica
