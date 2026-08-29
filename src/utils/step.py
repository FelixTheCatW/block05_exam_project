import colorsys
import time
from contextlib import contextmanager

from rich.color import Color
from rich.console import Console
from rich.live import Live
from rich.style import Style
from rich.text import Text

console = Console()

@contextmanager
def step(name, wait=False):
    with console.status(f"[purple]{name}[/purple]") as status:
        start = time.time()
        yield
        elapsed = time.time() - start
        # status.update(f"[bold green]√ {name} за {elapsed:.2f} с)[/bold green]")
        console.print(
            f"[purple]√ {name}[/purple]....[green]{elapsed:.2f} с[/green]"
        )
    if wait:
        input("Нажмите любую клавишу для продолжения...")
        print("\033[F\033[K", end="", flush=True)
