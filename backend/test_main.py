# test_main.py
import pytest
import httpx
from main import app


@pytest.mark.asyncio
async def make_http_request(
    method: str,
    url: str,
    headers: dict = None,
    params: dict = None,
    json: dict = None,
) -> httpx.Response:
    """
    Effettua una richiesta HTTP asincrona utilizzando httpx.AsyncClient.
    """

    async with httpx.AsyncClient(app=app, base_url="http://test") as async_client:
        # Definisci il metodo della richiesta
        if method == "GET":
            return await async_client.get(url, headers=headers, params=params)
        elif method == "POST":
            return await async_client.post(
                url, headers=headers, params=params, json=json
            )
        elif method == "PATCH":
            return await async_client.patch(
                url, headers=headers, params=params, json=json
            )
        elif method == "DELETE":
            return await async_client.delete(
                url, headers=headers, params=params, json=json
            )
