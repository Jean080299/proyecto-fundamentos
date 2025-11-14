import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def pitch_figure(width=700, height=450):
    """Crea una figura base de cancha de fútbol con Plotly."""
    fig = go.Figure()
    fig.update_layout(
        xaxis=dict(range=[0, 100], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(range=[0, 100], showgrid=False, zeroline=False, showticklabels=False, scaleanchor='x'),
        width=width, height=height,
        plot_bgcolor='#2b7a3a'
    )
    # Añadir marcas de cancha (línea central, área, etc.)
    # Fondo/rectángulo principal (relleno con color césped)
    fig.add_shape(type="rect", x0=0, y0=0, x1=100, y1=100, line=dict(color="white", width=2), fillcolor='#2b7a3a', layer='below')
    # Línea de medio campo
    fig.add_shape(type="line", x0=50, y0=0, x1=50, y1=100, line=dict(color="white", width=1), layer='below')
    # Círculo central
    fig.add_shape(type="circle", x0=45, y0=45, x1=55, y1=55, line=dict(color="white", width=1), layer='below')
    # Áreas de gol (ambos extremos)
    # Área derecha
    fig.add_shape(type="rect", x0=85, y0=20, x1=100, y1=80, line=dict(color="white", width=1), layer='below')
    fig.add_shape(type="rect", x0=92, y0=40, x1=100, y1=60, line=dict(color="white", width=1), layer='below')
    # Área izquierda (simétrica)
    fig.add_shape(type="rect", x0=0, y0=20, x1=15, y1=80, line=dict(color="white", width=1), layer='below')
    fig.add_shape(type="rect", x0=0, y0=40, x1=8, y1=60, line=dict(color="white", width=1), layer='below')

    # Penalty arcs en ambos extremos (simulados con líneas)
    theta_right = np.linspace(-0.6, 0.6, 24)
    arc_x_r = 90 + 10 * np.cos(theta_right)
    arc_y_r = 50 + 10 * np.sin(theta_right)
    fig.add_trace(go.Scatter(x=arc_x_r, y=arc_y_r, mode='lines', line=dict(color='white', width=1), showlegend=False))

    theta_left = np.linspace(np.pi - 0.6, np.pi + 0.6, 24)
    arc_x_l = 10 + 10 * np.cos(theta_left)
    arc_y_l = 50 + 10 * np.sin(theta_left)
    fig.add_trace(go.Scatter(x=arc_x_l, y=arc_y_l, mode='lines', line=dict(color='white', width=1), showlegend=False))
    return fig


def plot_shot_scatter(df, team=None):
    """Gráfico de dispersión de tiros en la cancha."""
    fig = pitch_figure(width=900, height=560)
    d = df.copy()
    if team:
        d = d[d["team"] == team]

    # Defensive assumption: goal at x=100, y=50
    if 'x' not in d.columns or 'y' not in d.columns:
        raise ValueError('DataFrame must contain x and y columns for shot positions')

    # Calculate distance to goal to size markers
    d = d.dropna(subset=['x', 'y']).copy()
    d['distance_to_goal'] = np.sqrt((100 - d['x'])**2 + (50 - d['y'])**2)
    # size: closer => larger
    d['marker_size'] = np.clip(18 - (d['distance_to_goal'] / 6), 6, 20)
    d['opacity'] = np.clip(1 - (d['distance_to_goal'] / 200), 0.45, 0.95)

    # Hover text: include available info
    def make_hover(row):
        parts = []
        parts.append(f"<b>Jugador:</b> {row.get('player', 'N/A')}")
        parts.append(f"<b>Equipo:</b> {row.get('team', 'N/A')}")
        if 'minute' in row.index:
            try:
                parts.append(f"<b>Minuto:</b> {int(row['minute'])}")
            except Exception:
                parts.append(f"<b>Minuto:</b> {row['minute']}")
        parts.append(f"<b>Posición:</b> ({row['x']:.1f}, {row['y']:.1f})")
        if 'xg' in row.index:
            try:
                parts.append(f"<b>xG:</b> {row['xg']:.2f}")
            except Exception:
                parts.append(f"<b>xG:</b> {row['xg']}")
        return '<br>'.join(parts)

    d['hover_text'] = d.apply(make_hover, axis=1)

    # Goals vs non-goals
    goals = d[d['is_goal'] == True]
    non_goals = d[d['is_goal'] == False]

    # Plot non-goals with subtle color
    fig.add_trace(go.Scatter(
        x=non_goals['x'], y=non_goals['y'], mode='markers',
        marker=dict(size=non_goals['marker_size'], color='rgba(255,255,255,0.9)', line=dict(color='rgba(0,0,0,0.6)', width=1)),
        hovertext=non_goals['hover_text'], hoverinfo='text',
        name='Tiro (No Gol)'
    ))

    # Plot goals with standout styling
    fig.add_trace(go.Scatter(
        x=goals['x'], y=goals['y'], mode='markers+text',
        marker=dict(size=goals['marker_size'] + 4, color='gold', line=dict(color='#ff7f50', width=2)),
        text=["⭐" for _ in range(len(goals))], textposition='top center',
        hovertext=goals['hover_text'], hoverinfo='text',
        name='GOL'
    ))

    # Add a subtle density layer (2D histogram contour)
    try:
        fig.add_trace(go.Histogram2dContour(
            x=d['x'], y=d['y'], colorscale='YlOrRd', reversescale=False, showscale=False, contours=dict(showlines=False, coloring='fill'), opacity=0.25, hoverinfo='skip'
        ))
    except Exception:
        pass

    # Layout improvements
    fig.update_layout(
        title=dict(text=f"Mapa de Tiros {'- ' + team if team else ''}", x=0.5, xanchor='center', font=dict(size=18, color='white')),
        legend=dict(x=0.02, y=0.98, bgcolor='rgba(0,0,0,0)'),
        margin=dict(l=10, r=10, t=60, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='#2b7a3a'
    )

    # Tune axes to look like a pitch
    fig.update_xaxes(range=[0, 100], showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(range=[0, 100], showgrid=False, zeroline=False, visible=False)

    return fig


def plot_shot_heatmap(df, team=None, ax=None):
    """Mapa de calor de densidad de tiros."""
    d = df.copy()
    if team:
        d = d[d["team"] == team]
    
    x_bins = np.linspace(0, 100, 25)
    y_bins = np.linspace(0, 100, 25)
    heat, xedges, yedges = np.histogram2d(d['x'].dropna(), d['y'].dropna(), bins=[x_bins, y_bins])
    heat = np.rot90(heat)
    heat = np.flipud(heat)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    sns.heatmap(heat, cmap='YlOrRd', ax=ax, cbar_kws={'label': 'Densidad de Tiros'})
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor('green')
    ax.set_title(f"Heatmap de Densidad {'- ' + team if team else ''}")
    return fig


def plot_goal_zones_heatmap(df, bins=10):
    """Mapa de calor de probabilidad de gol por zona."""
    from src.data import identify_goal_zones
    
    zones = identify_goal_zones(df, bins=bins, min_shots=1)
    
    # Crear matriz de probabilidades
    prob_matrix = np.zeros((bins, bins))
    for _, row in zones.iterrows():
        prob_matrix[int(row['y_bin']), int(row['x_bin'])] = row['goal_probability_%']
    
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(prob_matrix, cmap='RdYlGn', ax=ax, cbar_kws={'label': 'Probabilidad de Gol (%)'}, 
                vmin=0, vmax=100)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor('green')
    ax.set_title("Zonas del Campo con Mayor Probabilidad de Gol")
    return fig


def plot_efficiency_comparison(df, group_by='team'):
    """Gráfico comparativo de eficacia entre equipos/jugadores."""
    from src.data import calculate_shooting_efficiency
    
    efficiency = calculate_shooting_efficiency(df, group_by=group_by)
    
    fig = px.bar(
        efficiency,
        x=group_by,
        y='efficiency_%',
        color='efficiency_%',
        color_continuous_scale='RdYlGn',
        title=f'Eficacia de Tiros por {group_by.capitalize()}',
        labels={'efficiency_%': 'Eficacia (%)', group_by: group_by.capitalize()},
        text='efficiency_%'
    )
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    return fig


def plot_shots_vs_goals(df, group_by='team'):
    """Gráfico de tiros totales vs goles por grupo."""
    from src.data import calculate_shooting_efficiency
    
    efficiency = calculate_shooting_efficiency(df, group_by=group_by)
    
    fig = go.Figure(data=[
        go.Bar(name='Total Tiros', x=efficiency[group_by], y=efficiency['total_shots'], marker_color='lightblue'),
        go.Bar(name='Goles', x=efficiency[group_by], y=efficiency['goals'], marker_color='gold')
    ])
    fig.update_layout(
        title=f'Tiros Totales vs Goles por {group_by.capitalize()}',
        barmode='group',
        xaxis_title=group_by.capitalize(),
        yaxis_title='Cantidad'
    )
    return fig


def plot_top_performers(df, metric='goals', top_n=10):
    """Gráfico de top jugadores/equipos por métrica."""
    from src.data import calculate_shooting_efficiency
    
    efficiency = calculate_shooting_efficiency(df, group_by='player')
    top_players = efficiency.nlargest(top_n, metric)
    
    fig = px.bar(
        top_players,
        x='player',
        y=metric,
        color=metric,
        color_continuous_scale='Viridis',
        title=f'Top {top_n} Jugadores por {metric.capitalize()}',
        labels={'player': 'Jugador', metric: metric.capitalize()}
    )
    fig.update_xaxes(tickangle=45)
    return fig
