import telegram
import random
import requests
import logging
from telegram import Update
import os
from telegram.ext import Updater,CommandHandler, MessageHandler, Filters,ConversationHandler
from bs4 import BeautifulSoup
from dbhelper import DBHELPER 
db=DBHELPER()
NOTES=range(1)
def savenotes(update,text):
  update.message.reply_text("alright! what you wanna save? just type it...type /cancel to cancel")
  return NOTES
def notes(update,context):
  items=db.get_items()
  if update.message.text in items:
    db.delete_items(update.message.text)
    items=db.get_items()
  else:
    db.add_item(update.message.text)
  update.message.reply_text("ok saved!")  
  return ConversationHandler.END 
def getnotes(update,context):
  items=db.get_items()
  update.message.text="\n".join(items)
  update.message.reply_text(update.message.text)
def cancel(update,context):
  update.message.reply_text("cool")
  return ConversationHandler.END


PORT = int(os.environ.get('PORT', 5000))

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
def echo(update, context):
    if update.message.text in text1:
       update.message.reply_text(random.choice(text2))
    elif update.message.text in dogggg:
      update.message.reply_photo(dogurl)
    elif update.message.text in wikitext:
      update.message.reply_text("I hope you like this article...\n"+wikii["content_urls"]["desktop"]["page"])
    elif update.message.text=="Dictionary":
      update.message.reply_text("Just type the your word with '/' \nFor example /islam")
    else:
      url="https://www.oxfordlearnersdictionaries.com/definition/english/"+update.message.text
      page=requests.get(url)
      soup=BeautifulSoup(page.text,'html.parser')
      defi=soup.find('span',{'class': 'def'}).text 
      update.message.reply_text(defi)
      mp3=soup.find('div',{'class': 'sound audio_play_button pron-uk icon-audio'}).get('data-src-mp3')
      update.message.reply_voice(mp3)
    
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    db.setup()
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher


    conv_hand=ConversationHandler(entry_points=[CommandHandler("savenotes",savenotes)],states={NOTES:[MessageHandler(Filters.text& ~Filters.command,notes)]},fallbacks=[CommandHandler("cancel",cancel)])
    dp.add_handler(conv_hand)
    dp.add_handler(CommandHandler('getnotes',getnotes))
    dp.add_handler(MessageHandler(Filters.text, echo))
    
    
    dp.add_error_handler(error)
    updater.start_webhook(listen="0.0.0.0",port=int(PORT),url_path=TOKEN)
    
    updater.bot.setWebhook('https://huk-huk.herokuapp.com/'+TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()