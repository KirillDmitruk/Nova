from ai import chat_loop
from config import ConfigurationError, validate_config
from ui import console
from utils import SystemPromptError


def main() -> None:
    try:
        validate_config()
        chat_loop()
    except (ConfigurationError, SystemPromptError) as error:
        console.print()
        console.print("[bold red]Startup error[/bold red]")
        console.print(str(error), style="red")
        console.print()


if __name__ == "__main__":
    main()