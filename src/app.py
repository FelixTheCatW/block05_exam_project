from functools import partial
from pathlib import Path

from IPython.display import display
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

import src.clean_data as clean
import src.load_data as load
from src import analysis
from src.utils import excel_utils
from src.utils.pipe import Pipe
from src.utils.step import step

console = Console()

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"
SRC_DATA = Path("d:\\Downloads\\mfp-diaries.tsv\\mfp-diaries.tsv")
PARQUET_PATH = DATA_DIR / "diaries.parquet"
WAIT_FOR_INPUT = True


def main() -> None:
    print("Добрый день.")
    print("Ввод чтобы начать")
    input()

    if not PARQUET_PATH.exists():
        load.json_to_parquet(SRC_DATA, PARQUET_PATH)

    with step("1. Загрузка данных", wait=WAIT_FOR_INPUT):
        df = load.load_parquet_data(PARQUET_PATH)

    df_holder = Pipe(df)

    with step("2. Очистка данных", WAIT_FOR_INPUT):
        df_holder = df_holder | clean.lower_columns | clean.drop_na | clean.filter_outliers

    with step("3. Вычисляемые колонки", WAIT_FOR_INPUT):
        df_holder = df_holder | clean.add_computed_columns | clean.add_weekday

    df = df_holder.get()

    with step("4. Анализ", True):
        stats = analysis.summary_stats(df)
        by_weekday = analysis.calories_by_weekday(df)
        by_category = analysis.macros_by_category(df)
        by_protein = analysis.protein_analysis(df)
        pivot_cat = analysis.pivot_weekday_category(df)
        pivot_prot = analysis.pivot_weekday_protein(df)
        corr = analysis.correlation_matrix(df)
        norm_cat = analysis.normalized_by_category(df)
        norm_weekday = analysis.normalized_by_weekday(df)

    print_table(stats, "Описательная статистика")
    print_table(by_weekday, "Калории по дням недели")
    print_table(by_category, "Макронутриенты по категориям")
    print_table(by_protein, "Анализ белка")
    print_table(norm_cat, "Нормализация на 1000 ккал по категориям")
    print_table(norm_weekday, "Нормализация на 1000 ккал по дням недели")

    with step("5. Сохранение CSV-отчётов", True):
        REPORTS_DIR.mkdir(exist_ok=True)
        by_weekday.to_csv(REPORTS_DIR / "calories_by_weekday.csv", index=False)
        by_category.to_csv(REPORTS_DIR / "macros_by_category.csv", index=False)
        by_protein.to_csv(REPORTS_DIR / "protein_analysis.csv", index=False)
        pivot_cat.to_csv(REPORTS_DIR / "pivot_weekday_category.csv")
        pivot_prot.to_csv(REPORTS_DIR / "pivot_weekday_protein.csv")
        corr.to_csv(REPORTS_DIR / "correlation_matrix.csv")
        stats.to_csv(REPORTS_DIR / "summary_stats.csv")
        norm_cat.to_csv(REPORTS_DIR / "normalized_by_category.csv", index=False)
        norm_weekday.to_csv(REPORTS_DIR / "normalized_by_weekday.csv", index=False)

    with step("6. Экспорт в Excel с диаграммами", True):
        excel_utils.export_to_excel(
            df,
            stats,
            by_weekday,
            by_category,
            pivot_cat,
            pivot_prot,
            corr,
            norm_cat,
            norm_weekday,
            REPORTS_DIR / "analysis_report.xlsx",
        )

    print("Готово! Все отчёты в папке", REPORTS_DIR)


import pandas as pd


def print_table(df: pd.DataFrame, title: str):
    # console = Console()
    table = Table(title=title, show_header=True, header_style="bold magenta")

    table.add_column("Index", style="dim", width=6)
    for column in df.columns:
        table.add_column(column)

    for index, row in df.iterrows():
        row_values = [str(index)] + [str(item) for item in row]
        table.add_row(*row_values)

    console.print(table)


if __name__ == "__main__":
    main()
