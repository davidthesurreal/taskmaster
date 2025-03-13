from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters
from telegram import Update, InlineKeyboardButton,InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from appwrite.client import Client
from appwrite.services.users import Users
from appwrite.services.databases import Databases


from actions import create_account
    
TOKEN: str = "8113951537:AAFYWMplTsiGD_J771vrmjhCO_tk43DfsEQ"

APPWRITE_KEY: str = "standard_d1d2a406cd91ce7a92c3bceaf25fed79bc3666a437b2f842eda2f2fb226cd6ebb1b337ee26b6dbf55f76ce5ed1359dfc419ced63ec998c3b0b0696f870e281d3d1683a682ac7057f9ddbb415948b586e4a224d7a5f31b8630a90c5a22d3af9c2aa3d71eda475ff3b99db23911a198d822b0d138f37ee5baba06782ce1e31de25"


client = Client()
client.set_endpoint('https://cloud.appwrite.io/v1')
client.set_project(APPWRITE_KEY) 

users = Users(client)




async def check_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text("Your balance is: 0")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  
  start_buttons = [
    [InlineKeyboardButton("Get Started",callback_data="get_started_btn")]
  ]
  
  start_markup = InlineKeyboardMarkup(start_buttons)
  
  
  reply_markup = InlineKeyboardMarkup(start_buttons)

  response = await create_account(users, str(update.message.from_user.id), update.message.from_user.first_name)

  print(response)
  await update.message.reply_text(
        "Welcome to TaskMaster! Please choose an option:",
        reply_markup=reply_markup
    )
  
  
  # first_name: str = update.message.chat.first_name
  # await update.message.reply_text(f"Hello {first_name}, Welcome to TaskMaster!", reply_markup=start_markup)
  
  

async def listen_for_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  query = update.callback_query
  await query.answer()
  
  if query.data == "get_started_btn":
    await query.message.reply_text("Hello again, welcome to TaskMaster, We provide a way to earn money through tasks, We support a variery of commands to ensure simplicity.")
  
  
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