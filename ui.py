import time

APP_VERSION = "0.1.0"


def startup() -> None:
    print()
    print("╔══════════════════════════════════════════════╗")
    print("║                                              ║")
    print("║                N O V A   A I                 ║")
    print(f"║         Personal AI Assistant v{APP_VERSION:<12}  ║")
    print("║                                              ║")
    print("╚══════════════════════════════════════════════╝")
    print()

    _loading("Initializing core")
    _loading("Loading configuration")
    _loading("Loading system prompt")
    _loading("Connecting to Gemini")

    print()
    print("✓ System online")
    print("Ready to assist you.")
    print("Type 'exit' to close Nova.")
    print("─" * 46)
    print()


def shutdown() -> None:
    print()
    print("─" * 46)
    print("🤖 Nova:")
    print("Session terminated.")
    print("Have a productive day. Goodbye!")
    print()


def thinking() -> None:
    print("🤖 Nova is thinking...")


def _loading(text: str) -> None:
    print(f"{text}", end="", flush=True)

    for _ in range(3):
        time.sleep(0.2)
        print(".", end="", flush=True)

    print(" ✓")