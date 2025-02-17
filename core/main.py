import numpy as np
import pandas as pd

from core.aux import map_ids_to_functions
from core.display import create_notebook_with_matrix
from core.select_parents import select_parents
from core.crossover import crossover
from core.fitness import calculate_fitness_with_custom_penalty
from core.mutate import mutate
from core.population import create_initial_population
from core.fitness import calculate_fitness_with_custom_penalty
# Carregar o arquivo CSV
file_path = 'result.csv'
data = pd.read_csv(file_path)

df_doadores = data[data["Pollination Gender"] == "M"]

# Definir as dimensões da matriz do layout
layout_dimensions = (9, 20)  # Exemplo: 5 linhas por 20 colunas
total_positions = layout_dimensions[0] * layout_dimensions[1]

# Número total de plantas
num_plants = data.shape[0]

# Calcular o número de espaços vazios (0) que precisarão ser preenchidos na matriz
num_empty_positions = total_positions - num_plants

# Criar a lista de IDs das plantas
plant_ids = data['Inventory BID'].tolist()

# Preencher os espaços vazios com 0
initial_population = plant_ids + [0] * num_empty_positions

# Embaralhar a lista para gerar uma disposição inicial aleatória
np.random.shuffle(initial_population)

# Converter a lista em uma matriz com as dimensões especificadas
initial_matrix = np.array(initial_population).reshape(layout_dimensions)

num_pdsid_columns = sum(col.startswith("PDSID") for col in data.columns)



def genetic_algorithm(
    data,
    layout_dimensions,
    population_size=10,
    generations=50,
    mutation_rate=0.00,
    num_parents=2
):
    """Executa o algoritmo genético para otimizar a disposição das plantas."""

    # Passo 1: Criar a população inicial
    plant_ids = data['Inventory BID'].tolist()
    population = create_initial_population(population_size, layout_dimensions, plant_ids)

    # Loop de gerações
    for generation in range(generations):
        print(f"Geração {generation+1}")

        # Passo 2: Calcular o fitness de cada cromossomo na população
        fitness_values = [calculate_fitness_with_custom_penalty(matrix, data,(4, 2), num_pdsid_columns) for matrix in population]

        # Passo 3: Selecionar os pais com base no fitness
        parents = select_parents(population, fitness_values, num_parents=num_parents)

        # Criar a próxima geração de cromossomos
        next_population = []

        while len(next_population) < population_size:
            # Passo 4: Cruzar os pais para criar filhos
            child1, child2 = crossover(parents[0], parents[1])

            # Passo 5: Aplicar mutação nos filhos
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)

            # Adicionar os filhos à próxima geração
            next_population.extend([child1, child2])

        # Garantir que a população não exceda o tamanho desejado
        population = next_population[:population_size]

    # Calcular o fitness final da população
    final_fitness_values = [calculate_fitness_with_custom_penalty(matrix, data, (4, 2), pdsid_columns=num_pdsid_columns) for matrix in population]

    # Encontrar o melhor cromossomo da população final
    best_index = np.argmin(final_fitness_values)
    best_solution = population[best_index]
    best_fitness = final_fitness_values[best_index]

    print(f"Melhor solução encontrada com fitness {best_fitness}")
    return best_solution, best_fitness



if __name__ == "__main__":
    best_solution, best_fitness = genetic_algorithm(data, layout_dimensions)


    function_matrix = map_ids_to_functions(best_solution, data)
    # A melhor disposição de plantas encontrada será retornada em `best_solution`.
    print(function_matrix)
    root = create_notebook_with_matrix(function_matrix, df_doadores, data)
    root.mainloop()
