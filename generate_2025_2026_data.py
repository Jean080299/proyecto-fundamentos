"""
Script para generar dataset de la UEFA Champions League TEMPORADA 2025-2026
con información actualizada de fichajes y plantillas actuales.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# EQUIPOS TEMPORADA 2025-2026 - DATOS ACTUALIZADOS CON FICHAJES
TEAMS_2025_2026 = {
    'Real Madrid': {
        'players': ['Vinícius Jr', 'Kylian Mbappé', 'Jude Bellingham', 'Rodrygo Goes', 'Federico Valverde',
                   'Eduardo Camavinga', 'Aurélien Tchouaméni', 'Luka Modrić', 'Toni Kroos', 'Eder Militao',
                   'Nacho Fernández', 'Antonio Rüdiger', 'Lucas Vázquez'],
        'efficiency': 0.30,
        'avg_shots_per_match': 19,
        'possession': 0.64
    },
    'Manchester City': {
        'players': ['Erling Haaland', 'Phil Foden', 'Julián Álvarez', 'Jack Grealish', 'Kevin De Bruyne',
                   'Mateo Kovačić', 'Rodri', 'Ilkay Gündogan', 'Kyle Walker', 'Ruben Dias',
                   'Manuel Akanji', 'John Stones', 'Ederson'],
        'efficiency': 0.28,
        'avg_shots_per_match': 17,
        'possession': 0.66
    },
    'Arsenal': {
        'players': ['Bukayo Saka', 'Gabriel Jesus', 'Martin Ødegaard', 'Leandro Trossard', 'Kai Havertz',
                   'Thomas Partey', 'Granit Xhaka', 'Declan Rice', 'Ben White', 'Aaron Ramsdale',
                   'Jurrien Timber', 'William Saliba', 'Gabriel Magalhaes'],
        'efficiency': 0.26,
        'avg_shots_per_match': 16,
        'possession': 0.60
    },
    'Barcelona': {
        'players': ['Robert Lewandowski', 'Ferran Torres', 'Ansu Fati', 'Ousmane Dembélé', 'Pedri',
                   'Gavi', 'Sergio Busquets', 'Ilkay Gündogan', 'Jules Koundé', 'Jordi Alba',
                   'Ronald Araújo', 'Andreas Christensen', 'Ter Stegen'],
        'efficiency': 0.27,
        'avg_shots_per_match': 18,
        'possession': 0.65
    },
    'Bayern Munich': {
        'players': ['Serge Gnabry', 'Leroy Sané', 'Harry Kane', 'Jamal Musiala', 'Kingsley Coman',
                   'Joshua Kimmich', 'Leon Goretzka', 'Dayot Upamecano', 'Noussair Mazraoui', 'Manuel Neuer',
                   'Héctor Bellerín', 'Alphonso Davies', 'Matthijs de Ligt'],
        'efficiency': 0.29,
        'avg_shots_per_match': 18,
        'possession': 0.62
    },
    'Liverpool': {
        'players': ['Mohamed Salah', 'Luis Díaz', 'Diogo Jota', 'Cody Gakpo', 'Darwin Núñez',
                   'Jordan Henderson', 'Alexis Mac Allister', 'Dominic Szoboszlai', 'Virgil van Dijk',
                   'Trent Alexander-Arnold', 'Andy Robertson', 'Ibrahima Konaté', 'Alisson'],
        'efficiency': 0.24,
        'avg_shots_per_match': 15,
        'possession': 0.57
    },
    'Inter Milan': {
        'players': ['Lautaro Martínez', 'Marcus Thuram', 'Nicolo Barella', 'Henrikh Mkhitaryan',
                   'Hakan Çalhanoglu', 'Mateo Kovačić', 'Alessandro Bastoni', 'Federico Dimarco',
                   'Matteo Darmian', 'André Onana', 'Yann Bissuma', 'Benjamin Pavard'],
        'efficiency': 0.24,
        'avg_shots_per_match': 15,
        'possession': 0.54
    },
    'AC Milan': {
        'players': ['Rafael Leão', 'Christian Pulisic', 'Álvaro Morata', 'Olivier Giroud', 'Fikayo Tomori',
                   'Ismael Bennacer', 'Théo Hernández', 'Davide Calabria', 'Alessandro Florenzi',
                   'Mike Maignan', 'Malick Thiaw', 'Matteo Gabbia'],
        'efficiency': 0.23,
        'avg_shots_per_match': 14,
        'possession': 0.52
    },
    'Paris Saint-Germain': {
        'players': ['Kylian Mbappé', 'Neymar', 'Marco Asensio', 'Achraf Hakimi', 'Ousmane Dembélé',
                   'Vitinha', 'Mário Hermoso', 'Marquinhos', 'Gianluigi Donnarumma', 'Juan Bernat',
                   'Sergei Milinković-Savić', 'Nicolás González'],
        'efficiency': 0.25,
        'avg_shots_per_match': 16,
        'possession': 0.59
    },
    'Borussia Dortmund': {
        'players': ['Marco Reus', 'Karim Adeyemi', 'Jadon Sancho', 'Salih Özdemir', 'Jérôme Azcona',
                   'Emre Can', 'Niklas Süle', 'Mats Hummels', 'Gregor Kobel', 'Ian Maatsen',
                   'Felix Passlack', 'Julian Bruma'],
        'efficiency': 0.22,
        'avg_shots_per_match': 14,
        'possession': 0.50
    },
    'Atlético Madrid': {
        'players': ['Antoine Griezmann', 'Álvaro Morata', 'Rodrigo De Paul', 'Nahuel Molina',
                   'José Giménez', 'Felipe', 'Axel Witsel', 'Sergio Reguilón', 'Jan Oblak',
                   'Jérôme Boateng', 'César Azpilicueta', 'Stefan Savić'],
        'efficiency': 0.20,
        'avg_shots_per_match': 13,
        'possession': 0.47
    },
    'Napoli': {
        'players': ['Victor Osimhen', 'Matteo Politano', 'Khvicha Kvaratskhelia', 'Piotr Zieliński',
                   'Alessandro Buongiorno', 'Juan Jesús', 'Mário Rui', 'Stanislav Lobotka',
                   'Alex Meret', 'Leonardo Spinazzola', 'Kim Min-jae', 'Amir Rrahmani'],
        'efficiency': 0.25,
        'avg_shots_per_match': 15,
        'possession': 0.54
    },
    'Manchester United': {
        'players': ['Marcus Rashford', 'Antony', 'Bruno Fernandes', 'Alejandro Garnacho', 'Casemiro',
                   'Aaron Wan-Bissaka', 'Luke Shaw', 'Jonny Evans', 'André Onana', 'Lisandro Martínez',
                   'Mason Mount', 'Scott McTominay'],
        'efficiency': 0.22,
        'avg_shots_per_match': 14,
        'possession': 0.52
    },
    'Aston Villa': {
        'players': ['Ollie Watkins', 'Bukayo Saka', 'John McGinn', 'Philippe Coutinho', 'Emiliano Martínez',
                   'Jhon Durán', 'Ezri Konsa', 'Pau Torres', 'Lucas Digne', 'Tyrone Mings',
                   'Ross Barkley', 'Emi Martínez'],
        'efficiency': 0.23,
        'avg_shots_per_match': 14,
        'possession': 0.50
    },
    'Benfica': {
        'players': ['Gonçalo Ramos', 'João Félix', 'Rafa Silva', 'Petar Musa', 'Álex Grimaldo',
                   'Enzo Fernández', 'Nicolás Otamendi', 'Gilberto', 'João Neves', 'Odysseas Vlachodimos',
                   'Tomás Araújo', 'Alexander Bah'],
        'efficiency': 0.22,
        'avg_shots_per_match': 13,
        'possession': 0.49
    },
    'PSV Eindhoven': {
        'players': ['Luuk de Jong', 'Ismael Saibari', 'Hirving Lozano', 'Yorbe Vertessen', 'Xavi Simons',
                   'Sergiño Dest', 'Malik Tillman', 'Joey Veerman', 'Walter Benítez', 'Matteo Darmian',
                   'Sergei Milinković-Savić', 'André Ramalho'],
        'efficiency': 0.21,
        'avg_shots_per_match': 13,
        'possession': 0.48
    },
    'RB Leipzig': {
        'players': ['Benjamin Sesko', 'Christoph Baumgartner', 'Willi Orbán', 'Dani Olmo', 'Loïs Openda',
                   'Mohamed Simakan', 'Xaver Schlager', 'Péter Gulácsi', 'Emil Forsberg', 'Yussuf Poulsen',
                   'Marcel Halstenberg', 'Lutsharel Geertruida'],
        'efficiency': 0.21,
        'avg_shots_per_match': 13,
        'possession': 0.47
    },
    'Girona FC': {
        'players': ['Artem Dovbyk', 'Yangel Herrera', 'Antony Silva', 'Javi Martínez', 'Aleix García',
                   'Cristhian Stuani', 'Yaser Asprilla', 'Gonzalo Montiel', 'Juan Carlos Martín',
                   'Paulo Gazzaniga', 'Matías Arezo', 'Sávio'],
        'efficiency': 0.20,
        'avg_shots_per_match': 12,
        'possession': 0.46
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
        if np.random.random() < team_possession:
            x = np.random.normal(loc=77, scale=12)
        else:
            x = np.random.normal(loc=72, scale=15)
    else:
        x = np.random.normal(loc=25, scale=12)
    
    y = np.random.normal(loc=50, scale=20)
    
    x = np.clip(x, 5, 95)
    y = np.clip(y, 0, 100)
    
    return round(x, 2), round(y, 2)

def generate_shots_for_match(home_team, away_team, match_id, date, season='2025-26'):
    """Genera tiros realistas para un partido."""
    shots = []
    
    home_data = TEAMS_2025_2026[home_team]
    away_data = TEAMS_2025_2026[away_team]
    
    home_shots = int(np.random.normal(loc=home_data['avg_shots_per_match'], scale=3))
    away_shots = int(np.random.normal(loc=away_data['avg_shots_per_match'], scale=3))
    
    home_shots = max(8, min(26, home_shots))
    away_shots = max(8, min(26, away_shots))
    
    home_efficiency = home_data['efficiency'] * np.random.normal(1.0, 0.12)
    away_efficiency = away_data['efficiency'] * np.random.normal(1.0, 0.12)
    
    home_efficiency = np.clip(home_efficiency, 0.10, 0.45)
    away_efficiency = np.clip(away_efficiency, 0.10, 0.45)
    
    # Tiros del equipo local
    for i in range(home_shots):
        minute = np.random.randint(1, 91)
        is_goal = np.random.random() < home_efficiency
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
    
    # Tiros del equipo visitante
    for i in range(away_shots):
        minute = np.random.randint(1, 91)
        is_goal = np.random.random() < away_efficiency
        x, y = generate_realistic_position(away_data['possession'], is_shot_side=False)
        x = 100 - x
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

def generate_2025_2026_dataset():
    """Genera dataset completo para temporada 2025-2026."""
    
    team_list = list(TEAMS_2025_2026.keys())
    all_shots = []
    match_id = 1
    start_date = datetime(2025, 9, 1)
    
    print("🎯 Generando partidos UEFA Champions League TEMPORADA 2025-2026...")
    print(f"📅 Equipos: {len(team_list)}")
    
    # Crear múltiples rondas
    for round_num in range(14):
        shuffled_teams = team_list.copy()
        random.shuffle(shuffled_teams)
        
        for i in range(0, len(shuffled_teams) - 1, 2):
            home_team = shuffled_teams[i]
            away_team = shuffled_teams[i + 1]
            
            match_date = start_date + timedelta(days=round_num * 7 + np.random.randint(0, 5))
            
            shots = generate_shots_for_match(home_team, away_team, match_id, match_date.strftime('%Y-%m-%d'))
            all_shots.extend(shots)
            
            match_id += 1
            
            if match_id > 250:
                break
        
        if match_id > 250:
            break
    
    df = pd.DataFrame(all_shots)
    
    total_goals = (df['result'] == 'goal').sum()
    global_efficiency = (total_goals / len(df) * 100)
    
    print(f"\n✅ Dataset generado exitosamente:")
    print(f"   📊 {len(df)} tiros en {df['match_id'].nunique()} partidos")
    print(f"   🏆 {df['team'].nunique()} equipos")
    print(f"   👥 {df['player'].nunique()} jugadores únicos")
    print(f"   ⚽ {total_goals} goles ({global_efficiency:.1f}% eficacia)")
    
    print(f"\n🥅 TOP 8 EQUIPOS 2025-2026:")
    top_teams = df[df['result'] == 'goal'].groupby('team').size().sort_values(ascending=False).head(8)
    for rank, (team, goals) in enumerate(top_teams.items(), 1):
        team_shots = len(df[df['team'] == team])
        eff = (goals / team_shots * 100) if team_shots > 0 else 0
        print(f"   {rank}. {team}: {goals} goles ({eff:.1f}% - {team_shots} tiros)")
    
    print(f"\n⭐ TOP 12 JUGADORES 2025-2026:")
    top_players = df[df['result'] == 'goal'].groupby('player').size().sort_values(ascending=False).head(12)
    for rank, (player, goals) in enumerate(top_players.items(), 1):
        print(f"   {rank:2d}. {player}: {goals} goles")
    
    return df

if __name__ == '__main__':
    dataset = generate_2025_2026_dataset()
    
    output_path = 'data/sample_shots.csv'
    dataset.to_csv(output_path, index=False)
    print(f"\n✅ Dataset TEMPORADA 2025-2026 guardado en: {output_path}")
    print(f"\n🚀 Ejecutar app:")
    print(f"   streamlit run src/app.py")
