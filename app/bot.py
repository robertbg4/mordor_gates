import asyncio

from telebot.async_telebot import AsyncTeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from config import TELEGRAM_API_TOKEN
from gates import open_gates_inner, open_gates_outer


auth = 0
bot = AsyncTeleBot(TELEGRAM_API_TOKEN)

buttons = {}
markup = ReplyKeyboardMarkup(resize_keyboard=True)


def add_button(markup, button_text, button_callback):
    item = KeyboardButton(button_text)
    markup.add(item)
    buttons.update({button_text: button_callback})


async def button_inner(message):
    open_gates_inner()
    await bot.reply_to(message, "Открываю", reply_markup=markup)


async def button_outer(message):
    open_gates_outer()
    await bot.reply_to(message, "Открываю", reply_markup=markup)


async def button_exit(message):
    open_gates_inner()
    await bot.reply_to(message, "Открываю внутренние ворота", reply_markup=markup)
    await asyncio.sleep(113)
    open_gates_outer()
    await bot.reply_to(message, "Открываю внешние ворота", reply_markup=markup)


async def button_enter(message):
    open_gates_outer()
    await bot.reply_to(message, "Открываю внешние ворота", reply_markup=markup)
    await asyncio.sleep(113)
    open_gates_inner()
    await bot.reply_to(message, "Открываю внутренние ворота", reply_markup=markup)


add_button(markup, "Внутренние", button_inner)
add_button(markup, "Внешние", button_outer)
add_button(markup, "Выехать", button_exit)
add_button(markup, "Заехать", button_enter)


@bot.message_handler(commands=["start"])
async def start(message):
    await bot.reply_to(message, "Что открываем?", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
async def handle_text(message):
    if (handler := buttons.get(message.text.strip())) is None:
        await bot.reply_to(message, "Error", reply_markup=markup)
    else:
        await handler(message)


@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    await bot.reply_to(message, message.text)


asyncio.run(bot.polling())
