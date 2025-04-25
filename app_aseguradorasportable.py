import streamlit as st

# Diccionario de aseguradoras y sus descuentos
aseguradoras = {
    "Assa": 0.20,
    "Ancon": 0.15,
    "Mapfre": 0.10,
    "Blue Cross": 0.15,
    "Vivir": 0.15,
    "Palig": 0.15,
}

# Título de la app
st.title("🩺 Cálculo de Pagos - Aseguradoras")

# Entrada de datos
aseguradora = st.selectbox("Selecciona una Aseguradora", list(aseguradoras.keys()))
total_gastos = st.number_input("Total de Gastos ($)", min_value=0.0, step=100.0)
copago = st.slider("Copago del Cliente (%)", min_value=0, max_value=100, step=1)

# Botón para calcular
if st.button("Calcular"):
    descuento = aseguradoras[aseguradora]
    monto_con_descuento = total_gastos * (1 - descuento)
    pago_cliente = monto_con_descuento * (copago / 100)
    pago_aseguradora = monto_con_descuento - pago_cliente

    st.subheader("📊 Resultados")
    st.write(f"**Total de Gastos:** ${total_gastos:,.2f}")
    st.write(f"**Cliente Paga ({copago}%):** ${pago_cliente:,.2f}")
    st.write(f"**Aseguradora Paga:** ${pago_aseguradora:,.2f}")
