
"""
Simple Bot to reply to Telegram messages taken from the python-telegram-bot examples.
Deployed using heroku.
Author: liuhh02 https://medium.com/@liuhh02
"""
import telegram
import random
import requests
import logging
from telegram import Update
from telegram.ext import Updater,CommandHandler, MessageHandler, Filters
import os
PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = '1342071556:AAGA0MGRNEoRhwR8ej8l5V_wdqwva6XRxDU'

text1=["Hey","Hello","Hi","Howdy","Hi bot","Hey there","Hey bot","Hola"]
text2=["Hey😀","Helloo😄","Hohohaai...🤣"]
dogggg=["Dog photo","Can you send me dog photo?","What is dog?","Send dog photo","Photo of dog","Send dog","More dog"]
contents = requests.get('https://random.dog/woof.json').json()
dogurl=contents['url']
wikitext=["Article","Wiki","Wikipedia","Give me article","Read Article"]
resp = requests.get("https://en.wikipedia.org/wiki/Special:Random")
article_name = resp.url.split("/")[-1]
url1 = f"https://en.wikipedia.org/api/rest_v1/page/summary/{article_name}"
wikii=requests.get(url1).json()
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hello there!\nI am AI bot...\nchat with me anything...\n[please make sure your first letter is in caps]')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Tell... what help???')

def echo(update, context):
    if update.message.text in text1:
       update.message.reply_text(random.choice(text2))
    elif update.message.text in dogggg:
      update.message.reply_photo(dogurl)
    elif update.message.text in wikitext:
      update.message.reply_text("I hope you like this article...\n"+wikii["content_urls"]["desktop"]["page"])
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the bot
    updater.start_webhook(listen="0.0.0.0",port=int(PORT),url_path=TOKEN)
    
    updater.bot.setWebhook('https://duk-duk.herokuapp.com/'+TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
 

if __name__ == '__main__':
    main()