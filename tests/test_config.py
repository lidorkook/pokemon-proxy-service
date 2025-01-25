import pytest

from app.config import get_pokemon_rule, load_config


def test_load_config(mocker):
    mocker.patch(
        "builtins.open",
        mocker.mock_open(
            read_data='{"rules": [{"pokemon_name": "Pikachu", "url": "http://example.com", "reason": "test"}]}'
        ),
    )
    mocker.patch("app.config.settings.POKEPROXY_CONFIG", "dummy_path")
    load_config()
    rule = get_pokemon_rule("Pikachu")
    assert rule.url == "http://example.com"
    assert rule.reason == "test"


def test_malformed_config_file(mocker):
    mocker.patch("builtins.open", mocker.mock_open(read_data="malformed json"))
    mocker.patch("app.config.settings.POKEPROXY_CONFIG", "dummy_path")
    with pytest.raises(Exception):
        load_config()


def test_get_pokemon_rule_not_found():
    with pytest.raises(KeyError):
        get_pokemon_rule("Unknown")
