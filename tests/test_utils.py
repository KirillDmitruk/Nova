import utils, pytest


def test_load_system_prompt(tmp_path, monkeypatch):
    prompt_file = tmp_path / "test_prompt.txt"
    prompt_file.write_text("You are Nova!", encoding="utf-8")

    monkeypatch.setattr(utils, "PROMPT_PATH", prompt_file)

    result = utils.load_system_prompt()

    assert result == "You are Nova!"



def test_empty_prompt(tmp_path, monkeypatch):
    prompt_file = tmp_path / "test_prompt.txt"
    prompt_file.write_text("", encoding="utf-8")

    monkeypatch.setattr(utils, "PROMPT_PATH", prompt_file)

    with pytest.raises(ValueError):
        utils.load_system_prompt()

def test_whitespace_prompt(tmp_path, monkeypatch):
    prompt_file = tmp_path / "test_prompt.txt"
    prompt_file.write_text("\n   Nova   \n", encoding="utf-8")

    monkeypatch.setattr(utils, "PROMPT_PATH", prompt_file)

    assert utils.load_system_prompt() == "Nova"


def test_missing_prompt_file(tmp_path, monkeypatch):
    prompt_file = tmp_path / "non_existent_prompt.txt"

    monkeypatch.setattr(utils, "PROMPT_PATH", prompt_file)

    with pytest.raises(FileNotFoundError):
        utils.load_system_prompt()
