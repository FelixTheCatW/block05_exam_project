import pandas as pd


def filter_outliers_iqr_all(
    df: pd.DataFrame, cols: [str], multiplier=1.5
) -> pd.DataFrame:
    """
    Удаляет выбросы.

    Для каждой колонки из `cols` вычисляются нижняя и верхняя границы на основе
    межквартильного размаха (IQR) с возможным масштабированием. Остаются только строки,
    в которых все указанные столбцы попадают в интервал.
    Границы дополнительно ограничиваются глобальными
    константами (нижняя граница ≥ 1, верхняя ≤ 10 000) для предотвращения
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
        upper = min(q3 + multiplier * iqr, 10_000)
        lower = max(q1 - multiplier * iqr, 1)
        mask &= (df[col] >= lower) & (df[col] <= upper)

    cleaned = df[mask].reset_index(drop=True)
    print(
        f"Удалено строк: {initial_len - len(cleaned)} ({100 * (initial_len - len(cleaned)) / initial_len:.2f}%)"
    )
    return cleaned


def drop_mistakes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Удаляет строки с пропусками и дубликатами.
    Возвращает:
        Очищенную копию.
    """
    initial_len = len(df)
    cleaned = df.dropna().drop_duplicates().reset_index(drop=True)
    print(
        f"Удалено строк: {initial_len - len(cleaned)} ({100 * (initial_len - len(cleaned)) / initial_len:.2f}%)"
    )
    return cleaned
