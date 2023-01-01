from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ContextTypes
from convert import convert_value


async def inline_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id
    query = update.inline_query.query

    if query == '':
        return

    result = [
        InlineQueryResultArticle(
            id=update.inline_query.id,
            title=convert_value(user, query, False),
            input_message_content=InputTextMessageContent(
                message_text=convert_value(user, query, False)
                )
        )
    ]

    try:
        await update.inline_query.answer(result)
    except Exception as ex:
        print(ex)
