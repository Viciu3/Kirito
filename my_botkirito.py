from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Список готовых РП команд
ready_rp_commands = {
    "/spisok_cmd список": "— показывает этот список.",
    "/create1 добавь имя": "ваше имя или друга, подруги.",
    "/create2 dodaj nazwę": "ваше имя или друга, подруги.",
    "/create3 добавь імя": "ваше имя или друга, подруги.",        
    "/set_language (ru)-(pl)-(uk)": "ru end pl end uk"    
}

# Словарик для языков
language_responses = {
    "ru": {
        "start": "Привет! Я Кирито бот для использования РП команд. Используйте /spisok_cmd для просмотра доступных команд. Сменить язык можно командой /set_language.",
        "command_not_found": "Команда не найдена.",
        "command_list": "Доступные команды:\n"
    },
    "pl": {
        "start": "Cześć! Jestem botem Kirito do używania komend RP. Użyj /spisok_cmd, aby zobaczyć dostępne komendy. Możesz zmienić język za pomocą polecenia /set_language.",
        "command_not_found": "Komenda nie znaleziona.",
        "command_list": "Dostępne komendy:\n"
    },
    "uk": {
        "start": "Привіт! Я бот Кирито для використання РП команд. Використовуйте /spisok_cmd для перегляду доступних команд. Змінити мову можна командою /set_language.",
        "command_not_found": "Команду не знайдено.",
        "command_list": "Доступні команди:\n"
    }
}

user_languages = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(language_responses[user_languages.get(update.effective_chat.id, "ru")]["start"])

async def show_commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = user_languages.get(update.effective_chat.id, "ru")
    commands = language_responses[lang]["command_list"] + "\n".join(ready_rp_commands.keys())
    await update.message.reply_text(commands)

async def handle_rp_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.strip()
    response = ready_rp_commands.get(text, language_responses[user_languages.get(update.effective_chat.id, "ru")]["command_not_found"])
    await update.message.reply_text(response)

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args or context.args[0] not in ["ru", "pl","uk"]:
        await update.message.reply_text("Пожалуйста, укажите язык (ru / pl / uk). Пример: /set_language ru")
        return
    
    user_languages[update.effective_chat.id] = context.args[0]
    await update.message.reply_text(f"Язык установлен на {context.args[0]}.")
  
    # Изменение на filters
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_rp_command))

    application.run_polling()
async def create1_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = ' '.join(context.args)
    if not text:
         await update.message.reply_text('Пожалуйста, укажите текст. Пример использования: /create1 ваше имя.')
         return

    # Форматирование текста
    formatted_text1 = f""".....................................
.  _❤️❤️❤️_     _❤️❤️❤️_
./💋💋💋❤️\/❤️💋💋💋\.
.| ⛔️🔞🚭🔞⛔️🔞🚭🔞⛔️ |
.\ 🍓🍓🍓🍓🍓🍓🍓🍓  /
 .\       Я.     💥    Тебе.   /
  . \ ..люблю🥰{text}../
    . \🍫🍫🍫.🍫🍫🍫/
      . \¤¤¤¤¤¤¤¤¤/
         .\♡♡♡    ♡♡♡/
          . \□○□ □○□/
            . \●●●●●●/
               .\¡¡¡¡¡¡¡¡¡¡¡/
                 .\‽‽‽‽/
                   .\☆/
                     .\/"""
    await update.message.reply_text(formatted_text1)                     

async def create2_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = ' '.join(context.args)
    if not text:
         await update.message.reply_text('Podaj tekst. Przykładowe użycie: /create2 your name.')
         return                     
    formatted_text2 = f""".....................................
.  _❤️❤️❤️_     _❤️❤️❤️_
./💋💋💋❤️\/❤️💋💋💋\.
.| ⛔️🔞🚭🔞⛔️🔞🚭🔞⛔️ |
.\ 🍓🍓🍓🍓🍓🍓🍓🍓  /
 .\   Kocham.💥  cię.     /
  . \ ..{text}    🥰../
    . \🍫🍫🍫.🍫🍫🍫/
      . \¤¤¤¤¤¤¤¤¤/
         .\♡♡♡    ♡♡♡/
          . \□○□ □○□/
            . \●●●●●●/
               .\¡¡¡¡¡¡¡¡¡¡¡/
                 .\‽‽‽‽/
                   .\☆/
                     .\/"""
                     
    await update.message.reply_text(formatted_text2)                     

async def create3_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = ' '.join(context.args)
    if not text:
         await update.message.reply_text('Пожалуйста, укажіть текст. Прімер використання: /create3 ваше імя.')
         return
    formatted_text3 = f""".....................................
.  _❤️❤️❤️_     _❤️❤️❤️_
./💋💋💋❤️\/❤️💋💋💋\.
.| ⛔️🔞🚭🔞⛔️🔞🚭🔞⛔️ |
.\ 🍓🍓🍓🍓🍓🍓🍓🍓  /
 .\       Я.     💥    Тебе.   /
  . \ ..кохаю🥰{text}../
    . \🍫🍫🍫.🍫🍫🍫/
      . \¤¤¤¤¤¤¤¤¤/
         .\♡♡♡    ♡♡♡/
          . \□○□ □○□/
            . \●●●●●●/
               .\¡¡¡¡¡¡¡¡¡¡¡/
                 .\‽‽‽‽/
                   .\☆/
                     .\/"""                     
                     
    await update.message.reply_text(formatted_text3)                     
def main() -> None:
    application = ApplicationBuilder().token("7230239139:AAED6QitKSDs_K-ihYLQHJYH5C6OFg9LMEE").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("spisok_cmd", show_commands))
    application.add_handler(CommandHandler("set_language", set_language))
    application.add_handler(CommandHandler("create1", create1_message))
    application.add_handler(CommandHandler("create2", create2_message))
    application.add_handler(CommandHandler("create3", create3_message))
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_rp_command))

    application.run_polling()

if __name__ == '__main__':
    main()
    
    #: cd /storage/emulated/0/Оооо 
    #: python my_bot.py
    
    