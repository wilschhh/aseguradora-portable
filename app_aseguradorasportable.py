import streamlit as st
import pandas as pd

# Inicializamos la sesión para guardar referencias verificadas
def init_session():
    if "verificados" not in st.session_state:
        st.session_state.verificados = []
    if "resultados" not in st.session_state:
        st.session_state.resultados = []

init_session()

# Diccionario de aseguradoras y sus fórmulas
aseguradoras = {
    "MAPFRE": "descuento",
    "BLUE CROSS": "descuento",
    "ASSA": "descuento",
    "PALIG": "copago_directo",
    "VIVIR": "vivir_formula",
    "SAGICOR": "vivir_formula",
    "SURA": "vivir_formula",
    "ANCON": "descuento",
}

descuentos = {
    "MAPFRE": 0.20,
    "BLUE CROSS": 0.25,
    "ASSA": 0.25,
    "ANCON": 0.20,
    "PALIG": 0.30,
    "VIVIR": 0.20,
    "SAGICOR": 0.20,
    "SURA": 0.15,
}

# Dividimos en dos columnas
col1, col2 = st.columns([2, 1])

with col1:
    st.title("Cálculo de Pagos - Aseguradoras")

    referencia = st.text_input("Número de Referencia del Cliente")

    aseguradora = st.selectbox("Selecciona una Aseguradora", list(aseguradoras.keys()))
    total_gastos = st.number_input("Total de Gastos ($)", min_value=0.0, step=100.0)
    copago = st.number_input("Copago del Cliente (%)", min_value=0.0, max_value=100.0, step=1.0)

    col_b1, col_b2 = st.columns(2)

    if col_b1.button("Calcular"):
        formula = aseguradoras[aseguradora]
        descuento = descuentos[aseguradora]

        if formula == "descuento":
            monto_con_descuento = total_gastos * (1 - descuento)
            pago_cliente = monto_con_descuento * (copago / 100)
            pago_aseguradora = monto_con_descuento - pago_cliente

        elif formula == "copago_directo":
            pago_cliente = total_gastos * (copago / 100)
            pago_aseguradora = total_gastos * (1 - copago / 100)

        elif formula == "vivir_formula":
            pago_cliente = total_gastos * (copago / 100)
            pago_aseguradora = (total_gastos * (1 - descuento)) - pago_cliente

        # Guardar el resultado en la sesión
        st.session_state.resultados.append({
            "TOTAL CARGOS": f"{total_gastos:,.2f}",
            "MONTO PAGADO ASEGURADO": f"{pago_cliente:,.2f}",
            "SALDO PAGAR": f"{pago_aseguradora:,.2f}",
            " ": f"{total_gastos:,.2f}"  # Repetido como pediste
        })

    if col_b2.button("Verificado"):
        if referencia.strip() != "":
            st.session_state.verificados.append(referencia.strip())
        else:
            st.warning("Por favor, ingresa un número de referencia.")

    if st.session_state.resultados:
        st.subheader("Resultados")
        df_resultados = pd.DataFrame(st.session_state.resultados)
        st.dataframe(df_resultados, hide_index=True, use_container_width=True)

with col2:
    st.subheader("Checklist de Referencias Verificadas ✅")
    if st.session_state.verificados:
        df_verificados = pd.DataFrame({
            "Referencia": st.session_state.verificados,
            "Verificado": ["✅"] * len(st.session_state.verificados)
        })
        st.dataframe(df_verificados, hide_index=True, use_container_width=True)
    else:
        st.info("Aún no hay referencias verificadas.")

