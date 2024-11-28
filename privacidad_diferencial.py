import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sales_df = pd.read_csv('sales_data.csv')
ventas = sales_df['Weekly_Sales'].values

def laplace_noise(scale, size=1):
    return np.random.laplace(0, scale, size)

def apply_privacy_differential(data, epsilon):
    scale = 1 / epsilon
    return data + laplace_noise(scale, len(data))

# Valores de epsilon
epsilons = [0.1, 0.5, 1, 2, 5]
noisy_sales = []

for epsilon in epsilons:
    noisy_sales.append(apply_privacy_differential(ventas, epsilon))

plt.figure(figsize=(10, 6))
for i, epsilon in enumerate(epsilons):
    plt.plot(ventas, noisy_sales[i], 'o-', label=f'Epsilon = {epsilon}')

plt.title("Impacto de Epsilon en la Privacidad Diferencial")
plt.xlabel("Ventas Originales")
plt.ylabel("Ventas con Ruido (Privacidad Diferencial)")
plt.legend()
plt.grid(True)
plt.show()
