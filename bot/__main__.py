from bot.config import get_settings
from bot.logic import conv_handler
from telegram.ext import Application


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(get_settings().TOKEN).build()

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    print(get_settings().nats_uri)
    print(get_settings().TOKEN)

    main()
