from telegram.ext import Updater,CommandHandler, MessageHandler, Filters,ConversationHandler 
from coffeehouse import LydiaAI
lydia = LydiaAI("cd1389d58c70ea56987145f7011e0a05658873616e54c5ba14bf8f307a63367e9600fef02c39e1b0583c469a2be7c546fb97b6524f5a4790f7a3c17b81684808") 
session = lydia.create_session("en")
TOKEN="1274963738:AAE4oL0XaLure5sC5TNqu5kLX03f6euz4Y0" 
def chat(update,context): 
  output = session.think_thought(update.message.text)
  update.message.reply_text(output)
def main():
  updater = Updater(TOKEN, use_context=True) 
  dp = updater.dispatcher 
  dp.add_handler(MessageHandler(Filters.text,chat))
  updater.start_polling()
  updater.idle()
if __name__=='__main__':
  main()
