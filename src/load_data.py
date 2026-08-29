import json
import time
from pathlib import Path

import orjson
import pandas as pd
from IPython import display
from IPython.display import display

from src.utils.step import step


def load_parquet_data(path: str | Path) -> pd.DataFrame:
    """
    Загружает данные из parquet-файла.
    path — путь к файлу.
    Возвращает:
        pandas DataFrame.
    """

    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {path}")

    df = pd.read_parquet(path)
    initial_len = len(df)
    print(f"Данные загружены: {initial_len} строк")
    return df


def data_info(df: pd.DataFrame):
    print("Размер таблицы:", df.shape)

    print("\nНазвания столбцов:")
    print(df.columns.tolist())

    print("\nТипы данных:")
    print(df.dtypes)

    print("\nПропуски по столбцам:")
    print(df.isna().sum())


def json_to_parquet(
    input_data_path: str | Path, output_parquet_path: str | Path
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

    with step("Сохранение Parquet"):
        Path(output_parquet_path).parent.mkdir(parents=True, exist_ok=True)
        result.to_parquet(output_parquet_path, index=False)

    elapsed = time.time() - start_time
    print(f"Готово! Σ время: {elapsed:.2f}")
    print(f"Записей: {len(result)}")

    return result


def get_total_dict(parsed: dict):
    total = parsed.get("total", [])
    return {item["name"]: item["value"] for item in total}
