import textwrap
import time

from rich.console import Console
from rich.prompt import Prompt

from config import MODEL_NAME

console = Console()

APP_VERSION = "0.1.0"
LINE_WIDTH = 46


def startup() -> None:
    console.print()

    console.print("╔══════════════════════════════════════════════╗", style="cyan")
    console.print("║                                              ║", style="cyan")
    console.print("║                  [bold cyan]N O V A[/bold cyan]                     ║")
    console.print("║                                              ║", style="cyan")
    console.print("║             [white]Personal AI Assistant[/white]            ║")
    console.print("║                                              ║", style="cyan")
    console.print("╠══════════════════════════════════════════════╣", style="cyan")
    console.print(f"║  Version │ [white]{APP_VERSION:<31}[/white]   ║")
    console.print(f"║  Engine  │ [white]{MODEL_NAME:<31}[/white]   ║")
    console.print("║  Status  │ [bold green]● ONLINE[/bold green]                          ║")
    console.print("╚══════════════════════════════════════════════╝", style="cyan")

    console.print()

    _loading("Initializing core")
    _loading("Loading configuration")
    _loading("Loading system prompt")
    _loading("Connecting to Gemini")

    console.print()
    console.print("[bold green]✓ Nova is ready[/bold green]")
    console.rule(style="grey35")
    console.print()


def shutdown():
    console.rule(style="grey35")
    console.print("[bold cyan]🤖 Nova[/bold cyan]")
    console.print("[dim]Session terminated.[/dim]")
    console.print("[green]Have a productive day! 👋[/green]")


def ask_user() -> str:
    return Prompt.ask("[bold green]🧑 You[/bold green]").strip()


def thinking():
    return console.status(
        "[cyan]Nova is thinking...[/cyan]",
        spinner="dots"
    )


def print_answer(answer):
    wrapped = "\n".join(
        textwrap.wrap(
            answer,
            width=LINE_WIDTH,
            break_long_words=False,
        )
    )

    console.print("[bold cyan]🤖 Nova[/bold cyan]")
    _typewriter(wrapped)


def print_error(message: str) -> None:
    console.print("[bold red]✗ Request failed[/bold red]")
    console.print(message, style="red")
    console.print()


def _loading(text: str):
    with console.status(
            f"[cyan]{text}[/cyan]",
            spinner="dots",
    ):
        time.sleep(0.7)


def _typewriter(text: str, delay: float = 0.05):
    for char in text:
        console.print(char, end="")
        time.sleep(delay)

    console.print()
