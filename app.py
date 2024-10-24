from flask import Flask, jsonify, request
import pandas as pd
import bcrypt

app = Flask(__name__)

try:
    vendedores_df = pd.read_csv('vendedores.csv')
    sales_df = pd.read_csv('sales_data.csv')
except FileNotFoundError as e:
    print(f"Error: {e}")
    vendedores_df = pd.DataFrame(columns=['Vendedor_ID', 'Nombre_Vendedor', 'Rol', 'Store', 'Password_Hash'])
    sales_df = pd.DataFrame(
        columns=['Store', 'Date', 'Weekly_Sales', 'Holiday_Flag', 'Temperature', 'Fuel_Price', 'CPI', 'Vendedor_ID'])


def autenticar_vendedor_con_contraseña(vendedor_id, password):
    try:
        vendedor = vendedores_df[vendedores_df['Vendedor_ID'] == vendedor_id]
        if vendedor.empty:
            return None

        vendedor_info = vendedor.iloc[0]
        stored_hash = vendedor_info['Password_Hash'].encode('utf-8')

        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            return vendedor_info
        else:
            return None
    except Exception as e:
        print(f"Error en la autenticación: {e}")
        return None


def autenticar_vendedor_1(vendedor_id):
    try:
        vendedor = vendedores_df[vendedores_df['Vendedor_ID'] == vendedor_id]
        if vendedor.empty:
            return None
        return vendedor.iloc[0]
    except Exception as e:
        print(f"Error en la autenticación: {e}")
        return None


def tiene_permiso(vendedor, store=None, accion="ver"):
    rol = vendedor['Rol']
    vendedor_store = vendedor['Store']

    print(f"Permiso solicitado: {accion}, Vendedor Rol: {rol}, Sede: {store}, Vendedor Sede: {vendedor_store}")

    if rol == "Administrador":
        return True

    if accion == "ver" and rol == "Supervisor" and vendedor_store == store:
        return True

    if accion == "agregar" and vendedor_store == store:
        return True

    return False


@app.route('/autenticar', methods=['POST'])
def autenticar_vendedor():
    try:
        data = request.json
        vendedor_id = int(data.get('vendedor_id'))
        password = data.get('password')

        vendedor = autenticar_vendedor_con_contraseña(vendedor_id, password)

        if vendedor is None:
            print("Autenticación fallida")
            return jsonify({"error": "Autenticación fallida"}), 403
        else:
            print(f"Autenticación exitosa para el vendedor {vendedor_id}")
            return jsonify({"message": "Autenticación exitosa", "vendedor": vendedor.to_dict()})
    except Exception as e:
        print(f"Error en la autenticación: {e}")
        return jsonify({"error": "Ocurrió un error en la autenticación"}), 500


@app.route('/ventas/<store>', methods=['GET'])
def obtener_ventas(store):
    try:
        vendedor_id = int(request.args.get('vendedor_id'))
        vendedor = autenticar_vendedor_1(vendedor_id)

        if vendedor is None:
            print("Autenticación fallida")
            return jsonify({"error": "Autenticación fallida"}), 403

        if tiene_permiso(vendedor, store, "ver"):
            ventas_store = sales_df[sales_df['Store'] == store]
            if not ventas_store.empty:
                ventas_json = ventas_store.to_dict(orient='records')
                return jsonify(ventas_json)
            else:
                print(f"No hay ventas para la sede: {store}")
                return jsonify({"error": f"No hay ventas para la sede: {store}"}), 404
        else:
            print("Permiso denegado para ver las ventas")
            return jsonify({"error": "No tienes permiso para ver las ventas de esta sede"}), 403
    except Exception as e:
        print(f"Error en la solicitud de ventas: {e}")
        return jsonify({"error": "Ocurrió un error en la solicitud de ventas"}), 500


if __name__ == '__main__':
    app.run(debug=True)
