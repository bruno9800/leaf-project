import pandas as pd

# Caminho do arquivo CSV
file_path = "maranaSet.csv"  # Substitua pelo caminho correto

# Ler o arquivo CSV
df = pd.read_csv(file_path)

# Selecionar apenas as colunas desejadas
selected_columns = ["Inventory BID", "Pollination Gender", "PDSID"]
df_selected = df[selected_columns].copy()

# Dividir os valores da coluna 'PDSID' em novas colunas
pdsid_expanded = df_selected["PDSID"].str.split(",", expand=True)

# Renomear as novas colunas PDSID 1, PDSID 2, ...
pdsid_expanded.columns = [f"PDSID {i+1}" for i in range(pdsid_expanded.shape[1])]

# Concatenar com as colunas iniciais
df_final = pd.concat([df_selected.drop(columns=["PDSID"]), pdsid_expanded], axis=1)

# Salvar o resultado em um novo arquivo CSV
df_final.to_csv("result.csv", index=False)

print("Arquivo 'result.csv' salvo com sucesso!")
