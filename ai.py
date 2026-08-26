from google import genai

from config import MODEL_NAME, GEMINI_API_KEY
from logs.logging_config import logger
from ui import startup, shutdown, thinking, ask_user, print_answer, console
from utils import load_system_prompt

client = genai.Client(api_key=GEMINI_API_KEY)
SYSTEM_PROMPT = load_system_prompt()


def ask_genai(prompt):
    try:
        interaction = client.interactions.create(
            model=MODEL_NAME,
            input=f"{SYSTEM_PROMPT}\n\nUser: {prompt}"
        )
        print('')
        if hasattr(interaction, 'output_text'):
            answer = interaction.output_text
        else:
            answer = "Error: an unexpected type of response was received"
        logger.info(answer)
        return answer

    except FileNotFoundError:
        logger.exception('System file not found')
        raise

    except Exception:
        logger.exception('Unknown error Gemini')
        raise


startup()

while True:
    user_input = ask_user()

    if not user_input:
        continue

    if user_input.lower() in {"exit", "quit", "bye"}:
        shutdown()
        break

    console.print()

    with thinking():
        answer = ask_genai(user_input)

    print_answer(answer)

    console.print()