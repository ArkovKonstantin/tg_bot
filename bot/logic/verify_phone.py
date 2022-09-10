import json
import logging

from telegram import __version__ as TG_VER, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

CONFIRM, CONTINUE = range(2)



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user phone number."""

    key = None
    arr = update.message.text.split()
    if len(arr) == 2:
        key = arr[1]

    context.user_data["key"] = key

    print("user_data1", context.user_data)

    contact_keyboard = KeyboardButton(text="Отправить номер телефона", request_contact=True)
    custom_keyboard = [[contact_keyboard]]

    reply_markup = ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True)
    await update.message.reply_text("Подтвердите номер телефона", reply_markup=reply_markup)

    return CONFIRM


async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Confirm phone number"""

    key = context.user_data['key']
    print("user_data1", context.user_data)

    logger.info("Contact %s", update.message.to_json())
    answer = json.loads(update.message.to_json())

    # verification of belonging phone number to user
    if answer["contact"]["user_id"] != answer["from"]["id"]:
        return ConversationHandler.END

    # send phone number to data bus

    phone_number = answer["contact"]["phone_number"]
    print("key", key)
    print("phone_number", phone_number)

    keyboard = [
        [InlineKeyboardButton("Продолжить", url="https://reg.eda.yandex.ru/placement")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Номер подтвержден",
        # reply_markup=ReplyKeyboardRemove(),
        reply_markup=reply_markup,
    )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)

    return ConversationHandler.END
async def continue_(update: Update, context: ContextTypes.DEFAULT_TYPE):

    pass

# Add conversation handler with the states
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        CONFIRM: [MessageHandler(filters.CONTACT, confirm)],
        # CONTINUE: [MessageHandler(filters.TEXT, continue_)],
        # CONFIRM: [MessageHandler(filters.CONTACT, confirm)],
        # CONFIRM: [MessageHandler(filters.CONTACT, confirm)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)


