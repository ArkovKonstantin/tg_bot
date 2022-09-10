import json
import logging
import os

from telegram import __version__ as TG_VER, KeyboardButton

from bot.nats import provider

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

CONFIRM, = range(1)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user phone number."""

    contact_keyboard = KeyboardButton(text="Отправить номер телефона", request_contact=True)
    custom_keyboard = [[contact_keyboard]]

    reply_markup = ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True)
    await update.message.reply_text("Подтвердите номер телефона", reply_markup=reply_markup)

    return CONFIRM


async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Confirm phone number"""

    logger.info("Contact %s", update.message.to_json())
    answer = json.loads(update.message.to_json())

    # verification of belonging phone number to user
    if answer["contact"]["user_id"] != answer["from"]["id"]:
        return ConversationHandler.END

    # send phone number to data bus
    try:
        msg = answer["contact"]["phone_number"].encode()
        await provider.nc.publish(update.message.from_user.username, msg)
        # TODO receive ack
    except Exception as e:
        logger.info("Error while sending phone number: %s", e)
        return ConversationHandler.END

    await update.message.reply_text(
        "Номер подтвержден",
        reply_markup=ReplyKeyboardRemove(),
    )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)

    return ConversationHandler.END


# Add conversation handler with the states
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        CONFIRM: [MessageHandler(filters.CONTACT, confirm)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
