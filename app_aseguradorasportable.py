import streamlit as st

# Diccionario de aseguradoras y sus descuentos
aseguradoras = {
    "ASSA": 0.25,
    "ANCON": 0.20,
    "MAPFRE": 0.20,
    "BLUE CROSS": 0.25,
    "VIVIR": 0.20,
    "PALIG": 0.30,
    "SAGICOR": 0.20,
    "SURA": 0.15,
}

# Título de la app
st.title("Cálculo de Pagos - Aseguradoras")

# Entrada de datos
aseguradora = st.selectbox("Selecciona una Aseguradora", list(aseguradoras.keys()))
total_gastos = st.number_input("Total de Gastos ($)", min_value=0.0, step=100.0)
copago = st.number_input("Copago del Cliente (%)", min_value=0.0, max_value=100.0, step=1.0)

# Botón para calcular
if st.button("Calcular"):
    descuento = aseguradoras[aseguradora]

    if aseguradora in ["MAPFRE", "BLUE CROSS", "ASSA", "ANCON"]:
        monto_con_descuento = total_gastos * (1 - descuento)
        pago_cliente = monto_con_descuento * (copago / 100)
        pago_aseguradora = monto_con_descuento - pago_cliente

    elif aseguradora == "PALIG":
        pago_cliente = total_gastos * (copago / 100)
        pago_aseguradora = pago_cliente * (1 - descuento)

    elif aseguradora in ["VIVIR", "SAGICOR", "SURA"]:
        pago_cliente = total_gastos * (copago / 100)
        descuento_valor = total_gastos * descuento
        pago_aseguradora = pago_cliente - descuento_valor

    # Mostrar resultados
    st.subheader("Resultados")
    st.write(f"**Total de Gastos:** ${total_gastos:,.2f}")
    st.write(f"**Cliente Paga ({copago}%):** ${pago_cliente:,.2f}")
    st.write(f"**Aseguradora Paga:** ${pago_aseguradora:,.2f}")
