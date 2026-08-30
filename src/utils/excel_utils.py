from functools import partial
from pathlib import Path

import pandas as pd

import src.excel_charts as chart
from src.utils.pipe import Pipe


def export_to_excel(
    df: pd.DataFrame,
    sample_200,
    stats: pd.DataFrame,
    by_weekday: pd.DataFrame,
    by_category: pd.DataFrame,
    pivot_cat: pd.DataFrame,
    pivot_protein: pd.DataFrame,
    corr: pd.DataFrame,
    norm_cat: pd.DataFrame,
    norm_weekday: pd.DataFrame,
    output_path: Path,
) -> None:
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        write_table(stats, "Статистика", writer)
        chart.chart_calorie_distribution(writer.sheets["Статистика"])
        chart.write_calorie_bins(writer, "Статистика", df)

        write_pipe = Pipe(writer)

        (
            write_pipe
            | partial(write_table, by_weekday, "По дням недели")
            | chart.chart_by_weekday
        )

        (
            write_pipe
            | partial(write_table, by_category, "По категориям")
            | chart.chart_by_category
            | chart.chart_category_pie
        )

        (
            write_pipe
            | partial(write_table, norm_cat, "Нормализация категорий")
            | chart.chart_norm_cat
        )

        (
            write_pipe
            | partial(write_table, norm_weekday, "Распред. по дням")
            | chart.chart_norm_weekday
        )

        (
            write_pipe
            | partial(write_table, pivot_cat, "Сводная по категориям")
            | chart.chart_pivot_day_cat
        )

        (
            write_pipe
            | partial(write_table, pivot_protein, "Белок")
            | chart.chart_pivot_day_protein
        )

        write_table(corr, "Корреляция", writer)
        
        (
            write_pipe
            | partial(write_table, sample_200, "Первые 200")
            | chart.chart_scatter_calories_protein
        )

    chart.style_scatter_chart(output_path)

    print(f"Отчёт с диаграммами сохранён:\n{output_path}")


import uuid

from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo


def write_table(df, sheet_name, writer):
    df.to_excel(writer, sheet_name=sheet_name, index=False)
    ws = writer.sheets[sheet_name]

    if df.empty:
        return ws

    max_row = df.shape[0] + 1
    max_col = df.shape[1]
    start_cell = "A1"
    end_cell = f"{get_column_letter(max_col)}{max_row}"
    table_range = f"{start_cell}:{end_cell}"

    safe_sheet_name = sheet_name.replace(" ", "_").replace("(", "").replace(")", "")
    table_name = f"Table_{safe_sheet_name}_{uuid.uuid4().hex[:6]}"

    try:
        table = Table(displayName=table_name, ref=table_range)
        style = TableStyleInfo(
            name="TableStyleMedium4",
            showFirstColumn=False,
            showLastColumn=False,
            showRowStripes=True,
            showColumnStripes=False,
        )
        table.tableStyleInfo = style
        ws.add_table(table)

    except Exception as e:
        print(f"Не удалось применить стиль к листу '{sheet_name}': {e}")

    return ws
