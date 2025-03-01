from random import randint
from typing import List


class Individual:
    def __init__(self, genes: list):
        self.decoded_gene = genes
        self.encoded_gene: str = self.encode_genes(genes)

    def encode_genes(self, genes: list):
        # TODO: Надо уйти от семерки и как-то поэлегантнее написать
        return "".join(f"{bin(g)[2:]:0>7}" for g in genes)


class Population(List[Individual]):
    def __init__(self, num_of_genes: int, population_size: int):
        super().__init__()
        self.num_of_genes = num_of_genes
        self.population_size = population_size
        self.individuals = self.generate_start_population(population_size)

    def generate_start_population(self, population_size: int):
        population = []
        for _ in range(population_size):
            genes = self.generate_genes()
            individual = Individual(genes)
            population.append(individual)
        return population

    def generate_random_gene(self, max_value: int):
        return randint(0, max_value)

    def generate_genes(self):
        genes = []
        max_value = 100
        for _ in range(self.num_of_genes):
            new_gene = self.generate_random_gene(max_value)
            genes.append(new_gene)
            max_value -= new_gene
        return genes
