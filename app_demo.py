import streamlit as st
import pandas as pd
import os

# ================= CONFIGURACIÓN =================
st.set_page_config(
    page_title="Demo - Buscador de Filtros MANN-FILTER",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================= RUTA DEL CSV =================
directorio_actual = os.path.dirname(os.path.abspath(__file__))
ruta_csv = os.path.join(directorio_actual, "demo_data.csv")

# ================= ESTILOS CSS MÍNIMOS =================
st.markdown("""
<style>
    .demo-banner {
        background: linear-gradient(90deg, #ff6b6b, #ee5a6f);
        color: white;
        padding: 1rem;
        text-align: center;
        font-weight: bold;
        font-size: 1.1rem;
        border-radius: 8px;
        margin-bottom: 2rem;
    }
    .watermark {
        position: fixed;
        bottom: 20px;
        right: 20px;
        color: rgba(255, 0, 0, 0.15);
        font-size: 3rem;
        font-weight: bold;
        transform: rotate(-15deg);
        z-index: 9999;
        pointer-events: none;
    }
    .filter-card {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid #1f77b4;
        margin-bottom: 0.5rem;
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# ================= CARGA DE DATOS =================
@st.cache_data
def cargar_demo():
    if not os.path.exists(ruta_csv):
        st.error(f"⚠️ No se encuentra el archivo: {ruta_csv}")
        st.info("Por favor, ejecute primero el script 'crear_csv_demo.py' para generar este archivo.")
        st.stop()
    
    df = pd.read_csv(ruta_csv)
    
    def enmascarar_codigo(codigo):
        if pd.isna(codigo) or str(codigo).strip() == "No disponible":
            return "No disponible"
        codigo = str(codigo)
        if len(codigo) > 4:
            return codigo[:4] + "***"
        return codigo + "***"
    
    df['Filtro_Aire'] = df['Filtro_Aire'].apply(enmascarar_codigo)
    df['Filtro_Aceite'] = df['Filtro_Aceite'].apply(enmascarar_codigo)
    df['Filtro_Combustible'] = df['Filtro_Combustible'].apply(enmascarar_codigo)
    df['Cod_Filtro_Habitaculo'] = df['Cod_Filtro_Habitaculo'].apply(enmascarar_codigo)
    df['Referencia_OEM'] = df['Referencia_OEM'].apply(enmascarar_codigo)
    
    return df

df_demo = cargar_demo()

# ================= ENCABEZADO =================
st.markdown('<div class="demo-banner">🔒 VERSIÓN DEMOSTRATIVA - Datos limitados. Versión completa disponible bajo licencia</div>', unsafe_allow_html=True)
st.markdown('<div class="watermark">DEMO</div>', unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🔧 Demo - Buscador Inteligente de Filtros</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Base de datos MANN-FILTER 2024-26 (Muestra limitada)</p>', unsafe_allow_html=True)

# ================= ESTADÍSTICAS =================
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🚗 Marcas", df_demo['Marca'].nunique())
with col2:
    st.metric("🚙 Modelos", df_demo['Modelo'].nunique())
with col3:
    st.metric("⚙️ Motores", df_demo['Motor'].nunique())
with col4:
    st.metric("📊 Registros", f"{len(df_demo):,}")

st.markdown("---")

# ================= BÚSQUEDA =================
st.markdown("### 🔍 Pruebe el buscador (datos enmascarados)")

col_marca, col_modelo, col_motor = st.columns(3)

with col_marca:
    marcas = sorted(df_demo['Marca'].unique())
    marca_sel = st.selectbox("🚗 Marca", marcas)

with col_modelo:
    modelos = sorted(df_demo[df_demo['Marca'] == marca_sel]['Modelo'].unique())
    modelo_sel = st.selectbox(" Modelo", modelos)

with col_motor:
    df_filtrado = df_demo[(df_demo['Marca'] == marca_sel) & (df_demo['Modelo'] == modelo_sel)]
    motores = sorted(df_filtrado['Motor'].unique())
    motor_sel = st.selectbox("⚙️ Motor", motores)

# ================= RESULTADOS =================
if motor_sel:
    registro = df_filtrado[df_filtrado['Motor'] == motor_sel].iloc[0]
    
    st.markdown("---")
    st.markdown(f"### 📊 Resultado para {marca_sel} {modelo_sel}")
    
    col_info1, col_info2 = st.columns(2)
    
    with col_info1:
        st.markdown('<div class="filter-card">', unsafe_allow_html=True)
        st.markdown(f"#### ⚙️ Motor")
        st.markdown(f"**{registro['Motor']}**")
        st.markdown(f"#### 💪 Potencia")
        st.markdown(f"**{registro['Potencia_kW_CV']}**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_info2:
        st.markdown('<div class="filter-card">', unsafe_allow_html=True)
        st.markdown(f"#### 📅 Año")
        st.markdown(f"**{registro['Año_Rango']}**")
        st.markdown(f"#### 🔢 OEM (enmascarado)")
        st.markdown(f"**{registro['Referencia_OEM']}**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🔧 Filtros Recomendados (códigos parciales)")
    
    col_filtros1, col_filtros2 = st.columns(2)
    
    with col_filtros1:
        st.markdown('<div class="filter-card">', unsafe_allow_html=True)
        st.markdown("#### 🌬️ Filtro de Aire")
        st.markdown(f"**{registro['Filtro_Aire']}**")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="filter-card">', unsafe_allow_html=True)
        st.markdown("#### 🛢️ Filtro de Aceite")
        st.markdown(f"**{registro['Filtro_Aceite']}**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_filtros2:
        st.markdown('<div class="filter-card">', unsafe_allow_html=True)
        st.markdown("#### ⛽ Filtro de Combustible")
        st.markdown(f"**{registro['Filtro_Combustible']}**")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="filter-card">', unsafe_allow_html=True)
        st.markdown("#### 🏠 Filtro de Habitáculo")
        st.markdown(f"**{registro['Cod_Filtro_Habitaculo']}**")
        st.markdown('</div>', unsafe_allow_html=True)

# ================= CTA CON COMPONENTES NATIVOS =================
st.markdown("---")

# Título principal
st.header("🎯 ¿Necesita acceso completo a los 6,058 registros?")
st.subheader("Obtenga la base de datos más completa del mercado automotriz")

st.markdown("---")

# Beneficios en dos columnas
st.markdown("#### ✅ Lo que incluye:")

col_ben1, col_ben2 = st.columns(2)

with col_ben1:
    st.markdown("**Columna 1:**")
    st.markdown("- ✅ **99 marcas** de vehículos (no solo 5)")
    st.markdown("- ✅ **Todos los modelos y motores** (no solo 15)")
    st.markdown("- ✅ **Códigos de filtros completos** sin enmascarar")

with col_ben2:
    st.markdown("**Columna 2:**")
    st.markdown("- ✅ **60% de registros con OEM verificado**")
    st.markdown("- ✅ **Actualizaciones trimestrales** incluidas por 1 año")
    st.markdown("- ✅ **Soporte técnico** por email (WhatsApp a solicitud)")

st.markdown("---")

# Precio destacado con container
with st.container():
    st.markdown("### 💰 Inversión única")
    st.markdown("## $299 USD")
    st.markdown("**Pago único - Acceso de por vida**")

st.markdown("---")

# Contacto
st.header("📧 Contacto directo")

col_contact1, col_contact2 = st.columns(2)

with col_contact1:
    st.markdown("**Opción 1: Enviar correo**")
    st.link_button(
        "✉️ Enviar correo ahora",
        "mailto:rodofrelance@gmail.com?subject=Interés%20en%20la%20Base%20de%20Datos%20MANN-FILTER%20Completa&body=Hola,%20estoy%20interesado%20en%20adquirir%20la%20base%20de%20datos%20completa%20de%20filtros%20MANN-FILTER."
    )

with col_contact2:
    st.markdown("**Opción 2: Copiar correo**")
    st.code("rodofrelance@gmail.com", language=None)
    st.caption("💡 Haga clic en el ícono de copiar (↗️) al lado del código")

st.markdown("---")

# Métodos de pago
st.markdown("### 💳 Métodos de pago aceptados")
st.markdown("**Transferencia bancaria | BNB | USDT (Binance)**")

st.markdown("---")

# Pie de página
st.markdown("*💡 Demo generada desde catálogo oficial MANN-FILTER 2024-26 | Datos completos disponibles bajo licencia*")