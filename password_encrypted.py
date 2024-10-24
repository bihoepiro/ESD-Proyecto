import bcrypt
import pandas as pd

try:
    vendedores_df = pd.read_csv('vendedores.csv')
except FileNotFoundError as e:
    print(f"Error: {e}")
    vendedores_df = pd.DataFrame(columns=['Vendedor_ID', 'Nombre_Vendedor', 'Rol', 'Store'])

def asignar_contraseñas_a_vendedores(vendedores_df):
    if 'Password_Hash' not in vendedores_df.columns:
        vendedores_df['Password_Hash'] = ''

    for index, row in vendedores_df.iterrows():
        if not row['Password_Hash']:
            nueva_password = 'password' + str(row['Vendedor_ID'])
            hashed_password = bcrypt.hashpw(nueva_password.encode('utf-8'), bcrypt.gensalt())
            vendedores_df.at[index, 'Password_Hash'] = hashed_password.decode('utf-8')
            print(f"Asignada contraseña 'password{row['Vendedor_ID']}' al vendedor {row['Nombre_Vendedor']}")

    vendedores_df.to_csv('vendedores.csv', index=False)
    print("Contraseñas asignadas y guardadas en 'vendedores.csv'.")

asignar_contraseñas_a_vendedores(vendedores_df)
