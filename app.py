import streamlit as st

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Calculadora de Balance de Masa",
    page_icon="🍓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Título y Descripción ---
st.title("🍓 Calculadora de Balance de Masa para Pulpas")
st.markdown("""
Esta aplicación web resuelve problemas de balance de masa para calcular la cantidad de azúcar necesaria 
para ajustar la concentración de sólidos solubles (°Brix) de una pulpa de fruta. 

Introduce los valores en la barra lateral de la izquierda y los resultados se actualizarán automáticamente.
""")

# --- Interfaz de Usuario para Entradas en la Barra Lateral ---
st.sidebar.header("Parámetros de Entrada")
st.sidebar.markdown("Introduce los valores del proceso:")

# Usamos los valores del ejercicio como valores por defecto
m1 = st.sidebar.number_input(
    "Masa Inicial de Pulpa (M1) en kg", 
    min_value=0.0, value=50.0, step=1.0, format="%.2f",
    help="Ingresa la masa inicial de la pulpa que vas a procesar."
)
x1_percent = st.sidebar.number_input(
    "Concentración Inicial (°Brix)", 
    min_value=0.0, max_value=99.9, value=7.0, step=0.1, format="%.1f",
    help="Porcentaje de sólidos solubles (azúcar) en la pulpa inicial."
)
x3_percent = st.sidebar.number_input(
    "Concentración Final Deseada (°Brix)", 
    min_value=0.0, max_value=99.9, value=10.0, step=0.1, format="%.1f",
    help="El porcentaje de °Brix que deseas alcanzar en el producto final."
)

# --- Lógica de Cálculo y Validación ---
# Validamos que la concentración final sea mayor que la inicial para evitar errores
if x3_percent <= x1_percent:
    st.error("⚠️ **Error:** La concentración final deseada debe ser mayor que la concentración inicial.")
else:
    # Convertimos los porcentajes a fracción decimal para los cálculos
    x1_frac = x1_percent / 100
    x3_frac = x3_percent / 100

    # Calculamos las fracciones de agua (Y = 1 - X)
    y1 = 1 - x1_frac  # Fracción de agua en la pulpa inicial
    y3 = 1 - x3_frac  # Fracción de agua en la pulpa final

    # --- Cálculos del Balance ---
    # Como solo agregamos azúcar (sin agua), la masa total de agua es constante.
    # Balance de Agua: M1 * Y1 = M3 * Y3
    # Despejamos la masa final (M3):
    m3 = (m1 * y1) / y3

    # Balance General de Masa: M1 + M2 = M3
    # Despejamos el azúcar a agregar (M2):
    m2 = m3 - m1

    # --- Mostrar Resultados ---
    st.header("📊 Resultados del Cálculo")
    col1, col2 = st.columns(2)

    with col1:
        st.metric(label="Azúcar a Agregar (M2)", value=f"{m2:.2f} kg")
        st.image("https://i.imgur.com/S50mF4w.png", width=150, caption="Azúcar (M2)")

    with col2:
        st.metric(label="Masa Final de la Pulpa (M3)", value=f"{m3:.2f} kg")
        st.image("https://i.imgur.com/Y32LffH.png", width=150, caption="Pulpa Final (M3)")
    
    st.success(f"**Conclusión:** Se deben agregar **{m2:.2f} kg** de azúcar para llevar los 50 kg de pulpa desde 7°Brix hasta 10°Brix, resultando en una masa final de **{m3:.2f} kg**.")

    # --- Explicación detallada del proceso (como en la imagen) ---
    with st.expander("Haz clic para ver el paso a paso del cálculo"):
        st.subheader("Fórmulas Utilizadas")
        st.markdown("""
        - **M1**: Masa de Pulpa Inicial
        - **M2**: Masa de Azúcar a agregar
        - **M3**: Masa de Pulpa Final
        - **Y1**: Fracción de agua inicial (`1 - X1/100`)
        - **Y3**: Fracción de agua final (`1 - X3/100`)
        """)

        st.subheader("1. Balance por Agua (Componente que no cambia)")
        st.latex(r'''M_1 \cdot Y_1 = M_3 \cdot Y_3''')
        st.markdown("La cantidad total de agua no varía, ya que solo agregamos azúcar (sólidos). A partir de esta relación, despejamos la masa final (M3).")
        st.latex(fr'''M_3 = \frac{{M_1 \cdot Y_1}}{{Y_3}} = \frac{{{m1:.2f} \text{{ kg}} \cdot {y1:.2f}}}{{{y3:.2f}}} = {m3:.2f} \text{{ kg}}''')

        st.subheader("2. Balance General de Masa")
        st.latex(r'''M_1 + M_2 = M_3''')
        st.markdown("Con la masa inicial y la final ya calculada, despejamos la cantidad de azúcar (M2) que se necesita.")
        st.latex(fr'''M_2 = M_3 - M_1 = {m3:.2f} \text{{ kg}} - {m1:.2f} \text{{ kg}} = {m2:.2f} \text{{ kg}}''')
