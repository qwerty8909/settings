from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

token = "5445332563:AAFLddxllZ2YdDrnIM0eO8hjeLhmYneKveM"
openai_token = "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"

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)