import numpy as np
import pandas as pd

WEEKDAY_NAMES = {
    0: "Пн",
    1: "Вт",
    2: "Ср",
    3: "Чт",
    4: "Пт",
    5: "Сб",
    6: "Вс",
}


def calories_by_weekday(df: pd.DataFrame) -> pd.DataFrame:
    result = (
        df.groupby("weekday", as_index=False)
        .agg(
            mean_calories=("calories", "mean"),
            median_calories=("calories", "median"),
            std_calories=("calories", "std"),
            count=("calories", "count"),
        )
        .sort_values("weekday")
    )
    result["weekday_name"] = result["weekday"].map(WEEKDAY_NAMES)
    return result


def macros_by_category(df: pd.DataFrame) -> pd.DataFrame:
    result = (
        df.groupby("cal_category", as_index=False)
        .agg(
            mean_calories=("calories", "mean"),
            mean_fat=("fat", "mean"),
            mean_carbs=("carbs", "mean"),
            mean_protein=("protein", "mean"),
            mean_pct_fat=("pct_cal_fat", "mean"),
            mean_pct_carbs=("pct_cal_carbs", "mean"),
            mean_pct_protein=("pct_cal_protein", "mean"),
            count=("calories", "count"),
        )
        .sort_values("mean_calories")
    )
    return result


def protein_analysis(df: pd.DataFrame) -> pd.DataFrame:
    result = df.groupby("high_protein", as_index=False).agg(
        mean_calories=("calories", "mean"),
        mean_fat=("fat", "mean"),
        mean_carbs=("carbs", "mean"),
        mean_protein=("protein", "mean"),
        mean_pct_protein=("pct_cal_protein", "mean"),
        count=("calories", "count"),
    )
    result["high_protein"] = result["high_protein"].map(
        {True: "Высокий белок (>30%)", False: "Обычный"}
    )
    return result


def pivot_weekday_category(df: pd.DataFrame) -> pd.DataFrame:
    pivot = pd.pivot_table(
        df,
        index="weekday",
        columns="cal_category",
        values="calories",
        aggfunc="mean",
        fill_value=0,
    )
    pivot.index = pivot.index.map(WEEKDAY_NAMES)
    return pivot


def pivot_weekday_protein(df: pd.DataFrame) -> pd.DataFrame:
    count_pivot = pd.pivot_table(
        df,
        index="weekday",
        columns="high_protein",
        values="calories",
        aggfunc="count",
        fill_value=0,
    )
    mean_pivot = pd.pivot_table(
        df,
        index="weekday",
        columns="high_protein",
        values="calories",
        aggfunc="mean",
        fill_value=0,
    )
    count_pivot.index = count_pivot.index.map(WEEKDAY_NAMES)
    mean_pivot.index = mean_pivot.index.map(WEEKDAY_NAMES)
    count_pivot.columns = [f"count_{c}" for c in count_pivot.columns]
    mean_pivot.columns = [f"mean_cal_{c}" for c in mean_pivot.columns]
    return pd.concat([count_pivot, mean_pivot], axis=1)


def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    cols = ["calories", "fat", "carbs", "protein"]
    return df[cols].corr()


def summary_stats(df: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "calories",
        "fat",
        "carbs",
        "protein",
        "pct_cal_fat",
        "pct_cal_carbs",
        "pct_cal_protein",
        "fat_per_1k",
        "carbs_per_1k",
        "protein_per_1k",
    ]
    return df[cols].describe().round(2)


def normalized_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Средний состав рациона по категориям калорийности:
    доля калорий (%) из жиров/углеводов/белков + средняя калорийность.
    Параметры суммируются в понятную картину "из чего состоят калории".
    """
    result = (
        df.groupby("cal_category", as_index=False)
        .agg(
            mean_calories=("calories", "mean"),
            pct_fat=("pct_cal_fat", "mean"),
            pct_carbs=("pct_cal_carbs", "mean"),
            pct_protein=("pct_cal_protein", "mean"),
            count=("calories", "count"),
        )
        .sort_values("mean_calories")
    )
    return _format_composition(result)


def _format_composition(result: pd.DataFrame) -> pd.DataFrame:
    result["mean_calories"] = result["mean_calories"].round(1)
    for col in ["pct_fat", "pct_carbs", "pct_protein"]:
        result[col] = result[col].round(1)
    result["count"] = result["count"].astype(int)
    return result

def normalized_groued_by_category(df: pd.DataFrame) -> pd.DataFrame:
    
    for col in ["fat_per_1k", "carbs_per_1k", "protein_per_1k"]:
        df[f"{col}_norm"] = df.groupby("cal_category")[col].transform(
            lambda x: (x - x.mean()) / x.std() if x.std() != 0 else 0
        )
        
    result = (
        df.groupby('cal_category', as_index=False)
        .agg(
            mean_fat_per_1k=("fat_per_1k", "mean"),
            mean_carbs_per_1k=("carbs_per_1k", "mean"),
            mean_protein_per_1k=("protein_per_1k", "mean"),
            count=("calories", "count"),)
        .rename(columns={
            'fat_per_1k': 'mean_fat_per_1k',
            'carbs_per_1k': 'mean_carbs_per_1k',
            'protein_per_1k': 'mean_protein_per_1k',
            'fat_per_1k_norm': 'mean_fat_norm',
            'carbs_per_1k_norm': 'mean_carbs_norm',
            'protein_per_1k_norm': 'mean_protein_norm',
            'calories': 'count'
        })
        .sort_values('mean_fat_per_1k'))
    
    return result

def normalized_by_weekday(df: pd.DataFrame) -> pd.DataFrame:
    """
    Средний состав рациона по дням недели:
    доля калорий (%) из жиров/углеводов/белков + средняя калорийность.
    """
    result = (
        df.groupby("weekday", as_index=False)
        .agg(
            mean_calories=("calories", "mean"),
            pct_fat=("pct_cal_fat", "mean"),
            pct_carbs=("pct_cal_carbs", "mean"),
            pct_protein=("pct_cal_protein", "mean"),
            count=("calories", "count"),
        )
        .sort_values("weekday")
    )
    result["weekday_name"] = result["weekday"].map(WEEKDAY_NAMES)
    return _format_composition(result)
