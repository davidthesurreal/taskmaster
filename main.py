from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters
from telegram import Update, InlineKeyboardButton,InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from appwrite.client import Client
from appwrite.services.users import Users
from appwrite.services.databases import Databases
from appwrite.exception import AppwriteException


from actions import create_account
    
TOKEN: str = "8113951537:AAFYWMplTsiGD_J771vrmjhCO_tk43DfsEQ"

APPWRITE_KEY: str = "standard_d1d2a406cd91ce7a92c3bceaf25fed79bc3666a437b2f842eda2f2fb226cd6ebb1b337ee26b6dbf55f76ce5ed1359dfc419ced63ec998c3b0b0696f870e281d3d1683a682ac7057f9ddbb415948b586e4a224d7a5f31b8630a90c5a22d3af9c2aa3d71eda475ff3b99db23911a198d822b0d138f37ee5baba06782ce1e31de25"


client = Client()
client.set_endpoint('https://cloud.appwrite.io/v1')
client.set_project("67c8048d0000b428658b")
client.set_key(APPWRITE_KEY) 

users = Users(client)




async def check_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text("Your balance is: 0")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  
  start_buttons = [
    [InlineKeyboardButton("Help",callback_data="help_callback"), InlineKeyboardButton("Balance", callback_data="balance_callback")],
    [InlineKeyboardButton("Join Community", url="https://t.me/taskmastercommunity")],
    [InlineKeyboardButton("Get Task", callback_data="get_task_callback")]
  ]
  
  start_markup = InlineKeyboardMarkup(start_buttons)
  
  
  reply_markup = InlineKeyboardMarkup(start_buttons)

  first_name = update.message.from_user.first_name
  
  try:
    response = await create_account(users, str(update.message.from_user.id), first_name)

    await update.message.reply_text(
        f"Hello {first_name}, welcome to TaskMaster, We provide a way to earn money through tasks, We support a variery of commands to ensure simplicity",
        reply_markup=reply_markup
    )

    
  except AppwriteException as e:
    if e.code == 409:
      await update.message.reply_text(f"Welcome back, {first_name}", reply_markup=reply_markup)

    else: 
      await update.message.reply_text("Something went wrong, please try again later")

  
  
      
  
  
  # first_name: str = update.message.chat.first_name
  # await update.message.reply_text(f"Hello {first_name}, Welcome to TaskMaster!", reply_markup=start_markup)
  
  

async def listen_for_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  query = update.callback_query
  await query.answer()
  
  
  
  
def main():
  print("Starting bot...")
  app = Application.builder().token(TOKEN).build()
    
  print("Bot active!")
    
  app.add_handler(CommandHandler("start", start))
  app.add_handler(CallbackQueryHandler(listen_for_button_callback))

  app.add_handler(MessageHandler(filters.Text("Check Balance"), check_balance))
    
  app.run_polling()
    
    
    
if __name__ == '__main__':
  main()