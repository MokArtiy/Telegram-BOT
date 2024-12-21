# Asynchronous Example
import asyncio
from mistralai import Mistral
import os

async def generate_ai(content):
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
    
async def generate_anecdote():
    async with Mistral(
        api_key=os.getenv('AI_TOKEN'),
    ) as s:
        res = await s.chat.complete_async(model="mistral-large-latest", messages=[
            {
                "content": "Расскажи анекдот",
                "role": "user",
            },
        ])

        if res is not None:
            return res
        return res

async def generate_presents(gender: str, age: str, hobby: str):
    async with Mistral(
        api_key=os.getenv('AI_TOKEN'),
    ) as s:
        res = await s.chat.complete_async(model="mistral-large-latest", messages=[
            {
                "content": f"Что подарить {gender}, которому(-ой) {age} лет и который(-ая) {hobby}?"
                           f"Составь список подарков из 10 пунктов, список должен выглядить так: в каждом пункте только наименование подарка без дополнительных пояснений",
                "role": "user",
            },
        ])

        if res is not None:
            return res
        return res