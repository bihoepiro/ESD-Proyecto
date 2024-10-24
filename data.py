from faker import Faker
import pandas as pd
import random

fake = Faker()

stores = ['Lima Norte', 'Barranco', 'Miraflores', 'San Isidro', 'Surco', 'La Molina']
weeks = pd.date_range(start="2023-01-01", periods=52, freq='W')
holiday_flags = [0, 1]

vendedor_data = []
vendedor_id_counter = 1
supervisores = []

for store in stores:
    for i in range(3):
        nombre_vendedor = fake.name()
        vendedor = {
            'Vendedor_ID': vendedor_id_counter,
            'Nombre_Vendedor': nombre_vendedor,
            'Email': fake.email(),
            'Telefono': fake.phone_number(),
            'Store': store,
            'Rol': 'Supervisor' if i == 0 else 'Vendedor'
        }
        if i == 0:
            supervisores.append(vendedor_id_counter)
        vendedor_data.append(vendedor)
        vendedor_id_counter += 1

administrador = {
    'Vendedor_ID': vendedor_id_counter,
    'Nombre_Vendedor': fake.name(),
    'Email': fake.email(),
    'Telefono': fake.phone_number(),
    'Store': 'Admin',
    'Rol': 'Administrador'
}
vendedor_data.append(administrador)
administrador_id = vendedor_id_counter

vendedor_df = pd.DataFrame(vendedor_data)

sales_data = []

for store in stores:
    for week in weeks:
        vendedores_sede = vendedor_df[vendedor_df['Store'] == store]['Vendedor_ID'].tolist()
        vendedor_id = random.choice(vendedores_sede)

        sales_record = {
            'Store': store,
            'Date': week.date(),
            'Weekly_Sales': round(random.uniform(5000, 15000), 2),
            'Holiday_Flag': random.choice(holiday_flags),
            'Temperature': round(random.uniform(15, 30), 2),
            'Fuel_Price': round(random.uniform(3, 5), 2),
            'CPI': round(random.uniform(100, 120), 2),
            'Vendedor_ID': vendedor_id
        }
        sales_data.append(sales_record)

sales_df = pd.DataFrame(sales_data)

# Guardar Data
vendedor_df.to_csv('vendedores.csv', index=False)
sales_df.to_csv('sales_data.csv', index=False)