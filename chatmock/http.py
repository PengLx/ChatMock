from __future__ import annotations

import hmac

from flask import Response, jsonify, request


def build_cors_headers() -> dict:
    origin = request.headers.get("Origin", "*")
    req_headers = request.headers.get("Access-Control-Request-Headers")
    allow_headers = req_headers if req_headers else "Authorization, Content-Type, Accept"
    return {
        "Access-Control-Allow-Origin": origin,
        "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
        "Access-Control-Allow-Headers": allow_headers,
        "Access-Control-Max-Age": "86400",
    }


def json_error(message: str, status: int = 400) -> Response:
    resp = jsonify({"error": {"message": message}})
    response: Response = Response(response=resp.response, status=status, mimetype="application/json")
    for k, v in build_cors_headers().items():
        response.headers.setdefault(k, v)
    return response


def bearer_token_from_header(header_value: str | None) -> str | None:
    if not isinstance(header_value, str):
        return None
    parts = header_value.strip().split(None, 1)
    if len(parts) != 2:
        return None
    scheme, token = parts
    if scheme.lower() != "bearer" or not token.strip():
        return None
    return token.strip()


def is_authorized_bearer(header_value: str | None, expected_token: str | None) -> bool:
    if not isinstance(expected_token, str) or not expected_token.strip():
        return True
    token = bearer_token_from_header(header_value)
    if token is None:
        return False
    return hmac.compare_digest(token, expected_token.strip())


def unauthorized_bearer_response() -> Response:
    response = json_error("Invalid or missing bearer token.", 401)
    response.headers.setdefault("WWW-Authenticate", 'Bearer realm="chatmock"')
    return response
