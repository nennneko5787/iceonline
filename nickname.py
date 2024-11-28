import asyncio
import json

import httpx

client = httpx.AsyncClient()


async def main():
    response = await client.post(
        "https://iceonline.azurewebsites.net/User/GetUserInfo",
        headers={"content-type": "application/json; charset=utf-8"},
        data=json.dumps({"nickname": "XxねんねこxX", "season": "-1"}),
    )
    print(response.json())


asyncio.run(main())
