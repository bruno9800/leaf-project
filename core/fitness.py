from core.aux import find_receptor, get_plant_position
import pandas as pd;

def calculate_fitness_with_custom_penalty(matrix, data, bench_size=(4, 2), pdsid_columns=0):
    total_distance = 0

    def get_bench_position(position, bench_size):
        return (position[0] // bench_size[0], position[1] // bench_size[1])

    for _, row in data.iterrows():
        if row['Pollination Gender'] == 'M':
            donor_id = row['Inventory BID']
            donor_position = get_plant_position(matrix, donor_id)
            if donor_position:
                donor_bench = get_bench_position(donor_position, bench_size)
                for i in range(1, pdsid_columns):
                    relation_id = row.get(f'PDSID {i + 1}', None)  # Usar get() para evitar KeyError

                    if pd.notna(relation_id):
                        receptor_id = find_receptor(data, relation_id, donor_id)
                        if receptor_id:
                            receptor_position = get_plant_position(matrix, receptor_id)
                            if receptor_position:
                                receptor_bench = get_bench_position(receptor_position, bench_size)
                                distance = abs(donor_position[0] - receptor_position[0]) + abs(donor_position[1] - receptor_position[1])

                                # Verificar se o receptor também é um doador
                                receptor_role = data.loc[data['Inventory BID'] == receptor_id, 'Pollination Gender'].values[0]

                                if donor_bench != receptor_bench:
                                    if receptor_role == 'M':
                                        distance *= 1  # Penalidade menor se o receptor for também um doador
                                    else:
                                        distance *= 4  # Penalidade máxima para receptores fora da bancada do doador
                                else:
                                    if receptor_role == 'M':
                                        distance *= 2  # Penalidade média se o receptor for doador e estiver na bancada do doador
                                    else:
                                        distance *= 3  # Penalidade se for apenas receptor na bancada do doador

                                total_distance += distance

    return total_distance