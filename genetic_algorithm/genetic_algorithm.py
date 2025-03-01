from genetic_algorithm.population import Population


class GeneticAlgorithm:

    def __init__(
        self, num_of_genes: int, historical_data: list, population_size: int = 30
    ):
        self.historical_data = historical_data
        self.population = Population(num_of_genes, population_size)
