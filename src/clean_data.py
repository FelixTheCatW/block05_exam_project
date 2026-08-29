import numpy as np
import pandas as pd


def filter_outliers(
    df: pd.DataFrame, cols: [str] = ['calories'], multiplier=1.5
) -> pd.DataFrame:
    """
    Удаляет выбросы.

    Для каждой колонки из `cols` вычисляются нижняя и верхняя границы на основе
    межквартильного размаха (IQR) с возможным масштабированием. Остаются только строки,
    в которых все указанные столбцы попадают в интервал.
    Границы дополнительно ограничиваются глобальными
    константами (нижняя граница ≥ 1, верхняя ≤ 15 000) для предотвращения
    экстремальных и ошибочных значений.

    Возвращает:
        Очищенную копию, индекс сброшен.
    """
    initial_len = len(df)
    mask = pd.Series([True] * initial_len)
    for col in cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        upper = min(q3 + multiplier * iqr, 15_000)
        lower = max(q1 - multiplier * iqr, 1)
        mask &= (df[col] >= lower) & (df[col] <= upper)

    cleaned = df[mask].reset_index(drop=True)
    print(
        f"Удалено строк: {initial_len - len(cleaned)} ({100 * (initial_len - len(cleaned)) / initial_len:.2f}%)"
    )
    return cleaned


def drop_na(df: pd.DataFrame) -> pd.DataFrame:
    """
    Удаляет строки с пропусками и дубликатами.
    Возвращает:
        Очищенную копию.
    """
    initial_len = len(df)
    cleaned = df.dropna(subset=["calories"]).drop_duplicates().reset_index(drop=True)
    print(
        f"Удалено ошибочных строк: {initial_len - len(cleaned)} ({100 * (initial_len - len(cleaned)) / initial_len:.2f}%)"
    )
    return cleaned


def lower_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [col.lower() for col in df.columns]
    return df


<<<<<<< HEAD
def add_weekday(df: pd.DataFrame) -> pd.DataFrame:
    df["weekday"] = df["date"].dt.weekday
    return df


def add_computed_columns(df: pd.DataFrame) -> pd.DataFrame:
=======
def add_weekday(df: pd.DataFrame) -> None:
    df["weekday"] = df["date"].dt.weekday


def add_computed_columns(df: pd.DataFrame) -> None:
>>>>>>> origin/main
    """
    Добавляет вычисляемые колонки на основе fat, carbs, protein, calories.
    Изменяет DataFrame на месте.
    """
    print("Добавил расчетные колонки - колонки процент от общей калорийности")
    df["pct_cal_fat"] = (df["fat"] * 9) / df["calories"] * 100
    df["pct_cal_carbs"] = (df["carbs"] * 4) / df["calories"] * 100
    df["pct_cal_protein"] = (df["protein"] * 4) / df["calories"] * 100

    
<<<<<<< HEAD
    print("Добавил расчетные колонки - граммы на 1000 ккал")
=======
    print("Добавил рпасчетные колонки - граммы на 1000 ккал")
>>>>>>> origin/main
    df["fat_per_1k"] = df["fat"] / (df["calories"] / 1000)
    df["carbs_per_1k"] = df["carbs"] / (df["calories"] / 1000)
    df["protein_per_1k"] = df["protein"] / (df["calories"] / 1000)

    print("Добавил расчетные колонки - соотношение макронутриентов")
    df["fat_to_carbs"] = df["fat"] / df["carbs"].replace(0, np.nan)
    df["protein_to_fat"] = df["protein"] / df["fat"].replace(0, np.nan)
    df["carbs_to_protein"] = df["carbs"] / df["protein"].replace(0, np.nan)
    
    def cal_category(val):
        if pd.isna(val):
            return np.nan
        if val < 1200:
            return "low"
        elif val <= 2000:
            return "medium"
        else:
            return "high"

    print("Добавил расчетную колонку - категория калорийности")
    df["cal_category"] = df["calories"].apply(cal_category)

    print("Добавил расчетную колонку - флаг высокого белка (>30% от калорий)")
    df["high_protein"] = df["pct_cal_protein"] > 30
<<<<<<< HEAD
    
    return df

=======
>>>>>>> origin/main
