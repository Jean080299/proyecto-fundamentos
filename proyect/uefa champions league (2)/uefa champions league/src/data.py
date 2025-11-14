import pandas as pd
import numpy as np


def load_shots(csv_path: str) -> pd.DataFrame:
    """Carga un CSV de tiros y realiza preprocesado mínimo.

    Espera columnas: match_id, season, team, opponent, player, minute, x, y, result, situation, shot_type
    x,y están en una escala 0-100 donde (0,0) es la esquina superior izquierda del campo.
    """
    df = pd.read_csv(csv_path)

    # Normalizar nombres de columnas
    df.columns = [c.strip() for c in df.columns]

    # Convertir coordenadas a numeric
    for col in ("x", "y"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Resultado: goal/missed/saved/blocked
    if "result" in df.columns:
        df["result"] = df["result"].astype(str)

    # Añadir columna de tipo binario éxito
    if "result" in df.columns:
        df["is_goal"] = df["result"].str.lower().eq("goal")
    else:
        df["is_goal"] = False

    return df


def calculate_shooting_efficiency(df: pd.DataFrame, group_by: str = None) -> pd.DataFrame:
    """Calcula la eficacia de tiros (% de goles) por equipo o jugador.
    
    Args:
        df: DataFrame con tiros.
        group_by: 'team', 'player', o None (global).
    
    Returns:
        DataFrame con total de tiros, goles y eficacia (%).
    """
    if group_by is None:
        total_shots = len(df)
        total_goals = df['is_goal'].sum()
        efficiency = (total_goals / total_shots * 100) if total_shots > 0 else 0
        return pd.DataFrame({
            'total_shots': [total_shots],
            'goals': [total_goals],
            'efficiency_%': [efficiency]
        })
    
    grouped = df.groupby(group_by).agg({
        'is_goal': ['sum', 'count']
    }).reset_index()
    grouped.columns = [group_by, 'goals', 'total_shots']
    grouped['efficiency_%'] = (grouped['goals'] / grouped['total_shots'] * 100).round(2)
    grouped = grouped.sort_values('efficiency_%', ascending=False)
    return grouped


def identify_goal_zones(df: pd.DataFrame, bins: int = 10, min_shots: int = 1) -> pd.DataFrame:
    """Identifica zonas del campo con mayor probabilidad de gol.
    
    Args:
        df: DataFrame con tiros.
        bins: Número de divisiones del campo (bins x bins).
        min_shots: Mínimo de tiros en una zona para considerarla.
    
    Returns:
        DataFrame con zona (x_bin, y_bin), total tiros, goles y probabilidad.
    """
    df_valid = df[['x', 'y', 'is_goal']].dropna()
    
    # Crear bins para x e y
    df_valid['x_bin'] = pd.cut(df_valid['x'], bins=bins, labels=False)
    df_valid['y_bin'] = pd.cut(df_valid['y'], bins=bins, labels=False)
    
    # Agrupar por zona
    zones = df_valid.groupby(['x_bin', 'y_bin']).agg({
        'is_goal': ['sum', 'count']
    }).reset_index()
    zones.columns = ['x_bin', 'y_bin', 'goals', 'total_shots']
    
    # Filtrar zonas con mínimo de tiros
    zones = zones[zones['total_shots'] >= min_shots]
    
    # Calcular probabilidad de gol
    zones['goal_probability_%'] = (zones['goals'] / zones['total_shots'] * 100).round(2)
    zones = zones.sort_values('goal_probability_%', ascending=False)
    
    return zones


def compare_teams(df: pd.DataFrame) -> pd.DataFrame:
    """Compara eficacia de tiros entre equipos.
    
    Returns:
        DataFrame con estadísticas de cada equipo.
    """
    if 'team' not in df.columns:
        return pd.DataFrame()
    
    return calculate_shooting_efficiency(df, group_by='team')


def compare_players(df: pd.DataFrame, min_shots: int = 3) -> pd.DataFrame:
    """Compara eficacia de tiros entre jugadores.
    
    Args:
        df: DataFrame con tiros.
        min_shots: Mínimo de tiros para listar al jugador.
    
    Returns:
        DataFrame con estadísticas de cada jugador.
    """
    if 'player' not in df.columns:
        return pd.DataFrame()
    
    efficiency = calculate_shooting_efficiency(df, group_by='player')
    efficiency = efficiency[efficiency['total_shots'] >= min_shots]
    return efficiency


def analyze_by_match(df: pd.DataFrame) -> pd.DataFrame:
    """Analiza eficacia de tiros por partido.
    
    Returns:
        DataFrame con estadísticas de cada partido.
    """
    if 'match_id' not in df.columns:
        return calculate_shooting_efficiency(df)
    
    grouped = df.groupby('match_id').agg({
        'is_goal': ['sum', 'count'],
        'team': 'first',
        'opponent': 'first'
    }).reset_index()
    grouped.columns = ['match_id', 'goals', 'total_shots', 'team', 'opponent']
    grouped['efficiency_%'] = (grouped['goals'] / grouped['total_shots'] * 100).round(2)
    grouped = grouped.sort_values('efficiency_%', ascending=False)
    return grouped


def analyze_by_season(df: pd.DataFrame) -> pd.DataFrame:
    """Analiza eficacia de tiros por temporada.
    
    Returns:
        DataFrame con estadísticas de cada temporada.
    """
    if 'season' not in df.columns:
        return calculate_shooting_efficiency(df)
    
    return calculate_shooting_efficiency(df, group_by='season')


# ------------------ Overrides / Edición de estadísticas ------------------
import json
from pathlib import Path

OVERRIDES_FILE = 'data/stats_overrides.json'


def _ensure_overrides_file():
    Path('data').mkdir(exist_ok=True)
    if not Path(OVERRIDES_FILE).exists():
        with open(OVERRIDES_FILE, 'w') as f:
            json.dump({}, f)


def load_stats_overrides() -> dict:
    """Carga overrides de estadísticas (si existen)."""
    _ensure_overrides_file()
    with open(OVERRIDES_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def save_stats_overrides(overrides: dict):
    """Guarda los overrides de estadísticas en disco."""
    _ensure_overrides_file()
    with open(OVERRIDES_FILE, 'w') as f:
        json.dump(overrides, f, indent=2)


def get_stats_with_overrides(df: pd.DataFrame, group_by: str = None) -> pd.DataFrame:
    """Obtiene estadísticas (global o agrupadas) aplicando overrides si existen.

    Overrides format (JSON):
    {
      "global": {"total_shots": 123, "goals": 12, "efficiency_%": 9.8},
      "team:Real Madrid": {"total_shots": 50, "goals": 8},
      "player:Cristiano": {"goals": 5}
    }

    Los valores en overrides reemplazan los calculados. Si se provee solo 'goals', se recalcula 'efficiency_%' cuando sea aplicable.
    """
    overrides = load_stats_overrides()

    if group_by is None:
        base = calculate_shooting_efficiency(df, group_by=None)
        if 'global' in overrides:
            ov = overrides['global']
            total_shots = ov.get('total_shots', int(base['total_shots'].iloc[0]))
            goals = ov.get('goals', int(base['goals'].iloc[0]))
            efficiency = ov.get('efficiency_%', (goals / total_shots * 100) if total_shots > 0 else 0)
            return pd.DataFrame({'total_shots': [total_shots], 'goals': [goals], 'efficiency_%': [efficiency]})
        return base

    # Agrupar y luego aplicar overrides por llave (p.ej. 'team:TeamName' o 'player:PlayerName')
    grouped = calculate_shooting_efficiency(df, group_by=group_by)
    # grouped has columns [group_by, 'goals', 'total_shots', 'efficiency_%']
    def _apply_row_override(row):
        key = f"{group_by}:{row[group_by]}"
        if key in overrides:
            ov = overrides[key]
            goals = ov.get('goals', int(row['goals']))
            total_shots = ov.get('total_shots', int(row['total_shots']))
            efficiency = ov.get('efficiency_%', (goals / total_shots * 100) if total_shots > 0 else 0)
            row['goals'] = goals
            row['total_shots'] = total_shots
            row['efficiency_%'] = round(efficiency, 2)
        return row

    grouped = grouped.apply(_apply_row_override, axis=1)
    grouped = grouped.sort_values('efficiency_%', ascending=False).reset_index(drop=True)
    return grouped
