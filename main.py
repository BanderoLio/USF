import logging
import random
import datetime
import os

from functools import wraps
from telegram import Update, Bot
from telegram.constants import MessageLimit, ChatMemberStatus
from telegram.ext import filters, ApplicationBuilder
from telegram.ext import MessageHandler, CommandHandler
from telegram.ext import CallbackContext
from states import States
from catgirl import CatgirlDownloader


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


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
                         CatgirlDownloader.get_image())


async def jcat(update: Update, context: CallbackContext):
    bot: Bot = context.bot
    await bot.send_photo(update.effective_chat.id,
                         CatgirlDownloader.get_cat())


async def states_callback(update: Update, context: CallbackContext):
    id = update.effective_chat.id
    s = "\n".join(f'{i+1}. {state}' for i, state in enumerate(states(id)))
    max_len = MessageLimit.MAX_TEXT_LENGTH.value
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
    s = update.message.text
    idx = s.find("инфа") + len("инфа") + 1
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


if __name__ == '__main__':
    print(f"Текущая рабочая директория: {os.getcwd()}")
    TOKEN = os.getenv('TELEGRAM_TOKEN')
    app = ApplicationBuilder().token(TOKEN).build()

    states = States()
    # with open("states.json") as f:
    #     states = json.load(f)

    start_handler = CommandHandler('start', start)
    info_handler = MessageHandler(filters.TEXT & (~filters.COMMAND)
                                  & filters.Regex("(?i)^инфа +"),
                                  info)

    add_handler = CommandHandler('add', add)
    remove_handler = CommandHandler('remove', remove)
    catgirl_handler = CommandHandler('catty', catgirl)
    jcat_handler = CommandHandler('justcat', jcat)

    states_handler = CommandHandler('points', states_callback)

    ato_handler = MessageHandler(filters.Regex("^ато$"), ato)

    fagot_handler = MessageHandler(filters.Regex("^кто пидор$"), fagot)

    state_handler = MessageHandler(filters.TEXT & ~filters.COMMAND
                                   & filters.Regex(r'^\d+$'), state)

    hello_time = datetime.time(7)

    app.add_handler(start_handler)
    app.add_handler(info_handler)
    app.add_handler(add_handler)
    app.add_handler(remove_handler)
    app.add_handler(catgirl_handler)
    app.add_handler(jcat_handler)
    app.add_handler(states_handler)
    app.add_handler(ato_handler)
    app.add_handler(state_handler)
    app.add_handler(fagot_handler)

    app.job_queue.run_daily(
        hello_world,
        hello_time
    )

    app.run_polling()
