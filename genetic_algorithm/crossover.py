import random
from typing import List
from genetic_algorithm.population import Individual, Population


class Crossover:
    def __init__(self, population: Population, crossover_points_count: int = 1):
        self.population = population
        # TODO: использовать кол-во точек кроссовера для их создания
        self.crossover_point = len(self.population.population_list[0].coded_gene) // 2

    def conduct_crossover(self, population_size):
        # FIXME: Поддержать работу с популяциями из нечетного количества
        for _ in range(population_size // 2):
            offspring_1, offspring_2 = self._singe_point_crossover()
            self.population.population_list.append(offspring_1)
            if population_size == len(self.population.population_list):
                break
            self.population.population_list.append(offspring_2)
        return self.population

    def _singe_point_crossover(self):
        parent_1, parent_2 = random.sample(self.population.population_list, 2)

        offspring_1_coded_gene = (
            parent_1.coded_gene[: self.crossover_point]
            + parent_2.coded_gene[self.crossover_point :]
        )
        offspring_2_coded_gene = (
            parent_2.coded_gene[: self.crossover_point]
            + parent_1.coded_gene[self.crossover_point :]
        )
        normalized_offspring_1_coded_gene = self.__normalize_and_decode_gene(
            offspring_1_coded_gene
        )
        normalized_offspring_2_coded_gene = self.__normalize_and_decode_gene(
            offspring_2_coded_gene
        )

        profitability = self.population.profitability
        offspring_1 = Individual(normalized_offspring_1_coded_gene, profitability)
        offspring_2 = Individual(normalized_offspring_2_coded_gene, profitability)

        return offspring_1, offspring_2

    def __normalize_and_decode_gene(self, coded_gene: str):
        # FIXME: использвовать
        decoded_gene = self.__decode_gene(coded_gene)
        normalized_gene = self.__normalize_gene(decoded_gene)
        return normalized_gene

    @staticmethod
    def __decode_gene(coded_gene: str):
        length = len(coded_gene)
        part_size = length // 3
        return [
            int(coded_gene[:part_size], 2),
            int(coded_gene[part_size : 2 * part_size], 2),
            int(coded_gene[2 * part_size :], 2),
        ]

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
