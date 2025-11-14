"""
Script para generar un dataset simulado AVANZADO de la UEFA Champions League 2024-25
con más realismo, variabilidad y datos actualizados.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Equipos actuales de la UEFA Champions League 2024-25 con datos más detallados
TEAMS_ADVANCED = {
    'Real Madrid': {
        'players': ['Vinícius Jr', 'Jude Bellingham', 'Rodrygo', 'Kylian Mbappé', 'Nacho', 
                   'Federico Valverde', 'Eder Militao', 'Dani Carvajal', 'Aurelien Tchouameni'],
        'efficiency': 0.28,
        'avg_shots_per_match': 18,
        'possession': 0.62
    },
    'Manchester City': {
        'players': ['Erling Haaland', 'Phil Foden', 'Julián Álvarez', 'Jack Grealish', 'Kevin De Bruyne', 
                   'Ilkay Gündogan', 'Kalvin Phillips', 'Kyle Walker', 'Ruben Dias'],
        'efficiency': 0.26,
        'avg_shots_per_match': 16,
        'possession': 0.65
    },
    'Arsenal': {
        'players': ['Bukayo Saka', 'Gabriel Jesus', 'Martin Ødegaard', 'Leandro Trossard', 'Kai Havertz',
                   'Thomas Partey', 'Granit Xhaka', 'Ben White', 'Aaron Ramsdale'],
        'efficiency': 0.24,
        'avg_shots_per_match': 15,
        'possession': 0.58
    },
    'Barcelona': {
        'players': ['Robert Lewandowski', 'Ferran Torres', 'Ansu Fati', 'Ousmane Dembélé', 'Pedri',
                   'Gavi', 'Sergio Busquets', 'Jordi Alba', 'Jules Koundé'],
        'efficiency': 0.25,
        'avg_shots_per_match': 17,
        'possession': 0.63
    },
    'Bayern Munich': {
        'players': ['Serge Gnabry', 'Leroy Sané', 'Harry Kane', 'Jamal Musiala', 'Kingsley Coman',
                   'Dayot Upamecano', 'Joshua Kimmich', 'Leon Goretzka', 'Noussair Mazraoui'],
        'efficiency': 0.27,
        'avg_shots_per_match': 17,
        'possession': 0.60
    },
    'Liverpool': {
        'players': ['Mohamed Salah', 'Luis Díaz', 'Diogo Jota', 'Cody Gakpo', 'Darwin Núñez',
                   'Jordan Henderson', 'Alexis Mac Allister', 'Virgil van Dijk', 'Trent Alexander-Arnold'],
        'efficiency': 0.23,
        'avg_shots_per_match': 14,
        'possession': 0.55
    },
    'Inter Milan': {
        'players': ['Lautaro Martínez', 'Marcus Thuram', 'Nicolo Barella', 'Henrikh Mkhitaryan',
                   'Hakan Çalhanoglu', 'Federico Dimarco', 'Alessandro Bastoni', 'Matteo Darmian', 'André Onana'],
        'efficiency': 0.22,
        'avg_shots_per_match': 14,
        'possession': 0.52
    },
    'AC Milan': {
        'players': ['Rafael Leão', 'Christian Pulisic', 'Olivier Giroud', 'Álvaro Morata', 'Fikayo Tomori',
                   'Ismael Bennacer', 'Théo Hernández', 'Davide Calabria', 'Mike Maignan'],
        'efficiency': 0.21,
        'avg_shots_per_match': 13,
        'possession': 0.50
    },
    'Paris Saint-Germain': {
        'players': ['Kylian Mbappé', 'Neymar', 'Marco Asensio', 'Achraf Hakimi', 'Ousmane Dembélé',
                   'Vitinha', 'Mário Hermoso', 'Marquinhos', 'Gianluigi Donnarumma'],
        'efficiency': 0.24,
        'avg_shots_per_match': 15,
        'possession': 0.57
    },
    'Dortmund': {
        'players': ['Jude Bellingham', 'Marco Reus', 'Niclas Füllkrug', 'Karim Adeyemi', 'Ian Maatsen',
                   'Emre Can', 'Jérôme Azcona', 'Mats Hummels', 'Gregor Kobel'],
        'efficiency': 0.20,
        'avg_shots_per_match': 13,
        'possession': 0.48
    },
    'Atlético Madrid': {
        'players': ['Antoine Griezmann', 'Álvaro Morata', 'Rodrigo De Paul', 'Nahuel Molina',
                   'José Giménez', 'Felipe', 'Axel Witsel', 'Sergio Reguilón', 'Jan Oblak'],
        'efficiency': 0.19,
        'avg_shots_per_match': 12,
        'possession': 0.45
    },
    'Napoli': {
        'players': ['Victor Osimhen', 'Matteo Politano', 'Khvicha Kvaratskhelia', 'Piotr Zieliński',
                   'Alessandro Buongiorno', 'Juan Jesús', 'Mário Rui', 'Stanislav Lobotka', 'Alex Meret'],
        'efficiency': 0.23,
        'avg_shots_per_match': 14,
        'possession': 0.52
    },
    'Manchester United': {
        'players': ['Marcus Rashford', 'Antony', 'Bruno Fernandes', 'Alejandro Garnacho', 'Casemiro',
                   'Aaron Wan-Bissaka', 'Luke Shaw', 'Jonny Evans', 'André Onana'],
        'efficiency': 0.20,
        'avg_shots_per_match': 13,
        'possession': 0.50
    },
    'Aston Villa': {
        'players': ['Ollie Watkins', 'Bukayo Saka', 'Philippe Coutinho', 'John McGinn', 'Emiliano Martínez',
                   'Jhon Durán', 'Ezri Konsa', 'Pau Torres', 'Lucas Digne'],
        'efficiency': 0.21,
        'avg_shots_per_match': 13,
        'possession': 0.48
    },
    'Benfica': {
        'players': ['João Félix', 'Rafa Silva', 'Petar Musa', 'Gonçalo Ramos', 'Álex Grimaldo',
                   'Enzo Fernández', 'Nicolás Otamendi', 'Gilberto', 'Odysseas Vlachodimos'],
        'efficiency': 0.20,
        'avg_shots_per_match': 12,
        'possession': 0.47
    },
    'Shakhtar Donetsk': {
        'players': ['Mykhailo Mudryk', 'Sergei Mudryk', 'Alan Patrick', 'Pedrinho', 'Taison',
                   'Tetê', 'Andriy Lunin', 'Viktor Korniienko', 'Anatoliy Trubin'],
        'efficiency': 0.18,
        'avg_shots_per_match': 11,
        'possession': 0.42
    },
    'RB Leipzig': {
        'players': ['Benjamin Sesko', 'Christoph Baumgartner', 'Willi Orbán', 'Dani Olmo', 'Loïs Openda',
                   'Mohamed Simakan', 'Xaver Schlager', 'Péter Gulácsi', 'Emil Forsberg'],
        'efficiency': 0.19,
        'avg_shots_per_match': 12,
        'possession': 0.45
    }
}

# Situaciones de tiro con pesos realistas
SITUATIONS = {
    'open_play': 0.45,
    'counter_attack': 0.15,
    'corner': 0.15,
    'free_kick': 0.15,
    'penalty': 0.10
}

# Tipos de tiro
SHOT_TYPES = ['left_foot', 'right_foot', 'header', 'bicycle_kick']

def weighted_choice(choices_dict):
    """Selecciona una opción basada en pesos."""
    keys = list(choices_dict.keys())
    weights = list(choices_dict.values())
    return np.random.choice(keys, p=weights)

def generate_realistic_position(team_possession, is_shot_side=True):
    """Genera posición realista de tiro basada en posesión del equipo."""
    if is_shot_side:
        # Tiro hacia arco contrario
        if np.random.random() < team_possession:
            # Equipo con posesión: tiros desde lejos (creación de oportunidades)
            x = np.random.normal(loc=75, scale=12)
        else:
            # Equipo sin posesión: tiros rápidos desde más atrás
            x = np.random.normal(loc=70, scale=15)
    else:
        # Defensa
        x = np.random.normal(loc=25, scale=12)
    
    y = np.random.normal(loc=50, scale=20)
    
    x = np.clip(x, 5, 95)
    y = np.clip(y, 0, 100)
    
    return round(x, 2), round(y, 2)

def generate_shots_for_match(home_team, away_team, match_id, date, season='2024-25'):
    """Genera tiros realistas para un partido con dinámicas avanzadas."""
    shots = []
    
    home_data = TEAMS_ADVANCED[home_team]
    away_data = TEAMS_ADVANCED[away_team]
    
    # Tiros basados en promedio del equipo con variabilidad
    home_shots = int(np.random.normal(loc=home_data['avg_shots_per_match'], scale=3))
    away_shots = int(np.random.normal(loc=away_data['avg_shots_per_match'], scale=3))
    
    home_shots = max(8, min(25, home_shots))
    away_shots = max(8, min(25, away_shots))
    
    # Eficiencia del equipo con variabilidad (algunos partidos mejor/peor)
    home_efficiency = home_data['efficiency'] * np.random.normal(1.0, 0.1)
    away_efficiency = away_data['efficiency'] * np.random.normal(1.0, 0.1)
    
    home_efficiency = np.clip(home_efficiency, 0.08, 0.40)
    away_efficiency = np.clip(away_efficiency, 0.08, 0.40)
    
    # Generar tiros del equipo local
    for i in range(home_shots):
        minute = np.random.randint(1, 91)
        
        # Probabilidad de gol basada en eficiencia
        is_goal = np.random.random() < home_efficiency
        
        # Generar posición realista
        x, y = generate_realistic_position(home_data['possession'], is_shot_side=True)
        
        player = np.random.choice(home_data['players'])
        situation = weighted_choice(SITUATIONS)
        
        shots.append({
            'match_id': match_id,
            'date': date,
            'season': season,
            'team': home_team,
            'opponent': away_team,
            'player': player,
            'minute': minute,
            'x': x,
            'y': y,
            'result': 'goal' if is_goal else np.random.choice(['missed', 'saved', 'blocked'], p=[0.4, 0.35, 0.25]),
            'situation': situation,
            'shot_type': np.random.choice(SHOT_TYPES),
        })
    
    # Generar tiros del equipo visitante
    for i in range(away_shots):
        minute = np.random.randint(1, 91)
        
        # Probabilidad de gol basada en eficiencia
        is_goal = np.random.random() < away_efficiency
        
        # Generar posición realista (desde el otro lado)
        x, y = generate_realistic_position(away_data['possession'], is_shot_side=False)
        x = 100 - x  # Invertir eje X
        
        player = np.random.choice(away_data['players'])
        situation = weighted_choice(SITUATIONS)
        
        shots.append({
            'match_id': match_id,
            'date': date,
            'season': season,
            'team': away_team,
            'opponent': home_team,
            'player': player,
            'minute': minute,
            'x': x,
            'y': y,
            'result': 'goal' if is_goal else np.random.choice(['missed', 'saved', 'blocked'], p=[0.4, 0.35, 0.25]),
            'situation': situation,
            'shot_type': np.random.choice(SHOT_TYPES),
        })
    
    return shots

def generate_advanced_dataset():
    """Genera un dataset completo avanzado de la temporada 2024-25."""
    
    team_list = list(TEAMS_ADVANCED.keys())
    all_shots = []
    match_id = 1
    start_date = datetime(2024, 9, 1)
    
    print("🎯 Generando partidos avanzados de la UEFA Champions League 2024-25...")
    
    # Crear más partidos (fase de grupos completa + eliminatorias)
    for round_num in range(12):  # 12 rondas para más variabilidad
        shuffled_teams = team_list.copy()
        random.shuffle(shuffled_teams)
        
        for i in range(0, len(shuffled_teams) - 1, 2):
            home_team = shuffled_teams[i]
            away_team = shuffled_teams[i + 1]
            
            match_date = start_date + timedelta(days=round_num * 7 + np.random.randint(0, 5))
            
            # Generar tiros para este partido
            shots = generate_shots_for_match(home_team, away_team, match_id, match_date.strftime('%Y-%m-%d'))
            all_shots.extend(shots)
            
            match_id += 1
            
            if match_id > 200:  # Limitar a 200 partidos simulados
                break
        
        if match_id > 200:
            break
    
    # Crear DataFrame
    df = pd.DataFrame(all_shots)
    
    # Estadísticas finales
    total_goals = (df['result'] == 'goal').sum()
    global_efficiency = (total_goals / len(df) * 100)
    
    print(f"\n✅ Dataset generado exitosamente:")
    print(f"   📊 {len(df)} tiros en {df['match_id'].nunique()} partidos")
    print(f"   🏆 {df['team'].nunique()} equipos")
    print(f"   👥 {df['player'].nunique()} jugadores únicos")
    print(f"   ⚽ {total_goals} goles ({global_efficiency:.1f}% eficacia)")
    
    print(f"\n🥅 TOP 5 EQUIPOS:")
    top_teams = df[df['result'] == 'goal'].groupby('team').size().sort_values(ascending=False).head(5)
    for rank, (team, goals) in enumerate(top_teams.items(), 1):
        team_shots = len(df[df['team'] == team])
        eff = (goals / team_shots * 100) if team_shots > 0 else 0
        print(f"   {rank}. {team}: {goals} goles ({eff:.1f}%)")
    
    print(f"\n⭐ TOP 10 JUGADORES:")
    top_players = df[df['result'] == 'goal'].groupby('player').size().sort_values(ascending=False).head(10)
    for rank, (player, goals) in enumerate(top_players.items(), 1):
        print(f"   {rank:2d}. {player}: {goals} goles")
    
    return df

if __name__ == '__main__':
    # Generar dataset avanzado
    dataset = generate_advanced_dataset()
    
    # Guardar a CSV
    output_path = 'data/sample_shots.csv'
    dataset.to_csv(output_path, index=False)
    print(f"\n✅ Dataset guardado en: {output_path}")
    print(f"\n🚀 Para ejecutar la app:")
    print(f"   streamlit run src/app.py")
