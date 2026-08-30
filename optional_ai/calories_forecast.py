import os
from pathlib import Path
from IPython.display import display
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import src.clean_data as clean
from src.utils.step import step
from src.utils.pipe import Pipe

DATA_DIR = Path("data")
REPORTS_DIR = Path("reports")


def filter_outliers_iqr_all(df, cols, multiplier=1.5):
    """
    Фильтрация выбросов по методу межквартильного размаха (IQR).
    Удаляются строки, где значения выходят за пределы [lower, upper],
    где lower = max(Q1 - multiplier * IQR, 1), upper = min(Q3 + multiplier * IQR, 10000).
    """
    mask = pd.Series([True] * len(df))
    for col in cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        upper = min(q3 + multiplier * iqr, 10_000)  # физический предел
        lower = max(q1 - multiplier * iqr, 1)
        mask &= (df[col] >= lower) & (df[col] <= upper)
    return df[mask].reset_index(drop=True)


def main():
    # Проверяем наличие данных
    data_file = DATA_DIR / "diaries_ai.parquet"
    if not data_file.exists():
        print(f"Ошибка: файл {data_file} не найден.")
        return

    # Загрузка данных
    df = pd.read_parquet(data_file)
    # Размер таблицы.
    print("Размер таблицы:", df.shape)

    # Названия столбцов.
    print("\nНазвания столбцов:")
    print(df.columns.tolist())

    # Типы данных.
    print("\nТипы данных:")
    print(df.dtypes)

    # Проверка пропусков.
    print("\nПропуски по столбцам:")
    print(df.isna().sum())

    # Описательная статистика.
    print("\nОписательная статистика:")
    display(df.describe())
    # Список колонок для очистки
    cols_to_clean = [
        "goal_calories",
        "goal_carbs",
        "goal_fat",
        "goal_protein",
        "goal_sugar",
        "total_calories",
        "total_carbs",
        "total_fat",
        "total_protein",
        "total_sodium",
        "total_sugar",
    ]

    # Фильтрация выбросов

    # df_holder = Pipe(df)

    
    # df_holder = (
    #     df_holder | clean.lower_columns | clean.drop_na | clean.filter_outliers
    # )


    # df_holder = df_holder | clean.add_computed_columns | clean.add_weekday

    # df = df_holder.get()
    initial_len = len(df)
    df = filter_outliers_iqr_all(df, cols_to_clean, multiplier=1.5)
    removed = initial_len - len(df)
    print(f"Удалено строк: {removed} ({100 * removed / initial_len:.2f}%)")

    # Выбор целевой переменной и признаков
    target_column = "total_calories"
    feature_columns = ["total_carbs", "total_fat", "total_protein"]

    # Проверка наличия колонок
    missing = [
        col for col in feature_columns + [target_column] if col not in df.columns
    ]
    if missing:
        print(f"Ошибка: в данных отсутствуют колонки: {missing}")
        return

    model_df = df[feature_columns + [target_column]].copy()

    # Разделение на обучающую и тестовую выборки
    X = model_df[feature_columns]
    y = model_df[target_column]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Обучение модели линейной регрессии
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Предсказание на тестовой выборке
    y_pred = model.predict(X_test)

    # Метрики качества
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    # Вывод результатов
    print("\n=== Результаты модели ===")
    print(f"Целевая переменная: {target_column}")
    print(f"Признаки: {feature_columns}")
    print(f"Размер обучающей выборки: {len(X_train)}")
    print(f"Размер тестовой выборки: {len(X_test)}")
    print(f"MAE: {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"R²: {r2:.4f}")

    # Коэффициенты модели
    print("\nКоэффициенты модели:")
    for feat, coef in zip(feature_columns, model.coef_):
        print(f"  {feat}: {coef:.4f}")
    print(f"  intercept: {model.intercept_:.4f}")


if __name__ == "__main__":
    main()
