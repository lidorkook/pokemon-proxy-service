import signal

from pyngrok import ngrok
from pyngrok.conf import get_default

from . import settings
from .logger import logger


def _cleanup_tunnel(*args, **kwargs):
    logger.info("shutting off")
    ngrok.kill()
    exit(0)


def _handle_shutting_down():
    signal.signal(signal.SIGINT, _cleanup_tunnel)
    signal.signal(signal.SIGTERM, _cleanup_tunnel)


def setup_tunnel():
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
