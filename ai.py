from google import genai

from config import MODEL_NAME, GEMINI_API_KEY
from logs.logging_config import logger
from ui import startup, shutdown, thinking
from utils import load_system_prompt

client = genai.Client(api_key=GEMINI_API_KEY)
SYSTEM_PROMPT = load_system_prompt()


def ask_genai(prompt):
    try:
        interaction = client.interactions.create(
            model=MODEL_NAME,
            input=SYSTEM_PROMPT + prompt,
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


def chat_loop():
    startup()

    while True:
        user_input = input("🧑 You: ").strip()

        if not user_input:
            continue

        thinking()

        answer = ask_genai(user_input)
        print(f"\n🤖 Nova: {answer}\n")

        if user_input.lower() in {"exit", "quit", "bye"}:
            shutdown()
            break
