import time

import requests
from flask import Blueprint, jsonify, request
from google.protobuf.json_format import MessageToJson

from .auth import stream_secret, validate_signature
from .config import Rule, get_pokemon_rule
from .exceptions import InvalidSignatureException, MalformedDataException
from .logger import logger
from .proto.pokemon_pb2 import Pokemon
from .stats import StatsTracker
from .utils import parse_pokemon

bp = Blueprint("routes", __name__)
stats = StatsTracker()

REASON_HEADER_KEY = "X-Grd-Reason"
SIGNATURE_HEADER_KEY = "X-Grd-Signature"


def _proxy_request(pokemon: Pokemon, headers: dict, rule: Rule):
    start_time = time.time()
    headers[REASON_HEADER_KEY] = rule.reason
    proxy_response = requests.post(
        rule.url,
        json=MessageToJson(pokemon, preserving_proto_field_name=True),
        headers=headers,
    )
    try:
        proxy_response.raise_for_status()
        response_succeeded = True
    except requests.RequestException:
        response_succeeded = False
    response_time = time.time() - start_time

    stats.log_request(
        pokemon.name.lower(),
        response_succeeded,
        response_time,
        len(request.get_data()),
        len(proxy_response.content),
    )
    return proxy_response


def _build_json_res(payload, status_code=200):
    return jsonify(payload), status_code


@bp.route("/stream", methods=["POST"])
def stream():
    # signature validations
    try:
        headers = dict(request.headers)
        signature = headers.pop(SIGNATURE_HEADER_KEY)
        body = request.get_data()
        validate_signature(body, stream_secret, signature)
    except (KeyError, InvalidSignatureException):
        logger.error(
            "invalid signature",
            exc_info=True,
        )
        return _build_json_res({"error": "Invalid signature"}, 401)

    # Validate payload schema
    try:
        pokemon = parse_pokemon(body)
    except MalformedDataException as e:
        logger.error("failed to parse pokemon", exc_info=True)
        return _build_json_res({"error": str(e)}, 400)

    try:
        matched_rule = get_pokemon_rule(pokemon.name)
        response = _proxy_request(pokemon, headers, matched_rule)
        return response.content, response.status_code, dict(response.headers)
    except KeyError:
        return _build_json_res({"error": "No matching rule found"}, 404)


@bp.route("/stats", methods=["GET"])
def stats_endpoint():
    return _build_json_res(stats.get_stats())
