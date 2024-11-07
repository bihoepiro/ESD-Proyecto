import pandas as pd
import random
from hashlib import sha256

vendedores_df = pd.read_csv('vendedores.csv')
sales_df = pd.read_csv('sales_data.csv')

def seudonimizar_id(vendedor_id):
    return sha256(str(vendedor_id).encode()).hexdigest()[:10]

vendedores_df['Vendedor_ID_Anon'] = vendedores_df['Vendedor_ID'].apply(seudonimizar_id)
sales_df = sales_df.merge(vendedores_df[['Vendedor_ID', 'Vendedor_ID_Anon']], on='Vendedor_ID', how='left')
sales_df.drop(columns=['Vendedor_ID'], inplace=True)

def generalizar_fecha(fecha):
    fecha_obj = pd.to_datetime(fecha)
    return f"{fecha_obj.year}-{fecha_obj.month}"

sales_df['Date'] = sales_df['Date'].apply(generalizar_fecha)

def seudonimizar_email(email):
    hash_email = sha256(email.encode()).hexdigest()[:10]
    dominio = email.split('@')[-1]
    return f"{hash_email}@{dominio}"

vendedores_df['Email_Anon'] = vendedores_df['Email'].apply(seudonimizar_email)
vendedores_df.drop(columns=['Email'], inplace=True)
def agregar_ruido(ventas):
    ruido = random.uniform(-0.1, 0.1) * ventas
    return round(ventas + ruido, 2)

sales_df['Weekly_Sales'] = sales_df['Weekly_Sales'].apply(agregar_ruido)

vendedores_df.to_csv('vendedores_anon.csv', index=False)
sales_df.to_csv('sales_data_anon.csv', index=False)

print("Anonimización completada y guardada en 'vendedores_anon.csv' y 'sales_data_anon.csv'")
