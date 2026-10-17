from unittest.mock import MagicMock, patch

import pytest

from core.providers.gemini import GeminiProvider


@pytest.fixture
def provider():
    with patch("core.providers.gemini.genai.Client") as mock_client:
        provider = GeminiProvider(
            api_key="test_api_key",
            model_name="test_model",
            system_prompt="You are NOVA",
        )

        yield provider, mock_client.return_value


def test_ask_genai_success(provider):
    gemini, client = provider

    client.interactions.create.return_value = MagicMock(
        output_text="Hello, user!"
    )

    result = gemini.ask(prompt="Hi")

    assert result == "Hello, user!"

    client.interactions.create.assert_called_once_with(
        model="test_model",
        input="You are NOVA\n\nUser: Hi",
    )


def test_ask_genai_empty_response(provider):
    gemini, client = provider

    client.interactions.create.return_value = MagicMock(
        output_text=None
    )

    with pytest.raises(ValueError, match="Gemini returned an empty response"):
        gemini.ask(prompt="Hi")


def test_ask_genai_exception(provider):
    gemini, client = provider

    client.interactions.create.side_effect = Exception("API error")

    with pytest.raises(Exception, match="API error"):
        gemini.ask(prompt="Hi")