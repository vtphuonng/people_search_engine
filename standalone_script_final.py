import logging
import psycopg2
import psycopg2.extras
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater
from queue import Queue
from telegram import ChatAction
import time

update_queue = Queue()

# --- Configuration ---
DATABASE_CONFIG = {
    'database': 'residentinformation',
    'user': 'pps_admin',
    'password': 'pps_Admin!23$%',
    'host': 'localhost',
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
            
                cur.execute(query, params)
                columns = [desc[0] for desc in cur.description]
                rows = cur.fetchall()
                result_dict = {column: [] for column in columns}
                for row in rows:
                    for i in range(len(columns)):
                        result_dict[columns[i]].append(row[i])
                filtered_dict = {key: value for key, value in result_dict.items() if any(value)}
                return filtered_dict

# --- Search Functions ---
def search_phonenumber(phone_number):
    time.sleep(2)
    phone_number = str(phone_number)
    if phone_number.startswith('0'):
        phone_number = phone_number.replace('0', '+84', 1)
    query = f"""
            SELECT * 
            FROM peopledata.person_full 
            WHERE phone ->> 0 = '{phone_number}'; 
            """
    filtered_dict = execute_query(query)

    response = "Search results:\n"
    if filtered_dict:
        for key, values in filtered_dict.items():
            response += f"{key}: {', '.join(map(str, values))}\n"
    else:
        response = "No results found for that phone number."

    return response

def search_facebook(uid_or_phone):
    time.sleep(2)
    query = f"""
            SELECT * from peopledata.socialnetworkprofile s
            WHERE s.fbuid ->> 0 = '{uid_or_phone}'
            or s.fbuid ->> '$numberLong' = '{uid_or_phone}'
            or s.fbuid ->> '$numberInt' = '{uid_or_phone}'
            """
    filtered_dict = execute_query(query)
    respone_str = 'Facebook search result:\n'
    if filtered_dict:
        for key, values in filtered_dict.items():
            respone_str += f"{key}: {', '.join(map(str, values))}\n"
    else:
        respone_str = "No Facebook profiles found."
    return respone_str

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
    time.sleep(2)
    query = f"""
                SELECT *
                FROM peopledata.person_full 
                WHERE address ->> 'street' like '%{location.title()}%'
                LIMIT 1; 
                """      
    results = execute_query(query)

    response = "Search results:\n"
    if results:
        for key, values in results.items():
            response += f"{key}: {', '.join(map(str, values))}\n"
    else:
        response = f"No profiles found for location {location.title()}"
    return response

def search_mailaddress(email):
    time.sleep(2)
    query = """
            SELECT *
            FROM peopledata.person_full 
            WHERE email->> 0 = %s; 
            """
    results = execute_query(query, (email,))

    response = "Email Search Results:\n"
    if results:
        for key, values in results.items():
            response += f"{key}: {', '.join(map(str, values))}\n"
    else:
        response = "No profiles found for that email."
    return response

def search_name(name):
    time.sleep(2)
    query = """
            SELECT *
            FROM peopledata.person_full 
            WHERE name = %s; 
            """
    results = execute_query(query, (name,))

    response = "Name Search Results:\n"
    if results:
        for key, values in results.items():
            response += f"{key}: {', '.join(map(str, values))}\n"
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
        '/search_mailaddress <địa chỉ email>\n' 
        '/search_name <họ và tên>'    
    )

def handle_search_phonenumber(update: Update, context: CallbackContext) -> None:
    if context.args:
        phone_number = context.args[0]
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

        response = search_phonenumber(phone_number)
        update.message.reply_text(response)
    else:
        update.message.reply_text("Vui lòng cung cấp số điện thoại.")

def handle_search_facebook(update: Update, context: CallbackContext):
    if context.args:
        uid_or_phone = context.args[0]
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
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
    #location = [param.strip() for param in context.args[0].split(',')]
    if context.args:
        location = context.args
        location = ' '.join(location)
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
        response = search_location(location)
        update.message.reply_text(response)
    else:
        update.message.reply_text("Vui lòng cung cấp địa chỉ cư trú.")

def handle_search_mailaddress(update: Update, context: CallbackContext) -> None:
    if context.args:
        email = context.args[0]
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
        response = search_mailaddress(email)
        update.message.reply_text(response)
    else:
        update.message.reply_text("Vui lòng cung cấp địa chỉ email.")

def handle_search_name(update: Update, context: CallbackContext) -> None:
    if context.args:
        name = context.args
        name = ' '.join(name)
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
        response = search_name(name)
        update.message.reply_text(response)
    else:
        update.message.reply_text("Vui lòng cung cấp tên.")

# --- Main Function ---
def main():
    updater = Updater('7086978759:AAEpwfTwit1J7hqG6qxRXRxiJVi6HL-xJ_0') 
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("search_phonenumber", handle_search_phonenumber))
    dp.add_handler(CommandHandler("search_facebook", handle_search_facebook))
    dp.add_handler(CommandHandler("search_instagram", handle_search_instagram))
    dp.add_handler(CommandHandler("search_location", handle_search_location,pass_args=True))
    dp.add_handler(CommandHandler("search_mailaddress", handle_search_mailaddress))
    dp.add_handler(CommandHandler("search_name", handle_search_name))

    

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    #print(search_facebook(100003986334132))
    main()