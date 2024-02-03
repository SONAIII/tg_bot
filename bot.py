from dotenv import load_dotenv
import os
import telebot

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
NEWS_TOKEN = os.getenv('NEWS_TOKEN')


COMMAND_LIST = [
	r"/help  - shows the list of commands available",
	r"/start - starts the bot",
	r"/menu  - shows the menu"
]


bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message)->None:
	bot.reply_to(message, "Hi there, George!")
 
@bot.message_handler(commands=['help'])
def send_help(message)->None:
    msg = "\n".join(COMMAND_LIST)
    bot.send_message(message.chat.id, msg)

@bot.message_handler(func=lambda message: True)
def echo_all(message)->None:	
	bot.reply_to(message, message.text)

@bot.message_handler(commands=['menu'])
def show_menu(message)->None:
    bot.send_message(message.chat.id, "What would you like to read?")
    


if __name__ == "__main__":
    print("Start")
    bot.infinity_polling()