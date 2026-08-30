import msvcrt
from functools import partial
from pathlib import Path

import pandas as pd
from IPython.display import display
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

import src.clean_data as clean
import src.load_data as load
from src import analysis
from src.utils import excel_utils
from src.utils.pipe import Pipe
from src.utils.step import step

console = Console()

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"
SRC_DATA = Path("d:\\Downloads\\mfp-diaries.tsv\\mfp-diaries.tsv")
PARQUET_PATH = DATA_DIR / "diaries.parquet"
WAIT_FOR_INPUT = True

def test_norm_group_cat():
    df = load.load_parquet_data(PARQUET_PATH)
    print(analysis.normalized_groued_by_category(df))