import threading
import datetime
import time
import sqlite3
import asyncio
from aiogram import Bot
from telegram.ext import *


conn=sqlite3.connect("database.db",check_same_thread=False)
cursor = conn.cursor()


current_name = None
current_date = None
bot_token = '6398719762:AAF7WSsW5xWsvrc-iCdxts7-z3IDYDs782E'



async def start_commmand(update, context):
    await update.message.reply_text("Hey there! If you'd like to set up a new reminder, just type /new. I'm here to help!")
    

async def new_reminder(update, context):
    await update.message.reply_text('Whose birthday should I help you remind?')
    return 1


async def get_name(update,context):
    global current_name
    current_name = update.message.text
    await update.message.reply_text('When is the birthday? Please give me the date in the format Year-Month-Day so I can set the reminder correctly.'
                                    ' (Year-Month-Day) ?')
    return 2


async def get_date(update,context):
    global current_date
    global cursor
    
    current_date = update.message.text
    user_id = update.message.from_user.id 
  
    cursor.execute("SELECT * FROM user WHERE id = ?",(user_id,))
    
    if not cursor.fetchone():
        cursor.execute("INSERT INTO user (id) VALUES (?)",(user_id,))
        
    cursor.execute("INSERT INTO birthday_reminder (user_id, name, date, reminded) VALUES(?, ?, ?, ?)",(user_id, current_name, current_date,0 ))

    conn.commit()
    await update.message.reply_text("sure i will remined you.....")
    return ConversationHandler.END

async def cancel(update, context):
    await update.message.reply_text("Reminder conversation canceled.")
    return ConversationHandler.END
    

#reminder
def do_reminders():
    while True:
        
        cursor.execute("SELECT * FROM birthday_reminder WHERE strftime('%d', date) = strftime('%d', 'now')"
                       "AND strftime('%m',date) = strftime('%m','now') AND reminded = 0")
                      
        
        rows = cursor.fetchall()
        for row in rows:
            row_id = row[0]
            name = row[2]
            user_id = row[4]
            
            
            #msg sending
            async def send_telegram_message(bot_token, user_id, message):
                bot = Bot(token=bot_token)
                await bot.send_message(chat_id=user_id, text=message)
                print("Message sent successfully!")

            async def main():
                
                target_user_id = user_id
                message = f"It's {name}'s birthday today!"
            
                
                await send_telegram_message(bot_token, target_user_id, message)

            asyncio.run(main())

            
            cursor.execute("UPDATE birthday_reminder SET reminded = 1 WHERE id = ? ",(row_id,))
            
            
            conn.commit()
        time.sleep(10)
        
    
        
            


conv_handler = ConversationHandler(
        entry_points=[CommandHandler("new", new_reminder)],
        states= {
            1:[MessageHandler(filters.TEXT, get_name)],
            2:[MessageHandler(filters.TEXT, get_date)]
            
            
            
        },
        
        fallbacks=[CommandHandler("cancel",cancel)]
        )





#####------run function------------------#########

application = Application.builder().token(bot_token).build()

    # Commands
    #start
    
application.add_handler(CommandHandler('start', start_commmand))
application.add_handler(conv_handler)

threading.Thread(target = do_reminders).start()
 
    # Run bot
application.run_polling(1.0)

