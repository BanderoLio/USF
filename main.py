import logging
import random
import datetime
import os
import json
import pytz
import psycopg2

from enum import Enum
from functools import wraps
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import MessageLimit, ChatMemberStatus
from telegram.ext import filters, ApplicationBuilder, CallbackQueryHandler
from telegram.ext import MessageHandler, CommandHandler
from telegram.ext import CallbackContext, ConversationHandler
from states import States
from catgirl import CatgirlDownloader


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


class State(Enum):
    MENU = 0
    GENERATE = 1
    SETTINGS = 2
    CHANGE_MOD = 3


def admin_only(func):
    @wraps(func)
    async def wrapped(update: Update, context: CallbackContext,
                      *args, **kwargs):
        user = await context.bot.get_chat_member(
            chat_id=update.effective_chat.id,
            user_id=update.effective_user.id
        )

        if user.status in [ChatMemberStatus.ADMINISTRATOR,
                           ChatMemberStatus.OWNER]:
            return await func(update, context, *args, **kwargs)
        else:
            await update.message.reply_text("Эта команда"
                                            " только для администраторов")
            return
    return wrapped


async def start(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="фонтанам usf привет,"
                                   "остальным соболезнуем")


async def hello_world(context: CallbackContext):
    await context.bot.send_sticker(-1002257016094,
                                   'CAACAgIAAxkBAAENdaFnfUjE83DOiuwvBe'
                                   '-a24lA3Z5gQAAC5UgAAhplQUtrs_B3W6khOjYE')


@admin_only
async def add(update: Update, context: CallbackContext):
    id = update.effective_chat.id
    s = update.message.text
    if ' ' not in s:
        return
    s = s[s.find(' ') + 1:]
    print(f'{s} ::to add')
    states(id).append(s)
    states.save(id)

    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f'Пункт {len(states(id))} добавлен')


@admin_only
async def remove(update: Update, context: CallbackContext):
    id = update.effective_chat.id
    s = update.message.text
    if ' ' not in s:
        return
    s = s[s.find(' ') + 1:].strip()

    if not s.isdigit():
        return
    s = int(s) - 1
    if not 0 < s < len(states(id)):
        return
    states(id).pop(s)
    print(f'{s} ::to remove')
    states.save(id)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f'Пункт {s+1} был удалён')


async def catgirl(update: Update, context: CallbackContext):
    bot: Bot = context.bot
    await bot.send_photo(update.effective_chat.id,
                         CatgirlDownloader.get_image(nsfw=False))


async def jcat(update: Update, context: CallbackContext):
    bot: Bot = context.bot
    await bot.send_photo(update.effective_chat.id,
                         CatgirlDownloader.get_cat())


async def furry(update: Update, context: CallbackContext):
    bot: Bot = context.bot
    await bot.send_photo(update.effective_chat.id,
                         CatgirlDownloader.get_furry())


async def schedule_callback(update: Update, context: CallbackContext):
    bot: Bot = context.bot
    await bot.send_message(update.effective_chat.id,
                           f'РАСПОРЯДОК ДНЯ ФОНАТА ЮСФ\n'
                           f'{'\n'.join([' '.join(p) for p in schedule])}')


async def whatsnow(update: Update, context: CallbackContext):
    bot: Bot = context.bot

    def find_pos(arr: list, key):
        left, right = 0, len(arr) - 1
        while left <= right:
            mid = left + (right-left)//2
            if key < arr[mid]:
                right = mid - 1
            else:
                left = mid + 1

        return left - 1

    key = datetime.datetime.now(tz=pytz.timezone('Europe/Moscow'))
    key = key.hour * 100 + key.minute
    pos = find_pos([int(x[0].split(':')[0]) * 100 + int(x[0].split(':')[1])
                    for x in schedule], key)
    await bot.send_message(update.effective_chat.id, ' '.join(schedule[pos]))


async def states_callback(update: Update, context: CallbackContext):
    id = update.effective_chat.id
    s = "\n".join(f'{i+1}. {state}' for i, state in enumerate(states(id)))
    max_len = MessageLimit.MAX_TEXT_LENGTH.value
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='Ну что, опять в копатель?')
    for i in range(len(s) // max_len + (1 if len(s) % max_len else 0)):
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=s[i*max_len:min((i+1)*max_len,
                                                            len(s))])


async def state(update: Update, context: CallbackContext):
    id = update.effective_chat.id
    bot: Bot = context.bot
    s = update.message.text
    s = s.strip().split()
    if len(s) != 1 or not s[0].isdigit():
        return

    s = int(s[0]) - 1
    if s < 0 or s >= len(states(id)):
        return
    await bot.send_message(update.effective_chat.id, f'{s+1}. {states(id)[s]}')


async def info(update: Update, context: CallbackContext):
    s = update.message.text.lstrip()
    idx = len("инфа") + 1
    bot: Bot = context.bot
    s = f'🔮 Вероятность того, что {s[idx:] if idx < len(s) else ""}' \
        f' — {random.randint(0, 100)}%'
    await bot.send_message(chat_id=update.effective_chat.id, text=s)


async def ato(update: Update, context: CallbackContext):
    bot: Bot = context.bot
    print(update.effective_chat.id)
    await bot.send_sticker(update.effective_chat.id,
                           'CAACAgIAAxkBAAENdZ1nfUh1_cVcnPUiQl1'
                           '-5CIwqCy5HQACnVQAAiD3AUmA9alLufD68TYE')


async def fagot(update: Update, context: CallbackContext):
    bot: Bot = context.bot
    chat = await bot.getChat(update.effective_chat.id)

    print(chat.active_usernames)

    await bot.send_message(chat_id=update.effective_chat.id,
                           text='пока хз')


async def main_menu(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Генерация",
                              callback_data=str(State.GENERATE))],
        [InlineKeyboardButton("Настройки (Администрация)",
                              callback_data=str(State.SETTINGS))]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите действие:', reply_markup=markup)
    return State.MENU


@admin_only
async def admin_menu(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Настройки",
                              callback_data=str(State.SETTINGS))]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите действие:', reply_markup=markup)
    return State.MENU


async def settings(update: Update, context: CallbackContext):
    q = update.callback_query
    await q.answer()
    keyboard = [
        [InlineKeyboardButton("NSFW Кошкодевочки",
                              callback_data=str(State.CHANGE_MOD))]
    ]
    await q.edit_message_text("Z", reply_markup=InlineKeyboardMarkup(keyboard))
    return State.SETTINGS


async def change(update: Update, context: CallbackContext):
    q = update.callback_query
    await q.answer()
    id = abs(update.effective_chat.id) // 100000
    nsfw = True
    try:
        cursor.execute(f"SELECT catgirl_nsfw FROM ztable WHERE id = {id}")
        nsfw = cursor.fetchone()
    except Exception:
        ...
    nsfw = not nsfw
    try:
        cursor.execute(f"INSERT INTO ztable (id, catgirl_nsfw) VALUES"
                             f"({id}, {nsfw}) ON CONFLICT (id) DO UPDATE SET"
                             f" catgirl_nsfw = EXCLUDED.catgirl_nsfw",
                            )
        conn.commit()
        await q.edit_message_text(f"Кошкодевочки++"
                                  f"в{"" if nsfw else "ы"}ключены")
    except psycopg2.Error as e:
        conn.rollback()
        print(f'Ошибка: {e}')


if __name__ == '__main__':
    dbname = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    assert (dbname and user and password)

    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host='db',
        port='5432'
    )

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ztable (
    id BIGSERIAL PRIMARY KEY,
    points TEXT[] DEFAULT '{}',
    catgirl_nsfw BOOLEAN NOT NULL DEFAULT FALSE
    )
""")

    conn.commit()

    print(f"Текущая рабочая директория: {os.getcwd()}")
    # TOKEN = os.getenv('TELEGRAM_TOKEN')
    TOKEN = '7017664204:AAEH1oHU5hWDt4T-HdJu9Tp7a0g9ZMhRRaI'
    app = ApplicationBuilder().token(TOKEN).build()

    states = States()

    schedule = None
    with open("schedule.json") as f:
        schedule = json.load(f)

    start_handler = CommandHandler('start', start)
    info_handler = MessageHandler(filters.TEXT & (~filters.COMMAND)
                                  & filters.Regex("(?i)^инфа +"),
                                  info)

    add_handler = CommandHandler('add', add)
    remove_handler = CommandHandler('remove', remove)
    catgirl_handler = CommandHandler('catty', catgirl)
    jcat_handler = CommandHandler('justcat', jcat)
    furry_handler = CommandHandler('furry', furry)
    schedule_handler = CommandHandler('USF_schedule', schedule_callback)
    whatsnow_handler = CommandHandler('whatsnow', whatsnow)

    states_handler = CommandHandler('points', states_callback)

    ato_handler = MessageHandler(filters.Regex("^ато$"), ato)

    fagot_handler = MessageHandler(filters.Regex("^кто пидор$"), fagot)

    state_handler = MessageHandler(filters.TEXT & ~filters.COMMAND
                                   & filters.Regex(r'^\d+$'), state)

    hello_time = datetime.time(4)

    app.add_handler(start_handler)
    app.add_handler(info_handler)
    app.add_handler(add_handler)
    app.add_handler(remove_handler)
    app.add_handler(catgirl_handler)
    app.add_handler(jcat_handler)
    app.add_handler(furry_handler)
    app.add_handler(schedule_handler)
    app.add_handler(whatsnow_handler)
    app.add_handler(states_handler)
    app.add_handler(ato_handler)
    app.add_handler(state_handler)
    app.add_handler(fagot_handler)

    admin_menu_handler = CommandHandler('admin_menu', admin_menu)
    app.add_handler(ConversationHandler(
        entry_points=[admin_menu_handler],
        states={
            State.MENU: [
                CallbackQueryHandler(settings,
                                     pattern=f'^{str(State.SETTINGS)}$')
            ],
            State.SETTINGS: [
                CallbackQueryHandler(change,
                                     pattern=f'^{str(State.CHANGE_MOD)}$')
            ]
        },
        fallbacks=[admin_menu_handler]
    ))

    app.job_queue.run_daily(
        hello_world,
        hello_time
    )

    try:
        app.run_polling()
    finally:
        cursor.close()
        conn.close()
