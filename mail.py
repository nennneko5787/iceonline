import asyncio
import httpx

client = httpx.AsyncClient()


async def main():
    response = await client.post(
        "https://iceonline.azurewebsites.net/User/GetMailList",
        headers={"content-type": "application/json; charset=utf-8"},
        json={"user_index": "1955121"},
    )

    print(response.json())


asyncio.run(main())
