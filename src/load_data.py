from pathlib import Path

import pandas as pd
from IPython import display

DATA_DIR = Path("../data")
DATA_DIR.mkdir(exist_ok=True)

REPORTS_DIR = Path("../reports")
REPORTS_DIR.mkdir(exist_ok=True)

assert DATA_DIR.exists()
assert REPORTS_DIR.exists()

print("Окружение готово.")


def load_parquet_data(path: str | Path) -> pd.DataFrame:
    """
    Загружает данные из parquet-файла.
    path — путь к файлу.
    Возвращает:
        pandas DataFrame.
    """

    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {path}")

    df = pd.read_parquet(DATA_DIR / "diaries.parquet")
    initial_len = len(df)
    print(f"Данный загружены: {initial_len} строк")
    return df


def data_info(df: pd.DataFrame):
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