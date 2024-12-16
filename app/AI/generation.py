# Asynchronous Example
import asyncio
from mistralai import Mistral
import os

async def generate(content):
    async with Mistral(
        api_key=os.getenv('AI_TOKEN'),
    ) as s:
        res = await s.chat.complete_async(model="mistral-large-latest", messages=[
            {
                "content": content,
                "role": "user",
            },
        ])

        if res is not None:
            return res
        return res