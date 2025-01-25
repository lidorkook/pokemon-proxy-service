import asyncio
import logging
import signal
import threading

from dotenv import load_dotenv
from flask import Flask
from pyngrok import ngrok
from pyngrok.conf import get_default

from app.stream_initializer import initialize_stream

from . import settings
from .config import load_config
from .logger import logger
from .routes import bp as routes_bp


def _create_app():
    app = Flask(__name__)
    app.register_blueprint(routes_bp)

    return app


def _cleanup_tunnel(*args, **kwargs):
    logger.info("shutting off")
    ngrok.kill()
    exit(0)


def _handle_shutting_down():
    signal.signal(signal.SIGINT, _cleanup_tunnel)
    signal.signal(signal.SIGTERM, _cleanup_tunnel)


async def start_stream(stream_url, app_url):
    try:
        logger.info("start_stream")
        await initialize_stream(
            base_url=stream_url, email="test@guard.io", app_url=app_url
        )
    except Exception as e:
        logger.exception(f"stream failed to initialize {e}")
        raise e


def run_flask_app(app):
    app.run(host="0.0.0.0", port=settings.PORT)


def _setup_ngrok_tunnel():
    auth_token = settings.NGROK_AUTHTOKEN
    if not auth_token:
        raise Exception("NGROK_AUTHTOKEN is required for local environment")
    pyngrok_config = get_default()
    pyngrok_config.auth_token = auth_token
    app_url = ngrok.connect(settings.PORT, pyngrok_config=pyngrok_config).public_url
    logger.info(f"Ngrok tunnel started at: {app_url}")
    logger.info("Service accessible at this URL during local development.")
    _handle_shutting_down()
    return app_url


def main():
    load_dotenv()
    stream_url = settings.STREAM_URL
    if not stream_url:
        raise Exception("STREAM_URL env var missing")
    load_config()

    if settings.IS_LOCAL:
        app_url = _setup_ngrok_tunnel()
    else:
        proxy_service_url = settings.PROXY_SERVICE_URL
        if not proxy_service_url:
            raise Exception("PROXY_SERVICE_URL for cloud environment")
        app_url = proxy_service_url
    print(f"App URL: {app_url}")

    app = _create_app()
    if settings.IS_LOCAL:
        app.logger.setLevel(logging.DEBUG)

    flask_thread = threading.Thread(target=run_flask_app, args=(app,))
    flask_thread.start()

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        loop.create_task(start_stream(stream_url, app_url))
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()


if __name__ == "__main__":
    main()
