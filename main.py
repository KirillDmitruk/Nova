from ai import chat_loop
from config import validate_config
from ui import console


def main() -> None:
    validate_config()
    chat_loop()

    console.print()
    console.print("[bold red]Startup error[/bold red]")
    console.print()


if __name__ == "__main__":
    main()