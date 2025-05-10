import ast
import pandas as pd
import plotly.express as px
import streamlit as st
from genetic_algorithm.genetic_algorithm import GeneticAlgorithm


def init_session_state():
    if "ga" not in st.session_state:
        st.session_state.ga = None
    if "auto_mode" not in st.session_state:
        st.session_state.auto_mode = False


def main():
    init_session_state()
    st.title("Генетический алгоритм")

    if st.session_state.ga and st.session_state.ga.is_plateau:
        st.header(
            "Алгоритм достиг плато. Лучший найденный портфель - "
            + str(st.session_state.ga.best_portfolio),
        )

    st.header(
        "Итерация № "
        + str(
            st.session_state.ga.current_iteration if st.session_state.ga else 0,
        )
    )

    show_sidebar = True
    if show_sidebar:
        with st.sidebar:
            st.header("Начальные настройки")
            st.header("Доходности облигаций (%)")
            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                e1 = st.number_input(
                    "Доходность 1",
                    min_value=0,
                    max_value=100,
                    step=1,
                    value=15,
                )

            with col2:
                e2 = st.number_input(
                    "Доходность 2",
                    min_value=0,
                    max_value=100,
                    step=1,
                    value=10,
                )

            with col3:
                e3 = st.number_input(
                    "Доходность 3",
                    min_value=0,
                    max_value=100,
                    step=1,
                    value=25,
                )

            st.header("Параметры популяции")
            population_size = st.number_input("Размер популяции", 50, 1000, 100)
            parent_pool_ratio = st.number_input(
                "Доля родительского пула",
                min_value=0.0,
                max_value=1.0,
                value=0.25,
                step=1.0,
            )
            plateau_generations = st.number_input(
                "Порог стагнации",
                step=1,
                value=12,
            )

            if not st.session_state.ga or st.session_state.ga.is_plateau:

                st.session_state.auto_mode = st.checkbox("Автоматический режим")
                if st.button("Инициализировать"):
                    profit = [e1, e2, e3]
                    parent_pool_size = round(population_size * parent_pool_ratio)
                    st.session_state.ga = GeneticAlgorithm(
                        profitability=profit,
                        population_size=population_size,
                        parent_pool_size=parent_pool_size,
                        plateau_generations=plateau_generations,
                    )
                    show_sidebar = False

                    if st.session_state.auto_mode:
                        st.session_state.ga.run()
                    st.rerun()

    col1, col2 = st.columns(2)
    if (
        not st.session_state.auto_mode
        and st.session_state.ga
        and not st.session_state.ga.is_plateau
    ):
        with col1:
            if st.button("Следующее поколение"):
                st.session_state.ga.run_iteration()

    if st.session_state.ga:
        render_population()
        render_stats()
        render_parent_pool()


def render_population():
    st.subheader("Текущая популяция")
    ga = st.session_state.ga

    df = pd.DataFrame(
        [
            {
                "ID": idx,
                "Гены": str(ind.decoded_gene),
                "Хромосома": ind.coded_gene,
                "Фитнес": ind.fitness,
            }
            for idx, ind in enumerate(ga.population.population_list)
        ]
    )

    if "original_population_df" not in st.session_state:
        st.session_state.original_population_df = df.copy()

    edited_df = st.data_editor(
        df,
        key="population_table",
        disabled=["ID", "Фитнес"],
        column_config={
            "Гены": {"help": "Редактируйте гены (например, [1, 2, 3])"},
            "Хромосома": {"help": "Редактируйте строку хромосомы"},
        },
    )

    if not edited_df.equals(st.session_state.original_population_df):
        try:
            for idx in edited_df.index:
                edited_row = edited_df.iloc[idx]
                original_row = st.session_state.original_population_df.iloc[idx]
                individual = ga.population.population_list[idx]

                genes_changed = edited_row["Гены"] != original_row["Гены"]
                chromo_changed = edited_row["Хромосома"] != original_row["Хромосома"]

                if genes_changed and chromo_changed:
                    st.error(
                        f"Особь {idx}: Изменены оба поля. Редактируйте только одно."
                    )
                    continue

                if genes_changed:
                    new_genes = ast.literal_eval(edited_row["Гены"])
                    print(sum(new_genes))
                    if sum(new_genes) != 100:
                        raise Exception("Ген не нормализован")
                    else:
                        individual.decoded_gene = new_genes
                        individual.coded_gene = individual.code_genes(new_genes)
                        individual.fitness = individual.calculate_fitness()

                elif chromo_changed:
                    individual.coded_gene = edited_row["Хромосома"]
                    individual.decoded_gene = individual.decode_genes(
                        individual.coded_gene
                    )
                    individual.fitness = individual.calculate_fitness()

            st.session_state.original_population_df = edited_df.copy()
            st.rerun()
        except Exception as e:
            st.error(f"Ошибка обработки: {str(e)}")


def render_stats():
    max_fits = st.session_state.ga.max_fits
    avg_fits = st.session_state.ga.avg_fits
    if max_fits:
        st.subheader("Динамика приспособленности")
        fig = px.line(
            pd.DataFrame({"max_fitness": max_fits, "avg_fitness": avg_fits}),
            x=range(len(max_fits)),
            y=["max_fitness", "avg_fitness"],
            labels={
                "value": "Приспособленность",
                "variable": "Тип",
                "index": "Поколение",
            },
            title="Изменение приспособленности по поколениям",
        )
        st.plotly_chart(fig)


def render_parent_pool():
    if len(st.session_state.ga.parent_pool.population_list) > 0:
        st.subheader("Родительский пул")
        df = pd.DataFrame(
            [
                {
                    "ID": idx,
                    "Гены": ind.decoded_gene,
                    "Хромосома": ind.coded_gene,
                    "Фитнес": ind.fitness,
                }
                for idx, ind in enumerate(
                    st.session_state.ga.parent_pool.population_list
                )
            ]
        )
        st.dataframe(df)


if __name__ == "__main__":
    main()
