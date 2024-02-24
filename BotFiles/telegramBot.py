from datetime import datetime
import telebot
from .generalFunctions import *
import os

telegram_bot_running = False

def telegram_bot():
    global telegram_bot_running
    if telegram_bot_running:
        return
    # Token for the bot
    BASE_DIR = os.path.join(os.getcwd(), "static", "assets")
    user_data = read_json_file(os.path.join(BASE_DIR, "userData.json"))
    TOKEN = user_data['telegram-api']
    PASSWORD = user_data['telegram-password']
    DRIVERS = user_data['drivers']
    DRIVERS_CHAT_ID = [driver['chat_id'] for driver in DRIVERS]

    # Create a bot object
    bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

    def get_current_date():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_driver_name_by_chat_id(chat_id):
        for driver in DRIVERS:
            if driver['chat_id'] == chat_id:
                return driver['surname']
        return None

    @bot.message_handler(commands=['start'])
    def start(message):
        if message.chat.id in DRIVERS_CHAT_ID:
            bot.send_message(message.chat.id, "Welcome back " + get_driver_name_by_chat_id(message.chat.id))
        else:
            bot.send_message(message.chat.id, "Welcome to the bot")
            bot.send_message(message.chat.id, "Please enter your password to verify")
            bot.register_next_step_handler(message, get_password)

    def get_password(message):
        if message.text == PASSWORD:
            bot.send_message(message.chat.id, "Please enter your surname")
            bot.register_next_step_handler(message, get_surname)
        else:
            bot.send_message(message.chat.id, "Wrong password, please try again")
            bot.register_next_step_handler(message, get_password)

    def get_surname(message):
        details = {
            "chat_id": message.chat.id,
            "surname": str(message.text).strip().title(),
            "date": get_current_date()
        }

        DRIVERS.append(details)
        DRIVERS_CHAT_ID.append(details['chat_id'])

        write_json_file(os.path.join(BASE_DIR, "userData.json"), user_data)

        details_message = f"Chat ID: {details['chat_id']}\nSurname: {details['surname']}\nDate: {details['date']}"
        bot.send_message(message.chat.id, details_message)
        bot.send_message(message.chat.id, "Thank you for using the bot")

    print("Bot is running...")
    telegram_bot_running = True

    bot.infinity_polling()
