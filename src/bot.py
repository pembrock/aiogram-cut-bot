import asyncio
import logging
import os
import sys
from config.config_reader import config

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message


# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message()
async def echo_handler(message: Message, bot: Bot) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        # check if message.audio is None
        if message.audio is None:
            await message.send_copy(chat_id=message.chat.id)
        else:
            await message.answer("It's audio message")

            user_directory = f"tmp/{message.from_user.id}"
            if not os.path.exists(user_directory):
                os.makedirs(user_directory)
            await bot.download(message.audio, destination=f"{user_directory}/{message.audio.file_name}")
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def main() -> None:
    # And the run events dispatching
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())