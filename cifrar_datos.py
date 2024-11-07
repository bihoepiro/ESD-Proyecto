import pandas as pd
from cryptography.fernet import Fernet
import os

key_path = 'clave.key'
if not os.path.exists(key_path):
    key = Fernet.generate_key()
    with open(key_path, 'wb') as key_file:
        key_file.write(key)
    print("Clave generada y guardada en clave.key")
else:
    with open(key_path, 'rb') as key_file:
        key = key_file.read()

cipher_suite = Fernet(key)

vendedores_df = pd.read_csv('vendedores.csv')

def cifrar_dato(dato):
    return cipher_suite.encrypt(dato.encode()).decode()
def descifrar_dato(dato_cifrado):
    return cipher_suite.decrypt(dato_cifrado.encode()).decode()

vendedores_df['Telefono'] = vendedores_df['Telefono'].apply(cifrar_dato)

vendedores_df.to_csv('vendedores.csv', index=False)
print("Datos cifrados y guardados en vendedores.csv")
