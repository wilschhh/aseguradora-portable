import tkinter as tk
from tkinter import ttk, messagebox

# Ventana principal
ventana = tk.Tk()
ventana.title("Cálculo de Pagos - Aseguradoras")
ventana.geometry("420x300")

# Aseguradoras disponibles
aseguradoras = [
    "ASSA",
    "MAPFRE",
    "PALIG",
    "BLUE CROSS",
    "VIVIR"
]

# Función para calcular según aseguradora
def calcular():
    try:
        aseguradora = combo_aseguradora.get()
        if aseguradora not in aseguradoras:
            messagebox.showerror("Error", "Selecciona una aseguradora válida.")
            return

        subtotal = float(entry_total.get())
        copago_porcentaje = float(entry_copago.get()) / 100  # % a decimal

        if aseguradora == "ASSA":
            descuento = 0.25
            monto_descuento = subtotal * descuento
            pago_cliente = subtotal - monto_descuento - (subtotal * copago_porcentaje)
            pago_aseguradora = subtotal - pago_cliente
        elif aseguradora == "MAPFRE":
            descuento = 0.20
            monto_descuento = subtotal * descuento
            pago_cliente = subtotal - monto_descuento - (subtotal * copago_porcentaje)
            pago_aseguradora = subtotal - pago_cliente
        elif aseguradora == "PALIG":
            descuento = 0.30
            monto_copago = subtotal * copago_porcentaje
            pago_cliente = monto_copago - (subtotal * descuento)
            pago_aseguradora = subtotal - pago_cliente
        elif aseguradora == "BLUE CROSS":
            descuento = 0.25
            monto_copago = subtotal * copago_porcentaje
            pago_cliente = monto_copago - (subtotal * descuento)
            pago_aseguradora = subtotal - pago_cliente
        elif aseguradora == "VIVIR":
            descuento = 0.20
            monto_descuento = subtotal * descuento
            pago_cliente = subtotal - monto_descuento - (subtotal * copago_porcentaje)
            pago_aseguradora = subtotal - pago_cliente
        else:
            messagebox.showerror("Error", "Fórmula no definida para esta aseguradora.")
            return

        resultado.set(
            f"Total Gastos: ${subtotal:,.2f}\n"
            f"Cliente Paga: ${pago_cliente:,.2f}\n"
            f"Aseguradora Paga: ${pago_aseguradora:,.2f}"
        )
    except ValueError:
        messagebox.showerror("Error", "Por favor ingresa valores numéricos válidos.")

# Interfaz
tk.Label(ventana, text="Selecciona Aseguradora:").pack()
combo_aseguradora = ttk.Combobox(ventana, values=aseguradoras)
combo_aseguradora.pack()

tk.Label(ventana, text="Total de Gastos:").pack()
entry_total = tk.Entry(ventana)
entry_total.pack()

tk.Label(ventana, text="Copago del Cliente (%):").pack()
entry_copago = tk.Entry(ventana)
entry_copago.pack()

tk.Button(ventana, text="Calcular", command=calcular).pack(pady=10)

resultado = tk.StringVar()
tk.Label(ventana, textvariable=resultado, justify="left").pack()

ventana.mainloop()
