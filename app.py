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
        st.header("Алгоритм достиг плато")

    st.header(
        "Итерация № "
        + str(
            st.session_state.ga.current_iteration if st.session_state.ga else 0,
        )
    )

    # Секция параметров
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

    # Управление выполнением
    col1, col2 = st.columns(2)
    if (
        not st.session_state.auto_mode
        and st.session_state.ga
        and not st.session_state.ga.is_plateau
    ):
        with col1:
            if st.button("Следующее поколение"):
                st.session_state.ga.run_iteration()

    # Визуализация
    if st.session_state.ga:
        render_population()
        render_stats()
        render_parent_pool()


def render_population():
    st.subheader("Текущая популяция")
    ga = st.session_state.ga
    df = pd.DataFrame(
        [
            {"ID": idx, "Гены": ind.decoded_gene, "Фитнес": ind.fitness}
            for idx, ind in enumerate(ga.population.population_list)
        ]
    )
    st.dataframe(df)


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
                {"ID": idx, "Гены": ind.decoded_gene, "Фитнес": ind.fitness}
                for idx, ind in enumerate(
                    st.session_state.ga.parent_pool.population_list
                )
            ]
        )
        st.dataframe(df)


if __name__ == "__main__":
    main()
