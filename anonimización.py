import pandas as pd
import random
from hashlib import sha256
import re

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

def anonimizar_email(email):
    return email[0] + "****@" + email.split('@')[-1]  # Solo mostrar el primer caracter y poner asteriscos

vendedores_df['Email_Anon'] = vendedores_df['Email'].apply(anonimizar_email)
vendedores_df.drop(columns=['Email'], inplace=True)

def anonimizar_telefono(telefono):
    return "****-****"

vendedores_df['Telefono_Anon'] = vendedores_df['Telefono'].apply(anonimizar_telefono)
vendedores_df.drop(columns=['Telefono'], inplace=True)

def anonimizar_direccion(direccion):
    direccion_parts = direccion.split(",")
    distrito = direccion_parts[-2].strip() if len(direccion_parts) > 1 else direccion
    distrito = re.sub(r'\d+', '', distrito).strip()
    return distrito

vendedores_df['Direccion_Anon'] = vendedores_df['Direccion'].apply(anonimizar_direccion)
vendedores_df.drop(columns=['Direccion'], inplace=True)

def agregar_ruido(ventas):
    ruido = random.uniform(-0.1, 0.1) * ventas  # Ruido entre -10% y +10%
    return round(ventas + ruido, 2)

sales_df['Weekly_Sales'] = sales_df['Weekly_Sales'].apply(agregar_ruido)

vendedores_df.to_csv('vendedores_anon.csv', index=False)
sales_df.to_csv('sales_data_anon.csv', index=False)

