from flask import Flask, jsonify, request, session, send_file
import pandas as pd
import bcrypt
import random
import logging
from datetime import timedelta
from flask_session import Session
from tkinter import messagebox, ttk

# Configuración de Flask y Flask-Session
app = Flask(__name__)
app.secret_key = 'secreto_seguro_y_largo_para_la_sesion'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
Session(app)


logging.basicConfig(filename='auditoria.log', level=logging.INFO, format='%(asctime)s - %(message)s')


try:
    vendedores_df = pd.read_csv('vendedores.csv')
    sales_df = pd.read_csv('sales_data.csv')
except FileNotFoundError as e:
    print(f"Error: {e}")
    vendedores_df = pd.DataFrame(columns=['Vendedor_ID', 'Nombre_Vendedor', 'Rol', 'Store', 'Password_Hash'])
    sales_df = pd.DataFrame(columns=['Store', 'Date', 'Weekly_Sales', 'Holiday_Flag', 'Temperature', 'Fuel_Price', 'CPI', 'Vendedor_ID'])

# Consentimiento y política de privacidad
def mostrar_consentimiento():
    consentimiento_texto = ("Al iniciar sesión, usted consiente que sus datos serán utilizados "
                            "exclusivamente para gestionar acceso y reportes de ventas. Puede "
                            "restringir ciertos datos en el apartado de configuración.")
    respuesta = messagebox.askyesno("Consentimiento de Privacidad", consentimiento_texto)
    if not respuesta:
        exit()

# Llamar a mostrar_consentimiento() al iniciar la aplicación
mostrar_consentimiento()

# Seguridad de Datos y Protección (Hashing y Cifrado)
def hashear_contraseña(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Función para enviar código de verificación (simulación)
def enviar_codigo_verificacion(vendedor_id):
    codigo = random.randint(100000, 999999)
    session['codigo_2fa'] = codigo
    print(f"Código de verificación para 2FA (almacenado en sesión): {codigo}")
    return codigo

# Autenticación con Contraseña y 2FA
def autenticar_vendedor_con_contraseña(vendedor_id, password):
    vendedor = vendedores_df[vendedores_df['Vendedor_ID'] == vendedor_id]
    if vendedor.empty:
        return None

    vendedor_info = vendedor.iloc[0]
    stored_hash = vendedor_info['Password_Hash'].encode('utf-8')

    if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
        enviar_codigo_verificacion(vendedor_id)
        return vendedor_info
    else:
        return None

# Endpoint para verificar el código 2FA
@app.route('/verificar_2fa', methods=['POST'])
def verificar_2fa():
    data = request.json
    codigo_usuario = int(data.get('codigo'))
    codigo_sesion = session.get('codigo_2fa')

    if codigo_usuario :
        session.pop('codigo_2fa', None)
        return jsonify({"message": "Autenticación completa con 2FA"})
    else:
        return jsonify({"error": "Código de verificación incorrecto"}), 403

# Endpoint para autenticación inicial con contraseña
@app.route('/autenticar', methods=['POST'])
def autenticar_vendedor():
    data = request.json
    vendedor_id = int(data.get('vendedor_id'))
    password = data.get('password')

    vendedor = autenticar_vendedor_con_contraseña(vendedor_id, password)
    if vendedor is None:
        return jsonify({"error": "Autenticación fallida"}), 403
    return jsonify({"message": "Código de verificación enviado para 2FA"})

# Endpoint para ver y editar datos personales
@app.route('/perfil/<vendedor_id>', methods=['GET', 'PUT'])
def perfil_vendedor(vendedor_id):
    if request.method == 'GET':
        vendedor = vendedores_df[vendedores_df['Vendedor_ID'] == int(vendedor_id)]
        if not vendedor.empty:
            return jsonify(vendedor.iloc[0].to_dict())
        else:
            return jsonify({"error": "Vendedor no encontrado"}), 404
    elif request.method == 'PUT':
        data = request.json
        vendedor = vendedores_df[vendedores_df['Vendedor_ID'] == int(vendedor_id)]
        if not vendedor.empty:
            for key in data:
                if key in vendedores_df.columns:
                    vendedores_df.at[vendedor.index[0], key] = data[key]
            vendedores_df.to_csv('vendedores.csv', index=False)
            return jsonify({"message": "Datos actualizados con éxito"})
        else:
            return jsonify({"error": "Vendedor no encontrado"}), 404

# Endpoint para obtener ventas con logs de auditoría
@app.route('/ventas/<store>', methods=['GET'])
def obtener_ventas(store):
    vendedor_id = int(request.args.get('vendedor_id'))
    vendedor = vendedores_df[vendedores_df['Vendedor_ID'] == vendedor_id].iloc[0]

    if (vendedor['Rol'] == 'Supervisor' and vendedor['Store'] == store) or (vendedor['Rol'] == 'Administrador'):
        ventas_store = sales_df[sales_df['Store'] == store]
        logging.info(f"Acceso a ventas: Vendedor {vendedor_id} solicitó ver ventas de {store}")

        if not ventas_store.empty:
            ventas_json = ventas_store.to_dict(orient='records')
            return jsonify(ventas_json)
        else:
            return jsonify({"error": f"No hay ventas para la sede: {store}"}), 404
    else:
        return jsonify({"error": "No tienes permiso para ver las ventas de esta sede"}), 403

# Endpoint para agregar ventas con logs de auditoría
@app.route('/agregar_venta', methods=['POST'])
def agregar_venta():
    data = request.json
    vendedor_id = int(data.get('vendedor_id'))
    store = data.get('Store')

    vendedor = vendedores_df[vendedores_df['Vendedor_ID'] == vendedor_id].iloc[0]
    if vendedor['Store'] == store or vendedor['Rol'] == "Administrador":
        nueva_venta = {
            'Store': store,
            'Date': data['Date'],
            'Weekly_Sales': data['Weekly_Sales'],
            'Holiday_Flag': data['Holiday_Flag'],
            'Temperature': data['Temperature'],
            'Fuel_Price': data['Fuel_Price'],
            'CPI': data['CPI'],
            'Vendedor_ID': vendedor_id
        }
        global sales_df
        sales_df = sales_df._append(nueva_venta, ignore_index=True)
        sales_df.to_csv('sales_data.csv', index=False)
        logging.info(f"Venta agregada: Vendedor {vendedor_id} agregó una venta para la sede {store}")
        return jsonify({"message": "Venta agregada con éxito!"})
    else:
        return jsonify({"error": "No tienes permiso para agregar ventas en esta sede"}), 403

# Políticas de Privacidad y términos
def mostrar_politica_privacidad():
    politica = ("Política de privacidad: \n"
                "1. Solo usamos sus datos para gestionar acceso y ventas.\n"
                "2. Puede eliminar o restringir sus datos en cualquier momento.\n"
                "3. Nos comprometemos a proteger sus datos en todo momento.")
    messagebox.showinfo("Política de Privacidad", politica)

# Función para eliminar cuenta
@app.route('/eliminar_cuenta/<vendedor_id>', methods=['DELETE'])
def eliminar_cuenta(vendedor_id):
    index = vendedores_df[vendedores_df['Vendedor_ID'] == int(vendedor_id)].index
    if not index.empty:
        vendedores_df.drop(index, inplace=True)
        vendedores_df.to_csv('vendedores.csv', index=False)
        return jsonify({"message": "Cuenta eliminada y datos borrados exitosamente"})
    return jsonify({"error": "Vendedor no encontrado"}), 404


@app.route('/configurar_restriccion', methods=['POST'])
def configurar_restriccion():
    data = request.json
    vendedor_id = int(data.get('vendedor_id'))
    restricciones = data.get('restricciones')  # lista de datos a restringir

    # Actualizar restricciones en vendedores_df
    global vendedores_df
    vendedor_idx = vendedores_df[vendedores_df['Vendedor_ID'] == vendedor_id].index
    if len(restricciones) <= 2:
        vendedores_df.at[vendedor_idx[0], 'Restricciones'] = ",".join(restricciones)
        vendedores_df.to_csv('vendedores.csv', index=False)  # Guardar cambios
        return jsonify({"message": "Restricciones actualizadas exitosamente"})
    else:
        return jsonify({"error": "Máximo de 2 restricciones permitido"}), 400

@app.route('/descargar_datos/<vendedor_id>', methods=['GET'])
def descargar_datos(vendedor_id):
    datos_vendedor = sales_df[sales_df['Vendedor_ID'] == int(vendedor_id)]
    if not datos_vendedor.empty:
        file_path = f"{vendedor_id}_datos.csv"
        datos_vendedor.to_csv(file_path, index=False)

        # Enviar el archivo para su descarga
        return send_file(file_path, as_attachment=True)
    return jsonify({"error": "No se encontraron datos para exportar"}), 404

# Ejecutar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)
