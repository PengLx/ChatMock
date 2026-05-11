from __future__ import annotations

import os

from flask import Flask, jsonify, request
from flask_sock import Sock

from .config import BASE_INSTRUCTIONS, GPT5_CODEX_INSTRUCTIONS
from .http import build_cors_headers, is_authorized_bearer, unauthorized_bearer_response
from .routes_openai import openai_bp
from .routes_ollama import ollama_bp
from .websocket_routes import register_websocket_routes


def create_app(
    verbose: bool = False,
    verbose_obfuscation: bool = False,
    reasoning_effort: str = "medium",
    reasoning_summary: str = "auto",
    reasoning_compat: str = "think-tags",
    fast_mode: bool = False,
    debug_model: str | None = None,
    expose_reasoning_models: bool = False,
    default_web_search: bool = False,
    api_key: str | None = None,
) -> Flask:
    app = Flask(__name__)

    app.config.update(
        VERBOSE=bool(verbose),
        VERBOSE_OBFUSCATION=bool(verbose_obfuscation),
        REASONING_EFFORT=reasoning_effort,
        REASONING_SUMMARY=reasoning_summary,
        REASONING_COMPAT=reasoning_compat,
        FAST_MODE=bool(fast_mode),
        DEBUG_MODEL=debug_model,
        BASE_INSTRUCTIONS=BASE_INSTRUCTIONS,
        GPT5_CODEX_INSTRUCTIONS=GPT5_CODEX_INSTRUCTIONS,
        EXPOSE_REASONING_MODELS=bool(expose_reasoning_models),
        DEFAULT_WEB_SEARCH=bool(default_web_search),
        API_KEY=api_key if isinstance(api_key, str) and api_key.strip() else os.getenv("CHATMOCK_API_KEY"),
    )

    @app.get("/")
    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.before_request
    def _require_bearer_auth():
        if request.method == "OPTIONS":
            return None
        if request.path in ("/", "/health"):
            return None
        expected_token = app.config.get("API_KEY")
        if is_authorized_bearer(request.headers.get("Authorization"), expected_token):
            return None
        return unauthorized_bearer_response()

    @app.after_request
    def _cors(resp):
        for k, v in build_cors_headers().items():
            resp.headers.setdefault(k, v)
        return resp

    app.register_blueprint(openai_bp)
    app.register_blueprint(ollama_bp)
    sock = Sock(app)
    register_websocket_routes(sock)

    return app
