import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import time

# Configuración de la página
st.set_page_config(page_title="Monitor de Clima", layout="wide")

st.title("🌤️ Monitor de Clima en Tiempo Real")

# Conexión a la Base de Datos (Nota que el host es 'db')
CONN_STRING = 'postgresql://usuario_datos:password_secreto@db:5432/base_integrador'

def load_data():
    """Lee los últimos 500 registros de la base de datos"""
    try:
        engine = create_engine(CONN_STRING)
        # Leemos con Pandas directo de SQL
        query = "SELECT * FROM clima_real ORDER BY timestamp DESC LIMIT 500"
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        st.error(f"Error conectando a la base de datos: {e}")
        return pd.DataFrame()

# Botón de actualización manual
if st.button('🔄 Actualizar Datos'):
    st.rerun()

# Cargar datos
df = load_data()

if not df.empty:
    # Métricas rápidas (KPIs) - Tomamos la última lectura de cada ciudad
    latest_reading = df.sort_values('timestamp').groupby('ciudad').tail(1)
    
    col1, col2, col3 = st.columns(3)
    
    # Mostramos tarjetas con la temperatura actual
    for index, row in latest_reading.iterrows():
        if row['ciudad'] == 'Londres':
            col1.metric("Londres", f"{row['temperatura']} °C", row['descripcion'])
        elif row['ciudad'] == 'Nueva York':
            col2.metric("Nueva York", f"{row['temperatura']} °C", row['descripcion'])
        elif row['ciudad'] == 'Tokio':
            col3.metric("Tokio", f"{row['temperatura']} °C", row['descripcion'])

    st.markdown("---")

    # Gráfico de Líneas
    st.subheader("📈 Tendencia de Temperatura (Histórico)")
    
    # Streamlit necesita una tabla pivotada para graficar líneas por categoría
    chart_data = df.pivot_table(index='timestamp', columns='ciudad', values='temperatura')
    st.line_chart(chart_data)

    # Tabla de datos crudos (opcional, para debug)
    with st.expander("Ver datos crudos"):
        st.dataframe(df)

else:
    st.warning("Esperando datos... asegúrate de que el ETL esté corriendo.")