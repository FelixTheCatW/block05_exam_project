from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid", palette="muted")

WEEKDAY_NAMES = {
    0: "Пн", 1: "Вт", 2: "Ср", 3: "Чт", 4: "Пт", 5: "Сб", 6: "Вс",
}


def chart_calories_histogram(df: pd.DataFrame, output_path: str | Path) -> Path:
    output_path = Path(output_path)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(df["calories"], bins=40, color="#4C72B0", edgecolor="white", alpha=0.8)
    ax.set_title("Распределение калорий", fontsize=14)
    ax.set_xlabel("Калории")
    ax.set_ylabel("Количество записей")
    ax.axvline(df["calories"].mean(), color="red", linestyle="--", label=f'Среднее: {df["calories"].mean():.0f}')
    ax.axvline(df["calories"].median(), color="green", linestyle="--", label=f'Медиана: {df["calories"].median():.0f}')
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path


def chart_macros_boxplot(df: pd.DataFrame, output_path: str | Path) -> Path:
    output_path = Path(output_path)
    melt = df[["fat", "carbs", "protein"]].melt(var_name="Макронутриент", value_name="Граммы")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=melt, x="Макронутриент", y="Граммы", hue="Макронутриент", ax=ax, palette="Set2", legend=False)
    ax.set_title("Распределение макронутриентов", fontsize=14)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path


def chart_by_weekday(df: pd.DataFrame, output_path: str | Path) -> Path:
    output_path = Path(output_path)
    stats = df.groupby("weekday", as_index=False)["calories"].mean()
    stats["weekday_name"] = stats["weekday"].map(WEEKDAY_NAMES)
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(stats["weekday_name"], stats["calories"], color="#55A868", edgecolor="white")
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 10, f"{h:.0f}", ha="center", fontsize=9)
    ax.set_title("Средние калории по дням недели", fontsize=14)
    ax.set_xlabel("День недели")
    ax.set_ylabel("Средние калории")
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path


def chart_by_category(df: pd.DataFrame, output_path: str | Path) -> Path:
    output_path = Path(output_path)
    counts = df["cal_category"].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(8, 5))
    colors = {"low": "#4C72B0", "medium": "#55A868", "high": "#C44E52"}
    bars = ax.bar(counts.index, counts.values, color=[colors.get(c, "#888") for c in counts.index], edgecolor="white")
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 2, str(int(h)), ha="center", fontsize=10)
    ax.set_title("Количество записей по категориям калорийности", fontsize=14)
    ax.set_xlabel("Категория")
    ax.set_ylabel("Количество")
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path


def chart_heatmap_pivot(df: pd.DataFrame, output_path: str | Path) -> Path:
    output_path = Path(output_path)
    pivot = pd.pivot_table(
        df, index="weekday", columns="cal_category",
        values="calories", aggfunc="mean", fill_value=0,
    )
    pivot.index = pivot.index.map(WEEKDAY_NAMES)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlOrRd", ax=ax)
    ax.set_title("Средние калории: день недели × категория", fontsize=14)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path


def chart_pairplot(df: pd.DataFrame, output_path: str | Path) -> Path:
    output_path = Path(output_path)
    cols = ["calories", "fat", "carbs", "protein"]
    g = sns.pairplot(df[cols], diag_kind="kde", plot_kws={"alpha": 0.4, "s": 15})
    g.figure.suptitle("Попарные зависимости макронутриентов", y=1.02, fontsize=14)
    g.savefig(output_path, dpi=150)
    plt.close(g.figure)
    return output_path


def chart_correlation_heatmap(df: pd.DataFrame, output_path: str | Path) -> Path:
    output_path = Path(output_path)
    corr = df[["calories", "fat", "carbs", "protein"]].corr()
    fig, ax = plt.subplots(figsize=(7, 6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, ax=ax, square=True)
    ax.set_title("Корреляционная матрица", fontsize=14)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path


def chart_calories_boxplot_by_weekday(df: pd.DataFrame, output_path: str | Path) -> Path:
    output_path = Path(output_path)
    data = df.copy()
    data["weekday_name"] = data["weekday"].map(WEEKDAY_NAMES)
    order = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=data, x="weekday_name", y="calories", hue="weekday_name", order=order, ax=ax, palette="Set3", legend=False)
    ax.set_title("Распределение калорий по дням недели", fontsize=14)
    ax.set_xlabel("День недели")
    ax.set_ylabel("Калории")
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path


def chart_stacked_by_category(df: pd.DataFrame, output_path: str | Path) -> Path:
    output_path = Path(output_path)
    data = (
        df.groupby("cal_category", as_index=False)
        .agg(
            fat=("fat_per_1k", "mean"),
            carbs=("carbs_per_1k", "mean"),
            protein=("protein_per_1k", "mean"),
        )
    )
    cat_order = ["low", "medium", "high"]
    data = data.set_index("cal_category").reindex(cat_order)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(data.index, data["fat"], label="Жиры", color="#4C72B0")
    ax.bar(data.index, data["carbs"], bottom=data["fat"], label="Углеводы", color="#55A868")
    bottom = data["fat"] + data["carbs"]
    ax.bar(data.index, data["protein"], bottom=bottom, label="Белки", color="#C44E52")
    for i, idx in enumerate(data.index):
        cum = 0
        for col in ["fat", "carbs", "protein"]:
            cum += data.loc[idx, col]
        ax.text(i, cum + 2, f"{cum:.0f}", ha="center", fontsize=10)
    ax.set_title("Состав рациона на 1000 ккал по категориям калорийности", fontsize=14)
    ax.set_xlabel("Категория калорийности")
    ax.set_ylabel("Граммы на 1000 ккал")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path


def chart_stacked_by_weekday(df: pd.DataFrame, output_path: str | Path) -> Path:
    output_path = Path(output_path)
    data = (
        df.groupby("weekday", as_index=False)
        .agg(
            fat=("fat_per_1k", "mean"),
            carbs=("carbs_per_1k", "mean"),
            protein=("protein_per_1k", "mean"),
        )
    )
    data["weekday_name"] = data["weekday"].map(WEEKDAY_NAMES)
    order = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    data = data.set_index("weekday_name").reindex(order)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(data.index, data["fat"], label="Жиры", color="#4C72B0")
    ax.bar(data.index, data["carbs"], bottom=data["fat"], label="Углеводы", color="#55A868")
    bottom = data["fat"] + data["carbs"]
    ax.bar(data.index, data["protein"], bottom=bottom, label="Белки", color="#C44E52")
    for i, idx in enumerate(data.index):
        cum = data.loc[idx, "fat"] + data.loc[idx, "carbs"] + data.loc[idx, "protein"]
        ax.text(i, cum + 2, f"{cum:.0f}", ha="center", fontsize=10)
    ax.set_title("Состав рациона на 1000 ккал по дням недели", fontsize=14)
    ax.set_xlabel("День недели")
    ax.set_ylabel("Граммы на 1000 ккал")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path


def chart_boxplot_protein_per_1k(df: pd.DataFrame, output_path: str | Path) -> Path:
    output_path = Path(output_path)
    cat_order = ["low", "medium", "high"]
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=df, x="cal_category", y="protein_per_1k", hue="cal_category", order=cat_order, ax=ax, palette="Set2", legend=False)
    ax.set_title("Белок на 1000 ккал по категориям калорийности", fontsize=14)
    ax.set_xlabel("Категория калорийности")
    ax.set_ylabel("Белок, г/1000 ккал")
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path


def chart_boxplot_fat_per_1k_by_weekday(df: pd.DataFrame, output_path: str | Path) -> Path:
    output_path = Path(output_path)
    data = df.copy()
    data["weekday_name"] = data["weekday"].map(WEEKDAY_NAMES)
    order = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=data, x="weekday_name", y="fat_per_1k", hue="weekday_name", order=order, ax=ax, palette="Set3", legend=False)
    ax.set_title("Жиры на 1000 ккал по дням недели", fontsize=14)
    ax.set_xlabel("День недели")
    ax.set_ylabel("Жиры, г/1000 ккал")
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path
