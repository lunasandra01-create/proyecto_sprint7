import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------------
# Configuración inicial de la página
# --------------------------------------------------------
st.set_page_config(
    page_title="Dashboard de Vehículos", 
    page_icon="🚗", 
    layout="wide" # Para que los gráficos usen todo el espacio disponible
)

# --------------------------------------------------------
# 1. Cargar los datos
# --------------------------------------------------------
# Utilizamos cache_data para que no recargue el CSV cada vez que interactuamos
@st.cache_data
def load_data():
    # Ruta especificada
    path = "data/vehicles_us.csv"
    df = pd.read_csv(path)
    return df

df = load_data()

# --------------------------------------------------------
# 2. Título y subtítulo llamativos
# --------------------------------------------------------
st.title("🚗💨 ¡Súbete al Dashboard de Vehículos de EE. UU.! 🏁")
st.markdown("### 📊 *Explora, filtra y descubre las tendencias en el mercado de autos de segunda mano.* 🕵️‍♂️✨")
st.divider() # Una línea separadora elegante

# --------------------------------------------------------
# Filtros en la barra lateral para interactividad
# --------------------------------------------------------
st.sidebar.header("🔍 Filtros Dinámicos")

# Filtro por tipo de vehículo
tipos_vehiculos = df['type'].dropna().unique().tolist()
tipo_seleccionado = st.sidebar.multiselect(
    "Selecciona el Tipo de Vehículo:", 
    tipos_vehiculos, 
    default=tipos_vehiculos[:5] # Seleccionamos algunos por defecto
)

# Filtro por condición
condiciones = df['condition'].dropna().unique().tolist()
condicion_seleccionada = st.sidebar.multiselect(
    "Selecciona la Condición del Vehículo:", 
    condiciones, 
    default=condiciones
)

# Aplicar los filtros al DataFrame
df_filtrado = df.copy()
if tipo_seleccionado:
    df_filtrado = df_filtrado[df_filtrado['type'].isin(tipo_seleccionado)]
if condicion_seleccionada:
    df_filtrado = df_filtrado[df_filtrado['condition'].isin(condicion_seleccionada)]

# --------------------------------------------------------
# 3. Checkbox para la vista previa de datos
# --------------------------------------------------------
if st.checkbox("👀 Mostrar vista previa de los datos filtrados (Primeras 10 filas)"):
    # use_container_width asegura que la tabla ocupe el ancho completo
    st.dataframe(df_filtrado.head(10), use_container_width=True)

st.write("") # Espacio en blanco

# --------------------------------------------------------
# 4 y 5. Gráficos interactivos con Plotly Express
# --------------------------------------------------------
st.markdown("### 📈 Visualizaciones de Datos")

# Dividiremos la pantalla en 2 columnas para los primeros dos gráficos
col1, col2 = st.columns(2)

with col1:
    # --- Gráfico 1: Gráfico de barras horizontales ---
    st.subheader("💰 Precio Promedio por Tipo de Vehículo")
    
    # Agrupamos los datos para sacar el promedio
    df_agrupado = df_filtrado.groupby('type')['price'].mean().reset_index()
    df_agrupado = df_agrupado.sort_values(by='price', ascending=True)
    
    fig_bar = px.bar(
        df_agrupado, 
        x='price', 
        y='type', 
        orientation='h', # Barras horizontales
        color='type',
        labels={'type': 'Tipo', 'price': 'Precio Promedio ($)'},
        template='plotly_white' # Diseño profesional y limpio
    )
    # Ocultar la leyenda para un look más minimalista
    fig_bar.update_layout(showlegend=False) 
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    # --- Gráfico 2: Gráfico Circular (Donut Chart) ---
    st.subheader("⛽ Distribución por Tipo de Combustible")
    
    fig_donut = px.pie(
        df_filtrado, 
        names='fuel', 
        hole=0.45, # Esto lo convierte en un gráfico de dona
        color_discrete_sequence=px.colors.sequential.Teal,
        template='plotly_white'
    )
    fig_donut.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_donut, use_container_width=True)

# --- Gráfico 3: Histograma (Usa todo el ancho de la página) ---
st.subheader("🛣️ Distribución del Kilometraje (Odometer)")

fig_hist = px.histogram(
    df_filtrado, 
    x="odometer", 
    color="condition", 
    nbins=50, 
    labels={'odometer': 'Kilometraje (Millas)', 'count': 'Cantidad de Vehículos', 'condition': 'Condición'},
    template='plotly_white',
    opacity=0.8
)
# Ajustar el diseño para que las barras no se solapen sino que se apilen
fig_hist.update_layout(barmode='stack')
st.plotly_chart(fig_hist, use_container_width=True)