import tkinter as tk
from tkinter import messagebox, ttk
import requests


api_url = 'http://127.0.0.1:5000'

def autenticar_vendedor(vendedor_id, password, ventana_actual):
    try:
        url = f"{api_url}/autenticar"
        data = {'vendedor_id': vendedor_id, 'password': password}
        response = requests.post(url, json=data)

        if response.status_code == 200:
            ventana_actual.destroy()  # Cierra la ventana de autenticación
            mostrar_ventana_ventas(vendedor_id)  # Redirigir a la ventana de ventas
        else:
            error_data = response.json()
            messagebox.showerror("Error", error_data.get("error", "No se encontró el vendedor o contraseña incorrecta."))
    except Exception as e:
        messagebox.showerror("Error", f"Error al conectarse a la API: {e}")

def mostrar_ventana_ventas(vendedor_id):
    ventana_ventas = tk.Tk()
    ventana_ventas.title("Ventas de la Sede")
    ventana_ventas.geometry("900x600")
    ventana_ventas.configure(bg='#1E1E1E')

    etiqueta_bienvenida = tk.Label(ventana_ventas, text=f"Bienvenido, Vendedor ID: {vendedor_id}",
                                   font=("Roboto", 18, "bold"), bg="#1E1E1E", fg="white")
    etiqueta_bienvenida.pack(pady=20)

    store_var = tk.StringVar()
    store_label = tk.Label(ventana_ventas, text="Selecciona una Sede:", font=("Roboto", 12), bg="#1E1E1E", fg="white")
    store_label.pack(pady=10)
    store_dropdown = ttk.Combobox(ventana_ventas, textvariable=store_var)
    store_dropdown['values'] = ("Lima Norte", "Barranco", "Miraflores", "San Isidro", "Surco", "La Molina")
    store_dropdown.pack(pady=10)

    ver_ventas_btn = tk.Button(ventana_ventas, text="Ver Ventas",
                               command=lambda: obtener_ventas(vendedor_id, store_var.get(), ventana_ventas),
                               bg="#007BFF", fg="white", font=("Roboto", 12, "bold"), width=20, height=2, relief="flat")
    ver_ventas_btn.pack(pady=20)

    ventana_ventas.mainloop()


def obtener_ventas(vendedor_id, store, ventana_actual):
    if not store:
        messagebox.showerror("Error", "Por favor, selecciona una sede.")
        return

    try:
        url = f"{api_url}/ventas/{store}?vendedor_id={vendedor_id}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            mostrar_tabla_ventas(data, ventana_actual)
        else:
            error_data = response.json()
            messagebox.showerror("Error", error_data.get("error", "No tienes permiso para ver las ventas."))
    except Exception as e:
        messagebox.showerror("Error", f"Error al conectarse a la API: {e}")


def mostrar_tabla_ventas(data, ventana_actual):
    ventana_actual.destroy()
    ventana_tabla = tk.Tk()
    ventana_tabla.title("Ventas de la Sede")
    ventana_tabla.geometry("1000x600")
    ventana_tabla.configure(bg='#2C2C2C')  # Fondo gris oscuro

    etiqueta_ventas = tk.Label(ventana_tabla, text="Ventas de la Sede", font=("Roboto", 18, "bold"), bg="#2C2C2C",
                               fg="white")
    etiqueta_ventas.pack(pady=10)

    style = ttk.Style()
    style.configure("mystyle.Treeview", font=("Roboto", 12), rowheight=30, background="#333333", foreground="white",
                    fieldbackground="#333333")

    style.configure("mystyle.Treeview.Heading", font=("Roboto", 14, "bold"), background="#444444", foreground="black")

    tabla = ttk.Treeview(ventana_tabla, columns=("Fecha", "Ventas Semanales", "Vendedor ID", "Temperatura", "Precio Combustible", "CPI", "Festivo"), show="headings", style="mystyle.Treeview")

    tabla.heading("Fecha", text="Fecha")
    tabla.heading("Ventas Semanales", text="Ventas Semanales")
    tabla.heading("Vendedor ID", text="Vendedor ID")
    tabla.heading("Temperatura", text="Temperatura")
    tabla.heading("Precio Combustible", text="Precio Combustible")
    tabla.heading("CPI", text="CPI")
    tabla.heading("Festivo", text="Festivo (1=Sí)")

    tabla.pack(fill="both", expand=True, padx=20, pady=20)

    for venta in data:
        tabla.insert('', 'end', values=(
            venta['Date'],
            venta['Weekly_Sales'],
            venta['Vendedor_ID'],
            venta['Temperature'],
            venta['Fuel_Price'],
            venta['CPI'],
            venta['Holiday_Flag']
        ))

    ventana_tabla.mainloop()

def ventana_autenticacion():
    ventana = tk.Tk()
    ventana.title("Autenticación")
    ventana.geometry("400x300")
    ventana.configure(bg='#1d1f21')

    titulo = tk.Label(ventana, text="Sistema de Autenticación", font=("Roboto", 18, "bold"), bg="#1d1f21", fg="white")
    titulo.pack(pady=20)

    vendedor_id_label = tk.Label(ventana, text="ID del Vendedor:", font=("Roboto", 12), bg="#1d1f21", fg="white")
    vendedor_id_label.pack(pady=5)
    vendedor_id_entry = tk.Entry(ventana, font=("Roboto", 12))
    vendedor_id_entry.pack(pady=10)

    password_label = tk.Label(ventana, text="Contraseña:", font=("Roboto", 12), bg="#1d1f21", fg="white")
    password_label.pack(pady=5)
    password_entry = tk.Entry(ventana, font=("Roboto", 12), show="*")
    password_entry.pack(pady=10)

    login_btn = tk.Button(ventana, text="Autenticar",
                          command=lambda: autenticar_vendedor(vendedor_id_entry.get(), password_entry.get(), ventana),
                          bg="#28A745", fg="white", font=("Roboto", 12, "bold"), width=15, height=2, relief="flat")
    login_btn.pack(pady=20)

    ventana.mainloop()

ventana_autenticacion()
