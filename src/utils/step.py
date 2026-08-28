import time
from contextlib import contextmanager

COLOR_PURPLE = "\033[95m"
COLOR_GREEN = "\033[92m"
COLOR_RESET = "\033[0m"

STEP_WIDTH = 30

@contextmanager
def step(name, wait=False):
    print(f"→ {COLOR_PURPLE}{name:<{STEP_WIDTH}}{COLOR_RESET}", end="", flush=True)
    start = time.time()
    yield
    elapsed = time.time() - start
    print(
        f"\r√ {COLOR_PURPLE}{name:<{STEP_WIDTH}}{COLOR_RESET}{COLOR_GREEN}{elapsed:.2f}{COLOR_RESET}\n",
        end="",
    )
    
    if wait:
        input("Нажмите любую клавишу для продолжения...")
        print("\n") 
