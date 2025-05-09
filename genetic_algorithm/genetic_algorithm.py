from copy import deepcopy
from genetic_algorithm.crossover import Crossover
from genetic_algorithm.population import Population
from genetic_algorithm.selection import Selection


class GeneticAlgorithm:

    def __init__(
        self,
        profitability: list,
        population_size: int = 100,
        parent_pool_size: int = 30,
        plateau_generations: int = 20,
    ):
        # FIXME: Сделать возможность задачи размера родительского пула извне
        self.plateau_generations = plateau_generations
        self.population_size = population_size
        self.parent_pool_size = parent_pool_size
        self.population = Population(profitability)
        self.parent_pool = Population(profitability)
        self.population.generate_start_population(population_size)
        self.best_portfolio = None

        self.max_fits = []
        self.avg_fits = []

        self.current_iteration = 0
        self.is_plateau = False

    def run(self):
        has_increase = True
        while has_increase:
            self.run_iteration()

            if self.is_plateau:
                break

        print(
            "Итоговый лучший результат - ",
            max(self.max_fits),
            " Параметры портфеля - ",
            self.best_portfolio,
        )

    def run_iteration(self):
        print("Номер итерации - ", self.current_iteration)
        self.current_iteration += 1

        self.selection = Selection(self.population)

        self.parent_pool = deepcopy(
            self.selection.select_parent_pool(self.parent_pool_size)
        )

        print("Длина родительского пула - ", len(self.parent_pool.population_list))
        crossover = Crossover(self.parent_pool)
        self.population = deepcopy(crossover.conduct_crossover(self.population_size))
        print("Длина новой популяции - ", len(self.population.population_list))
        max_fit, avg_fit = self.get_max_and_average_fitness()
        print(
            "Максимальная приспособленность новой популяции -",
            max_fit,
            ", средняя приспособленность - ",
            avg_fit,
        )
        self.max_fits.append(max_fit)
        self.avg_fits.append(avg_fit)

        self.is_plateau = self.__check_plateau()

    def __check_plateau(self):
        current_max = self.avg_fits[-1]
        if len(self.avg_fits) < self.plateau_generations:
            return False

        history = self.avg_fits[-self.plateau_generations :]
        previous_max = max(history)

        return current_max <= previous_max

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
        if len(self.avg_fits) == 3:
            if (
                avg_fit - self.avg_fits[-1] <= 0.4
                and avg_fit - self.avg_fits[-2] <= 0.04
                and avg_fit - self.avg_fits[-3] <= 0.04
            ):
                return False
        return True
