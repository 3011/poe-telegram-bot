import time
import logging
import yaml
from telegram import (
    Update,
)
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
from telegram.constants import ParseMode
import poe_bot


"""===== Config ====="""
with open("config.yml", "r") as f:
    config_data = yaml.safe_load(f)
bot_token = config_data["bot_token"]
allowed_users = config_data["allowed_users"]
message_update_time = config_data["message_update_time"]


need_set_token = True
current_bot_code = "chinchilla"
bot_code_to_name_dict = {
    "capybara": "Sage",
    "hutia": "NeevaAI",
    "a2_2": "Claude+",
    "a2": "Claude-instant",
    "beaver": "GPT-4",
    "nutria": "Dragonfly",
    "chinchilla": "ChatGPT",
    "acouchy": "Google-PaLM",
}

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def check_user_id(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in allowed_users:
            await update.message.reply_text(text="You are not allowed to use this bot.")
            return
        return await func(update, context)

    return wrapper


def check_token_set(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if need_set_token:
            await update.message.reply_text(text="Please set token first.")
            return
        await func(update, context)

    return wrapper


@check_user_id
@check_token_set
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text="Poe is ready.")


@check_user_id
@check_token_set
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    reply_message = await update.message.reply_text(
        text="%s is typing..." % bot_code_to_name_dict[current_bot_code]
    )

    try:
        prev_time = time.time()
        prev_reply_text = ""
        for is_done, reply_text in poe_bot.get_reply_stream(current_bot_code, message):
            if is_done:
                try:
                    if prev_reply_text != reply_text:
                        await reply_message.edit_text(
                            text=reply_text,
                            parse_mode=ParseMode.MARKDOWN,
                        )
                except:
                    try:
                        await reply_message.edit_text(
                            text="[Default ParseMode]\n" + reply_text,
                        )
                    except Exception as err:
                        await reply_message.edit_text(
                            text="Error: %s" % err,
                        )

            else:
                if time.time() - prev_time > message_update_time and reply_text:
                    prev_time = time.time()
                    try:
                        await reply_message.edit_text(
                            text=reply_text,
                        )
                        prev_reply_text = reply_text
                    except Exception as err:
                        await reply_message.edit_text(
                            text="Error: %s" % err,
                        )

    except Exception as err:
        await reply_message.edit_text(
            text="Error: %s" % err,
        )


@check_user_id
async def set_token(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        token = update.message.text.split(" ")[1]
        poe_bot.set_token(token)
        global need_set_token
        need_set_token = False
        await update.message.reply_text(text="Token set.")
    except Exception as err:
        await update.message.reply_text(text="Token set failed. \nError: %s" % err)


@check_user_id
@check_token_set
async def set_bot_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_name_to_code_dict = {
        "sage": "capybara",
        "neevaai": "hutia",
        "claude_plus": "a2_2",
        "claude_instant": "a2",
        "gpt4": "beaver",
        "dragonfly": "nutria",
        "chatgpt": "chinchilla",
        "google_palm": "acouchy",
    }

    global current_bot_code
    current_bot_code = bot_name_to_code_dict[update.message.text.split("/")[1]]
    await update.message.reply_text(
        text="Bot is %s." % bot_code_to_name_dict[current_bot_code]
    )


@check_user_id
@check_token_set
async def clear_context(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        poe_bot.clear_context(current_bot_code)
        await update.message.reply_text(text="Conversation context cleared.")
    except Exception as err:
        await update.message.reply_text(
            text="Conversation context clear failed. \nError: %s" % err
        )


@check_user_id
@check_token_set
async def rollback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # try:
        #     count = int(update.message.text.split(" ")[1])
        # except:
        count = 1
        poe_bot.purge_conversation(current_bot_code, count)
        await update.message.reply_text(text=f"Rollback {count} message(s) succeeded.")
    except Exception as err:
        await update.message.reply_text(
            text="Rollback {count} message(s) failed. \nError: %s" % err
        )


if __name__ == "__main__":
    application = ApplicationBuilder().token(bot_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("set_token", set_token))
    application.add_handler(CommandHandler("clear_context", clear_context))
    application.add_handler(CommandHandler("rollback", rollback))

    application.add_handler(CommandHandler("sage", set_bot_name))
    application.add_handler(CommandHandler("claude_instant", set_bot_name))
    application.add_handler(CommandHandler("chatgpt", set_bot_name))
    application.add_handler(CommandHandler("claude_plus", set_bot_name))
    application.add_handler(CommandHandler("neevaai", set_bot_name))
    application.add_handler(CommandHandler("gpt4", set_bot_name))
    application.add_handler(CommandHandler("dragonfly", set_bot_name))
    application.add_handler(CommandHandler("google_palm", set_bot_name))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    application.run_polling()
