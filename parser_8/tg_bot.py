import asyncio
import json
from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
from parser_8.config import token, user_id
from parser_8.main import check_news_update
from aiogram.dispatcher.filters import Text


bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["All news", "Last five news", "Fresh news"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("News", reply_markup=keyboard)


@dp.message_handler(Text(equals="All news"))
async def get_all_news(message: types.Message):
    with open("news.json", encoding="utf-8") as file:
        new_dict = json.load(file)

    for k, v in sorted(new_dict.items()):
        # news = f"<b>{datetime.fromtimestamp(v['article_date_timestamp'])}</b>\n" \
        #        f"<u>{v['article_title']}</u>\n" \
        #        f"<code>{v['article_desc']}</code>\n" \
        #        f"{v['article_url']}\n"

        # news = f"{hbold(datetime.fromtimestamp(v['article_date_timestamp']))}\n" \
        #        f"{hunderline(v['article_title'])}\n" \
        #        f"{hcode(v['article_desc'])}\n" \
        #        f"{hlink(v['article_title'], v['article_url'])}"

        news = f"{hbold(datetime.fromtimestamp(v['article_date_timestamp']))}\n" \
               f"{hlink(v['article_title'], v['article_url'])}"
        await message.answer(news)


@dp.message_handler(Text(equals="Last five news"))
async def get_last_five_news(message: types.Message):
    with open("news.json", encoding="utf-8") as file:
        new_dict = json.load(file)

    for k, v in sorted(new_dict.items())[-5:]:
        news = f"{hbold(datetime.fromtimestamp(v['article_date_timestamp']))}\n" \
               f"{hlink(v['article_title'], v['article_url'])}"

        await message.answer(news)


@dp.message_handler(Text(equals="Fresh news"))
async def get_fresh_news(message: types.Message):
    fresh_news = check_news_update()

    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items()):
            news = f"{hbold(datetime.fromtimestamp(v['article_date_timestamp']))}\n" \
                   f"{hlink(v['article_title'], v['article_url'])}"

            await message.answer(news)

    else:
        await message.answer("No fresh news yet!")


async def news_every_minute():
    while True:
        fresh_news = check_news_update()

        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items()):
                news = f"{hbold(datetime.fromtimestamp(v['article_date_timestamp']))}\n" \
                       f"{hlink(v['article_title'], v['article_url'])}"

                await bot.send_message(user_id, news, disable_notification=True)

        else:
            await bot.send_message(user_id, "No new fresh news...", disable_notification=True)

        await asyncio.sleep(300)


if __name__ == "__main__":
    # return current loop of events
    loop = asyncio.get_event_loop()
    loop.create_task(news_every_minute())
    executor.start_polling(dp)
