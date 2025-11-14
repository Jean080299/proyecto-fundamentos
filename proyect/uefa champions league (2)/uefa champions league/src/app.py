import os
import sys

# Ensure project root is on sys.path so `from src...` imports work when
# running via `streamlit run` which may change import context.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import pandas as pd
import numpy as np
from src.data import (
    load_shots, calculate_shooting_efficiency, identify_goal_zones,
    compare_teams, compare_players, analyze_by_match, analyze_by_season,
    load_stats_overrides, save_stats_overrides, get_stats_with_overrides
)
from src.visuals import (
    plot_shot_scatter, plot_shot_heatmap, plot_goal_zones_heatmap,
    plot_efficiency_comparison, plot_shots_vs_goals, plot_top_performers
)
from src.auth import (
    register_user, login_user, get_user_info, update_password, list_all_users, user_exists, validate_password_strength,
    is_admin, set_user_admin
)
from src.styles import get_custom_css

# Aplicar estilos personalizados
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Configurar página
st.set_page_config(layout='wide', page_title='Analizador de Tiros - UEFA Champions League')

# ============ INICIALIZAR SESSION STATE ============
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.page = 'login'

# ============ PÁGINA DE LOGIN/REGISTRO ============
if not st.session_state.logged_in:
    # Header elegante
    st.markdown("""
    <div style='text-align: center; padding: 40px 30px; background: linear-gradient(135deg, rgba(42,111,191,0.95) 0%, rgba(42,111,191,0.78) 100%); border-radius: 20px; margin-bottom: 20px; box-shadow: 0 8px 28px rgba(0, 212, 255, 0.12); animation: fadeInDown 0.8s ease-out;'>
        <h1 style='color: white; font-size: 2.5em; margin-bottom: 10px; text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);'>🔐 UEFA Champions League</h1>
        <p style='color: #00d4ff; font-size: 1.1em; margin: 0;'>Analizador Avanzado de Tiros</p>
    </div>
    <style>
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='text-align: center; margin-bottom: 20px;'>
            <p style='color: #020024; font-size: 1em;'>Accede a tu cuenta o crea una nueva</p>
        </div>
        """, unsafe_allow_html=True)
        
        tab_login, tab_register = st.tabs(['🔑 Iniciar Sesión', '📝 Registrarse'])
        
        # TAB LOGIN
        with tab_login:
            st.markdown("<h3 style='color: #020024; text-align: center;'>Bienvenido</h3>", unsafe_allow_html=True)
            st.markdown("")
            
            login_user_input = st.text_input('👤 Usuario', key='login_user', placeholder='Ingresa tu usuario')
            login_pass_input = st.text_input('🔑 Contraseña', type='password', key='login_pass', placeholder='Ingresa tu contraseña')
            login_as_admin = st.checkbox('Entrar como administrador', key='login_as_admin')
            
            # Si marcó admin, pide clave secreta
            login_admin_key = None
            if login_as_admin:
                login_admin_key = st.text_input('🔐 Clave Secreta de Administrador', type='password', key='login_admin_key', placeholder='Ingresa la clave secreta')
            
            st.markdown("")
            
            if st.button('✅ Iniciar Sesión', use_container_width=True, key='btn_login'):
                if login_user_input and login_pass_input:
                    if login_as_admin and login_admin_key != 'admin123':
                        st.error('❌ Clave secreta de administrador incorrecta')
                    else:
                        result = login_user(login_user_input, login_pass_input)
                        if result['success']:
                            # If user requested admin login, verify admin flag
                            if login_as_admin:
                                if is_admin(result['user']):
                                    st.session_state.logged_in = True
                                    st.session_state.username = result['user']
                                    st.success('✅ Ingreso administrador correcto')
                                    st.rerun()
                                else:
                                    st.error('❌ El usuario no tiene permisos de administrador')
                            else:
                                st.session_state.logged_in = True
                                st.session_state.username = result['user']
                                st.success(result['message'])
                                st.rerun()
                        else:
                            st.error(result['message'])
                else:
                    st.warning('⚠️ Por favor completa todos los campos')
        
        # TAB REGISTER
        with tab_register:
            st.markdown("<h3 style='color: #020024; text-align: center;'>Crear Cuenta</h3>", unsafe_allow_html=True)
            st.markdown("")
            
            register_user_input = st.text_input('👤 Usuario', key='register_user', placeholder='Mínimo 3 caracteres')
            register_email_input = st.text_input('📧 Email', key='register_email', placeholder='tu@email.com')
            register_pass_input = st.text_input('🔑 Contraseña', type='password', key='register_pass', placeholder='Contraseña segura')
            register_pass_confirm = st.text_input('🔑 Confirmar Contraseña', type='password', key='register_pass_confirm', placeholder='Repetir contraseña')
            register_as_admin = st.checkbox('Registrar como administrador', key='register_as_admin')
            
            # Si marcó admin, pide clave secreta
            register_admin_key = None
            if register_as_admin:
                register_admin_key = st.text_input('🔐 Clave Secreta de Administrador', type='password', key='register_admin_key', placeholder='Ingresa la clave secreta')
            
            # Mostrar requisitos de contraseña con estilo
            st.markdown("""
            <div style='background-color: #f8f9fa; border-left: 4px solid #020024; padding: 12px; border-radius: 8px; margin: 15px 0;'>
                <p style='color: #020024; font-weight: bold; margin: 0 0 10px 0;'>📋 Requisitos de Contraseña:</p>
                <ul style='color: #020024; margin: 5px 0; padding-left: 20px;'>
                    <li>✅ Mínimo 8 caracteres</li>
                    <li>✅ Al menos 1 MAYÚSCULA (A-Z)</li>
                    <li>✅ Al menos 1 minúscula (a-z)</li>
                    <li>✅ Al menos 1 número (0-9)</li>
                    <li>✅ Al menos 1 carácter especial (!@#$%^&*)</li>
                </ul>
                <p style='color: #666; margin: 10px 0 0 0; font-size: 0.9em;'><em>Ejemplo: MiPass123!</em></p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("")
            
            if st.button('✅ Registrarse', use_container_width=True, key='btn_register'):
                if register_user_input and register_email_input and register_pass_input and register_pass_confirm:
                    if register_pass_input != register_pass_confirm:
                        st.error('❌ Las contraseñas no coinciden')
                    elif register_as_admin and register_admin_key != 'admin123':
                        st.error('❌ Clave secreta de administrador incorrecta')
                    else:
                        result = register_user(register_user_input, register_email_input, register_pass_input)
                        if result['success']:
                            # If user requested admin registration, set admin flag
                            if register_as_admin:
                                res_admin = set_user_admin(register_user_input, True)
                                if res_admin.get('success'):
                                    st.success(result['message'] + ' — Usuario registrado como administrador')
                                else:
                                    st.warning(result['message'] + ' — Registro OK, pero no se pudo asignar admin')
                            else:
                                st.success(result['message'])
                            st.info('✅ Ahora puedes iniciar sesión con tu usuario')
                        else:
                            st.error(result['message'])
                else:
                    st.warning('⚠️ Por favor completa todos los campos')
    
    st.stop()

# ============ PÁGINA PRINCIPAL (DESPUÉS DEL LOGIN) ============
st.markdown("""
<div style='background: linear-gradient(135deg, rgba(42,111,191,0.95) 0%, rgba(42,111,191,0.78) 100%); padding: 40px 30px; border-radius: 20px; margin-bottom: 20px; box-shadow: 0 8px 24px rgba(0, 212, 255, 0.12); animation: fadeInBubble 0.8s ease-out;'>
    <h1 style='color: white; margin: 0; text-align: center; text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);'>🎯 Analizador de Tiros - UEFA Champions League</h1>
    <p style='color: #00d4ff; text-align: center; margin: 10px 0 0 0;'>Sistema integral de análisis y visualización</p>
</div>
<style>
    @keyframes fadeInBubble {
        from {
            opacity: 0;
            transform: scale(0.95);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
</style>
""", unsafe_allow_html=True)

# ============ USUARIO Y OPCIONES ============
col1, col2, col3 = st.columns([3, 1, 1])

with col3:
    if st.button(f'👤 {st.session_state.username} (Salir)', use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()

# ============ BARRA LATERAL: CARGA DE DATOS ============
st.sidebar.markdown("""
<div style='text-align: center; padding: 20px 15px; background: linear-gradient(135deg, rgba(42,111,191,0.95) 0%, rgba(42,111,191,0.78) 100%); border-radius: 15px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0, 212, 255, 0.08);'>
    <h2 style='color: white; margin: 0; text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);'>📊 PANEL DE CONTROL</h2>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("**📂 Cargar Datos**")
uploaded = st.sidebar.file_uploader('📥 Sube un CSV de tiros', type=['csv'])

if uploaded is not None:
    df = load_shots(uploaded)
    st.sidebar.success('✅ Archivo cargado correctamente')
else:
    try:
        df = load_shots('data/sample_shots.csv')
        st.sidebar.info('📊 Usando dataset de ejemplo (2025-2026)')
    except FileNotFoundError:
        st.error("❌ No se encontró archivo de datos. Por favor carga un CSV.")
        st.stop()

# ============ OPCIONES DE USUARIO EN BARRA LATERAL ============
st.sidebar.markdown('---')
st.sidebar.markdown("**⚙️ Opciones de Usuario**")

with st.sidebar.expander(f'👤 Perfil ({st.session_state.username})'):
    user_info = get_user_info(st.session_state.username)
    if user_info:
        st.markdown(f"""
        <div style='background-color: #f8f9fa; padding: 12px; border-radius: 8px; border-left: 4px solid #020024;'>
            <p style='color: #020024; margin: 5px 0;'><strong>👤 Usuario:</strong> {user_info['username']}</p>
            <p style='color: #020024; margin: 5px 0;'><strong>📧 Email:</strong> {user_info['email']}</p>
            <p style='color: #666; margin: 5px 0;'><strong>📅 Registrado:</strong> {user_info['created_at'][:10]}</p>
            {f"<p style='color: #666; margin: 5px 0;'><strong>🕐 Último acceso:</strong> {user_info['last_login'][:10]}</p>" if user_info['last_login'] else ""}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("**🔐 Cambiar Contraseña**")
    old_pass = st.text_input('🔑 Contraseña Actual', type='password', key='old_pass', placeholder='Tu contraseña actual')
    new_pass = st.text_input('🔑 Nueva Contraseña', type='password', key='new_pass', placeholder='Nueva contraseña')
    new_pass_confirm = st.text_input('🔑 Confirmar Contraseña', type='password', key='new_pass_confirm', placeholder='Repetir contraseña')
    
    # Mostrar requisitos de contraseña
    st.markdown("""
    <div style='background-color: #f8f9fa; padding: 10px; border-radius: 8px; margin: 10px 0;'>
        <p style='color: #020024; font-size: 0.9em; margin: 5px 0;'><strong>📋 Requisitos:</strong></p>
        <ul style='color: #020024; font-size: 0.85em; margin: 5px 0; padding-left: 15px;'>
            <li>8+ caracteres</li>
            <li>1 MAYÚSCULA</li>
            <li>1 minúscula</li>
            <li>1 número</li>
            <li>1 carácter especial</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button('🔐 Cambiar Contraseña', use_container_width=True, key='btn_change_pass'):
        if old_pass and new_pass and new_pass_confirm:
            if new_pass != new_pass_confirm:
                st.error('❌ Las nuevas contraseñas no coinciden')
            else:
                result = update_password(st.session_state.username, old_pass, new_pass)
                if result['success']:
                    st.success('✅ ' + result['message'])
                else:
                    st.error(result['message'])
        else:
            st.warning('⚠️ Por favor completa todos los campos')

st.sidebar.markdown('---')

# ============ ESTADÍSTICAS GLOBALES ============
st.sidebar.markdown("**📈 Estadísticas Globales**")
# Use overrides-aware stats
global_stats = get_stats_with_overrides(df, group_by=None)
total_shots = int(global_stats['total_shots'].iloc[0])
total_goals = int(global_stats['goals'].iloc[0])
global_efficiency = float(global_stats['efficiency_%'].iloc[0])

col1, col2, col3 = st.sidebar.columns(3)
col1.metric('Tiros Totales', total_shots)
col2.metric('Goles', total_goals)
col3.metric('Eficacia', f'{global_efficiency:.1f}%')

# ============ EDITAR ESTADÍSTICAS (Overrides) ============
if is_admin(st.session_state.username):
    with st.sidebar.expander('✏️ Editar Estadísticas', expanded=False):
        st.markdown('**Editar valores calculados (overrides)**')
        overrides = load_stats_overrides()

        # Global override
        st.markdown('**Global**')
        g_total = st.number_input('Tiros totales (global)', value=overrides.get('global', {}).get('total_shots', total_shots), min_value=0)
        g_goals = st.number_input('Goles (global)', value=overrides.get('global', {}).get('goals', total_goals), min_value=0)
        # Build global override when user updates
        overrides.setdefault('global', {})
        overrides['global']['total_shots'] = int(g_total)
        overrides['global']['goals'] = int(g_goals)

        st.markdown('---')
        st.markdown('**Por Equipo (opcional)**')
        team_overrides = {}
        teams_local = df['team'].dropna().unique().tolist() if 'team' in df.columns else []
        for team in sorted(teams_local):
            col_a, col_b = st.columns([2, 1])
            with col_a:
                t_goals = st.number_input(f'Goles - {team}', value=overrides.get(f'team:{team}', {}).get('goals', 0), min_value=0, key=f'goals_{team}')
            with col_b:
                t_shots = st.number_input(f'Tiros - {team}', value=overrides.get(f'team:{team}', {}).get('total_shots', 0), min_value=0, key=f'shots_{team}')
            if t_goals or t_shots:
                team_overrides[f'team:{team}'] = {'goals': int(t_goals), 'total_shots': int(t_shots)}

        # Merge team overrides into main overrides dict
        for k, v in team_overrides.items():
            overrides[k] = v

        if st.button('💾 Guardar Overrides', use_container_width=True):
            save_stats_overrides(overrides)
            st.success('✅ Overrides guardados. Refresca la app para aplicar cambios.')
else:
    st.sidebar.info('🔒 La edición de estadísticas está restringida a administradores.')

# ============ FILTROS GENERALES ============
st.sidebar.markdown("---")
st.sidebar.markdown("**🔍 Filtros de Búsqueda**")

seasons = df['season'].dropna().unique().tolist() if 'season' in df.columns else []
teams = df['team'].dropna().unique().tolist() if 'team' in df.columns else []
players = df['player'].dropna().unique().tolist() if 'player' in df.columns else []
matches = df['match_id'].dropna().unique().tolist() if 'match_id' in df.columns else []

sel_season = st.sidebar.selectbox('📅 Temporada', options=['Todas'] + sorted(seasons))
sel_team = st.sidebar.selectbox('⚽ Equipo', options=['Todos'] + sorted(teams))
sel_player = st.sidebar.selectbox('👤 Jugador', options=['Todos'] + sorted(players))

# Aplicar filtros
filtered = df.copy()
if sel_season != 'Todas':
    filtered = filtered[filtered['season'] == sel_season]
if sel_team != 'Todos':
    filtered = filtered[filtered['team'] == sel_team]
if sel_player != 'Todos':
    filtered = filtered[filtered['player'] == sel_player]

# ============ TABS PRINCIPALES ============
tabs_labels = [
    '🗺️ Mapa de Tiros',
    '🔥 Heatmaps',
    '📊 Comparativas',
    '🎯 Análisis de Zonas',
    '👥 Ranking de Jugadores',
    '📋 Reportes'
]
if is_admin(st.session_state.username):
    tabs_labels.append('🔧 Admin')

tabs = st.tabs(tabs_labels)
tab_map = {label: tab for label, tab in zip(tabs_labels, tabs)}

# ============ TAB 1: MAPA DE TIROS ============
with tab_map['🗺️ Mapa de Tiros']:
    st.header('Mapa de Tiros en la Cancha')
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        fig = plot_shot_scatter(filtered, team=None if sel_team == 'Todos' else sel_team)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Información")
        filtered_stats = get_stats_with_overrides(filtered, group_by=None)
        st.write(f"**Tiros totales:** {int(filtered_stats['total_shots'].values[0]):.0f}")
        st.write(f"**Goles:** {int(filtered_stats['goals'].values[0]):.0f}")
        st.write(f"**Eficacia:** {float(filtered_stats['efficiency_%'].values[0]):.1f}%")

# ============ TAB 2: HEATMAPS ============
with tab_map['🔥 Heatmaps']:
    st.header('Análisis de Densidad de Tiros')
    
    heatmap_type = st.selectbox('Tipo de Heatmap', ['Densidad de Tiros', 'Probabilidad de Gol'])
    
    if heatmap_type == 'Densidad de Tiros':
        st.subheader('Densidad de Tiros en la Cancha')
        fig_heat = plot_shot_heatmap(filtered, team=None if sel_team == 'Todos' else sel_team)
        st.pyplot(fig_heat)
    else:
        st.subheader('Zonas del Campo con Mayor Probabilidad de Gol')
        fig_goal = plot_goal_zones_heatmap(filtered, bins=10)
        st.pyplot(fig_goal)

# ============ TAB 3: COMPARATIVAS ============
with tab_map['📊 Comparativas']:
    st.header('Comparativa de Eficacia')
    
    compare_by = st.selectbox('Comparar por:', ['Equipo', 'Jugador', 'Temporada'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f'Eficacia por {compare_by}')
        if compare_by == 'Equipo':
            fig_eff = plot_efficiency_comparison(filtered, group_by='team')
        elif compare_by == 'Jugador':
            fig_eff = plot_efficiency_comparison(filtered, group_by='player')
        else:
            fig_eff = plot_efficiency_comparison(filtered, group_by='season')
        st.plotly_chart(fig_eff, use_container_width=True)
    
    with col2:
        st.subheader(f'Tiros vs Goles por {compare_by}')
        if compare_by == 'Equipo':
            fig_vs = plot_shots_vs_goals(filtered, group_by='team')
        elif compare_by == 'Jugador':
            fig_vs = plot_shots_vs_goals(filtered, group_by='player')
        else:
            fig_vs = plot_shots_vs_goals(filtered, group_by='season')
        st.plotly_chart(fig_vs, use_container_width=True)

# ============ TAB 4: ANÁLISIS DE ZONAS ============
with tab_map['🎯 Análisis de Zonas']:
    st.header('🎯 Identificación de Zonas de Gol')
    
    bins = st.slider('Precisión del análisis (número de zonas por lado)', 5, 20, 10)
    min_shots = st.slider('Mínimo de tiros en una zona', 1, 20, 3)
    
    zones = identify_goal_zones(filtered, bins=bins, min_shots=min_shots)
    
    if len(zones) > 0:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader('Heatmap de Probabilidad de Gol')
            fig_zones = plot_goal_zones_heatmap(filtered, bins=bins)
            st.pyplot(fig_zones)
        
        with col2:
            st.subheader('Mejores Zonas')
            top_zones = zones.nlargest(10, 'goal_probability_%')
            st.dataframe(top_zones[['x_bin', 'y_bin', 'goals', 'total_shots', 'goal_probability_%']])
    else:
        st.warning('No hay datos suficientes para analizar zonas.')

# ============ TAB 5: RANKING DE JUGADORES ============
with tab_map['👥 Ranking de Jugadores']:
    st.header('👥 Ranking de Jugadores')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader('Top Jugadores por Goles')
        fig_goals = plot_top_performers(filtered, metric='goals', top_n=10)
        st.plotly_chart(fig_goals, use_container_width=True)
    
    with col2:
        st.subheader('Top Jugadores por Eficacia')
        efficiency_players = get_stats_with_overrides(filtered, group_by='player')
        efficiency_players = efficiency_players[efficiency_players['total_shots'] >= 3]  # Mínimo 3 tiros
        top_efficient = efficiency_players.nlargest(10, 'efficiency_%')
        
        import plotly.express as px
        fig_eff_players = px.bar(
            top_efficient,
            x='player',
            y='efficiency_%',
            color='efficiency_%',
            color_continuous_scale='RdYlGn',
            title='Top 10 Jugadores por Eficacia',
            labels={'efficiency_%': 'Eficacia (%)', 'player': 'Jugador'},
            text='efficiency_%'
        )
        fig_eff_players.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_eff_players.update_xaxes(tickangle=45)
        st.plotly_chart(fig_eff_players, use_container_width=True)
    
    st.subheader('📊 Tabla Completa de Jugadores')
    players_stats = get_stats_with_overrides(filtered, group_by='player')
    st.dataframe(players_stats.style.format({'efficiency_%': '{:.2f}%'}), use_container_width=True)

# ============ TAB 6: REPORTES Y RECOMENDACIONES ============
with tab_map['📋 Reportes']:
    st.header('📋 Reportes y Recomendaciones')
    
    report_section = st.selectbox('Tipo de Reporte', [
        'Resumen General',
        'Equipos',
        'Jugadores',
        'Análisis de Partidos',
        'Recomendaciones de Toma de Decisiones'
    ])
    
    if report_section == 'Resumen General':
        st.subheader('Resumen General del Análisis')
        
        col1, col2, col3, col4 = st.columns(4)
        
        stats = get_stats_with_overrides(filtered, group_by=None)
        col1.metric('Total Tiros', int(stats['total_shots'].values[0]))
        col2.metric('Total Goles', int(stats['goals'].values[0]))
        col3.metric('Eficacia Global', f"{float(stats['efficiency_%'].values[0]):.1f}%")
        col4.metric('Tiros por Gol', f"{int(stats['total_shots'].values[0]) / (int(stats['goals'].values[0]) + 0.1):.1f}")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Equipo Más Efectivo")
            teams_stats = get_stats_with_overrides(filtered, group_by='team')
            if len(teams_stats) > 0:
                best_team = teams_stats.nlargest(1, 'efficiency_%').iloc[0]
                st.write(f"**{best_team['team']}**")
                st.write(f"Eficacia: {best_team['efficiency_%']:.1f}%")
                st.write(f"Goles: {int(best_team['goals'])} / {int(best_team['total_shots'])} tiros")
        
        with col2:
            st.markdown("### Jugador Más Efectivo")
            players_stats = get_stats_with_overrides(filtered, group_by='player')
            players_stats = players_stats[players_stats['total_shots'] >= 2]
            if len(players_stats) > 0:
                best_player = players_stats.nlargest(1, 'efficiency_%').iloc[0]
                st.write(f"**{best_player['player']}**")
                st.write(f"Eficacia: {best_player['efficiency_%']:.1f}%")
                st.write(f"Goles: {int(best_player['goals'])} / {int(best_player['total_shots'])} tiros")
    
    elif report_section == 'Equipos':
        st.subheader('Análisis por Equipo')
        teams_stats = compare_teams(filtered)
        st.dataframe(teams_stats.style.format({'efficiency_%': '{:.2f}%'}), use_container_width=True)
        
        st.markdown("### Visualización")
        fig = plot_efficiency_comparison(filtered, group_by='team')
        st.plotly_chart(fig, use_container_width=True)
    
    elif report_section == 'Jugadores':
        st.subheader('Análisis por Jugador')
        min_shots_player = st.slider('Mínimo de tiros', 1, 20, 3)
        players_stats = compare_players(filtered, min_shots=min_shots_player)
        st.dataframe(players_stats.style.format({'efficiency_%': '{:.2f}%'}), use_container_width=True)
    
    elif report_section == 'Análisis de Partidos':
        st.subheader('Análisis por Partido')
        if 'match_id' in filtered.columns:
            matches_stats = analyze_by_match(filtered)
            st.dataframe(matches_stats.style.format({'efficiency_%': '{:.2f}%'}), use_container_width=True)
        else:
            st.info('No hay información de partidos en los datos.')
    
    elif report_section == 'Recomendaciones de Toma de Decisiones':
        st.subheader('💡 Recomendaciones Basadas en Datos')
        
        # Análisis de zonas para recomendaciones
        zones = identify_goal_zones(filtered, bins=10, min_shots=2)
        
        if len(zones) > 0:
            st.markdown("### 🎯 Zonas de Mayor Éxito")
            top_zones = zones.nlargest(3, 'goal_probability_%')
            for idx, (_, zone) in enumerate(top_zones.iterrows(), 1):
                st.write(f"**Zona {idx}**: Probabilidad de gol {zone['goal_probability_%']:.1f}% "
                         f"({int(zone['goals'])} goles en {int(zone['total_shots'])} tiros)")
        
        st.markdown("### 📊 Estrategias Recomendadas")
        
        teams_stats = get_stats_with_overrides(filtered, group_by='team')
        if len(teams_stats) > 0:
            best_team = teams_stats.nlargest(1, 'efficiency_%').iloc[0]
            worst_team = teams_stats.nsmallest(1, 'efficiency_%').iloc[0]
            
            st.write(f"✅ **Equipo Referencia ({best_team['team']})**: Analiza su estrategia y patrones de tiro. "
                    f"Eficacia: {best_team['efficiency_%']:.1f}%")
            st.write(f"⚠️ **Áreas de Mejora ({worst_team['team']})**: Implementar tiros desde zonas de alta probabilidad. "
                    f"Eficacia actual: {worst_team['efficiency_%']:.1f}%")
        
        st.markdown("### 👥 Jugadores Clave")
        players_stats = get_stats_with_overrides(filtered, group_by='player')
        players_stats = players_stats[players_stats['total_shots'] >= 2]
        if len(players_stats) > 0:
            top_3_players = players_stats.nlargest(3, 'goals')
            for idx, (_, player) in enumerate(top_3_players.iterrows(), 1):
                st.write(f"**{idx}. {player['player']}**: {int(player['goals'])} goles con {player['efficiency_%']:.1f}% de eficacia")
        
        st.markdown("### 🏆 Resumen de Decisiones")
        st.info("""
        **Basado en el análisis de datos:"
        - Enfoca tiros en zonas identificadas con alta probabilidad de gol
        - Replica estrategias de equipos/jugadores con mayor eficacia
        - Aumenta volumen de tiros desde posiciones de éxito histórico
        - Adapta defensa considerando patrones de tiro del equipo contrario
        """)

# ============ TAB: ADMIN (solo admins) ============
if is_admin(st.session_state.username):
    with tab_map.get('🔧 Admin'):
        # Header vibrante
        st.markdown("""
        <div style='background: linear-gradient(135deg, #020024 0%, #2b2f97 50%, #1a4d7a 100%); 
                    padding: 30px 25px; border-radius: 15px; color: white; 
                    box-shadow: 0 10px 30px rgba(0, 212, 255, 0.15); margin-bottom: 25px;'>
            <div style='display: flex; align-items: center; gap: 15px;'>
                <div style='font-size: 2.5em;'>🔧</div>
                <div>
                    <h1 style='margin: 0; font-size: 2em; text-shadow: 0 2px 8px rgba(0,0,0,0.3);'>Panel de Administrador</h1>
                    <p style='margin: 8px 0 0 0; color: #a8d5ff; font-size: 1em;'>⚡ Gestiona usuarios, permisos y configuración del sistema</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Tabs para Admin: Usuarios | Overrides
        admin_tab1, admin_tab2 = st.tabs(['👥 Gestión de Usuarios', '⚙️ Overrides y Utilidades'])

        # ============ PESTAÑA 1: USUARIOS ============
        with admin_tab1:
            st.markdown('### Usuarios del Sistema')
            users = list_all_users()
            
            if users:
                # Contador de usuarios
                col_stats1, col_stats2, col_stats3 = st.columns(3)
                with col_stats1:
                    admin_count = sum(1 for u in users if get_user_info(u['username']).get('is_admin', False))
                    col_stats1.metric('👥 Total de Usuarios', len(users), delta=None)
                with col_stats2:
                    col_stats2.metric('🔐 Administradores', admin_count, delta=None)
                with col_stats3:
                    col_stats3.metric('📝 Usuarios Regulares', len(users) - admin_count, delta=None)
                
                st.markdown('---')
                
                # Lista de usuarios con mejor estética
                for idx, u in enumerate(users):
                    info = get_user_info(u['username'])
                    is_admin_flag = info.get('is_admin', False) if info else False
                    
                    # Tarjeta mejorada con gradiente
                    badge_color = '#00d4ff' if is_admin_flag else '#888'
                    badge_text = '👑 ADMINISTRADOR' if is_admin_flag else '👤 USUARIO'
                    badge_bg = '#020024' if is_admin_flag else '#f0f0f0'
                    
                    card_html = f"""
                    <div style='background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%); 
                                border-left: 5px solid {badge_color}; 
                                padding: 18px; border-radius: 12px; margin-bottom: 15px;
                                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); transition: all 0.3s ease;'>
                        <div style='display: flex; justify-content: space-between; align-items: center;'>
                            <div>
                                <h4 style='margin: 0; color: #020024; font-size: 1.1em;'>👤 {u['username']}</h4>
                                <div style='color: #555; font-size: 0.95em; margin-top: 6px;'>
                                    📧 <span style='color: #0066cc;'>{u['email']}</span> • 📅 {u['created_at'][:10]}
                                </div>
                                {f"<div style='color: #666; font-size: 0.9em; margin-top: 4px;'>⏱️ Último acceso: {info.get('last_login')[:19]}</div>" if info and info.get('last_login') else "<div style='color: #999; font-size: 0.9em; margin-top: 4px;'>⏱️ Nunca ha ingresado</div>"}
                            </div>
                            <div style='text-align: center;'>
                                <span style='background: {badge_bg}; color: {badge_color}; padding: 8px 14px; 
                                            border-radius: 20px; font-weight: bold; font-size: 0.85em;'>
                                    {badge_text}
                                </span>
                            </div>
                        </div>
                    </div>
                    """
                    st.markdown(card_html, unsafe_allow_html=True)
                    
                    # Botones de acción en dos columnas
                    col_left, col_mid, col_right = st.columns([2, 1, 1])
                    with col_mid:
                        if is_admin_flag:
                            if st.button('🔓 Revocar admin', key=f'demote_{u["username"]}', use_container_width=True):
                                res = set_user_admin(u['username'], False)
                                if res['success']:
                                    st.success(f'✅ {u["username"]} ya no es administrador')
                                    st.experimental_rerun()
                                else:
                                    st.error(res['message'])
                        else:
                            if st.button('🔐 Promover a admin', key=f'promote_{u["username"]}', use_container_width=True):
                                res = set_user_admin(u['username'], True)
                                if res['success']:
                                    st.success(f'✅ {u["username"]} ahora es administrador')
                                    st.experimental_rerun()
                                else:
                                    st.error(res['message'])
            else:
                st.info('📭 No hay usuarios registrados aún. El primer usuario en registrarse será admin.')

        # ============ PESTAÑA 2: OVERRIDES Y UTILIDADES ============
        with admin_tab2:
            st.markdown('### Configuración de Overrides')
            
            col_override_left, col_override_right = st.columns([1.5, 1])
            
            with col_override_left:
                st.markdown('**📊 Preview de Overrides Actuales**')
                try:
                    overrides = load_stats_overrides()
                    if overrides:
                        st.json(overrides)
                        override_count = len(overrides)
                        st.markdown(f'<p style="color: #00d4ff; font-weight: bold;">📈 {override_count} override(s) activo(s)</p>', 
                                   unsafe_allow_html=True)
                    else:
                        st.info('ℹ️ No hay overrides guardados. Sistema usando datos originales.')
                except Exception as e:
                    st.warning(f'⚠️ Error al cargar overrides: {str(e)}')

            with col_override_right:
                st.markdown('**🛠️ Acciones Rápidas**')
                
                if st.button('🗑️ Vaciar Overrides', use_container_width=True, key='clear_overrides'):
                    save_stats_overrides({})
                    st.success('✅ Overrides vaciados. Sistema restaurado.')
                    st.experimental_rerun()
                
                if st.button('🔄 Recargar Sistema', use_container_width=True, key='reload_system'):
                    st.success('✅ Sistema recargado.')
                    st.experimental_rerun()

            st.markdown('---')
            st.markdown('### 📋 Información del Sistema')
            
            sys_col1, sys_col2, sys_col3 = st.columns(3)
            with sys_col1:
                st.markdown("""
                <div style='background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                            padding: 15px; border-radius: 10px; text-align: center;'>
                    <div style='font-size: 1.8em; margin-bottom: 8px;'>📁</div>
                    <div style='color: #1565c0; font-weight: bold;'>data/users.json</div>
                    <div style='color: #666; font-size: 0.9em; margin-top: 4px;'>Base de datos de usuarios</div>
                </div>
                """, unsafe_allow_html=True)
            
            with sys_col2:
                st.markdown("""
                <div style='background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); 
                            padding: 15px; border-radius: 10px; text-align: center;'>
                    <div style='font-size: 1.8em; margin-bottom: 8px;'>⚙️</div>
                    <div style='color: #6a1b9a; font-weight: bold;'>data/stats_overrides.json</div>
                    <div style='color: #666; font-size: 0.9em; margin-top: 4px;'>Configuración de estadísticas</div>
                </div>
                """, unsafe_allow_html=True)
            
            with sys_col3:
                st.markdown("""
                <div style='background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); 
                            padding: 15px; border-radius: 10px; text-align: center;'>
                    <div style='font-size: 1.8em; margin-bottom: 8px;'>🔐</div>
                    <div style='color: #2e7d32; font-weight: bold;'>Clave Admin</div>
                    <div style='color: #666; font-size: 0.9em; margin-top: 4px;'>admin123</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('---')
            st.markdown("""
            <div style='background: #fffacd; border-left: 4px solid #ff8c00; padding: 15px; border-radius: 8px;'>
                <strong style='color: #ff8c00;'>⚠️ Importante:</strong>
                <div style='color: #333; margin-top: 8px; font-size: 0.95em;'>
                    • Estas acciones afectan directamente a la seguridad y funcionamiento de la aplicación<br>
                    • Ten cuidado al modificar permisos de administrador<br>
                    • Los overrides anulan datos originales; vacíalos para restaurar valores reales<br>
                    • Considera hacer backups de data/users.json antes de cambios críticos
                </div>
            </div>
            """, unsafe_allow_html=True)

# ============ TABLA GENERAL ============
st.header('📋 Tabla de Datos Filtrados')
st.dataframe(filtered, use_container_width=True)
