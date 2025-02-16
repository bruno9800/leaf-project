import numpy as np;

def create_initial_population(population_size, layout_dimensions, plant_ids):
    """Cria a população inicial de cromossomos."""
    total_positions = layout_dimensions[0] * layout_dimensions[1]
    num_plants = len(plant_ids)
    num_empty_positions = total_positions - num_plants

    population = []

    for _ in range(population_size):
        # Preencher com plantas e espaços vazios
        individual = plant_ids + [0] * num_empty_positions
        np.random.shuffle(individual)

        # Converter a lista em uma matriz com as dimensões especificadas
        matrix = np.array(individual).reshape(layout_dimensions)
        population.append(matrix)

    return population

# Exemplo de uso:
# population_size = 3  # Define o tamanho da população inicial
# layout_dimensions = (9, 20)  # Dimensões da matriz
# plant_ids = data['Inventory BID'].tolist()  # IDs das plantas a partir do CSV
# initial_population = create_initial_population(population_size, layout_dimensions, plant_ids)
