import pytest

from app.stream_initializer import initialize_stream


@pytest.mark.asyncio
async def test_initialize_stream(mocker):
    mocker.patch("httpx.AsyncClient.post", return_value=mocker.Mock(status_code=200))
    await initialize_stream(
        "http://example.com", "test@example.com", "http://public.url"
    )
