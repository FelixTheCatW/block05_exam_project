import pandas as pd
from openpyxl.chart import BarChart, PieChart, Reference, ScatterChart
from openpyxl.chart.axis import ChartLines
from openpyxl.chart.marker import Marker
from openpyxl.chart.series_factory import SeriesFactory
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import LineProperties
from openpyxl.worksheet.worksheet import Worksheet

WS_ANCHOR = "E11"


def _style(title: str, chart) -> None:
    chart.style = 13

    chart.title = title
    chart.title.overlay = False

    chart.legend.position = "b"  # 'b' - снизу, 'r' - справа, 't' - сверху, 'l' - слева
    chart.legend.overlay = False

    if chart.y_axis is not None and chart.y_axis.title is not None:
        chart.y_axis.title.overlay = False

    if chart.x_axis is not None and chart.x_axis.title is not None:
        chart.x_axis.title.overlay = False


def set_axis_title(axis, title: str, font_size: int = 1400) -> None:
    axis.title = title
    axis.title.overlay = False


def chart_by_weekday(ws: Worksheet) -> None:
    chart = BarChart()
    chart.type = "col"
    data = Reference(ws, min_col=2, max_col=3, min_row=1, max_row=8)
    cats = Reference(ws, min_col=6, min_row=2, max_row=8)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.y_axis.title = "Ккал"
    chart.x_axis.title = "День недели"

    _style("Средние и медианные калории по дням недели", chart)
    ws.add_chart(chart, WS_ANCHOR)


def chart_by_category(ws: Worksheet) -> None:
    chart = BarChart()
    chart.type = "col"
    data = Reference(ws, min_col=3, max_col=5, min_row=1, max_row=4)
    cats = Reference(ws, min_col=1, min_row=2, max_row=4)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.y_axis.title = "Граммы"
    chart.x_axis.title = "Категория"
    _style("Средние макронутриенты по категориям", chart)
    ws.add_chart(chart, WS_ANCHOR)
    return ws


def chart_category_pie(ws: Worksheet) -> None:
    pie = PieChart()
    # pie.title = "Доля записей по категориям калорийности"
    pie.style = 13

    pie.title = "Доля записей по категориям калорийности"
    pie.title.overlay = False

    pie.legend.position = "b"  # 'b' - снизу, 'r' - справа, 't' - сверху, 'l' - слева
    pie.legend.overlay = False

    data = Reference(ws, min_col=9, min_row=1, max_row=4)
    cats = Reference(ws, min_col=1, min_row=2, max_row=4)
    pie.add_data(data, titles_from_data=True)
    pie.set_categories(cats)
    pie.height = 8
    pie.width = 12
    ws.add_chart(pie, "N4")


def chart_norm_cat(ws: Worksheet) -> None:
    chart = BarChart()
    chart.type = "col"
    chart.grouping = "percentStacked"
    chart.overlap = 100
    data = Reference(ws, min_col=3, max_col=5, min_row=1, max_row=4)
    cats = Reference(ws, min_col=1, min_row=2, max_row=4)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.y_axis.title = "% калорий"
    _style("Доля калорий из макронутриентов по категориям", chart)
    ws.add_chart(chart, WS_ANCHOR)


def chart_norm_weekday(ws: Worksheet) -> None:
    chart = BarChart()
    chart.type = "col"
    chart.grouping = "percentStacked"
    chart.overlap = 100
    data = Reference(ws, min_col=3, max_col=5, min_row=1, max_row=8)
    cats = Reference(ws, min_col=7, min_row=2, max_row=8)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.y_axis.title = "% калорий"
    _style("Доля калорий из макронутриентов по дням недели", chart)
    ws.add_chart(chart, WS_ANCHOR)


def chart_pivot_day_cat(ws: Worksheet) -> None:
    chart = BarChart()
    chart.type = "col"
    data = Reference(ws, min_col=1, max_col=3, min_row=1, max_row=8)
    cats = Reference(ws, min_col=1, min_row=3, max_row=8)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.y_axis.title = "Средние ккал"
    _style("Средние калории: день недели x категория", chart)
    ws.add_chart(chart, WS_ANCHOR)


def chart_pivot_day_protein(ws: Worksheet) -> None:
    chart = BarChart()
    chart.type = "col"
    data = Reference(ws, min_col=2, max_col=3, min_row=1, max_row=8)
    cats = Reference(ws, min_col=1, min_row=2, max_row=8)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.y_axis.title = "Число записей"
    _style("Число записей: обычные vs высокий белок", chart)
    ws.add_chart(chart, WS_ANCHOR)


def chart_calorie_distribution(ws: Worksheet) -> None:
    header_row = 14
    data_first = header_row + 1
    data_last = header_row + 6
    chart = BarChart()
    chart.type = "col"
    data = Reference(ws, min_col=2, min_row=header_row, max_row=data_last)
    cats = Reference(ws, min_col=1, min_row=data_first, max_row=data_last)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.y_axis.title = "Записей"
    chart.x_axis.title = "Ккал"
    _style("Распределение записей по калорийности", chart)
    ws.add_chart(chart, WS_ANCHOR)
    return ws


def chart_scatter_calories_protein(ws: Worksheet) -> None:
    headers = {
        cell.value: cell.column
        for cell in ws[1]
        if cell.value in ("calories", "protein")
    }
    if not {"calories", "protein"} <= set(headers):
        return
    chart = ScatterChart()
    chart.title = "Калории x белок (первые 200 записей)"
    xvalues = Reference(ws, min_col=headers["calories"], min_row=2, max_row=201)
    yvalues = Reference(ws, min_col=headers["protein"], min_row=1, max_row=201)
    series = SeriesFactory(yvalues, xvalues=xvalues, title_from_data=True)
    series.marker = Marker(symbol="circle", size=3)

    series.spPr = GraphicalProperties(ln=LineProperties(noFill=True))
    chart.series.append(series)
    chart.x_axis.title = "Калории"
    chart.y_axis.title = "Белок, граммы"

    _style("Калории x белок (первые 200 записей)", chart)
    chart.legend = None
    ws.add_chart(chart, WS_ANCHOR)


def write_calorie_bins(
    df: pd.DataFrame, sheet_name: str, writer: pd.ExcelWriter
) -> None:
    labels = ["0-500", "500-1000", "1000-1500", "1500-2000", "2000-2500", "2500-3000"]
    cal_range = pd.cut(
        df["calories"],
        bins=[0, 500, 1000, 1500, 2000, 2500, 3000],
        labels=labels,
        right=False,
    )
    dist = cal_range.value_counts().reindex(labels).reset_index()
    dist.columns = ["calories_range", "count"]
    dist.to_excel(writer, sheet_name=sheet_name, startrow=13, index=False)
