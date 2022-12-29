from contextlib import contextmanager
from typing import Optional, Dict, Any

from rich.console import Console
from rich.table import Table


out = Console()


@contextmanager
def busy(message: str, spinner: str = "aesthetic"):
    with out.status(message, spinner=spinner):
        yield


def print(message: str):
    out.print(message)


def result(
    message: Optional[str],
    rows: Optional[Dict[str, Any]] = None,
    is_success: bool = True,
):

    o = "[bold green] Success!" if is_success else "[bold red] Failure!"
    out.rule(o)

    if message and not is_success:
        out.print(f"[bold red]Failure:[\bold red] {message}")
        return

    if message:
        out.print(message)

    if rows:
        t = Table("Results")

        for k in rows:
            t.add_row(k, rows[k])
        out.print(t)
