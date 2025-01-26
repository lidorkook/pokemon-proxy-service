import base64
import hashlib
import hmac

import pytest

from app.auth import _generate_secret, validate_signature
from app.exceptions import InvalidSignatureException, MalformedDataException
from app.proto.pokemon_pb2 import Pokemon
from app.utils import parse_pokemon


def test_validate_signature_valid():
    body = b"test body"
    secret = base64.b64encode(b"test secret").decode("utf-8")
    signature = hmac.new(base64.b64decode(secret), body, hashlib.sha256).hexdigest()
    assert validate_signature(body, secret, signature) is None


def test_validate_signature_invalid():
    body = b"test body"
    secret = base64.b64encode(b"test secret").decode("utf-8")
    signature = "invalid_signature"
    with pytest.raises(InvalidSignatureException):
        validate_signature(body, secret, signature)


def test_parse_pokemon_valid():
    pokemon = Pokemon(name="Pikachu")
    body = pokemon.SerializeToString()
    parsed_pokemon = parse_pokemon(body)
    assert parsed_pokemon.name == "Pikachu"


def test_parse_pokemon_invalid():
    body = b"invalid body"
    with pytest.raises(MalformedDataException):
        parse_pokemon(body)


def test_generate_secret():
    secret = _generate_secret()
    assert isinstance(secret, str)
    assert len(secret) > 0
