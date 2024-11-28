import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sales_df = pd.read_csv('sales_data.csv')
vendedores_df = pd.read_csv('vendedores.csv')

merged_df = pd.merge(sales_df, vendedores_df, on='Vendedor_ID', how='inner')

plt.figure(figsize=(10, 6))
sns.boxplot(data=sales_df, x='Store', y='Weekly_Sales', palette='Set2')
plt.title("Distribución de Ventas por Ubicación de Tienda")
plt.xlabel("Ubicación de la Tienda")
plt.ylabel("Ventas Semanales")
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
sns.boxplot(data=merged_df, x='Rol', y='Weekly_Sales', palette='Set3')
plt.title("Distribución de Ventas por Rol (Supervisor vs Vendedor)")
plt.xlabel("Rol del Vendedor")
plt.ylabel("Ventas Semanales")
plt.grid(True)
plt.show()

vendedores_df['Fecha_Nacimiento'] = pd.to_datetime(vendedores_df['Fecha_Nacimiento'])

today = pd.to_datetime('today')
vendedores_df['Edad'] = (today - vendedores_df['Fecha_Nacimiento']).dt.days // 365

plt.figure(figsize=(10, 6))
sns.scatterplot(data=merged_df, x='Edad', y='Weekly_Sales')
plt.title("Ventas Semanales por Edad del Vendedor")
plt.xlabel("Edad del Vendedor")
plt.ylabel("Ventas Semanales")
plt.legend(title='Tienda', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.show()
