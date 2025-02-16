import numpy as np;

def select_parents(population, fitness_values, num_parents=2):
    """Seleciona os cromossomos mais aptos para reprodução."""
    # Converter os valores de fitness para probabilidades (quanto menor o fitness, maior a probabilidade)
    fitness_inverse = np.max(fitness_values) - fitness_values + 1
    selection_prob = fitness_inverse / np.sum(fitness_inverse)

    # Selecionar os pais com base nas probabilidades calculadas
    parents_indices = np.random.choice(len(population), size=num_parents, p=selection_prob, replace=False)
    parents = [population[i] for i in parents_indices]

    return parents

# Exemplo de uso:
# Considerando que `fitness_values` é a lista de valores de fitness dos cromossomos
# e `initial_population` é a lista de cromossomos

# selected_parents = select_parents(initial_population, fitness_values, num_parents=2)

# O resultado são os cromossomos selecionados como pais para a próxima geração
# print(selected_parents)