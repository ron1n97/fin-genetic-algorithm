from genetic_algorithm.crossover import Crossover
from genetic_algorithm.population import Population
from genetic_algorithm.selection import Selection


class GeneticAlgorithm:

    def __init__(
        self, num_of_genes: int, profitability: list, population_size: int = 30
    ):
        # FIXME: Сделать возможность задачи размера родительского пула извне
        self.parent_pool_size = 10
        self.population_size = population_size
        self.population = Population(profitability)
        self.population.generate_start_population(population_size)
        self.best_portfolio = None

        self.max_fits = []
        self.avg_fits = []

    def run(self):
        has_increase = True
        while has_increase:
            self.selection = Selection(self.population)
            parent_pool = self.selection.select_parent_pool(self.parent_pool_size)
            print("Длина родительского пула - ", len(parent_pool.population_list))
            crossover = Crossover(parent_pool)
            self.population = crossover.conduct_crossover(self.population_size)
            max_fit, avg_fit = self.get_max_and_average_fitness()
            print(
                "Максимальная приспособленность новой популяции -",
                max_fit,
                " средняя приспособленность - ",
                avg_fit,
            )
            has_increase = self.estimate_increase(max_fit, avg_fit)
            self.max_fits.append(max_fit)
            self.avg_fits.append(avg_fit)
        print(
            "Итоговый лучший результат - ",
            self.max_fits[-1],
            " Параметры портфеля - ",
            self.best_portfolio,
        )

    def get_max_and_average_fitness(self):
        sum_fitness = 0
        max_fitness = 0
        for individual in self.population.population_list:
            sum_fitness += individual.fitness
            if max_fitness < individual.fitness:
                max_fitness = individual.fitness
                self.best_portfolio = individual.decoded_gene
        average_fitness = sum_fitness / len(self.population.population_list)
        return max_fitness, average_fitness

    def estimate_increase(self, max_fit, avg_fit):
        if self.max_fits:
            if abs(max_fit - self.max_fits[-1]) <= 0.1:
                return False
        return True
