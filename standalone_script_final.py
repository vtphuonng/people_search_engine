import logging
import psycopg2
import psycopg2.extras
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater
from queue import Queue

update_queue = Queue()

# --- Configuration ---
DATABASE_CONFIG = {
    'database': 'residentinformation',
    'user': 'pps_admin',
    'password': 'pps_Admin!23$%',
    'host': '117.1.29.237',
    'port': 5432
}
BOT_TOKEN = "7086978759:AAEpwfTwit1J7hqG6qxRXRxiJVi6HL-xJ_0"

# --- Logging ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Database Functions ---
def connect_database():
    return psycopg2.connect(**DATABASE_CONFIG)

def execute_query(query, params=None):
    with connect_database() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            try:
                cur.execute(query, params)
                results = cur.fetchall()
                return results
            except (Exception, psycopg2.DatabaseError) as error:
                logger.error("Error in database operation: %s", error)
                return None

# --- Search Functions ---
def search_phonenumber(phone_number):
    query = """
            SELECT name, identitynumber, phone_number  
            FROM basicinformation 
            WHERE phone_number = %s; 
            """
    results = execute_query(query, (phone_number,))

    if results:
        response = "Search results:\n"
        for row in results:
            response += f"Name: {row['name']}\nIdentity Number: {row['identitynumber']}\nPhone Number: {row['phone_number']}\n\n"
    else:
        response = "No results found for that phone number."

    return response

def search_facebook(uid_or_phone):
    query = """
            SELECT name, uid, phone_number
            FROM socialnetworkprofile 
            WHERE uid = %s OR phone_number = %s; 
            """
    results = execute_query(query, (uid_or_phone, uid_or_phone))
    if results:
        response = "Facebook Search Results:\n"
        for row in results:
            response += f"Name: {row.get('name')}\nUID: {row['uid']}\nPhone: {row.get('phone_number')}\n\n"  
    else:
        response = "No Facebook profiles found."
    return response

def search_instagram(username):
    query = """
            SELECT username, name, bio 
            FROM socialnetworkprofile 
            WHERE username->>'username' = %s; 
            """
    results = execute_query(query, (username,))

    if results:
        response = "Instagram Search Results:\n"
        for row in results:
            response += f"Username: {row['username']}\nName: {row.get('name')}\nBio: {row.get('bio')}\n\n"
    else:
        response = "No Instagram profiles found."
    return response

def search_location(location):
    query = """
            SELECT name, location
            FROM socialnetworkprofile 
            WHERE location @> %s; 
            """
    results = execute_query(query, (location,))

    if results:
        response = "Location Search Results:\n"
        for row in results:
            response += f"Name: {row.get('name')}\nLocation: {row['location']}\n\n"
    else:
        response = "No profiles found for that location."
    return response

def search_mailaddress(email):
    query = """
            SELECT name, email
            FROM socialnetworkprofile 
            WHERE email->>'email' = %s; 
            """
    results = execute_query(query, (email,))

    if results:
        response = "Email Search Results:\n"
        for row in results:
            response += f"Name: {row.get('name')}\nEmail: {row['email']}\n\n"
    else:
        response = "No profiles found for that email."
    return response

# --- Telegram Bot Handlers ---
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'Chào mừng bạn! Sử dụng các lệnh sau để tra cứu thông tin: \n'
        '/search_phonenumber <số điện thoại>\n'
        '/search_facebook <uid/số điện thoại>\n'
        '/search_instagram <username Instagram>\n'
        '/search_location <vị trí>\n'
        '/search_mailaddress <địa chỉ email>'      
    )

def handle_search_phonenumber(update: Update, context: CallbackContext) -> None:
    if context.args:
        phone_number = context.args[0]
        response = search_phonenumber(phone_number)
        update.message.reply_text(response)
    else:
        update.message.reply_text("Vui lòng cung cấp số điện thoại.")

def handle_search_facebook(update: Update, context: CallbackContext) -> None:
    if context.args:
        uid_or_phone = context.args[0]
        response = search_facebook(uid_or_phone)
        update.message.reply_text(response)
    else:
        update.message.reply_text("Vui lòng cung cấp UID hoặc số điện thoại của tài khoản Facebook.")

def handle_search_instagram(update: Update, context: CallbackContext) -> None:
    if context.args:
        username = context.args[0]
        response = search_instagram(username)
        update.message.reply_text(response)
    else:
        update.message.reply_text("Vui lòng cung cấp username của tài khoản Instagram.")

def handle_search_location(update: Update, context: CallbackContext) -> None:
    if context.args:
        location = context.args[0]
        response = search_location(location)
        update.message.reply_text(response)
    else:
        update.message.reply_text("Vui lòng cung cấp địa chỉ cư trú.")

def handle_search_mailaddress(update: Update, context: CallbackContext) -> None:
    if context.args:
        email = context.args[0]
        response = search_mailaddress(email)
        update.message.reply_text(response)
    else:
        update.message.reply_text("Vui lòng cung cấp địa chỉ email.")

# --- Main Function ---
def main():
    updater = Updater('7086978759:AAEpwfTwit1J7hqG6qxRXRxiJVi6HL-xJ_0', update_queue=update_queue) 
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("search_phonenumber", handle_search_phonenumber))
    dp.add_handler(CommandHandler("search_facebook", handle_search_facebook))
    dp.add_handler(CommandHandler("search_instagram", handle_search_instagram))
    dp.add_handler(CommandHandler("search_location", handle_search_location))
    dp.add_handler(CommandHandler("search_mailaddress", handle_search_mailaddress))
    

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()