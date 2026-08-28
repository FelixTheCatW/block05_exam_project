from pathlib import Path

import pandas as pd

import src.excel_charts as excel


def export_to_excel(
    df: pd.DataFrame,
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
        stats.to_excel(writer, sheet_name="Статистика")
        bins_header_row = excel.write_calorie_bins(
            writer, "Статистика", df, stats.shape[0] + 3
        )

        by_weekday.to_excel(writer, sheet_name="Пweekday", index=False)
        by_category.to_excel(writer, sheet_name="Пcategory", index=False)
        norm_cat.to_excel(writer, sheet_name="Норм_cat", index=False)
        norm_weekday.to_excel(writer, sheet_name="Норм_weekday", index=False)
        pivot_cat.to_excel(writer, sheet_name="Pivot_day_cat")
        pivot_protein.to_excel(writer, sheet_name="Pivot_day_protein")
        corr.to_excel(writer, sheet_name="Корреляция")

        # Диаграммы на листах с данными
        excel.chart_by_weekday(writer.sheets["Пweekday"], by_weekday.shape[0])
        excel.chart_by_category(writer.sheets["Пcategory"], by_category.shape[0])
        excel.chart_category_pie(writer.sheets["Пcategory"], by_category.shape[0])
        excel.chart_norm_cat(writer.sheets["Норм_cat"], norm_cat.shape[0])
        excel.chart_norm_weekday(writer.sheets["Норм_weekday"], norm_weekday.shape[0])
        excel.chart_pivot_day_cat(writer.sheets["Pivot_day_cat"], pivot_cat.shape[0])
        excel.chart_pivot_day_protein(
            writer.sheets["Pivot_day_protein"], pivot_protein.shape[0]
        )
        excel.chart_calorie_distribution(
            writer.sheets["Статистика"], 6, bins_header_row
        )

        sample = df.head(200)
        sample.to_excel(writer, sheet_name="Данные (первые 200)", index=False)
        excel.chart_scatter_calories_protein(
            writer.sheets["Данные (первые 200)"], sample.shape[0]
        )

    print(f"Excel-отчёт с нативными диаграммами сохранён: {output_path}")
