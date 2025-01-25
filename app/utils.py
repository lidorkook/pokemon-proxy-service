import base64
import hashlib
import hmac
import secrets

from google.protobuf.message import DecodeError

from .logger import logger
from .proto.pokemon_pb2 import Pokemon


class InvalidSignatureException(Exception):
    """Custom exception for invalid HMAC signatures."""

    pass


class MalformedDataException(Exception):
    pass


def validate_signature(body: bytes, secret: str, signature: str):
    """Verify webhook signature using HMAC."""
    computed_hmac = hmac.new(base64.b64decode(secret), body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature, computed_hmac):
        raise InvalidSignatureException("The provided HMAC signature is invalid.")


def parse_pokemon(body: bytes) -> Pokemon:
    """Validate and convert dictionary payload to Pokemon model."""
    pokemon = Pokemon()
    try:
        pokemon.ParseFromString(body)
        return pokemon
    except DecodeError as e:
        raise MalformedDataException(f"Payload validation failed: {e}") from e


def _generate_secret(salt: str = "") -> str:
    """
    Generate a hashed UUID to use as the HMAC secret.
    """
    random_value = secrets.token_bytes(32)
    secret_value = random_value + salt.encode()
    secret = hashlib.sha256(secret_value).digest()
    logger.info(f"secret is {secret_value}")
    return base64.b64encode(secret).decode("utf-8")


stream_secret = _generate_secret()
