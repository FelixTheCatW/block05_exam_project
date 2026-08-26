import json
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


import time
from contextlib import contextmanager
from pathlib import Path

import orjson
import pandas as pd
from tqdm import tqdm

# Активируем поддержку прогресса для .apply()
tqdm.pandas(desc="Применение функций")


def json_to_parquet(
    input_data_path: str = "d:\\Downloads\\mfp-diaries.tsv\\mfp-diaries.tsv",
    output_parquet_path: str = "d:\\study\\excel\\block05_exam_project\\data\\diaries.parquet",
) -> None:
    start_time = time.time()
    print(f"Начало: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    with step("Чтение TSV"):
        df_raw = pd.read_csv(input_data_path, sep="\t", header=None, encoding="utf-8")

    with step("Преобразование типов"):
        df_raw[0] = df_raw[0].astype(int)
        df_raw[1] = pd.to_datetime(df_raw[1])

    with step("Парсинг JSON"):
        df_raw["parsed"] = df_raw[3].apply(orjson.loads)

    with step("Извлечение total"):
        df_raw["total_dict"] = df_raw["parsed"].apply(get_total_dict)

    with step("Разворачивание словарей"):
        total_df = pd.DataFrame(df_raw["total_dict"].tolist())

    with step("Сборка результата..."):
        result = pd.concat(
            [df_raw[[0, 1]].rename(columns={0: "user_id", 1: "date"}), total_df], axis=1
        )
        result["weekday"] = result["date"].dt.weekday

    with step("Сохранение Parquet"):
        Path(output_parquet_path).parent.mkdir(parents=True, exist_ok=True)
        result.to_parquet(output_parquet_path, index=False)

    elapsed = time.time() - start_time
    print(f"Готово! Σ время: {elapsed:.2f}")
    print(f"Записей: {len(result)}")    


def get_total_dict(parsed: dict):
    total = parsed.get("total", [])
    return {item["name"]: item["value"] for item in total}


COLOR_PURPLE = "\033[95m"  # фиолетовый
COLOR_GREEN = "\033[92m"  # зелёный
COLOR_RESET = "\033[0m"

# Фиксированная ширина для названия (подберите под свои шаги)
STEP_WIDTH = 30


@contextmanager
def step(name):
    print(f"→ {COLOR_PURPLE}{name:<{STEP_WIDTH}}{COLOR_RESET}", end="", flush=True)
    start = time.time()
    yield
    elapsed = time.time() - start    
    print(
        f"\r√ {COLOR_PURPLE}{name:<{STEP_WIDTH}}{COLOR_RESET}{COLOR_GREEN}{elapsed:.2f}{COLOR_RESET}\n",
        end="",
    )
