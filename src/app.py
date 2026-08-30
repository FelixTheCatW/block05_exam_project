import msvcrt
from functools import partial
from pathlib import Path

import pandas as pd
from IPython.display import display
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

import src.clean_data as clean
import src.excel_charts as chart
import src.load_data as load
from src import analysis
from src.utils.pipe import Pipe
from src.utils.report_writer import ReportWriter, write_table
from src.utils.step import step

console = Console()

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"
SRC_DATA = Path("d:\\Downloads\\mfp-diaries.tsv\\mfp-diaries.tsv")
PARQUET_PATH = DATA_DIR / "diaries.parquet"
WAIT_FOR_INPUT = True


def main() -> None:
    print("Добрый день.")

    print("Нажмите Enter или Space")
    key = msvcrt.getch()
    if key == b"\r":  # Enter
        WAIT_FOR_INPUT = True
    elif key == b" ":  # Space
        WAIT_FOR_INPUT = False

    if not PARQUET_PATH.exists():
        load.json_to_parquet(SRC_DATA, PARQUET_PATH)

    with step("Загрузка данных", wait=WAIT_FOR_INPUT):
        df = load.load_parquet_data(PARQUET_PATH)

    df_holder = Pipe(df)

    with step("Очистка данных", WAIT_FOR_INPUT):
        df_holder = (
            df_holder | clean.lower_columns | clean.drop_na | clean.filter_outliers
        )

    with step("Вычисляемые колонки", WAIT_FOR_INPUT):
        df_holder = df_holder | clean.add_computed_columns | clean.add_weekday

    df = df_holder.get()

    with step("Анализ", WAIT_FOR_INPUT):
        sample_200 = df.head(200)[["date", "calories", "carbs", "fat", "protein"]]
        stats = analysis.summary_stats(df)
        by_weekday = analysis.calories_by_weekday(df)
        by_category = analysis.macros_by_category(df)
        by_protein = analysis.protein_analysis(df)
        pivot_cat = analysis.pivot_weekday_category(df)
        pivot_protein = analysis.pivot_weekday_protein(df)
        corr = analysis.correlation_matrix(df)
        norm_cat = analysis.normalized_by_category(df)
        norm_weekday = analysis.normalized_by_weekday(df)

    print_table(stats, "Описательная статистика")
    print_table(by_weekday, "Калории по дням недели")
    print_table(by_category, "Макронутриенты по категориям")
    print_table(by_protein, "Анализ белка")
    print_table(norm_cat, "Доля калорий из макронутриентов по категориям")
    print_table(norm_weekday, "Доля калорий из макронутриентов по дням недели")

    with step("Экспорт в Excel с диаграммами", WAIT_FOR_INPUT):
        with ReportWriter(REPORTS_DIR / "report.xlsx") as rw:
            (
                rw.pipe
                | partial(write_table, stats, "Статистика")
                | chart.chart_calorie_distribution                
            )           
            chart.write_calorie_bins(stats, "Статистика", rw.writer)
            
            (
                rw.pipe
                | partial(write_table, by_weekday, "По дням недели")
                | chart.chart_by_weekday
            )

            (
                rw.pipe
                | partial(write_table, by_category, "По категориям")
                | chart.chart_by_category
                | chart.chart_category_pie
            )

            (
                rw.pipe
                | partial(write_table, norm_cat, "Нормализация категорий")
                | chart.chart_norm_cat
            )

            (
                rw.pipe
                | partial(write_table, norm_weekday, "Распред. по дням")
                | chart.chart_norm_weekday
            )

            (
                rw.pipe
                | partial(write_table, pivot_cat, "Сводная по категориям")
                | chart.chart_pivot_day_cat
            )

            (
                rw.pipe
                | partial(write_table, pivot_protein, "Белок")
                | chart.chart_pivot_day_protein
            )

            write_table(corr, "Корреляция", rw.writer)

            (
                rw.pipe
                | partial(write_table, sample_200, "Первые 200")
                | chart.chart_scatter_calories_protein
            )

    print("Готово ☻")


def print_table(df: pd.DataFrame, title: str):
    # console = Console()
    table = Table(title=title, show_header=True, header_style="magenta")

    table.add_column("Index", style="dim", width=6)
    for column in df.columns:
        table.add_column(column)

    for index, row in df.iterrows():
        row_values = [str(index)] + [str(item) for item in row]
        table.add_row(*row_values)

    console.print(table)


if __name__ == "__main__":
    main()
