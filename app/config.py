import json
from typing import Dict

from pydantic import BaseModel

from . import settings
from .logger import logger


class Rule(BaseModel):
    url: str
    reason: str


_rules: Dict[str, Rule] = {}


def _validate_rules(raw_rules_list):
    if not isinstance(raw_rules_list, list):
        raise TypeError("rules has to be a list")


def _parse_rules(raw_rules_list):
    _validate_rules(raw_rules_list)
    for rule_data in raw_rules_list:
        try:
            if not isinstance(rule_data, dict):
                raise TypeError(
                    f"Type of rule_data is `{type(rule_data)}`, not a dict."
                )
            pokemon_name = rule_data["pokemon_name"].lower()
            if pokemon_name in _rules:
                raise ValueError(
                    f"Rule for pokemon called `{pokemon_name}` already exists."
                )
            _rules[pokemon_name] = Rule(**rule_data)
        except (KeyError, TypeError, AttributeError, ValueError):
            logger.warning("Pokemon rule data is malformed and will be ignored.")


def load_config():
    config_path = settings.POKEPROXY_CONFIG
    try:
        with open(config_path, "r") as file:
            config = json.load(file)
            _parse_rules(config["rules"])
    except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError):
        logger.exception(f"Error loading config from file {config_path}", exc_info=True)
        raise


def get_pokemon_rule(pokemon_name: str):
    return _rules[pokemon_name.lower()]
