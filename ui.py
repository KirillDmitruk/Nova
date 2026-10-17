import textwrap
import time

from rich.console import Console
from rich.prompt import Prompt

from config import VERSION

console = Console()

LINE_WIDTH = 46


def startup() -> None:
    """Выводит приветственное сообщение и имитацию загрузки при запуске приложения."""
    console.print()

    console.print("╔══════════════════════════════════════════════╗", style="cyan")
    console.print("║                                              ║", style="cyan")
    console.print("║                  [bold cyan]N O V A[/bold cyan]                     ║")
    console.print("║                                              ║", style="cyan")
    console.print("║             [white]Personal AI Assistant[/white]            ║")
    console.print("║                                              ║", style="cyan")
    console.print("╠══════════════════════════════════════════════╣", style="cyan")
    console.print(f"║  Version │ [white]{VERSION:<31}[/white]   ║")
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
    """Выводит сообщение о завершении сессии и имитацию завершения работы приложения."""
    console.rule(style="grey35")
    console.print("[bold cyan]🤖 Nova[/bold cyan]")
    console.print("[dim]Session terminated.[/dim]")
    console.print("[green]Have a productive day! 👋[/green]")


def ask_user() -> str:
    """Запрашивает ввод пользователя и возвращает его в виде строки."""
    return Prompt.ask("[bold green]🧑 You[/bold green]").strip()


def thinking():
    """Отображает индикатор "Nova is thinking..." с анимацией загрузки."""
    return console.status(
        "[cyan]Nova is thinking...[/cyan]",
        spinner="dots"
    )


def print_answer(answer):
    """Выводит ответ от LLM в консоль с эффектом печати текста."""
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
    """Выводит сообщение об ошибке в консоль с красным цветом."""
    console.print("[bold red]✗ Request failed[/bold red]")
    console.print(message, style="red")
    console.print()


def _loading(text: str):
    """Отображает индикатор загрузки с анимацией и задержкой."""
    with console.status(
            f"[cyan]{text}[/cyan]",
            spinner="dots",
    ):
        time.sleep(0.7)


def _typewriter(text: str, delay: float = 0.05):
    """Эффект печати текста с задержкой между символами."""
    for char in text:
        console.print(char, end="")
        time.sleep(delay)

    console.print()
