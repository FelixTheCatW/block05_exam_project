# predict_calories.py
import os
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Пути к файлам
MODEL_PATH = Path("models/calories_model.joblib")
TEST_DATA_PATH = Path("data/test_data.parquet")
FEATURES_PATH = Path("models/features.joblib")


def load_model_and_predict():
    # Проверка наличия файлов
    if not MODEL_PATH.exists():
        print(f"Ошибка: файл модели {MODEL_PATH} не найден.")
        return
    if not TEST_DATA_PATH.exists():
        print(f"Ошибка: файл тестовых данных {TEST_DATA_PATH} не найден.")
        return

    # Загрузка модели и списка признаков
    model = joblib.load(MODEL_PATH)
    if FEATURES_PATH.exists():
        feature_columns = joblib.load(FEATURES_PATH)
    else:
        # Если список признаков не сохранён, можно задать вручную
        feature_columns = ["total_carbs", "total_fat", "total_protein"]
        print(
            "Предупреждение: файл признаков не найден. Используем стандартный список."
        )

    # Загрузка тестовых данных
    df_test = pd.read_parquet(TEST_DATA_PATH)

    # Проверка наличия признаков
    missing = [col for col in feature_columns if col not in df_test.columns]
    if missing:
        print(f"Ошибка: в тестовых данных отсутствуют колонки: {missing}")
        return

    X_test = df_test[feature_columns]
    # Если есть целевая переменная, можно вычислить метрики
    y_test = df_test["total_calories"] if "total_calories" in df_test.columns else None

    # Предсказание
    predictions = model.predict(X_test)

    # Вывод результатов
    print("\n=== Результаты предсказания ===")
    print(f"Количество примеров: {len(predictions)}")
    print(f"Первые 5 предсказаний: {predictions[:5]}")
    if y_test is not None:
        mae = mean_absolute_error(y_test, predictions)
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        r2 = r2_score(y_test, predictions)
        print(f"MAE: {mae:.4f}")
        print(f"RMSE: {rmse:.4f}")
        print(f"R²: {r2:.4f}")

    # Сохранение предсказаний (опционально)
    output = pd.DataFrame(
        {
            "actual": y_test if y_test is not None else [None] * len(predictions),
            "predicted": predictions,
        }
    )
    output.to_csv("predictions.csv", index=False)
    print("\nПредсказания сохранены в predictions.csv")


if __name__ == "__main__":
    load_model_and_predict()
