from genetic_algorithm.genetic_algorithm import GeneticAlgorithm
from utils.exchange import fetch_moex_data_by_ticker_list


tickers = ["SBER", "GAZP", "TBNK"]


if __name__ == "__main__":
    # moex_data = fetch_moex_data_by_ticker_list(tickers)
    # print("Исторические данные биржи", moex_data)
    moex_data = [0.3, 0.2, 0.6]
    num_of_genes = len(tickers)
    generic_algorithm = GeneticAlgorithm(num_of_genes, moex_data)
    print("Стартовая популяция:\n")
    print(generic_algorithm.population.population_list)
