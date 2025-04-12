from random import randint
from typing import List


class Individual:
    def __init__(self, genes: list, profitability: list):
        self.decoded_gene = genes
        self.coded_gene: str = self.code_genes(genes)
        self.fitness = self.fitness(profitability)
        self.roulette_point: int

    def code_genes(self, genes: list):
        # TODO: Надо уйти от семерки и как-то поэлегантнее написать
        return "".join(f"{bin(g)[2:]:0>7}" for g in genes)

    def fitness(self, profitability):
        fitness = 0
        for gene, profit in zip(self.decoded_gene, profitability):
            fitness += gene * profit
        return fitness


class Population(List[Individual]):
    def __init__(self, profitability: list):
        super().__init__()
        self.num_of_genes = len(profitability)
        self.profitability = profitability
        self.population_list = []

    def generate_start_population(self, population_size: int):
        for _ in range(population_size):
            genes = self.generate_genes()
            individual = Individual(genes, self.profitability)
            self.population_list.append(individual)

    def generate_random_gene(self, max_value: int):
        return randint(0, max_value)

    def generate_genes(self):
        genes = []
        max_value = 100
        for _ in range(self.num_of_genes - 1):
            new_gene = self.generate_random_gene(max_value)
            genes.append(new_gene)
            max_value -= new_gene
        # Последний ген не случайный, поскольку в сумме должно быть 100%
        genes.append(max_value)
        return genes
