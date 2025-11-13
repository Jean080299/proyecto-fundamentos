# 🎯 Analizador de Tiros - UEFA Champions League

Sistema integral de análisis y visualización de datos de tiros en la UEFA Champions League. Permite a equipos y analistas deportivos visualizar patrones de tiros, comparar eficacia entre equipos y jugadores, identificar zonas del campo con mayor probabilidad de gol, y facilitar la toma de decisiones basada en datos.

## 🔐 Sistema de Autenticación

La aplicación ahora incluye un sistema completo de **registro y login de usuarios** con **contraseñas seguras**:

- **Registro**: Crea una nueva cuenta con validaciones de seguridad robustas
- **Contraseñas Seguras**: Requisitos estrictos de complejidad
  - Mínimo 8 caracteres
  - Debe incluir mayúscula (A-Z)
  - Debe incluir minúscula (a-z)
  - Debe incluir número (0-9)
  - Debe incluir carácter especial (!@#$%^&*)
- **Login**: Acceso seguro a tu cuenta personal
- **Gestión de Perfil**: Visualiza tu información y cambia tu contraseña
- **Protección de Datos**: Contraseñas hasheadas con SHA-256
- **Session State**: Mantiene tu sesión activa mientras uses la app

👉 **Ver detalles en** [AUTENTICACION.md](AUTENTICACION.md)

## ✨ Características Principales

### 📊 Visualizaciones Avanzadas
- **Mapa de Tiros**: Visualización interactiva de tiros en la cancha con marcas de goles y no-goles
- **Heatmaps de Densidad**: Identifica zonas con mayor concentración de tiros
- **Heatmaps de Probabilidad**: Muestra zonas del campo con mayor probabilidad de gol
- **Gráficos Comparativos**: Análisis visual de eficacia entre equipos y jugadores

### 📈 Análisis de Datos
- **Eficacia de Tiros**: Calcula el porcentaje de goles por equipo, jugador, temporada y partido
- **Identificación de Zonas**: Detecta automáticamente áreas del campo con mayor probabilidad de éxito
- **Comparativas**: Compara métricas entre múltiples entidades (equipos, jugadores, temporadas)
- **Rankings**: Top jugadores por goles y eficacia

### 🎛️ Filtros Interactivos
- Por temporada
- Por equipo
- Por jugador
- Estadísticas globales y filtradas en tiempo real

### 💡 Toma de Decisiones Basada en Datos
- **Recomendaciones Automáticas**: Sugiere estrategias basadas en análisis de datos
- **Reportes Ejecutivos**: Resumen de rendimiento general
- **Análisis de Patrones**: Identifica equipos y jugadores referencia
- **Estrategias de Mejora**: Propuestas concretas basadas en datos históricos

## 📁 Estructura del Proyecto

```
.
├── README.md                    # Este archivo
├── requirements.txt             # Dependencias Python
├── data/
│   └── sample_shots.csv        # Dataset de ejemplo
└── src/
    ├── __init__.py             # Marcador de paquete
    ├── app.py                  # App Streamlit principal
    ├── data.py                 # Funciones de análisis de datos
    └── visuals.py              # Funciones de visualización
```

## 📋 Formato de Datos Esperado

El archivo CSV debe contener las siguientes columnas (flexibles, algunas opcionales):

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `match_id` | str/int | Identificador único del partido |
| `season` | str | Temporada (ej: 2023-24) |
| `team` | str | Equipo que dispara |
| `opponent` | str | Equipo contrario |
| `player` | str | Nombre del jugador |
| `minute` | int | Minuto del disparo |
| `x` | float | Coordenada X (0-100) |
| `y` | float | Coordenada Y (0-100) |
| `result` | str | Resultado: "goal", "missed", "saved", "blocked" |
| `situation` | str | Tipo de situación: "open_play", "corner", "free_kick" |
| `shot_type` | str | Tipo de tiro: "left_foot", "right_foot", "header" |

**Nota**: Las coordenadas (x, y) están en escala 0-100, donde (0,0) es la esquina superior izquierda del campo.

## 🚀 Instalación y Ejecución

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos

1. **Clonar o descargar el proyecto** (si aún no lo has hecho)

2. **Crear y activar entorno virtual** (recomendado):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. **Instalar dependencias**:
```powershell
pip install -r requirements.txt
```

4. **Ejecutar la aplicación**:
```powershell
streamlit run src/app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`.

## 📖 Guía de Uso

### 1. Autenticarse (Nuevo)
- Si es tu primer acceso, ve a la pestaña **"📝 Registrarse"** y crea tu cuenta
- En futuros accesos, usa **"🔑 Iniciar Sesión"** con tus credenciales
- Para más detalles, consulta [AUTENTICACION.md](AUTENTICACION.md)

### 2. Cargar Datos
- En la barra lateral, selecciona "Sube un CSV de tiros"
- Si no cuentas con un archivo, la app usará automáticamente `data/sample_shots.csv`
Usa los selectores en la barra lateral para filtrar por:
- Temporada
- Equipo
- Jugador

### 3. Explorar Tabs

#### 🗺️ **Mapa de Tiros**
- Visualiza todos los tiros en un mapa interactivo de la cancha
- Los goles aparecen en oro, los no-goles en blanco
- Pasa el cursor para ver detalles del jugador y la posición

#### 🔥 **Heatmaps**
- **Densidad de Tiros**: Identifica zonas con mayor concentración de disparos
- **Probabilidad de Gol**: Muestra dónde históricamente hay más goles

#### 📊 **Comparativas**
- Compara equipos, jugadores o temporadas
- Eficacia (%) vs. Total de tiros
- Visualizaciones interactivas para detectar patrones

#### 🎯 **Análisis de Zonas**
- Ajusta la precisión (número de zonas)
- Define mínimo de tiros en una zona para análisis
- Ve las mejores zonas con probabilidad de gol

#### 👥 **Ranking de Jugadores**
- Top 10 jugadores por goles y eficacia
- Tabla completa con todas las estadísticas
- Filtrable por número mínimo de tiros

#### 📋 **Reportes**
- **Resumen General**: Estadísticas clave y mejores performers
- **Equipos**: Tabla completa de eficacia por equipo
- **Jugadores**: Tabla completa de jugadores
- **Análisis de Partidos**: Estadísticas por partido
- **Recomendaciones**: Estrategias basadas en datos para toma de decisiones

## 🔧 Módulos Principales

### `src/data.py`

Funciones de análisis y procesamiento:

- `load_shots(csv_path)`: Carga y normaliza el CSV
- `calculate_shooting_efficiency(df, group_by)`: Calcula eficacia (%)
- `identify_goal_zones(df, bins, min_shots)`: Identifica zonas de gol
- `compare_teams(df)`: Compara equipos
- `compare_players(df, min_shots)`: Compara jugadores
- `analyze_by_match(df)`: Estadísticas por partido
- `analyze_by_season(df)`: Estadísticas por temporada

### `src/visuals.py`

Funciones de visualización:

- `plot_shot_scatter(df, team)`: Mapa de tiros (Plotly)
- `plot_shot_heatmap(df, team)`: Heatmap de densidad (Matplotlib)
- `plot_goal_zones_heatmap(df, bins)`: Heatmap de probabilidad
- `plot_efficiency_comparison(df, group_by)`: Gráfico de eficacia
- `plot_shots_vs_goals(df, group_by)`: Tiros vs goles
- `plot_top_performers(df, metric, top_n)`: Top jugadores

### `src/app.py`

Interfaz Streamlit con:
- Sidebar para carga de datos y filtros
- 6 tabs con diferentes análisis
- Estadísticas globales
- Reportes y recomendaciones

## 📊 Ejemplo de Uso

1. Abre la app: `streamlit run src/app.py`
2. Carga `data/sample_shots.csv` o tu propio CSV
3. En la barra lateral, filtra por equipo "Manchester City"
4. Ve al tab "🔥 Heatmaps" para ver zonas de mayor densidad
5. Ve a "📋 Reportes" → "Recomendaciones de Toma de Decisiones" para sugerencias estratégicas

## 🛠️ Desarrollo y Extensiones

### Agregar Nuevas Métricas

Edita `src/data.py` y añade funciones como:
```python
def calculate_xg(df):
    """Calcula Expected Goals (xG)"""
    # Tu lógica aquí
    pass
```

Luego úsala en `src/app.py`.

### Personalizar Visualizaciones

Edita `src/visuals.py` para cambiar colores, escalas, etc.

### Importar Datos Dinámicamente

Modifica `src/app.py` para conectar a una base de datos o API.

## 🚨 Solución de Problemas

### Error: `ModuleNotFoundError: No module named 'src'`
- Asegúrate de estar en la raíz del proyecto
- Ejecuta: `streamlit run src/app.py` (no `python src/app.py`)
- Activa el entorno virtual antes de ejecutar

### Error: `No such file or directory: 'data/sample_shots.csv'`
- Asegúrate de que el archivo existe en `data/`
- Carga un CSV manualmente con el uploader

### La app está lenta
- Reduce el número de bins en análisis de zonas
- Filtra datos antes de hacer análisis pesados
- Usa un dataset más pequeño para pruebas

## 📝 Dependencias

Ver `requirements.txt`:
- `streamlit`: Framework para apps web
- `pandas`: Análisis de datos
- `plotly`: Visualizaciones interactivas
- `seaborn`: Estadísticas visuales
- `matplotlib`: Gráficos
- `numpy`: Computación numérica

## 📜 Licencia

Este proyecto es de uso libre para fines educativos y deportivos.

## 🙋 Preguntas y Soporte

Para reportar bugs o sugerir mejoras, documenta el problema y proporciona:
- Paso a paso para reproducir
- Versión de Python y dependencias
- Tipo de datos usado (sample o propio)
