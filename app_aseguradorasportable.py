import streamlit as st

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

# Interfaz principal
st.title("Cálculo de Pagos - Aseguradoras")

aseguradora = st.selectbox("Selecciona una Aseguradora", list(aseguradoras.keys()))
total_gastos = st.number_input("Total de Gastos ($)", min_value=0.0, step=100.0)
copago = st.number_input("Copago del Cliente (%)", min_value=0.0, max_value=100.0, step=1.0)

if st.button("Calcular"):
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

    st.success("Resultado del Cálculo:")
    st.write(f"**Total de Gastos:** ${total_gastos:,.2f}")
    st.write(f"**Cliente Paga:** ${pago_cliente:,.2f}")
    st.write(f"**Aseguradora Paga:** ${pago_aseguradora:,.2f}")
