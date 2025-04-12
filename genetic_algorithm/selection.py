from random import random
from genetic_algorithm.population import Population


class Selection:
    """
    Реализация селекции методом рулетки
    """

    def __init__(self, population: Population):
        self.population = population

    def form_probabilities(self):
        total_fitness = self.form_total_fitness()
        roulette_point = 0
        for individual in self.population.population_list:
            roulette_point += individual.fitness / total_fitness
            individual.roulette_point = roulette_point

    def select_parent_pool(self, parent_pool_size: int) -> Population:
        parent_pool = Population(self.population.profitability)

        self.form_probabilities()
        for _ in range(parent_pool_size):
            r = random()

            for individual in self.population.population_list:
                if r <= individual.roulette_point:
                    parent_pool.population_list.append(individual)
                    break

        return parent_pool

    def form_total_fitness(self):
        return sum(individual.fitness for individual in self.population.population_list)
