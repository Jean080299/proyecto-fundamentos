"""
Script para generar un dataset simulado de tiros de la UEFA Champions League 2024-25
con equipos, jugadores y estadísticas realistas.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Equipos actuales de la UEFA Champions League 2024-25 (principales)
TEAMS = {
    'Real Madrid': {'players': ['Vinícius Jr', 'Jude Bellingham', 'Rodrygo', 'Kylian Mbappé', 'Nacho', 'Federico Valverde'], 
                     'efficiency': 0.28},
    'Manchester City': {'players': ['Erling Haaland', 'Phil Foden', 'Julián Álvarez', 'Grealish', 'De Bruyne', 'Álvarez'],
                        'efficiency': 0.25},
    'Arsenal': {'players': ['Bukayo Saka', 'Gabriel Jesus', 'Martin Ødegaard', 'Leandro Trossard', 'Kai Havertz', 'Thomas Partey'],
                'efficiency': 0.22},
    'Barcelona': {'players': ['Robert Lewandowski', 'Ferran Torres', 'Ansu Fati', 'Ousmane Dembélé', 'Pedri', 'Gavi'],
                  'efficiency': 0.23},
    'Bayern Munich': {'players': ['Serge Gnabry', 'Leroy Sané', 'Harry Kane', 'Jamal Musiala', 'Kingsley Coman', 'Dayot Upamecano'],
                      'efficiency': 0.24},
    'Liverpool': {'players': ['Mohamed Salah', 'Luis Díaz', 'Diogo Jota', 'Cody Gakpo', 'Darwin Núñez', 'Sadio Mané'],
                  'efficiency': 0.21},
    'Inter Milan': {'players': ['Lautaro Martínez', 'Marcus Thuram', 'Nicolo Barella', 'Henrikh Mkhitaryan', 'Hakan Çalhanoglu', 'Federico Dimarco'],
                    'efficiency': 0.20},
    'AC Milan': {'players': ['Rafael Leão', 'Christian Pulisic', 'Olivier Giroud', 'Álvaro Morata', 'Fikayo Tomori', 'Ismael Bennacer'],
                 'efficiency': 0.19},
    'Paris Saint-Germain': {'players': ['Kylian Mbappé', 'Neymar', 'Marco Asensio', 'Luis Enrique', 'Achraf Hakimi', 'Ousmane Dembélé'],
                            'efficiency': 0.22},
    'Dortmund': {'players': ['Jude Bellingham', 'Marco Reus', 'Niclas Füllkrug', 'Karim Adeyemi', 'Ian Maatsen', 'Emre Can'],
                 'efficiency': 0.20},
    'Atlético Madrid': {'players': ['Diego Simeone', 'Antoine Griezmann', 'Álvaro Morata', 'Rodrigo De Paul', 'Nahuel Molina', 'José Giménez'],
                        'efficiency': 0.18},
    'Napoli': {'players': ['Victor Osimhen', 'Matteo Politano', 'Khvicha Kvaratskhelia', 'Piotr Zieliński', 'Alessandro Buongiorno', 'Juan Jesús'],
               'efficiency': 0.21},
    'Manchester United': {'players': ['Marcus Rashford', 'Antony', 'Bruno Fernandes', 'Alejandro Garnacho', 'Casemiro', 'Aaron Wan-Bissaka'],
                          'efficiency': 0.19},
    'Aston Villa': {'players': ['Ollie Watkins', 'Bukayo Saka', 'Philippe Coutinho', 'John McGinn', 'Emiliano Martínez', 'Jhon Durán'],
                    'efficiency': 0.20},
    'Benfica': {'players': ['João Félix', 'Rafa Silva', 'Petar Musa', 'Gonçalo Ramos', 'Álex Grimaldo', 'Enzo Fernández'],
                'efficiency': 0.18},
}

# Situaciones de tiro
SITUATIONS = ['open_play', 'corner', 'free_kick', 'counter_attack', 'penalty']

# Tipos de tiro
SHOT_TYPES = ['left_foot', 'right_foot', 'header', 'bicycle_kick']

def generate_shots_for_match(home_team, away_team, match_id, date, season='2024-25'):
    """Genera tiros realistas para un partido."""
    shots = []
    
    # Número de tiros por equipo (realista: 10-30 tiros por equipo)
    home_shots = np.random.randint(12, 28)
    away_shots = np.random.randint(12, 28)
    
    # Eficiencia de los equipos
    home_efficiency = TEAMS[home_team]['efficiency']
    away_efficiency = TEAMS[away_team]['efficiency']
    
    # Generar tiros del equipo local
    for i in range(home_shots):
        minute = np.random.randint(1, 91)
        
        # Probabilidad de gol basada en eficiencia
        is_goal = np.random.random() < home_efficiency
        
        # Generar coordenadas realistas (más cercanas al arco contrario)
        x = np.random.normal(loc=85, scale=10)  # Concentración cerca del arco
        y = np.random.normal(loc=50, scale=15)
        x = np.clip(x, 60, 100)
        y = np.clip(y, 5, 95)
        
        player = np.random.choice(TEAMS[home_team]['players'])
        
        shots.append({
            'match_id': match_id,
            'date': date,
            'season': season,
            'team': home_team,
            'opponent': away_team,
            'player': player,
            'minute': minute,
            'x': round(x, 2),
            'y': round(y, 2),
            'result': 'goal' if is_goal else np.random.choice(['missed', 'saved', 'blocked']),
            'situation': np.random.choice(SITUATIONS),
            'shot_type': np.random.choice(SHOT_TYPES),
        })
    
    # Generar tiros del equipo visitante
    for i in range(away_shots):
        minute = np.random.randint(1, 91)
        
        # Probabilidad de gol basada en eficiencia
        is_goal = np.random.random() < away_efficiency
        
        # Generar coordenadas realistas (más cercanas al arco contrario, pero desde el otro lado)
        x = np.random.normal(loc=15, scale=10)  # Concentración cerca del arco contrario
        y = np.random.normal(loc=50, scale=15)
        x = np.clip(x, 0, 40)
        y = np.clip(y, 5, 95)
        
        player = np.random.choice(TEAMS[away_team]['players'])
        
        shots.append({
            'match_id': match_id,
            'date': date,
            'season': season,
            'team': away_team,
            'opponent': home_team,
            'player': player,
            'minute': minute,
            'x': round(x, 2),
            'y': round(y, 2),
            'result': 'goal' if is_goal else np.random.choice(['missed', 'saved', 'blocked']),
            'situation': np.random.choice(SITUATIONS),
            'shot_type': np.random.choice(SHOT_TYPES),
        })
    
    return shots

def generate_dataset():
    """Genera un dataset completo de la temporada 2024-25."""
    
    # Crear emparejamientos (fase de grupos y eliminatorias simuladas)
    team_list = list(TEAMS.keys())
    all_shots = []
    match_id = 1
    start_date = datetime(2024, 9, 1)
    
    # Crear algunos partidos realistas (fase de grupos)
    # Cada equipo juega múltiples partidos
    print("Generando partidos de la UEFA Champions League 2024-25...")
    
    for round_num in range(8):  # 8 jornadas en grupos + eliminatorias
        # Crear emparejamientos para esta ronda
        shuffled_teams = team_list.copy()
        random.shuffle(shuffled_teams)
        
        for i in range(0, len(shuffled_teams) - 1, 2):
            home_team = shuffled_teams[i]
            away_team = shuffled_teams[i + 1]
            
            match_date = start_date + timedelta(days=round_num * 7 + np.random.randint(0, 7))
            
            # Generar tiros para este partido
            shots = generate_shots_for_match(home_team, away_team, match_id, match_date.strftime('%Y-%m-%d'))
            all_shots.extend(shots)
            
            match_id += 1
            
            if match_id > 150:  # Limitar a 150 partidos simulados
                break
        
        if match_id > 150:
            break
    
    # Crear DataFrame
    df = pd.DataFrame(all_shots)
    
    print(f"Dataset generado: {len(df)} tiros en {df['match_id'].nunique()} partidos")
    print(f"Equipos: {df['team'].nunique()}")
    print(f"Jugadores únicos: {df['player'].nunique()}")
    print(f"\nResumen de eficacia:")
    print(df.groupby('team').agg({
        'result': lambda x: (x == 'goal').sum(),
    }).rename(columns={'result': 'goles'}).sort_values('goles', ascending=False))
    
    return df

if __name__ == '__main__':
    # Generar dataset
    dataset = generate_dataset()
    
    # Guardar a CSV
    output_path = 'data/sample_shots.csv'
    dataset.to_csv(output_path, index=False)
    print(f"\n✅ Dataset guardado en {output_path}")
    print(f"\nPrimeras filas:")
    print(dataset.head(10))
