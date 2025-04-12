from genetic_algorithm.population import Population
from genetic_algorithm.selection import Selection


class GeneticAlgorithm:

    def __init__(
        self, num_of_genes: int, profitability: list, population_size: int = 30
    ):
        # FIXME: Сделать возможность задачи размера родительского пула извне
        self.parent_pool_size = 10
        self.population = Population(profitability)
        self.population.generate_start_population(population_size)
        self.selection = Selection(self.population)
        parent_pool = self.selection.select_parent_pool(self.parent_pool_size)
        print("Длина родительского пула - ", len(parent_pool.population_list))
        for individual in parent_pool.population_list:
            print(
                "Выбран индивидум - ", individual, " Его профит - ", individual.fitness
            )
