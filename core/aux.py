import numpy as np;

# Função para obter a posição da planta na matriz
def get_plant_position(matrix, plant_id):
    """Retorna a posição (linha, coluna) de uma planta na matriz."""
    if plant_id:
        result = np.where(matrix == plant_id)
        if result[0].size > 0:
            return list(zip(result[0], result[1]))[0]
    return None


def find_receptor(data, relation_id, donor_id):
  related_row = data[data.isin([relation_id]).any(axis=1)]
  if not related_row.empty:
      related_row = related_row.iloc[0]
      related_plants = [related_row['Inventory BID'], donor_id]
      # Identificar o receptor (que é a planta diferente do donor_id)
      receptor_id = related_plants[0] if related_plants[1] == donor_id else related_plants[1]
      return receptor_id
  
def map_ids_to_functions(solution_matrix, data):
    """Substitui os IDs na matriz pela função correspondente (Doador ou Receptor)."""
    # Criar um dicionário mapeando IDs para suas funções
    id_to_function = dict(zip(data['Inventory BID'], data.index))

    # Criar uma nova matriz para armazenar as funções
    function_matrix = np.empty_like(solution_matrix, dtype=object)

    # Preencher a matriz de funções
    for i in range(solution_matrix.shape[0]):
        for j in range(solution_matrix.shape[1]):
            plant_id = solution_matrix[i, j]
            if plant_id in id_to_function:
                function_matrix[i, j] = id_to_function[plant_id]
            else:
                function_matrix[i, j] = "Vazio"  # Representar espaços vazios com "Vazio" ou "0"

    return function_matrix