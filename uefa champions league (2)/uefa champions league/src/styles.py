"""
Archivo de estilos CSS personalizados para Streamlit.
Aplicar con: st.markdown(load_css(), unsafe_allow_html=True)
"""

def get_custom_css():
    """Retorna CSS personalizado con el color #020024"""
    return """
    <style>
    /* Color principal */
    :root {
        --primary-color: #2a6fbf;
        --primary-dark: #1f5fa8;
        --primary-light: #4a8fe0;
        --primary-faded: rgba(42,111,191,0.85);
        --accent-color: #00d4ff;
        --text-dark: #123a6b;
    }
    
    /* Barra de búsqueda principal — estética y dinámica (sin cambiar colores) */
    .stTextInput > div > div > input,
    .stTextInput input {
        background-color: #f8f9fa !important;
        border: 2px solid var(--primary-color) !important;
        border-radius: 24px !important;
        padding: 12px 16px 12px 44px !important;
        color: var(--text-dark) !important;
        font-weight: 500 !important;
        transition: all 0.25s cubic-bezier(.2,.8,.2,1) !important;
        box-shadow: 0 4px 18px rgba(18,58,107,0.06) inset;
        background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='%23123a6b' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><circle cx='11' cy='11' r='7'></circle><line x1='21' y1='21' x2='16.65' y2='16.65'></line></svg>") !important;
        background-repeat: no-repeat !important;
        background-position: 14px center !important;
        background-size: 18px 18px !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextInput input:focus {
        border-color: var(--accent-color) !important;
        box-shadow: 0 10px 30px rgba(0, 212, 255, 0.12) !important, 0 4px 14px rgba(18,58,107,0.06) inset !important;
        background-color: #ffffff !important;
        transform: translateY(-1px) !important;
    }

    /* Placeholder — animación sutil */
    .stTextInput > div > div > input::placeholder {
        color: #9aa5b1 !important;
        opacity: 1 !important;
        transition: color 0.2s ease, transform 0.25s ease !important;
    }

    /* Clear button visual (non-functional in pure CSS, decorative) */
    .stTextInput > div > div > input::-ms-clear { display: none; }
    .stTextInput > div > div > input::-ms-reveal { display: none; }
    
    /* Botones */
    .stButton > button {
        background-color: var(--primary-color) !important;
        color: white !important;
        border: 2px solid var(--primary-color) !important;
        border-radius: 10px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background-color: var(--primary-dark) !important;
        border-color: var(--accent-color) !important;
        box-shadow: 0 4px 12px rgba(0, 212, 255, 0.18) !important;
    }
    
    /* Selectbox */
    .stSelectbox > div > div > select {
        background-color: #f8f9fa !important;
        border: 2px solid var(--primary-color) !important;
        border-radius: 10px !important;
        color: var(--text-dark) !important;
        padding: 10px 12px !important;
        font-weight: 500 !important;
    }
    
    .stSelectbox > div > div > select:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.1) !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] button {
        background-color: transparent !important;
        color: var(--text-dark) !important;
        border-bottom: 3px solid transparent !important;
        border-radius: 0 !important;
        padding: 12px 20px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stTabs [data-baseweb="tab-list"] button:hover {
        border-bottom-color: var(--primary-color) !important;
        color: var(--primary-color) !important;
    }
    
    .stTabs [aria-selected="true"] {
        border-bottom-color: var(--primary-color) !important;
        color: var(--primary-color) !important;
    }
    
    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-dark) !important;
    }
    
    /* H1 con fondo azul ligeramente desvanecido */
    h1 {
        background: linear-gradient(135deg, var(--primary-faded) 0%, rgba(42,111,191,0.7) 100%) !important;
        color: white !important;
        padding: 20px 30px !important;
        border-radius: 12px !important;
        text-align: center !important;
        margin-bottom: 20px !important;
        backdrop-filter: blur(2px) !important;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #f5f7fa !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(42,111,191,0.95) 0%, rgba(31,95,168,0.85) 100%) !important;
        color: white !important;
        border-left: 4px solid var(--accent-color) !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, rgba(31,95,168,0.9) 0%, rgba(42,111,191,0.85) 100%) !important;
        box-shadow: 0 2px 8px rgba(0, 212, 255, 0.14) !important;
    }
    
    /* Tabs contenedor */
    [data-baseweb="tab-list"] {
        background-color: #f8f9fa !important;
        border-bottom: 2px solid var(--primary-color) !important;
    }
    
    /* Métrica */
    .stMetric {
        background-color: #f8f9fa;
        border-left: 4px solid var(--primary-color);
        padding: 12px 16px;
        border-radius: 8px;
    }
    
    /* Labels */
    label {
        color: var(--primary-color) !important;
        font-weight: 600 !important;
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background-color: rgba(0, 212, 255, 0.1) !important;
        border: 1px solid #00d4ff !important;
        border-left: 4px solid #00d4ff !important;
    }
    
    .stError {
        background-color: rgba(255, 75, 75, 0.1) !important;
        border: 1px solid #ff4b4b !important;
        border-left: 4px solid #ff4b4b !important;
    }
    
    .stWarning {
        background-color: rgba(255, 193, 7, 0.1) !important;
        border: 1px solid #ffc107 !important;
        border-left: 4px solid #ffc107 !important;
    }
    
    .stInfo {
        background-color: rgba(0, 212, 255, 0.1) !important;
        border: 1px solid #00d4ff !important;
        border-left: 4px solid #00d4ff !important;
    }
    
    /* Slider */
    .stSlider > div > div > div > div {
        background-color: var(--primary-color) !important;
    }
    
    /* Container/Box personalizado */
    .custom-container {
        background-color: #f8f9fa;
        border: 2px solid var(--primary-color);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
    }
    
    /* Secciones con fondo azul oscuro */
    .section-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    
    /* Elementos de métrica */
    [data-testid="metric-container"] {
        background: white !important;
        border-left: 4px solid var(--primary-color) !important;
    }
    
    /* Cards de datos */
    [data-testid="stDataFrame"] {
        background-color: white !important;
    }
    
    /* Área de gráficos */
    [data-testid="stPlotlyChart"],
    [data-testid="stImage"] {
        background-color: white !important;
    }
    
    /* Transiciones suaves */
    * {
        transition: all 0.2s ease !important;
    }
    </style>
    """
