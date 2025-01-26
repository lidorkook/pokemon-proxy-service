from google.protobuf.message import DecodeError

from .exceptions import MalformedDataException
from .proto.pokemon_pb2 import Pokemon


def parse_pokemon(body: bytes) -> Pokemon:
    """Validate and convert dictionary payload to Pokemon model."""
    pokemon = Pokemon()
    try:
        pokemon.ParseFromString(body)
        return pokemon
    except DecodeError as e:
        raise MalformedDataException(f"Payload validation failed: {e}") from e
