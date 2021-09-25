# Implement By - @anasty17 (https://github.com/SlamDevs/slam-mirrorbot/pull/111)
# (c) https://github.com/SlamDevs/slam-mirrorbot
# All rights reserved

from telegram.ext import CommandHandler
from bot.helper.mirror_utils.upload_utils.gdriveTools import GoogleDriveHelper
from bot.helper.telegram_helper.message_utils import deleteMessage, sendMessage
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot import dispatcher


def countNode(update, context):
    args = update.message.text.split(" ", maxsplit=1)
    if len(args) > 1:
        link = args[1]
        msg = sendMessage(f"সাইজ হিসাব করা হচ্ছে: <code>{link}</code>", context.bot, update)
        gd = GoogleDriveHelper()
        result = gd.count(link)
        deleteMessage(context.bot, msg)
        if update.message.from_user.username:
            uname = f'@{update.message.from_user.username}'
        else:
            uname = f'<a href="tg://user?id={update.message.from_user.id}">{update.message.from_user.first_name}</a>'
        if uname is not None:
            cc = f'\n\n {uname} , এই হচ্ছে আপনার মোট ফাইল সাইজ'
        sendMessage(result + cc, context.bot, update)
    else:
        sendMessage("সাইজ হিসাব করার জন্য গুগল ড্রাইভের পাবলিক লিংক অথবা শেয়ার পারমিশন সহ লিংক প্রদান করুন.", context.bot, update)

count_handler = CommandHandler(BotCommands.CountCommand, countNode, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(count_handler)
