from dotenv import load_dotenv
import os
import data_scraper as ds
from telebot import types
import telebot as telebot


load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
NEWS_TOKEN = os.getenv('NEWS_TOKEN')


COMMAND_LIST = [
    r"/help  - shows the list of commands available",
    r"/start - starts the bot",
    r"/menu  - shows the menu"
]
user_state = dict()

replies = []
def set_user_state(user_id, state):
    user_state[user_id] = state

def get_user_state(user_id):
    return user_state.get(user_id, None)

bot = telebot.TeleBot(BOT_TOKEN)


def display_five_articles(articles, current_number=0):
    res = []
    for i in range(current_number, current_number + 5):
        res.append(articles[i]['title'])
    res = '\n'.join(res)
    return res

def handle_response(reply, message):
    try:
        if reply['status'] != 'ok':
            raise Exception 
    except Exception as e:
        bot.send_message(message.chat.id, reply['message'])
        set_user_state(message.from_user.id, None)
        
    else:
        
        set_user_state(message.from_user.id, "CHOOSING_ARTICLE")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        btns = [
            'Display'
        ]	
        markup.add(*btns)
        bot.send_message(message.chat.id, "Hit the button to display news",
                     reply_markup=markup)

 
 
@bot.message_handler(func=lambda message: get_user_state(message.from_user.id) == "CHOOSING_ARTICLE")
def display_article(message)->None:
    articles = [article for article in replies[0]['articles'][:10]]
    if message.text == 'Next 5 Articles' or message.text == 'Display':
        # msg = display_article(articles)
        res = []
        for i in range(5):
            res.append(articles[i]['title'])
        res = '\n\n'.join(res)
        bot.send_message(message.chat.id,res)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        btns = [
            '1',
            '2',
            '3',
            '4',
            '5',
        ]	
        markup.add(*btns)
        bot.send_message(message.chat.id, "Choose an article!",
                     reply_markup=markup)
    else:
        msg = articles[int(message.text) - 1]["url"]
        print(msg)
        bot.send_message(message.chat.id, msg)
        set_user_state(message.from_user.id, None)
        replies.pop()

        
    
        
    


@bot.message_handler(commands=['start'])
def send_welcome(message)->None:
    bot.reply_to(message, "Hi there, George!")
 
@bot.message_handler(commands=['help'])
def send_help(message)->None:
    msg = "\n".join(COMMAND_LIST)
    bot.send_message(message.chat.id, msg)

@bot.message_handler(commands=['menu'])
def show_menu(message)->None:
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    btns = [
        types.KeyboardButton("News"),
        types.KeyboardButton("AI"),
        types.KeyboardButton("IT"),
        types.KeyboardButton("Music"),
        types.KeyboardButton("Fashion"),
        types.KeyboardButton("Sport"),
        types.KeyboardButton("Enter category"),
    ]
    markup.add(*btns)
    bot.send_message(message.chat.id, "What would you like to read?",
                     reply_markup=markup)
    set_user_state(message.from_user.id, "CHOOSING_CATEGORY")
    # markup = types.ReplyKeyboardRemove(selective=False)
                                    

@bot.message_handler(func=lambda message: get_user_state(message.from_user.id) == "CHOOSING_CATEGORY")
def category_chooser(message):
    if message.text == 'Enter category':
        bot.send_message(message.chat.id, 'Please type your category:')
        set_user_state(message.from_user.id, "TYPING_CUSTOM_CATEGORY")
    else:
        # Handle predefined category selection
        bot.send_message(message.chat.id, f'Searching articles for {message.text}...')
        reply = ds.get_articles(message.text)
        replies.append(reply)
        handle_response(reply, message)
        # Optionally reset state


@bot.message_handler(func=lambda message: get_user_state(message.from_user.id) == "TYPING_CUSTOM_CATEGORY")
def custom_category_handler(message):
    # Handle custom category input
    bot.send_message(message.chat.id, f'Searching articles for your custom category: {message.text}')
    reply = ds.get_articles(message.text)
    replies.append(reply)
    handle_response(reply, message)
    
    # Optionally reset state




@bot.message_handler(func=lambda message: True)
def default_idle(message)->None:	
    bot.reply_to(message, "If you want to read an article please use the\
    menu or type /help for more information")
    set_user_state(message.from_user.id, None)

    


if __name__ == "__main__":
    print("Start")
    bot.infinity_polling()