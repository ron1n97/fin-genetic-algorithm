from random import random
from genetic_algorithm.population import Population


class Selection:
    """
    Реализация селекции методом рулетки
    """

    def __init__(self, population: Population):
        self.population = population

    def form_probabilities(self):
        roulette_point = 0
        for individual in self.population.population_list:
            roulette_point += individual.fitness
            individual.roulette_point = roulette_point

    def select_parent_pool(self, parent_pool_size: int) -> Population:
        parent_pool = Population(self.population.profitability)
        if not self.population.population_list:
            return parent_pool

        self.form_probabilities()
        total_fitness = self.population.population_list[-1].roulette_point

        for _ in range(parent_pool_size):
            r = (
                random() * total_fitness
            )  # Случайное вещественное число [0, total_fitness)
            for individual in self.population.population_list:
                if r <= individual.roulette_point:
                    parent_pool.population_list.append(individual)
                    break

        return parent_pool
