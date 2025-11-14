# Dataset Simulado - UEFA Champions League 2024-25

## 📊 Estadísticas del Dataset

- **Total de Tiros**: 2,233
- **Total de Partidos**: 56
- **Equipos**: 15 principales
- **Jugadores Únicos**: 85
- **Temporada**: 2024-25

## 🎯 Equipos Incluidos

| Equipo | Goles | Eficacia Esperada |
|--------|-------|-------------------|
| Real Madrid | 44 | 28% |
| Atlético Madrid | 42 | 18% |
| Arsenal | 42 | 22% |
| Manchester City | 42 | 25% |
| Barcelona | 40 | 23% |
| Bayern Munich | 40 | 24% |
| Paris Saint-Germain | 39 | 22% |
| Dortmund | 34 | 20% |
| Aston Villa | 32 | 20% |
| Liverpool | 30 | 21% |
| Benfica | 29 | 18% |
| AC Milan | 27 | 19% |
| Napoli | 24 | 21% |
| Manchester United | 21 | 19% |
| Inter Milan | 20 | 20% |

## 👥 Jugadores Destacados

### Real Madrid
- Vinícius Jr
- Jude Bellingham
- Rodrygo
- Kylian Mbappé
- Nacho
- Federico Valverde

### Manchester City
- Erling Haaland
- Phil Foden
- Julián Álvarez
- Grealish
- De Bruyne

### Barcelona
- Robert Lewandowski
- Ferran Torres
- Ansu Fati
- Ousmane Dembélé
- Pedri
- Gavi

## 📈 Características del Dataset

- **Coordenadas de Tiro**: Rango 0-100 (cancha normalizada)
  - Equipos locales tienden a disparar cerca del arco contrario (x: 60-100)
  - Equipos visitantes tienden a disparar desde el otro lado (x: 0-40)

- **Resultados de Tiro**:
  - goal
  - missed
  - saved
  - blocked

- **Situaciones de Tiro**:
  - open_play (juego abierto)
  - corner (córner)
  - free_kick (tiro libre)
  - counter_attack (contraataque)
  - penalty (penalti)

- **Tipos de Tiro**:
  - left_foot (pie izquierdo)
  - right_foot (pie derecho)
  - header (cabezazo)
  - bicycle_kick (chilena)

## 🔧 Generación del Dataset

El dataset fue generado usando `generate_sample_data.py` con:
- Distribución realista de tiros por partido (12-28 tiros por equipo)
- Eficiencia basada en datos reales de cada equipo
- Coordenadas realistas agrupadas alrededor de las áreas de peligro
- Fechas distribuidas a lo largo de la temporada 2024-25

## 📂 Archivo

`data/sample_shots.csv` - Contiene todas las estadísticas en formato CSV
