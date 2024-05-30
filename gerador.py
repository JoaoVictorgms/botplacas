import random
import string
import pandas as pd
import threading

# Função para gerar uma placa do Mercosul
def gerar_placa():
    letras = random.choices(string.ascii_uppercase, k=3)
    numeros = random.choices(string.digits, k=4)
    placa = f"{letras[0]}{letras[1]}{letras[2]}{numeros[0]}{letras[1]}{numeros[1]}{numeros[2]}"
    return placa

# Função Map: Gera uma parte das placas
def map_placas(num_placas, resultado):
    placas = [gerar_placa() for _ in range(num_placas)]
    resultado.extend(placas)

# Função Reduce: Junta todas as partes das placas
def reduce_placas(partes):
    placas = []
    for parte in partes:
        placas.extend(parte)
    return placas

# Número de placas a serem geradas
num_placas = 1000

# Número de threads a serem usadas
num_threads = 10

# Número de placas por thread
placas_por_thread = num_placas // num_threads

# Lista para armazenar os resultados de cada thread
resultados = [[] for _ in range(num_threads)]
threads = []

# Criando e iniciando threads
for i in range(num_threads):
    thread = threading.Thread(target=map_placas, args=(placas_por_thread, resultados[i]))
    threads.append(thread)
    thread.start()

# Esperando todas as threads terminarem
for thread in threads:
    thread.join()

# Reduzindo os resultados
placas_geradas = reduce_placas(resultados)

# Criando DataFrame e salvando em Excel
df = pd.DataFrame(placas_geradas, columns=['Placa'])
df.to_excel('placas_mercosul.xlsx', index=False)

print("Placas geradas e salvas em placas_mercosul.xlsx")
