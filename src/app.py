from src.clean_data import *
from src.load_data import *

src_csv_data: str = Path("d:\\Downloads\\mfp-diaries.tsv\\mfp-diaries.tsv")
src_parquet_data: str = Path(
    "d:\\study\\excel\\block05_exam_project\\data\\diaries.parquet"
)

if not src_parquet_data.exists():
    df = json_to_parquet(src_csv_data, src_parquet_data)

df = load_parquet_data(src_parquet_data)

df = lower_columns(df)
df = drop_mistakes(df)
df = filter_outliers_iqr_all(df, ["calories"])

add_computed_columns(df)
add_weekday(df)
df = df[
    [
        "user_id",
        "date",
        "weekday",
        "calories",
        "carbs",
        "fat",
        "protein",
        "pct_cal_fat",
        "pct_cal_carbs",
        "pct_cal_protein",
        "fat_per_1k",
        "carbs_per_1k",
        "protein_per_1k",
        "fat_to_carbs",
        "protein_to_fat",
        "carbs_to_protein",
        "cal_category",
        "high_protein",
    ]
]
data_info(df)

print("Описательная статистика:")
display(df[["fat", "carbs", "protein", "calories"]].describe())



