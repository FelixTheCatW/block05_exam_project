from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo


# def test_table_style():
#     wb = Workbook()
#     ws = wb.active

#     # 1. Add sample data
#     data = [
#         ["Apples", 1000, 2000],
#         ["Oranges", 1500, 3000],
#         ["Bananas", 2000, 4000],
#     ]
#     ws.append(["Product", "Quarter 1", "Quarter 2"])
#     for row in data:
#         ws.append(row)

#     # 2. Define the table boundaries
#     tab = Table(displayName="SalesTable", ref="A1:C4")

#     # 3. Apply the table style using style_name
#     style = TableStyleInfo(
#         name="TableStyleMedium9",  # <-- Specify style name here
#         showFirstColumn=False,
#         showLastColumn=False,
#         showRowStripes=True,
#         showColumnStripes=False,
#     )

#     # 4. Add the style to the table, and the table to the worksheet
#     tab.tableStyleInfo = style
#     ws.add_table(tab)

#     wb.save("reports/table_example.xlsx")


from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference


def test_chart_style():

    wb = Workbook()
    ws = wb.active
    ws.append(["Category", "Values"])
    ws.append(["A", 10])
    ws.append(["B", 20])

    chart = BarChart()
    chart.style = 6  # Apply predefined style number 10
    data = Reference(ws, min_col=2, min_row=1, max_row=3)
    cats = Reference(ws, min_col=1, min_row=2, max_row=3)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    ws.add_chart(chart, "D1")
    wb.export = wb.save("reports/styled_chart.xlsx")
