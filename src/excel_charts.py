import pandas as pd
from openpyxl.chart import BarChart, PieChart, Reference, ScatterChart
from openpyxl.worksheet.worksheet import Worksheet


def _style(title: str, chart) -> None:
    chart.title = title
    chart.style = 10


def chart_by_weekday(ws: Worksheet, n: int, anchor: str = "H2") -> None:
    chart = BarChart()
    chart.type = "col"
    _style("Средние и медианные калории по дням недели", chart)
    data = Reference(ws, min_col=2, max_col=3, min_row=1, max_row=n + 1)
    cats = Reference(ws, min_col=6, min_row=2, max_row=n + 1)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.y_axis.title = "Ккал"
    chart.x_axis.title = "День недели"
    ws.add_chart(chart, anchor)


def chart_by_category(ws: Worksheet, n: int, anchor: str = "G2") -> None:
    chart = BarChart()
    chart.type = "col"
    _style("Средние макронутриенты по категориям", chart)
    data = Reference(ws, min_col=3, max_col=5, min_row=1, max_row=n + 1)
    cats = Reference(ws, min_col=1, min_row=2, max_row=n + 1)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.y_axis.title = "Граммы"
    chart.x_axis.title = "Категория"
    ws.add_chart(chart, anchor)


def chart_category_pie(ws: Worksheet, n: int, anchor: str = "G20") -> None:
    pie = PieChart()
    pie.title = "Доля записей по категориям калорийности"
    pie.style = 10
    data = Reference(ws, min_col=9, min_row=1, max_row=n + 1)
    cats = Reference(ws, min_col=1, min_row=2, max_row=n + 1)
    pie.add_data(data, titles_from_data=True)
    pie.set_categories(cats)
    pie.height = 8
    pie.width = 12
    ws.add_chart(pie, anchor)


def chart_norm_cat(ws: Worksheet, n: int, anchor: str = "G2") -> None:
    chart = BarChart()
    chart.type = "col"
    chart.grouping = "percentStacked"
    chart.overlap = 100
    _style("Состав рациона на 1000 ккал по категориям", chart)
    data = Reference(ws, min_col=2, max_col=4, min_row=1, max_row=n + 1)
    cats = Reference(ws, min_col=1, min_row=2, max_row=n + 1)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.y_axis.title = "% по граммам/1000 ккал"
    ws.add_chart(chart, anchor)


def chart_norm_weekday(ws: Worksheet, n: int, anchor: str = "H2") -> None:
    chart = BarChart()
    chart.type = "col"
    chart.grouping = "percentStacked"
    chart.overlap = 100
    _style("Состав рациона на 1000 ккал по дням недели", chart)
    data = Reference(ws, min_col=2, max_col=4, min_row=1, max_row=n + 1)
    cats = Reference(ws, min_col=6, min_row=2, max_row=n + 1)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.y_axis.title = "% по граммам/1000 ккал"
    ws.add_chart(chart, anchor)


def chart_pivot_day_cat(ws: Worksheet, n: int, anchor: str = "E2") -> None:
    chart = BarChart()
    chart.type = "col"
    _style("Средние калории: день недели × категория", chart)
    data = Reference(ws, min_col=2, max_col=4, min_row=1, max_row=n + 1)
    cats = Reference(ws, min_col=1, min_row=2, max_row=n + 1)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.y_axis.title = "Средние ккал"
    ws.add_chart(chart, anchor)


def chart_pivot_day_protein(ws: Worksheet, n: int, anchor: str = "G2") -> None:
    chart = BarChart()
    chart.type = "col"
    _style("Число записей: обычные vs высокий белок", chart)
    data = Reference(ws, min_col=2, max_col=3, min_row=1, max_row=n + 1)
    cats = Reference(ws, min_col=1, min_row=2, max_row=n + 1)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.y_axis.title = "Число записей"
    ws.add_chart(chart, anchor)


def chart_calorie_distribution(
    ws: Worksheet, n: int, header_row: int, anchor: str = "M2"
) -> None:
    data_first = header_row + 1
    data_last = header_row + n
    chart = BarChart()
    chart.type = "col"
    _style("Распределение записей по калорийности", chart)
    data = Reference(ws, min_col=2, min_row=header_row, max_row=data_last)
    cats = Reference(ws, min_col=1, min_row=data_first, max_row=data_last)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.y_axis.title = "Записей"
    chart.x_axis.title = "Ккал"
    ws.add_chart(chart, anchor)


def chart_scatter_calories_protein(ws: Worksheet, n: int, anchor: str = "U2") -> None:
    chart = ScatterChart()
    chart.title = "Калории × белок (первые 200 записей)"
    chart.style = 10
    xvalues = Reference(ws, min_col=4, min_row=2, max_row=n + 1)
    yvalues = Reference(ws, min_col=7, min_row=1, max_row=n + 1)
    chart.add_data(yvalues, titles_from_data=True)
    chart.series[0].xvalues = xvalues
    chart.x_axis.title = "Калории"
    chart.y_axis.title = "Белок, граммы"
    chart.legend = None
    ws.add_chart(chart, anchor)


def write_calorie_bins(
    writer: pd.ExcelWriter,
    sheet_name: str,
    df: pd.DataFrame,
    start_row: int,
) -> int:
    labels = ["0-500", "500-1000", "1000-1500", "1500-2000", "2000-2500", "2500-3000"]
    cal_range = pd.cut(
        df["calories"],
        bins=[0, 500, 1000, 1500, 2000, 2500, 3000],
        labels=labels,
        right=False,
    )
    dist = cal_range.value_counts().reindex(labels).reset_index()
    dist.columns = ["calories_range", "count"]
    dist.to_excel(writer, sheet_name=sheet_name, startrow=start_row, index=False)
    return start_row + 1