import uuid
from functools import partial
from pathlib import Path

import pandas as pd
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

import src.excel_charts as chart
from src.utils.pipe import Pipe


class ReportWriter:
    """
    Контекстный менеджер для построения Excel-отчёта с диаграммами.
    Внутри блока with доступен атрибут `.pipe`, через который строятся цепочки
    вида: (rw.pipe | partial(write_table, ...) | chart.chart_...).
    При выходе из контекста файл сохраняется, применяется финальный стиль
    и печатается сообщение.
    """

    def __init__(self, output_path: Path):
        self.output_path = output_path
        self.writer = None
        self.pipe = None

    def __enter__(self):
        self.writer = pd.ExcelWriter(self.output_path, engine="openpyxl")
        self.pipe = Pipe(self.writer)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Закрываем ExcelWriter (сохраняет файл)
        if self.writer:
            self.writer.close()

        # Финальные действия, как в оригинальной функции
        chart.style_scatter_chart(self.output_path)
        print(f"Отчёт с диаграммами сохранён:\n{self.output_path}")

        # Подавляем исключения, если они возникли – пусть всплывают
        return False


# Вспомогательная функция write_table вынесена отдельно (как в исходнике)
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


# ===== Пример использования =====
# Вместо функции export_to_excel теперь можно писать:
#
# with ReportWriter(output_path) as rw:
#     # Первый лист – статистика (без pipe)
#     write_table(stats, "Статистика", rw.writer)
#     chart.chart_calorie_distribution(rw.writer.sheets["Статистика"])
#     chart.write_calorie_bins(rw.writer, "Статистика", df)
#
#     # Остальные листы через pipe
#     (rw.pipe
#      | partial(write_table, by_weekday, "По дням недели")
#      | chart.chart_by_weekday)
#
#     (rw.pipe
#      | partial(write_table, by_category, "По категориям")
#      | chart.chart_by_category
#      | chart.chart_category_pie)
#
#     (rw.pipe
#      | partial(write_table, norm_cat, "Нормализация категорий")
#      | chart.chart_norm_cat)
#
#     (rw.pipe
#      | partial(write_table, norm_weekday, "Распред. по дням")
#      | chart.chart_norm_weekday)
#
#     (rw.pipe
#      | partial(write_table, pivot_cat, "Сводная по категориям")
#      | chart.chart_pivot_day_cat)
#
#     (rw.pipe
#      | partial(write_table, pivot_protein, "Белок")
#      | chart.chart_pivot_day_protein)
#
#     write_table(corr, "Корреляция", rw.writer)
#
#     (rw.pipe
#      | partial(write_table, sample_200, "Первые 200")
#      | chart.chart_scatter_calories_protein)
