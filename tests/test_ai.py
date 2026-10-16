import ai, pytest
from unittest.mock import MagicMock

def test_ask_genai_success():
    client = MagicMock()
    client.interactions.create.return_value = MagicMock(output_text="Hello, user!")


    result = ai.ask_genai(
        prompt="Hi",
        client=client,
        system_prompt="You are NOVA",
    )

    assert result == "Hello, user!"


def test_ask_genai_empty_response():
    client = MagicMock()
    client.interactions.create.return_value = MagicMock(output_text=None)

    with pytest.raises(ValueError):
        ai.ask_genai(
            prompt="Hi",
            client=client,
            system_prompt="You are NOVA",
        )

def test_ask_genai_exception():
    client = MagicMock()
    client.interactions.create.side_effect = Exception("API error")

    with pytest.raises(Exception):
        ai.ask_genai(
            prompt="Hi",
            client=client,
            system_prompt="You are NOVA",
        )
        