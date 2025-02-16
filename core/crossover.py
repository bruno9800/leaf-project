import numpy as np;

def crossover(parent1, parent2):
    """Executa o crossover entre dois cromossomos (matrizes)."""
    # Converter os pais para vetores para facilitar a manipulação
    flat_parent1 = parent1.flatten()
    flat_parent2 = parent2.flatten()

    # Definir o ponto de corte
    crossover_point = np.random.randint(1, len(flat_parent1))

    # Criar os descendentes
    child1 = np.concatenate([flat_parent1[:crossover_point], flat_parent2[crossover_point:]])
    child2 = np.concatenate([flat_parent2[:crossover_point], flat_parent1[crossover_point:]])

    # Função para corrigir cromossomos e garantir que todos os genes sejam válidos
    def fix_individual(child, original_parent):
        fixed_child = []
        unique_elements = set()

        # Adiciona genes sem duplicatas
        for gene in child:
            if gene not in unique_elements:
                fixed_child.append(gene)
                unique_elements.add(gene)
            else:
                fixed_child.append(None)  # Colocar um placeholder para duplicatas

        # Substituir None por genes que faltam
        missing_genes = [gene for gene in original_parent if gene not in unique_elements]
        for i in range(len(fixed_child)):
            if fixed_child[i] is None:
                if missing_genes:
                    fixed_child[i] = missing_genes.pop(0)
                else:
                    fixed_child[i] = 0  # Substituir por 0 se não houver mais genes faltantes

        return np.array(fixed_child)

    # Corrigir os cromossomos resultantes
    child1 = fix_individual(child1, flat_parent1).reshape(parent1.shape)
    child2 = fix_individual(child2, flat_parent2).reshape(parent2.shape)

    return child1, child2
