from ai import chat_loop
from config import ConfigurationError, validate_config
from ui import console


def main() -> None:
    try:
        validate_config()
        chat_loop()
    except ConfigurationError as error:
        console.print()
        console.print("[bold red]Configuration error[/bold red]")
        console.print(f"[red]{error}[/red]")
        console.print()


if __name__ == "__main__":
    main()