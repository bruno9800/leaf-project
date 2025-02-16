import numpy as np;

def mutate(cromossomo, mutation_rate=0.01):
    """Realiza a mutação em um cromossomo com uma dada taxa de mutação."""
    # Copiar o cromossomo para evitar mutação direta
    mutated_cromossomo = cromossomo.copy()

    # Iterar sobre cada elemento da matriz
    for i in range(mutated_cromossomo.shape[0]):
        for j in range(mutated_cromossomo.shape[1]):
            if np.random.rand() < mutation_rate:
                # Selecionar uma posição aleatória na matriz para trocar
                swap_i = np.random.randint(0, mutated_cromossomo.shape[0])
                swap_j = np.random.randint(0, mutated_cromossomo.shape[1])

                # Realizar a troca dos valores
                mutated_cromossomo[i, j], mutated_cromossomo[swap_i, swap_j] = (
                    mutated_cromossomo[swap_i, swap_j],
                    mutated_cromossomo[i, j],
                )

    return mutated_cromossomo

# Exemplo de uso:
# mutation_rate = 0.05  # Taxa de mutação de 5%
# mutated_child1 = mutate(child1, mutation_rate)
# mutated_child2 = mutate(child2, mutation_rate)