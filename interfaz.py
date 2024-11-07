import tkinter as tk
from tkinter import messagebox, ttk
import requests
import webbrowser

api_url = 'http://127.0.0.1:5000'

# Función para autenticar al vendedor con contraseña inicial
def autenticar_vendedor(vendedor_id, password, ventana_actual):
    try:
        url = f"{api_url}/autenticar"
        data = {'vendedor_id': vendedor_id, 'password': password}
        response = requests.post(url, json=data)

        if response.status_code == 200:
            ventana_actual.destroy()  # Cierra la ventana de autenticación
            mostrar_ventana_2fa(vendedor_id)  # Redirige a la ventana para ingresar el código de 2FA
        else:
            error_data = response.json()
            messagebox.showerror("Error", error_data.get("error", "No se encontró el vendedor o contraseña incorrecta."))
    except Exception as e:
        messagebox.showerror("Error", f"Error al conectarse a la API: {e}")

# Ventana para ingresar el código de 2FA
def mostrar_ventana_2fa(vendedor_id):
    ventana_2fa = tk.Tk()
    ventana_2fa.title("Verificación 2FA")
    ventana_2fa.geometry("400x300")
    ventana_2fa.configure(bg='#1d1f21')

    etiqueta_codigo = tk.Label(ventana_2fa, text="Ingresa el código de verificación 2FA:", font=("Roboto", 12), bg="#1d1f21", fg="white")
    etiqueta_codigo.pack(pady=10)
    codigo_entry = tk.Entry(ventana_2fa, font=("Roboto", 12))
    codigo_entry.pack(pady=10)

    verificar_btn = tk.Button(ventana_2fa, text="Verificar",
                              command=lambda: verificar_2fa(vendedor_id, codigo_entry.get(), ventana_2fa),
                              bg="#28A745", fg="white", font=("Roboto", 12, "bold"), width=15, height=2, relief="flat")
    verificar_btn.pack(pady=20)

    ventana_2fa.mainloop()

# Verificación de 2FA con código
def verificar_2fa(vendedor_id, codigo, ventana_actual):
    try:
        url = f"{api_url}/verificar_2fa"
        data = {'codigo': codigo}
        response = requests.post(url, json=data)

        if response.status_code == 200:
            ventana_actual.destroy()
            mostrar_ventana_ventas(vendedor_id)
        else:
            error_data = response.json()
            messagebox.showerror("Error", error_data.get("error", "Código de verificación incorrecto."))
    except Exception as e:
        messagebox.showerror("Error", f"Error al conectarse a la API: {e}")

# Ventana de ventas donde se muestran los resultados
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

    agregar_venta_btn = tk.Button(ventana_ventas, text="Agregar Venta",
                                  command=lambda: mostrar_ventana_agregar_venta(vendedor_id, store_var.get()),
                                  bg="#28A745", fg="white", font=("Roboto", 12, "bold"), width=20, height=2, relief="flat")
    agregar_venta_btn.pack(pady=20)

    perfil_btn = tk.Button(ventana_ventas, text="Ver/Editar Perfil",
                           command=lambda: mostrar_ventana_perfil(vendedor_id),
                           bg="#FFD700", fg="black", font=("Roboto", 12, "bold"), width=20, height=2, relief="flat")
    perfil_btn.pack(pady=20)

    eliminar_cuenta_btn = tk.Button(ventana_ventas, text="Eliminar Cuenta",
                                    command=lambda: eliminar_cuenta(vendedor_id),
                                    bg="red", fg="white", font=("Roboto", 12, "bold"), width=20, height=2, relief="flat")
    eliminar_cuenta_btn.pack(pady=20)

    exportar_datos_btn = tk.Button(ventana_ventas, text="Exportar Datos",
                                   command=lambda: exportar_datos(vendedor_id),
                                   bg="#FFA500", fg="black", font=("Roboto", 12, "bold"), width=20, height=2, relief="flat")
    exportar_datos_btn.pack(pady=20)

    eliminar_datos_antiguos_btn = tk.Button(ventana_ventas, text="Eliminar Datos Antiguos",
                                            command=eliminar_datos_antiguos,
                                            bg="#FF4500", fg="white", font=("Roboto", 12, "bold"), width=20, height=2, relief="flat")
    eliminar_datos_antiguos_btn.pack(pady=20)

    ventana_ventas.mainloop()


# Función para mostrar y editar el perfil
def mostrar_ventana_perfil(vendedor_id):
    ventana_perfil = tk.Tk()
    ventana_perfil.title("Perfil del Vendedor")
    ventana_perfil.geometry("400x400")
    ventana_perfil.configure(bg='#1d1f21')

    # Acceder a datos de perfil
    url = f"{api_url}/perfil/{vendedor_id}"
    response = requests.get(url)
    datos = response.json()

    nombre_label = tk.Label(ventana_perfil, text="Nombre:", bg="#1d1f21", fg="white")
    nombre_label.pack(pady=5)
    nombre_entry = tk.Entry(ventana_perfil)
    nombre_entry.insert(0, datos.get("Nombre_Vendedor", ""))
    nombre_entry.pack(pady=5)

    store_label = tk.Label(ventana_perfil, text="Tienda:", bg="#1d1f21", fg="white")
    store_label.pack(pady=5)
    store_entry = tk.Entry(ventana_perfil)
    store_entry.insert(0, datos.get("Store", ""))
    store_entry.pack(pady=5)

    actualizar_btn = tk.Button(ventana_perfil, text="Actualizar",
                               command=lambda: actualizar_perfil(vendedor_id, nombre_entry.get(), store_entry.get(), ventana_perfil),
                               bg="#28A745", fg="white", font=("Roboto", 12, "bold"))
    actualizar_btn.pack(pady=20)

    ventana_perfil.mainloop()

# Actualizar datos de perfil
def actualizar_perfil(vendedor_id, nombre, store, ventana_perfil):
    url = f"{api_url}/perfil/{vendedor_id}"
    data = {"Nombre_Vendedor": nombre, "Store": store}
    response = requests.put(url, json=data)

    if response.status_code == 200:
        messagebox.showinfo("Éxito", "Perfil actualizado correctamente")
        ventana_perfil.destroy()
    else:
        messagebox.showerror("Error", "No se pudo actualizar el perfil")

def eliminar_cuenta(vendedor_id):
    respuesta = messagebox.askyesno("Confirmación", "¿Está seguro de que desea eliminar su cuenta? Esta acción es irreversible.")
    if respuesta:
        url = f"{api_url}/eliminar_cuenta/{vendedor_id}"
        response = requests.delete(url)
        if response.status_code == 200:
            messagebox.showinfo("Éxito", "Cuenta eliminada exitosamente")
        else:
            messagebox.showerror("Error", "No se pudo eliminar la cuenta")

# Función para obtener ventas
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

# Ventana para agregar una nueva venta
def mostrar_ventana_agregar_venta(vendedor_id, store):
    if not store:
        messagebox.showerror("Error", "Por favor, selecciona una sede antes de agregar una venta.")
        return

    ventana_agregar = tk.Tk()
    ventana_agregar.title("Agregar Nueva Venta")
    ventana_agregar.geometry("400x400")
    ventana_agregar.configure(bg='#1d1f21')

    # Campos para los datos de la venta
    date_label = tk.Label(ventana_agregar, text="Fecha (YYYY-MM-DD):", bg="#1d1f21", fg="white")
    date_label.pack(pady=5)
    date_entry = tk.Entry(ventana_agregar)
    date_entry.pack(pady=5)

    weekly_sales_label = tk.Label(ventana_agregar, text="Ventas Semanales:", bg="#1d1f21", fg="white")
    weekly_sales_label.pack(pady=5)
    weekly_sales_entry = tk.Entry(ventana_agregar)
    weekly_sales_entry.pack(pady=5)

    holiday_flag_label = tk.Label(ventana_agregar, text="Festivo (0 o 1):", bg="#1d1f21", fg="white")
    holiday_flag_label.pack(pady=5)
    holiday_flag_entry = tk.Entry(ventana_agregar)
    holiday_flag_entry.pack(pady=5)

    temperature_label = tk.Label(ventana_agregar, text="Temperatura:", bg="#1d1f21", fg="white")
    temperature_label.pack(pady=5)
    temperature_entry = tk.Entry(ventana_agregar)
    temperature_entry.pack(pady=5)

    fuel_price_label = tk.Label(ventana_agregar, text="Precio del Combustible:", bg="#1d1f21", fg="white")
    fuel_price_label.pack(pady=5)
    fuel_price_entry = tk.Entry(ventana_agregar)
    fuel_price_entry.pack(pady=5)

    cpi_label = tk.Label(ventana_agregar, text="CPI:", bg="#1d1f21", fg="white")
    cpi_label.pack(pady=5)
    cpi_entry = tk.Entry(ventana_agregar)
    cpi_entry.pack(pady=5)

    agregar_btn = tk.Button(ventana_agregar, text="Agregar Venta",
                            command=lambda: agregar_venta(vendedor_id, store, date_entry.get(),
                                                          weekly_sales_entry.get(),
                                                          holiday_flag_entry.get(), temperature_entry.get(),
                                                          fuel_price_entry.get(), cpi_entry.get(), ventana_agregar),
                            bg="#28A745", fg="white", font=("Roboto", 12, "bold"), width=15, height=2, relief="flat")
    agregar_btn.pack(pady=20)

    ventana_agregar.mainloop()


# Función para agregar la venta a través de la API
def agregar_venta(vendedor_id, store, date, weekly_sales, holiday_flag, temperature, fuel_price, cpi, ventana_agregar):
    try:
        url = f"{api_url}/agregar_venta"
        data = {
            'vendedor_id': vendedor_id,
            'Store': store,
            'Date': date,
            'Weekly_Sales': float(weekly_sales),
            'Holiday_Flag': int(holiday_flag),
            'Temperature': float(temperature),
            'Fuel_Price': float(fuel_price),
            'CPI': float(cpi)
        }
        response = requests.post(url, json=data)

        if response.status_code == 200:
            messagebox.showinfo("Éxito", "Venta agregada con éxito!")
            ventana_agregar.destroy()
        else:
            error_data = response.json()
            messagebox.showerror("Error", error_data.get("error", "No tienes permiso para agregar ventas."))
    except Exception as e:
        messagebox.showerror("Error", f"Error al conectarse a la API: {e}")


# Función para mostrar la tabla de ventas
def mostrar_tabla_ventas(data, ventana_actual):
    ventana_actual.destroy()
    ventana_tabla = tk.Tk()
    ventana_tabla.title("Ventas de la Sede")
    ventana_tabla.geometry("1000x600")
    ventana_tabla.configure(bg='#2C2C2C')

    etiqueta_ventas = tk.Label(ventana_tabla, text="Ventas de la Sede", font=("Roboto", 18, "bold"), bg="#2C2C2C",
                               fg="white")
    etiqueta_ventas.pack(pady=10)

    style = ttk.Style()
    style.configure("mystyle.Treeview", font=("Roboto", 12), rowheight=30, background="#333333", foreground="white",
                    fieldbackground="#333333")
    style.configure("mystyle.Treeview.Heading", font=("Roboto", 14, "bold"), background="#444444", foreground="black")

    tabla = ttk.Treeview(ventana_tabla, columns=(
        "Fecha", "Ventas Semanales", "Vendedor ID", "Temperatura", "Precio Combustible", "CPI", "Festivo"),
                         show="headings",
                         style="mystyle.Treeview")

    # Definir encabezados de la tabla
    tabla.heading("Fecha", text="Fecha")
    tabla.heading("Ventas Semanales", text="Ventas Semanales")
    tabla.heading("Vendedor ID", text="Vendedor ID")
    tabla.heading("Temperatura", text="Temperatura")
    tabla.heading("Precio Combustible", text="Precio Combustible")
    tabla.heading("CPI", text="CPI")
    tabla.heading("Festivo", text="Festivo (1=Sí)")

    tabla.pack(fill="both", expand=True, padx=20, pady=20)

    # Insertar datos en la tabla
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


# Función para exportar datos del usuario
def exportar_datos(vendedor_id):
    try:
        url = f"{api_url}/descargar_datos/{vendedor_id}"
        response = requests.get(url)

        if response.status_code == 200:
            # Obtiene el nombre del archivo de la respuesta
            file_path = f"{vendedor_id}_datos.csv"
            with open(file_path, 'wb') as file:
                file.write(response.content)

            messagebox.showinfo("Éxito", "Datos exportados exitosamente.")
            # Abrir el archivo o carpeta directamente
            webbrowser.open(file_path)
        else:
            error_data = response.json()
            messagebox.showerror("Error", error_data.get("error", "No se pudo exportar los datos."))
    except Exception as e:
        messagebox.showerror("Error", f"Error al conectarse a la API: {e}")

# Función para eliminar datos antiguos
def eliminar_datos_antiguos():
    respuesta = messagebox.askyesno("Confirmación", "¿Está seguro de que desea eliminar datos antiguos?")
    if respuesta:
        try:
            url = f"{api_url}/eliminar_datos_antiguos"
            response = requests.delete(url)
            if response.status_code == 200:
                messagebox.showinfo("Éxito", "Datos antiguos eliminados exitosamente.")
            else:
                messagebox.showerror("Error", "No se pudo eliminar datos antiguos.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al conectarse a la API: {e}")


# Ventana principal de autenticación
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

    # Botón para iniciar sesión
    login_btn = tk.Button(ventana, text="Autenticar",
                          command=lambda: autenticar_vendedor(vendedor_id_entry.get(), password_entry.get(), ventana),
                          bg="#28A745", fg="white", font=("Roboto", 12, "bold"), width=15, height=2, relief="flat")
    login_btn.pack(pady=20)

    ventana.mainloop()


# Iniciar la ventana de autenticación
ventana_autenticacion()

