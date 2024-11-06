from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import asyncio
import time
import requests

# Словари для хранения языковых настроек и текстов
language_settings = {}

texts = {
    'ru': {
        'welcome': "😁Добро пожаловать в бота Кирито.\n🚆Этот бот может обрабатывать вопрос пользователя командой: /gpt.\n🧭Также присутствует команда: /ping - для проверки скорости бота.\n\n📚Для новых пользоватилей у нас есть гайд бук по использованию команд.\n✏️Просто напиши команду: /help и вам покажет гайд.",
        'help': "📨Ссылка на гайд: [Гайд](https://teletype.in/@shadow_red1/editor/nTys2trZ5Mj)!",
        'command_not_exist': "Такой команды не существует.",
        'lang_set_ru': "✅️Язык установлен на русский.",
        'lang_set_en': "✅️Language set to English.",
        'usage_gpt': "🌟Используйте: /gpt <ваш вопрос>",
        'site_link': "📎 Вот ссылка на наш сайт: [Сайт](http://100.101.14.39:8080)!",
    },
    'en': {
        'welcome': "😁Welcome to Kirito bot.\n🚆This bot can process user questions with the command: /gpt.\n🧭There's also a command: /ping to check the bot's speed.\n\n📚For new users, we have a guide book on how to use the commands.\n✏️Just type the command: /help and it will show you the guide.",
        'help': "📨Link to the guide: [Guide](https://teletype.in/@shadow_red1/editor/nTys2trZ5Mj)!",
        'command_not_exist': "Such a command does not exist.",
        'lang_set_ru': "✅️Язык установлен на русский.",
        'lang_set_en': "✅️Language set to English.",
        'usage_gpt': "🌟Usage: /gpt <your question>",
        'site_link': "📎 Here's the link to our site: [Site](http://100.101.14.39:8080)!",
    }
}

# Приветственное сообщение
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    lang = language_settings.get(user_id, 'ru')
    
    welcome_message = texts[lang]['welcome']

    await update.message.reply_text(
        welcome_message,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("ru🇷🇺", callback_data='lang_ru')],
            [InlineKeyboardButton("En🇱🇷", callback_data='lang_en')]
        ])
    )

# Команда Пинг
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    lang = language_settings.get(user_id, 'ru')

    start_time = time.time()  # Исправлено
    await update.message.reply_text(f"⏳️Измеряем время отклика..." if lang == 'ru' else f"⏳️Measuring response time...")
    end_time = time.time()
    ping_time = (end_time - start_time) * 1000

    await update.message.reply_text(f"🚀Скорость отклика: {ping_time:.2f} ms" if lang == 'ru' else f"🚀Response speed: {ping_time:.2f} ms")

# Команда .help/help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    lang = language_settings.get(user_id, 'ru')
    await update.message.reply_text(texts[lang]['help'], parse_mode='Markdown')

# Команда для ChatGPT
async def gpt_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = ' '.join(context.args).strip()
    if not question:
        reply = await update.message.get_reply_to_message()
        if reply:
            question = reply.text
        else:
            await update.message.reply_text("Вы не задали вопрос.")
            return

    prompt = [{"role": "user", "content": question}]
    await update.message.reply_text("Генерирую ответ...")

    try:
        response = requests.post('http://api.onlysq.ru/ai/v1', json=prompt)
        response_json = response.json()
        answer = response_json.get('answer', 'Не удалось получить ответ.')
        await update.message.reply_text(f"**Вопрос:** {question}\n**Ответ:** {answer}")
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка: {e}")

# Команда для сайта
async def site_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    lang = language_settings.get(user_id, 'ru')
    await update.message.reply_text(texts[lang]['site_link'], parse_mode='Markdown')

# Новый обработчик для выбора языка
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    
    # Устанавливаем язык в зависимости от нажатой кнопки
    if query.data == 'lang_ru':
        language_settings[user_id] = 'ru'
        await query.answer(texts['ru']['lang_set_ru'])
    elif query.data == 'lang_en':
        language_settings[user_id] = 'en'
        await query.answer(texts['en']['lang_set_en'])
    
    # Отправляем приветственное сообщение на выбранном языке
    await start(update, context)

# Обработка команд
async def command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command = update.message.text.strip().lower()  # Преобразуем в нижний регистр
    user_id = update.message.from_user.id

    # Убираем символ '/' из команды
    if command.startswith('/'):
        command = command[1:]

    # Проверяем команды без учета регистра
    if command in ("start", "старт", "s"):
        await start(update, context)
    elif command in ("ping", "пинг", "p"):
        await ping(update, context)
    elif command in ("help", "помощь", "хелп", "h"):
        await help_command(update, context)
    elif command in ("gpt", "гпт", "g"):
        await gpt_command(update, context)
    elif command in ("сайт", "site"):
        await site_command(update, context)  # Обработка команды "сайт"
    else:
        lang = language_settings.get(user_id, 'ru')
        await update.message.reply_text(texts[lang]['command_not_exist'])

# Основная функция для запуска бота
def main():
    application = ApplicationBuilder().token("7230239139:AAED6QitKSDs_K-ihYLQHJYH5C6OFg9LMEE").build()  # Замените на свой токен

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ping", ping))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("gpt", gpt_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, command_handler))
    
    # Обработчик нажатий на кнопки
    application.add_handler(CallbackQueryHandler(button_handler))

    asyncio.get_event_loop().run_until_complete(application.run_polling())

if __name__ == "__main__":
    main()

    #: cd /storage/emulated/0/Оооо 
    #: python my_botkirito.py
    #: 7230239139:AAED6QitKSDs_K-ihYLQHJYH5C6OFg9LMEE токен
    
