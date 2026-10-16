import pytest
import config


def test_validate_config_success(monkeypatch):
    monkeypatch.setattr(config, "GEMINI_API_KEY", "test_key")
    monkeypatch.setattr(config, "MODEL_NAME", "test_model")

    config.validate_config()


def test_validate_config_missing_variables(monkeypatch):
    monkeypatch.setattr(config, "GEMINI_API_KEY", "")
    monkeypatch.setattr(config, "MODEL_NAME", "")

    with pytest.raises(ValueError) as excinfo:
        config.validate_config()

    assert "Missing required environment variables" in str(excinfo.value)


def test_validate_config_missing_api_key(monkeypatch):
    monkeypatch.setattr(config, "GEMINI_API_KEY", "")
    monkeypatch.setattr(config, "MODEL_NAME", "test_model")

    with pytest.raises(ValueError) as excinfo:
        config.validate_config()

    assert "GEMINI_API_KEY" in str(excinfo.value)

def test_validate_config_missing_model_name(monkeypatch):
    monkeypatch.setattr(config, "GEMINI_API_KEY", "test_key")
    monkeypatch.setattr(config, "MODEL_NAME", "")

    with pytest.raises(ValueError) as excinfo:
        config.validate_config()

    assert "MODEL_NAME" in str(excinfo.value)