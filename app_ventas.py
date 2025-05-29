import streamlit as st
import pandas as pd

# Configuración inicial
st.set_page_config(page_title="Dashboard de Ventas", layout="wide")
st.title("📊 Dashboard Interactivo de Ventas")
st.markdown("Acompañamiento visual en análisis de ingresos, productos y sucursales")

# Cargar datos
@st.cache_data
def cargar_datos():
    df = pd.read_excel("bd_ventas.xlsx", sheet_name="RegistroVentas")
    df[['Cantidad', 'Precio Unitario']] = df['Cantidad/Precio Unit'].str.split('/', expand=True)
    df['Cantidad'] = pd.to_numeric(df['Cantidad'], errors='coerce')
    df['Precio Unitario'] = pd.to_numeric(df['Precio Unitario'], errors='coerce')
    df['Ingresos'] = df['Cantidad'] * df['Precio Unitario']
    df['Fecha Pedido'] = pd.to_datetime(df['Fecha Pedido'])
    return df

df = cargar_datos()

# Filtros
col1, col2, col3 = st.columns(3)

with col1:
    tiendas = st.multiselect("Selecciona Tienda(s)", df["Código tienda"].unique(), default=df["Código tienda"].unique())

with col2:
    productos = st.multiselect("Selecciona Producto(s)", df["Producto"].unique(), default=df["Producto"].unique())

with col3:
    medios_pago = st.multiselect("Medio de Pago", df["Medio de pago"].unique(), default=df["Medio de pago"].unique())

fecha_inicio = st.date_input("Desde", df["Fecha Pedido"].min())
fecha_fin = st.date_input("Hasta", df["Fecha Pedido"].max())

# Aplicar filtros
df_filtrado = df[
    (df["Código tienda"].isin(tiendas)) &
    (df["Producto"].isin(productos)) &
    (df["Medio de pago"].isin(medios_pago)) &
    (df["Fecha Pedido"] >= pd.to_datetime(fecha_inicio)) &
    (df["Fecha Pedido"] <= pd.to_datetime(fecha_fin))
]

# KPIs
col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
col_kpi1.metric("🟢 Ingresos Totales", f"${df_filtrado['Ingresos'].sum():,.0f}")
col_kpi2.metric("📦 Unidades Vendidas", f"{df_filtrado['Cantidad'].sum():,.0f}")
col_kpi3.metric("🛍️ Órdenes", f"{df_filtrado.shape[0]:,.0f}")

# Gráficos
st.subheader("📌 Facturación por Tienda")
st.bar_chart(df_filtrado.groupby("Código tienda")["Ingresos"].sum())

st.subheader("📌 Facturación por Producto")
st.bar_chart(df_filtrado.groupby("Producto")["Ingresos"].sum())

st.subheader("📌 Medio de Pago")
st.dataframe(df_filtrado.groupby("Medio de pago")["Ingresos"].sum().reset_index(), use_container_width=True)

# Tabla detallada
st.subheader("📄 Detalle de Transacciones")
st.dataframe(df_filtrado.sort_values(by="Ingresos", ascending=False), use_container_width=True)
