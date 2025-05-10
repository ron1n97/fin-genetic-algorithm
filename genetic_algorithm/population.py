from random import randint
from typing import List


class Individual:
    def __init__(self, genes: list, profitability: list):
        self.decoded_gene = genes
        self.profitability = profitability
        self.coded_gene: str = self.code_genes(genes)
        self.fitness = self.calculate_fitness()
        self.roulette_point: int

    def code_genes(self, genes: list):
        return "".join(f"{bin(g)[2:]:0>7}" for g in genes)

    def decode_genes(self, coded_gene: str) -> list:
        if len(coded_gene) % 7 != 0:
            raise ValueError("Некорректная хромосома: длина должна быть кратна 7")
        genes = [int(coded_gene[i : i + 7], 2) for i in range(0, len(coded_gene), 7)]
        # Нормализуем ген
        normalized_gene = self.__normalize_gene(genes)
        self.coded_gene = self.code_genes(normalized_gene)
        return normalized_gene

    def calculate_fitness(self):
        fitness = 0
        for gene, profit in zip(self.decoded_gene, self.profitability):
            fitness += gene * profit
        return fitness / 100

    @staticmethod
    def __normalize_gene(genes: List[int]):
        gene_sum_value = sum(genes)
        normalized_genes = []
        # перебираем до предпоследнего
        for i in range(len(genes) - 1):
            gene = round(genes[i] / gene_sum_value * 100)
            normalized_genes.append(gene)
        # Явно задаем последний ген,
        # чтобы суммарное значение было 100%
        normalized_genes.append(100 - sum(normalized_genes))
        return normalized_genes


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
