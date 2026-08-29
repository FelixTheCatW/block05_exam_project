# Анализ дневников питания — экзаменационный проект, Блок 5

Анализ данных: загрузка TSV/parquet, очистка,
добавление вычисляемых колонок, групповая статистика и сводные таблицы,
экспорт в CSV и в Excel с **нативными** диаграммами (openpyxl, без картинок).

## Структура проекта

```
block05_exam_project/
├── .gitignore
├── README.md
├── requirements.txt
├── data/
│   └── diaries.parquet
├── reports/
│   └── analysis_report.xlsx
├── src/
│   ├── __init__.py
│   ├── app.py
│   ├── load_data.py
│   ├── clean_data.py
│   ├── analysis.py
│   ├── charts.py
│   ├── excel_charts.py
│   └── utils/
│       ├── __init__.py
│       ├── pipe.py
│       ├── step.py
│       └── excel_utils.py
├── tests/
│   └── test_pipe.py
└── optional_ai/
    └── README.md
```

## Установка
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск
```bash
python -m src.app
```