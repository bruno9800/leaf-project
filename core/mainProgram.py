import numpy as np
import pandas as pd

from core.aux import map_ids_to_functions
from core.select_parents import select_parents
from core.crossover import crossover
from core.fitness import calculate_fitness_with_custom_penalty
from core.mutate import mutate
from core.population import create_initial_population

def genetic_algorithm(data, layout_dimensions, bench_size, num_pdsid_columns,
                      population_size=10, generations=50, mutation_rate=0.0, num_parents=2):
    """
    Executa o algoritmo genético para otimizar a disposição das plantas.
    
    Parâmetros:
      - data: DataFrame com os dados das plantas.
      - layout_dimensions: tupla com as dimensões do layout (ex: (9,20)).
      - bench_size: tupla com o tamanho de cada bench (ex: (4,2)).
      - num_pdsid_columns: número de colunas PDSID presentes no data.
      - population_size: tamanho da população.
      - generations: número de gerações a serem processadas.
      - mutation_rate: taxa de mutação.
      - num_parents: número de pais para seleção.
    
    Retorna:
      - best_solution: a melhor disposição (matriz) encontrada.
      - best_fitness: o fitness associado à melhor solução.
    """
    # Passo 1: Criar a população inicial a partir dos IDs das plantas
    plant_ids = data['Inventory BID'].tolist()
    population = create_initial_population(population_size, layout_dimensions, plant_ids)

    # Loop de gerações
    for generation in range(generations):
        print(f"Geração {generation+1}")
        # Calcula o fitness para cada cromossomo, usando o bench_size e número de PDSID
        fitness_values = [
            calculate_fitness_with_custom_penalty(matrix, data, bench_size, num_pdsid_columns)
            for matrix in population
        ]
        # Seleciona os pais com base no fitness
        parents = select_parents(population, fitness_values, num_parents=num_parents)
        # Cria a próxima geração
        next_population = []
        while len(next_population) < population_size:
            # Cruzamento dos pais para gerar dois filhos
            child1, child2 = crossover(parents[0], parents[1])
            # Aplica mutação nos filhos
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)
            next_population.extend([child1, child2])
        # Garante que a população tenha exatamente population_size cromossomos
        population = next_population[:population_size]

    # Calcula o fitness final da população
    final_fitness_values = [
        calculate_fitness_with_custom_penalty(matrix, data, bench_size, num_pdsid_columns)
        for matrix in population
    ]
    # Encontra o melhor cromossomo
    best_index = np.argmin(final_fitness_values)
    best_solution = population[best_index]
    best_fitness = final_fitness_values[best_index]

    print(f"Melhor solução encontrada com fitness {best_fitness}")
    return best_solution, best_fitness

# Teste local (caso queira rodar o módulo isoladamente)
if __name__ == "__main__":
    file_path = 'result-program.csv'
    data = pd.read_csv(file_path)
    layout_dimensions = (9, 20)
    bench_size = (4, 2)
    num_pdsid_columns = sum(col.startswith("PDSID") for col in data.columns)
    best_solution, best_fitness = genetic_algorithm(data, layout_dimensions, bench_size, num_pdsid_columns)
    function_matrix = map_ids_to_functions(best_solution, data)
    print("Function Matrix:")
    print(function_matrix)
