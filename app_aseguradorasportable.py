import streamlit as st
import pandas as pd
import io
from datetime import datetime

# Configurar ancho completo de la app
st.set_page_config(page_title="Aseguradora Portable", layout="wide")

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

st.title("Cálculo de Pagos - Aseguradoras")

# Historial temporal de cálculos
if "historial" not in st.session_state:
    st.session_state.historial = []

with st.expander("➕ Ingresar Datos del Paciente", expanded=True):
    aseguradora = st.selectbox("Selecciona una Aseguradora", list(aseguradoras.keys()))
    copago = st.number_input("Copago del Cliente (%)", min_value=0.0, max_value=100.0, step=1.0)

    st.write("### Ingresa los montos de cargos (uno por línea)")
    cargos_texto = st.text_area("Montos separados por línea", height=150)

    if st.button("Calcular Pagos"):
        try:
            cargos = [float(x.strip()) for x in cargos_texto.strip().splitlines() if x.strip() != ""]
            if not cargos:
                st.error("⚠️ Debes ingresar al menos un monto válido.")
            else:
                total_gastos = sum(cargos)
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

                # Crear tabla de resultados
                data = {
                    "TOTAL CARGOS": [f"${total_gastos:,.2f}", "", "", f"${total_gastos:,.2f}"],
                    "MONTO PAGADO ASEGURADO": [f"${pago_cliente:,.2f}", "", "", f"${pago_cliente:,.2f}"],
                    "SALDO PAGAR": [f"${pago_aseguradora:,.2f}", "", "", f"${pago_aseguradora:,.2f}"],
                }

                df_resultado = pd.DataFrame(data)
                st.subheader("📋 Resumen de Pagos")
                st.dataframe(df_resultado, use_container_width=True, hide_index=True)

                # Guardar historial temporal
                st.session_state.historial.append({
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "aseguradora": aseguradora,
                    "copago": copago,
                    "cargos": total_gastos,
                    "cliente": pago_cliente,
                    "aseguradora_pago": pago_aseguradora,
                })

                # Descargar como Excel
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df_resultado.to_excel(writer, index=False, sheet_name='Resumen')
                st.download_button(
                    label="📥",
                    data=output.getvalue(),
                    file_name="resumen_pagos.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        except ValueError:
            st.error("❌ Asegúrate de ingresar solo números válidos en la lista de cargos.")

# Mostrar historial temporal
if st.session_state.historial:
    st.write("### Historial de cálculos en esta sesión")
    df_hist = pd.DataFrame(st.session_state.historial)
    st.dataframe(df_hist, use_container_width=True, hide_index=True)
