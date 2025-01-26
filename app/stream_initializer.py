import asyncio

import httpx

from .auth import stream_secret
from .logger import logger


async def _call_stream_endpoint(client, endpoint, payload):
    logger.info(f"Calling stream endpoint: {endpoint}")
    while True:
        try:
            response = await client.post(endpoint, json=payload)
            response.raise_for_status()
            logger.info("Stream successfully initialized")
        except httpx.RequestError as e:
            logger.exception(f"Error initializing stream: {e}")
        await asyncio.sleep(60)  # Wait for 60 seconds before the next call


async def initialize_stream(base_url, email, app_url):
    endpoint = f"{base_url}/be/stream_start"
    payload = {
        "url": f"{app_url}/stream",
        "email": email,
        "enc_secret": stream_secret,
    }

    logger.info(f"stream request payload is {payload}")

    client = httpx.AsyncClient(timeout=httpx.Timeout(30))
    logger.info("Starting stream initialization")
    asyncio.create_task(_call_stream_endpoint(client, endpoint, payload))
