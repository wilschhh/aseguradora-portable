import streamlit as st

# Inicializar la sesión
if "resultados" not in st.session_state:
    st.session_state.resultados = []

# Aseguradoras y fórmulas
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

st.title("Cálculo de Pagos - Aseguradoras")

# Entradas
aseguradora = st.selectbox("Selecciona una Aseguradora", list(aseguradoras.keys()))
total_gastos = st.number_input("Total de Gastos ($)", min_value=0.0, step=100.0)
copago = st.number_input("Copago del Cliente (%)", min_value=0.0, max_value=100.0, step=1.0)

if st.button("Agregar al Formulario"):
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

    st.session_state.resultados.append({
        "total": total_gastos,
        "cliente": pago_cliente,
        "aseguradora": pago_aseguradora
    })

# Mostrar estilo de formulario impreso
if st.session_state.resultados:
    st.markdown("---")
    st.subheader("Formulario de Cálculo")

    st.markdown("""
    <style>
    .registro {
        font-family: monospace;
        font-size: 22px;
        border-collapse: collapse;
        width: 100%;
        margin-bottom: 10px;
    }
    .registro td {
        padding: 12px 10px;
        border-bottom: 1px dashed #888;
        text-align: center;
    }
    .registro th {
        padding: 10px;
        text-align: center;
        font-weight: bold;
        color: #222;
    }
    </style>
    <table class="registro">
        <tr>
            <th>TOTAL<br>CARGOS</th>
            <th>MONTO PAGADO<br>ASEGURADO</th>
            <th>SALDO<br>PAGAR</th>
        </tr>
    """, unsafe_allow_html=True)

    for fila in st.session_state.resultados:
        st.markdown(f"""
        <tr>
            <td>${fila['total']:,.2f}</td>
            <td>${fila['cliente']:,.2f}</td>
            <td>${fila['aseguradora']:,.2f}</td>
        </tr>
        """, unsafe_allow_html=True)

    st.markdown("</table>", unsafe_allow_html=True)
