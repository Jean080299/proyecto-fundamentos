"""
Script para mostrar resumen del dataset
"""
import pandas as pd

df = pd.read_csv('data/sample_shots.csv')

print('='*60)
print('📊 ANÁLISIS DEL DATASET - UEFA CHAMPIONS LEAGUE 2024-25')
print('='*60)

print(f'\n✅ Dataset cargado: {len(df)} tiros')
print(f'🏆 Partidos: {df["match_id"].nunique()}')
print(f'🌍 Equipos: {df["team"].nunique()}')
print(f'👥 Jugadores: {df["player"].nunique()}')

global_goals = (df['result'] == 'goal').sum()
global_efficiency = (global_goals / len(df) * 100)
print(f'\n📈 EFICACIA GLOBAL: {global_efficiency:.1f}% ({global_goals} goles)')

print(f'\n🥅 TOP 10 EQUIPOS POR GOLES')
top_teams = df[df['result'] == 'goal'].groupby('team').size().sort_values(ascending=False)
for i, (team, goals) in enumerate(top_teams.items(), 1):
    team_shots = len(df[df['team'] == team])
    eff = (goals / team_shots * 100) if team_shots > 0 else 0
    print(f'  {i:2d}. {team:20s} | {goals:2d} goles | {eff:5.1f}% eficacia | {team_shots:3d} tiros')

print(f'\n⭐ TOP 10 JUGADORES POR GOLES')
top_players = df[df['result'] == 'goal'].groupby('player').size().sort_values(ascending=False).head(10)
for i, (player, goals) in enumerate(top_players.items(), 1):
    player_shots = len(df[df['player'] == player])
    eff = (goals / player_shots * 100) if player_shots > 0 else 0
    print(f'  {i:2d}. {player:25s} | {goals:2d} goles | {eff:5.1f}% eficacia')

print(f'\n🎯 ANÁLISIS POR SITUACIÓN')
for situation in sorted(df['situation'].unique()):
    situation_data = df[df['situation'] == situation]
    situation_goals = (situation_data['result'] == 'goal').sum()
    situation_eff = (situation_goals / len(situation_data) * 100) if len(situation_data) > 0 else 0
    print(f'  {situation:18s} | {situation_goals:2d} goles | {situation_eff:5.1f}% de {len(situation_data):4d} tiros')

print(f'\n✅ ARCHIVO: data/sample_shots.csv')
print('='*60)
