import asyncio
import requests

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from os import getenv
from dotenv import load_dotenv

router = Router()

load_dotenv()
API_KEY = getenv("API_KEY")
WEATHER_URL = getenv("WEATHER_URL")


class HumidityState(StatesGroup):
    waiting_for_city = State()


@router.message(Command("humidity"))
async def weather_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🌤 Влажность какого города вы хотите узнать?\n"
        "(Вводить название города на латинице)"
    )
    await state.set_state(HumidityState.waiting_for_city)


def fetch_weather(city: str):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru",
    }

    response = requests.get(WEATHER_URL, params=params, timeout=10)

    if response.status_code != 200:
        return None

    return response.json()


@router.message(HumidityState.waiting_for_city)
async def get_weather(message: Message, state: FSMContext):
    city = message.text.strip()

    
    data = await asyncio.to_thread(fetch_weather, city)

    if not data:
        await message.answer("❌ Город не найден, попробуйте ещё раз")
        return

    text = (
        f"🌍 <b>{data['name']}</b>\n"
        f"💧 Влажность: {data['main']['humidity']}%\n"
    )

    await message.answer(text)
    await state.clear()
