
import json
import requests
from module import send_welcome, handle_start_button, send_link
import telebot
from  telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton,  InlineQueryResultArticle,InputTextMessageContent
from telebot.apihelper import ApiException
import sqlite3
from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())
API_key = os.getenv("API_KOD")
bot_username = os.getenv("BOT_USERNAME")


bot = telebot.TeleBot(API_key)
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "I'm alive!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



bmd = "CAACAgIAAxkBAAIBlmdxZi6sK42VCA3-ogaIn30MXGrmAAJnIAACKVtpSNxijIXcPOrMNgQ"

holatbot = True


def setup_database_followers():
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS followers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_name TEXT,
            channel_url TEXT,
            num_follower INTEGER,
            now_follower INTEGER

        )
    ''')
    conn.commit()
    conn.close()

def setup_block_user():
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blockers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number_blok INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def setup_database_file_rus():
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files_rus (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_kod INTEGER,
            file_id TEXT,
            file_name TEXT,
            file_type TEXT

        )
    ''')
    conn.commit()
    conn.close()


def setup_database_file_eng():
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files_eng (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_kod INTEGER,
            file_id TEXT,
            file_name TEXT,
            file_type TEXT

        )
    ''')
    conn.commit()
    conn.close()


def setup_database_file():
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_kod INTEGER,
            file_id TEXT,
            file_name TEXT,
            file_type TEXT

        )
    ''')
    conn.commit()
    conn.close()

def save_file(file_kod, file_id, file_name,file_type):
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO files (file_kod, file_id, file_name, file_type)
        VALUES (?, ?, ?,?)
    ''', (file_kod, file_id, file_name,file_type))
    conn.commit()
    conn.close()

def save_file_eng(file_kod, file_id, file_name,file_type):
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO files_eng (file_kod, file_id, file_name, file_type)
        VALUES (?, ?, ?,?)
    ''', (file_kod, file_id, file_name,file_type))
    conn.commit()
    conn.close()

def save_file_rus(file_kod, file_id, file_name,file_type):
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO files_rus (file_kod, file_id, file_name, file_type)
        VALUES (?, ?, ?,?)
    ''', (file_kod, file_id, file_name,file_type))
    conn.commit()
    conn.close()

# Get file metadata from the database
def get_file(file_kod):
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    cursor.execute('SELECT  file_id, file_name, file_type FROM files WHERE file_kod = ?', (file_kod,))
    file = cursor.fetchall()
    conn.close()
    return file

def get_file_eng(file_kod):
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    cursor.execute('SELECT  file_id, file_name, file_type FROM files_eng WHERE file_kod = ?', (file_kod,))
    file = cursor.fetchall()
    conn.close()
    return file

def get_file_rus(file_kod):
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    cursor.execute('SELECT  file_id, file_name, file_type FROM files_rus WHERE file_kod = ?', (file_kod,))
    file = cursor.fetchall()
    conn.close()
    return file

def get_ani_kod(name):
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    cursor.execute('SELECT  id,file_kod,file_name  FROM files')
    fil = cursor.fetchall()
    l_a = []
    k = []
    for x in fil:
        if name in x[2].lower() and x[1] not in k:
            l_a.append(x)
            k.append(x[1])

    if len(l_a) == 0:
        l_a = [("Natija", "topilmadi.", "Natija topilmadi")]
    return l_a

def get_last_kod():
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    cursor.execute('SELECT  file_kod  FROM files')
    try:
        kod = max(cursor.fetchall())
    except:
        kod = [0]
    return kod

def get_last_kod_eng():
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    cursor.execute('SELECT  file_kod  FROM files_eng')
    try:
        kod = max(cursor.fetchall())
    except:
        return [0]
    return kod

def get_last_kod_rus():
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    cursor.execute('SELECT  file_kod  FROM files_rus')
    try:
        kod = max(cursor.fetchall())
    except:
        return [0]
    return kod

def show_anime_list():
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    cursor.execute('SELECT  file_kod, file_name  FROM files')
    names = cursor.fetchall()
    ls = ["Animelar Ro'yhati"]
    lr = []
    for x in names:
        if x not in lr:
            lr.append(x)
            ls.append(f"{x[0]}:  {x[1]}\n")
    return ls


def setup_database():
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE NOT NULL,
        username TEXT,
        first_name TEXT,
        last_name TEXT,
        join_date TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def setup_admin():
    conn = sqlite3.connect("bot_users.db",check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE NOT NULL,
        username TEXT,
        first_name TEXT,
        last_name TEXT,
        join_date TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def log_admin(user_id, username, first_name, last_name):
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT OR IGNORE INTO admins (user_id, username, first_name, last_name)
        VALUES (?, ?, ?, ?)
        """, (user_id, username, first_name, last_name))
        conn.commit()

    except sqlite3.Error as e:
        print("Error logging admin:", e)
    finally:
        conn.close()




# Count total users
def count_users():
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def setup_list_konkurs():
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS kon_users (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER UNIQUE NOT NULL, referrals INTEGER)""")
    conn.commit()
    conn.close()






def setup_yutuq():
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gifts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        gift_name TEXT
    )
    """)
    conn.commit()
    conn.close()





#Keyboards-------------------------

def get_control_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_st = types.KeyboardButton('📊Statistika')
    item_xy = types.KeyboardButton("📃Xabar yuborish")
    item_pt = types.KeyboardButton("📬Post tayyorlash")
    item_kn = types.KeyboardButton("🎁Ko'nkurs")
    item_as = types.KeyboardButton("🎥Anime sozlash")
    item_kl = types.KeyboardButton("📢Kanallar")
    item_ad = types.KeyboardButton("📋Adminlar")
    item_bh = types.KeyboardButton("🤖Bot holati")
    item_bc = types.KeyboardButton("◀️Orqaga")

    markup.row(item_st, item_xy)
    markup.row(item_pt, item_kn)
    markup.row(item_as, item_kl)
    markup.row(item_ad, item_bh)
    markup.row(item_bc)
    return markup

def main_keyboard(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_Ai = types.KeyboardButton('🔎Anime izlash')
    item_KN = types.KeyboardButton("🎁Konkurs")
    item_RK = types.KeyboardButton("💵Reklama va Homiylik")
    markup.row(item_Ai)
    markup.row(item_KN, item_RK)
    if is_admin(message.chat.id):
        item_BH = types.KeyboardButton(text="🛂Boshqaruv")
        markup.row(item_BH)
    return markup

def search_keyboard():
    tip_board = InlineKeyboardMarkup()
    butname = InlineKeyboardButton(text="🏷Nom orqali izlash", switch_inline_query_current_chat="")
    butkod = InlineKeyboardButton(text="📌Kod orqali izlash", callback_data="search_kod")
    butjanr = InlineKeyboardButton(text="💬Janr orqali qidirish", callback_data="search_janr")
    butlate = InlineKeyboardButton(text="⏱️So'nngi qo'shilganlar", callback_data="search_lates")
    butxit = InlineKeyboardButton(text="👁Eng ko'p ko'rilganlar", callback_data="search_xit")
    butlist = InlineKeyboardButton(text="📚Animelar ro'yhati", callback_data="show_list")
    tip_board.add(butname, butlate)
    tip_board.add(butjanr)
    tip_board.add(butkod, butxit)
    tip_board.add(butlist)
    return tip_board

def get_konkurs_keyboard():
    konkurs_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_YQ = types.KeyboardButton('🎁Yutuqlar')
    item_QA = types.KeyboardButton("📃Qoidalar")
    item_DE = types.KeyboardButton("⛔️To'xtatish")
    item_ST = types.KeyboardButton("🧩Boshlash")
    item_BC = types.KeyboardButton("◀️Orqaga")

    konkurs_keyboard.row(item_YQ,item_QA)
    konkurs_keyboard.row(item_ST,item_DE)
    konkurs_keyboard.row(item_BC)
    return konkurs_keyboard



def is_admin(user_id):
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admins")
    ids_of_admin = cursor.fetchall()
    for x in ids_of_admin:
        if user_id == x[1]:
            return True
    return False



# checking Inchannel----------------------------
channel_id = "@telegrabotkrito"

def check_user_in_channel(message):
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM followers")
    ll = cursor.fetchall()
    bo = len(ll)
    keyboard = InlineKeyboardMarkup()
    for c in ll:
        s: str = c[2]
        url1: str = f"@{s[13:]}"
        member = bot.get_chat_member(chat_id=url1, user_id=message.chat.id)
        if member.status not in ['member', 'administrator', 'creator']:
            keyboard.add(InlineKeyboardButton(text=c[1], url=c[2]))
        else:
            bo -= 1
    if bo > 0:
        start_button = InlineKeyboardButton("✅Tekshirish", callback_data="send_start")
        keyboard.add(start_button)

        bot.send_message(message.chat.id,
                         f"Assalomu alaykum \nAgar bizning xizmatlarimizdan foydalanmoqchi bo'lsangiz, Iltimos pastdagi kanallarga obuna bo'ling!",
                         reply_markup=keyboard)
        bot.send_sticker(message.chat.id, sticker=bmd)
        return False
    else:
        return True



# Starts bot--------------------------------------------------------------
@bot.callback_query_handler(func=lambda call: call.data == "send_start")
def a2(call):
    handle_start_button(call)
    send_welcome(call.message, konkurs_switch, kon_holat)

@bot.message_handler(commands = ['start'])
def a1(message):
    send_welcome(message, konkurs_switch, kon_holat)


#Anime Izlash ko'di--------------------------------------------------------

def say_sorry(message):
    bot.send_message(message.chat.id, "Uzr, bu xizmat vaqtinchalik ishlamayapti !")

@bot.callback_query_handler(func=lambda call: call.data == "search_kod")
def handle_kod_button(call):
    bot.answer_callback_query(call.id, "🔎Kod orqali qidirish boshlandi.\nAnime kodini kiriting...")

@bot.callback_query_handler(func=lambda call: call.data == "search_janr")
def handle_janr_button(call):
    bot.answer_callback_query(call.id, "🔎Janr orqali qidirish boshlandi.\nAnime janrini kiriting...")
    say_sorry(call.message)


@bot.callback_query_handler(func=lambda call: call.data == "search_lates")
def handle_late_button(call):
    bot.answer_callback_query(call.id, "Sending /Anime list...")
    roy:list = show_anime_list()
    roy.reverse()
    m = ""
    k = 0
    for i in roy:
        m += i + "\n"
        k += 1
        if k == 6:
            break
    bot.send_message(call.message.chat.id, m)

@bot.callback_query_handler(func=lambda call: call.data == "search_xit")
def handle_xit_button(call):
    bot.answer_callback_query(call.id, "Sending /Anime list...")
    roy = show_anime_list()
    m = ""
    k = 0
    for i in roy:
        m += i + "\n"
        k += 1
        if k == 6:
            break
    bot.send_message(call.message.chat.id ,m)



@bot.callback_query_handler(func=lambda call: call.data == "show_list")
def handle_list_button(call):
    bot.answer_callback_query(call.id, "Sending /Anime list...")
    roy = show_anime_list()
    m = ""
    for i in roy:
        m += ("🆔"+ i + "\n")

    m += "Ko'rmoqchi bo'lgan anime kodini kiriting !"
    bot.send_message(call.message.chat.id, m)


@bot.message_handler(func= lambda message: message.text == "🔎Anime izlash" and holatbot)
def relpy_search(message):
    if check_user_in_channel(message):
        bot.send_message(message.chat.id, "🔍Qidiruv tipini tanlang:", reply_markup= search_keyboard())



#💵Reklama va Homiylik--------------------------------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == "💵Reklama va Homiylik")
def show_adim(message):
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM admins""")
    adminlar = cursor.fetchall()
    mes_to_admin: str = "🫡Iltimos reklama va homiylik bo'yicha adminlarimizga murojat qiling.\n"
    for person in adminlar:

        mes_to_admin += f"{person[0]}."
        if person[2] != None:
            mes_to_admin += f" @{person[2]},"
        if person[3] != None:
            mes_to_admin += f" {person[3]},"
        if person[4] != None:
            mes_to_admin += f" {person[4]},"
        mes_to_admin += "\n"
    bot.send_message(message.chat.id, mes_to_admin)


#konkurs------------------------------------------------------------------------------
from koncurs import top_referrers_handler

@bot.callback_query_handler(func= lambda call: call.data == "show_list_kon")
def edit_text(call):
    top_referrers_handler(call.message)


@bot.message_handler(func= lambda message: message.text == "🎁Konkurs")
def k7(message):
    if check_user_in_channel(message):
        send_link(message, kon_holat)

#Boshqaruv paneli----------------

broadcast_mode = False
@bot.message_handler(func= lambda message: message.text == "🛂Boshqaruv")
def control(message):
    if is_admin(message.chat.id):
        bot.send_message(message.chat.id, "✅Siz admin ekanligingiz tasdiqlandi.",reply_markup= get_control_keyboard())
        bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAICmWd2qLc5grUQzAkIASgXwR4-jW1FAAKfGgAC43BwSQoc1Niaab0fNgQ")
    else:
        bot.send_message(message.chat.id, "❌Siz bu tizimdan foyadalanish huquqiga ega emasiz.")
        bot.send_sticker(message.chat.id, "CAACAgQAAxkBAAICk2d2pwlY_Az7yUl1HN1qkEGGlkLmAAI2EwACGJ3wUKir7ygymVAENgQ")



#statistika tugmasi----------------------------

def blockers_pp():
    s = 0
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    peaple = cursor.fetchall()
    for user_id in peaple:
        try:
            bot.send_message(chat_id=user_id[1], text="Hello! Just testing 😊")
        except ApiException as e:
            if "Forbidden: bot was blocked by the user" in str(e):
                s += 1


    cursor.execute("UPDATE blockers SET number_blok = ? WHERE id = ?", (s, 1))
    conn.commit()
    cursor.execute("SELECT * FROM blockers")
    try:
        return cursor.fetchone()
    except:
        return 0

@bot.callback_query_handler(func= lambda call: call.data == "num_blockers")
def num_b(call):
    son = blockers_pp()
    if son == None:
        son = 0
    bot.send_message(call.message.chat.id, f"❇️Faol foydalanuvchilar soni: {count_users() - int(son)}\n⭕️Blocklagan boydalanuvchilar soni: {son} " )

def bl_keybord():
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="Blocklagan foydalanuvchilar soni", callback_data="num_blockers")
    keyboard.add(button)
    return keyboard


@bot.message_handler(func= lambda message: message.text == "📊Statistika" and is_admin(message.chat.id))
def user_num(message):
    bot.send_message(message.chat.id, f"📋Bot foydalanuvchilar soni: {count_users()}" ,reply_markup= bl_keybord())




#Broadcast tugmasi-----------------------------

@bot.message_handler(func= lambda message: message.text == "📃Xabar yuborish" and is_admin(message.chat.id))
def start_broadcast(message):
    global broadcast_mode
    if is_admin(message.chat.id):
        broadcast_mode = True
        bot.send_message(message.chat.id, text= "❇️Yuboriladigan xabarni yozing...")
    else:
        bot.send_message(message.chat.id, "❌Siz bu tizimdan foyadalanish huquqiga ega emasiz.")
        bot.send_sticker(message.chat.id, "CAACAgQAAxkBAAICk2d2pwlY_Az7yUl1HN1qkEGGlkLmAAI2EwACGJ3wUKir7ygymVAENgQ")




#"🎁Ko'nkurs"--------------------------------------------------------------------------------------------------------
from koncurs import prize, taking_prizes,rues, taking_rules,kon_start,kon_stop
enable_yutuq = False
enable_rule = False
konkurs_switch = False

kon_holat = "🔴Konkurs tugagan"

@bot.message_handler(func = lambda message: message.text == "🎁Ko'nkurs" and is_admin(message.chat.id))
def referal(message):

    bot.send_message(message.chat.id, "Qiziqarli Ko'nkurslarni boshlang!😄", reply_markup = get_konkurs_keyboard())

@bot.message_handler(func = lambda message: message.text == "🎁Yutuqlar" and is_admin(message.chat.id))
def k1(message):
    global enable_yutuq
    enable_yutuq = True
    prize(message)


@bot.message_handler(func=lambda message: enable_yutuq and is_admin(message.chat.id))
def k2(message):
    global enable_yutuq
    enable_yutuq = False
    taking_prizes(message)

@bot.message_handler(func = lambda message: message.text == "📃Qoidalar" and is_admin(message.chat.id))
def k3(message):
    global enable_rule
    enable_rule = True
    rues(message)

@bot.message_handler(func=lambda message: enable_rule and is_admin(message.chat.id))
def k4(message):
    global enable_rule
    enable_rule = False
    taking_rules(message)

@bot.message_handler(func= lambda message: message.text == "🧩Boshlash")
def k5(message):
    global konkurs_switch, kon_holat
    kon_holat = "❇️Davom etmoqda..."
    konkurs_switch = True
    kon_start(message, kon_holat)

@bot.message_handler(func= lambda message: message.text == "⛔️To'xtatish")
def k6(message):
    global konkurs_switch, kon_holat
    kon_holat = "🔴Konkurs tugagan"
    konkurs_switch = False
    kon_stop(message)


#🎥Anime sozlash--------------------------------------------------------------------------------------------------
get_anime = False
get_anime_nom = False
anime_del = False
anime_change = False
anime_kod = get_last_kod()[0]
anime_kod2 = get_last_kod_eng()[0]
anime_kod3 = get_last_kod_rus()[0]
file_n: str = ""
print(anime_kod,anime_kod2,anime_kod3)
add_uz_bool = False
add_eng_bool = False
add_rus_bool = False

@bot.message_handler(func = lambda message: message.text == "🎥Anime sozlash" and is_admin(message.chat.id))
def create_keyboard_of_anime_change(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_st = types.KeyboardButton("❇️Anime qo'shish")
    item_xy = types.KeyboardButton("🗑Anime o'chrish")
    item_pt = types.KeyboardButton("🔱O'zgartirish")
    item_bc = types.KeyboardButton("◀️Orqaga")

    markup.row(item_st, item_xy)
    markup.row(item_bc,item_pt)

    bot.send_message(message.chat.id, "Anime Sozlash bo'limi!", reply_markup= markup)

@bot.callback_query_handler(func = lambda call: call.data == "add_uz_anime")
def qoshuz(call):
    global add_uz_bool, add_eng_bool, add_rus_bool
    add_uz_bool = True
    add_eng_bool = False
    add_rus_bool = False
    global get_anime_nom
    get_anime_nom = True
    bot.send_message(call.message.chat.id, "📃Ok, yuklamoqchi bo'lgan animening nomini tashlang...")

@bot.callback_query_handler(func = lambda call: call.data == "add_eng_anime")
def qosheng(call):
    global add_uz_bool, add_eng_bool, add_rus_bool
    add_uz_bool = False
    add_eng_bool = True
    add_rus_bool = False
    global get_anime_nom
    get_anime_nom = True
    bot.send_message(call.message.chat.id, "📃Ok, yuklamoqchi bo'lgan animening nomini tashlang...")

@bot.callback_query_handler(func = lambda call: call.data == "add_rus_anime")
def qoshrus(call):
    global add_uz_bool, add_eng_bool, add_rus_bool
    add_uz_bool = False
    add_eng_bool = False
    add_rus_bool = True
    global get_anime_nom
    get_anime_nom = True

    bot.send_message(call.message.chat.id, "📃Ok, yuklamoqchi bo'lgan animening nomini tashlang...")


@bot.message_handler(func = lambda message: message.text == "❇️Anime qo'shish" and is_admin(message.chat.id))
def add_anime(message):
    global add_eng_bool, add_rus_bool, add_uz_bool
    add_eng_bool, add_rus_bool, add_uz_bool = False, False, False
    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(text="🇺🇿 Uzb", callback_data="add_uz_anime")
    button2 = InlineKeyboardButton(text="🇬🇧 Eng", callback_data="add_eng_anime")
    button3 = InlineKeyboardButton(text="🇷🇺 Rus", callback_data="add_rus_anime")
    keyboard.add(button1,button2,button3)
    global anime_kod, anime_kod2, anime_kod3
    anime_kod += 1
    anime_kod2 += 1
    anime_kod3 += 1

    bot.send_message(message.chat.id , "Anime tilini tanlang !", reply_markup = keyboard)


@bot.message_handler(func = lambda message: get_anime_nom and is_admin(message.chat.id))
def get_file_name(message):
    global file_n, get_anime, get_anime_nom
    file_n = message.text
    get_anime = True
    get_anime_nom = False
    bot.send_message(message.chat.id , "🖼Ok, yuklamoqchi bo'lgan animening suratini tashlang.")


@bot.message_handler(content_types=['photo', 'video', 'document'], func = lambda message: get_anime and is_admin(message.chat.id))
def handle_file_upload(message):
    global anime_kod,anime_kod3, anime_kod2, file_n, add_rus_bool, add_eng_bool, add_uz_bool
    if add_uz_bool:
        if message.photo:
            file_id = message.photo[-1].file_id  # Get the largest photo
            file_type = 'photo'

        elif message.video:
            file_id = message.video.file_id
            file_type = 'video'
        elif message.document:
            file = message.document  # Get the uploaded file info
            if file.mime_type == "video/x-matroska":  # Check if it's an MKV file
                file_id = file.file_id
                file_type = "mkv"
            elif file.mime_type == "video/mp4" or file.file_name.endswith(".mp4"):
                file_id = file.file_id
                file_type = "mp4"
            else:
                bot.reply_to(message, "⛔️Unsupported file type.")

        else:
            bot.reply_to(message, "⛔️Unsupported file type.")
            return

        # Save file metadata to database

        save_file(anime_kod, file_id, file_n, file_type)

        bot.reply_to(message, f"✅{file_type.capitalize()} saved successfully!")
        if message.photo:
            bot.send_message(message.chat.id,"🎥Ok, yuklamoqchi bo'lgan anime qismlarini tartib bo'yicha tashlang (1 -> 12)")



    elif add_eng_bool:
        if message.photo:
            file_id = message.photo[-1].file_id  # Get the largest photo
            file_type = 'photo'
        elif message.video:
            file_id = message.video.file_id
            file_type = 'video'
        elif message.document:
            file = message.document  # Get the uploaded file info
            if file.mime_type == "video/x-matroska":  # Check if it's an MKV file
                file_id = file.file_id
                file_type = "mkv"
            elif file.mime_type == "video/mp4" or file.file_name.endswith(".mp4"):
                file_id = file.file_id
                file_type = "mp4"
            else:
                bot.reply_to(message, "⛔️Unsupported file type.")
        else:
            bot.reply_to(message, "⛔️Unsupported file type.")
            return

        # Save file metadata to database
        save_file_eng(anime_kod2, file_id, file_n, file_type)

        bot.reply_to(message, f"✅{file_type.capitalize()} saved successfully!")
        if message.photo:
            bot.send_message(message.chat.id,"🎥Ok, yuklamoqchi bo'lgan anime qismlarini tartib bo'yicha tashlang (1 -> 12)")
    elif add_rus_bool:
        if message.photo:
            file_id = message.photo[-1].file_id  # Get the largest photo
            file_type = 'photo'
        elif message.video:
            file_id = message.video.file_id
            file_type = 'video'
        elif message.document:
            file = message.document  # Get the uploaded file info
            if file.mime_type == "video/x-matroska":  # Check if it's an MKV file
                file_id = file.file_id
                file_type = "mkv"
            elif file.mime_type == "video/mp4" or file.file_name.endswith(".mp4"):
                file_id = file.file_id
                file_type = "mp4"
            else:
                bot.reply_to(message, "⛔️Unsupported file type.")
        else:
            bot.reply_to(message, "⛔️Unsupported file type.")
            return

        # Save file metadata to database
        save_file_rus(anime_kod3, file_id, file_n, file_type)

        bot.reply_to(message, f"✅{file_type.capitalize()} saved successfully!")
        if message.photo:
            bot.send_message(message.chat.id,"🎥Ok, yuklamoqchi bo'lgan anime qismlarini tartib bo'yicha tashlang (1 -> 12)")
    else:
        print("xatolik tilda")


@bot.message_handler(func= lambda message: message.text == "🗑Anime o'chrish" and is_admin(message.chat.id))
def del_anime(message):
    global anime_del
    anime_del = True
    roy = show_anime_list()
    m = ""
    for i in roy:
        m += (i + "\n")
    bot.send_message(message.chat.id, m)
    bot.send_message(message.chat.id, "O'chirmoqchi bo'lgan anime kodini kiriting...")

@bot.message_handler(func= lambda message: is_admin(message.chat.id) and anime_del)
def delete_anime_from_anime_list(message):
    global anime_del
    anime_del = False
    try:
        kod = int(message.text)
        conn = sqlite3.connect("bot_users.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM files WHERE file_kod = ?", (kod,))
        conn.commit()
        cursor.execute("DELETE FROM files_eng WHERE file_kod = ?", (kod,))
        conn.commit()
        cursor.execute("DELETE FROM files_rus WHERE file_kod = ?", (kod,))
        conn.commit()
        bot.send_message(message.chat.id, "✅Anime muvaffaqiyatli o'chirildi")
    except Exception as e:
        bot.send_message(message.chat.id, f"⛔️Tizimda xatolik yuz berdi: {e}")


add_ep_bool1 = False
add_ep_bool2 = False
ep_num: int = 0
an_name: str = "Unknown"
til: str = None

@bot.callback_query_handler(func= lambda call: call.data == "ep_anime")
def change_anime_ep(call):
    global add_ep_bool1
    roy = show_anime_list()
    m = ""
    for i in roy:
        m += (i + "\n")
    bot.send_message(call.message.chat.id, m)
    bot.send_message(call.message.chat.id, "Qism qo'shiladigan anime kodini va tilini (uz/eng/rus) vergul bilan kiriting...")
    add_ep_bool1 = True

@bot.message_handler(func= lambda message: is_admin(message.chat.id) and add_ep_bool1)
def add_episode(message):
    mm: list = message.text.split(",")
    global ep_num, an_name, add_ep_bool1, add_ep_bool2, til
    til = mm[1]
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    if mm[1] == "eng":
        cursor.execute("SELECT file_kod, file_name FROM files_eng")
        eplist = cursor.fetchall()
    elif mm[1] == "rus":
        cursor.execute("SELECT file_kod, file_name FROM files_rus")
        eplist = cursor.fetchall()
    else:
        cursor.execute("SELECT file_kod, file_name FROM files")
        eplist = cursor.fetchall()
    for i in eplist:
        if int(i[0]) == int(mm[0]):
            an_name = i[1]
            break
    if an_name == "Unknown":
        bot.send_message(message.chat.id,"Siz mavjud bo'lmagan kod kiritingiz!")
    else:
        ep_num = int(mm[0])
        add_ep_bool2 = True
        bot.send_message(message.chat.id, f"🎥Ok, {an_name} animesiga yuklamoqchi bo'lgan qismni/larni tartib bo'yicha tashlang...")
    add_ep_bool1 = False

@bot.message_handler(content_types=['video', 'document'], func = lambda message: add_ep_bool2 and is_admin(message.chat.id))
def handle_file_upload(message):
    global ep_num,an_name
    if message.video:
        file_id = message.video.file_id
        file_type = 'video'
    elif message.document:
        file = message.document  # Get the uploaded file info
        if file.mime_type == "video/x-matroska":  # Check if it's an MKV file
            file_id = file.file_id
            file_type = "mkv"
        elif file.mime_type == "video/mp4" or file.file_name.endswith(".mp4"):
            file_id = file.file_id
            file_type = "mp4"
        else:
            bot.reply_to(message, "⛔️Unsupported file type.")
    else:
        bot.reply_to(message, "⛔️Unsupported file type.")
        return

    # Save file metadata to database
    if til == "uz":
        save_file(ep_num, file_id, an_name,file_type)
        bot.reply_to(message, f"✅{file_type.capitalize()} saved successfully!")
    elif til == "eng":
        save_file_eng(ep_num, file_id , an_name,file_type)
        bot.reply_to(message, f"✅{file_type.capitalize()} saved successfully!")
    elif til == "rus":
        save_file_rus(ep_num, file_id, an_name,file_type)
        bot.reply_to(message, f"✅{file_type.capitalize()} saved successfully!")
    else:
        bot.reply_to(message, f"⛔️Saved unsuccessfully!")




@bot.callback_query_handler(func= lambda call: call.data == "name_anime")
def change_anime_name(call):
    global anime_change
    anime_change = True
    roy = show_anime_list()
    m = ""
    for i in roy:
        m += (i + "\n")
    bot.send_message(call.message.chat.id, m)
    bot.send_message(call.message.chat.id, "O'zgartirmoqchi bo'lgan anime kodi va yangi nomini kiriting Eg. 1, Anime_name. Vergul bo'lishi shart.")


@bot.message_handler(func= lambda message: anime_change and is_admin(message.chat.id))
def change_name(message):
    global anime_change
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    k = message.text.split(",")
    try:
        cursor.execute("UPDATE files SET file_name = ? WHERE file_kod = ?", (k[1], int(k[0])))
        conn.commit()
        bot.send_message(message.chat.id, "✅Anime muvaffaqiyatli o'zgartirildi.")

    except Exception as e:
        bot.send_message(message.chat.id, f"⛔️Tizimda xatolik yuz berdi: {e}")
    finally:
        anime_change = False


@bot.message_handler(func=lambda message: message.text == "🔱O'zgartirish" and is_admin(message.chat.id))
def change_anime(message):
    keyboard = InlineKeyboardMarkup()
    button_name = InlineKeyboardButton(text="Nomini o'zgartish", callback_data= "name_anime")
    button_ep = InlineKeyboardButton(text="Qismini o'zgartirish", callback_data= "ep_anime")
    keyboard.add(button_ep,button_name)
    bot.send_message(message.chat.id, "Animeni qanday o'zgartirmoqchisiz ?", reply_markup=keyboard)



#📬Post tayyorlash----------------------------------------------------------------------------------------------------------------
kd_bool = False
kd = 0
get_post_bool = False
CAPTION:str = "This is a caption for the photo!"
FILE_ID:str = "AgACAgIAAxkBAAIVLGeSgqErwpnTn6rQBDNA0MBLlueRAAJ96jEbetaRSPk5lM895IfOAQADAgADeAADNgQ"
BUTTON = {
        "inline_keyboard": [
            [
                {
                    "text": "🔹👉Anime ko'rish",  # Button text
                    "url": f"https://t.me/{bot_username}?start={kd}"  # URL the button links to
                }
            ]
        ]
    }



@bot.callback_query_handler(func= lambda call: call.data == "send_channel")
def channelsend(call):
    global get_payload

    response = requests.post(url, data= get_payload())

    if response.status_code == 200:
        print("Photo sent successfully!")
    else:
        print(f"Failed to send photo: {response.status_code} - {response.text}")



@bot.message_handler(func = lambda message: message.text == "📬Post tayyorlash" and is_admin(message.chat.id))
def create_post(message):
    global kd_bool
    kd_bool = True
    bot.send_message(message.chat.id, "Iltimos, Anime ko'dini kiriting.")

@bot.message_handler(func= lambda message: is_admin(message.chat.id) and kd_bool)
def get_post(message):
    global kd, kd_bool, get_post_bool
    kd_bool = False
    get_post_bool = True
    kd = int(message.text)
    bot.send_message(message.chat.id, "Iltimos, foto va anime postingizni tashlang...")

@bot.message_handler(content_types= ["text", "photo"] ,func= lambda message: is_admin(message.chat.id) and get_post_bool)
def ready_post(message):
    global kd, nm_channel, CAPTION, FILE_ID, get_post_bool, BUTTON
    get_post_bool = False
    CAPTION = message.caption

    BUTTON = {
        "inline_keyboard": [
            [
                {
                    "text": "🔹👉Anime ko'rish",  # Button text
                    "url": f"https://t.me/{bot_username}?start={kd}"  # URL the button links to
                }
            ]
        ]
    }

    link = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text ="🔹👉Anime ko'rish" ,url = f"https://t.me/{bot_username}?start={kd}")
    button2 = InlineKeyboardButton(text = nm_channel  , callback_data = "send_channel")
    link.add(button)
    link.add(button2)
    if message.content_type == "photo":
        bot.send_photo(message.chat.id, message.photo[-1].file_id, caption=message.caption, reply_markup= link)
        FILE_ID = message.photo[-1].file_id
    else:
        bot.send_message(message.chat.id, "Siz noto'g'ri turdagi xabar yubordiz!")




#"📢Kanallar"-----------------------------------------
add_channel_bool = False
del_channel_bool = False
hisobot_bool = False
CHANNEL_ID = "@telegrabotkrito"

nm_channel:str = "⚜️Cute Anime⚜️"

@bot.callback_query_handler(func= lambda call: call.data == "oth_channel")
def channel_add_to_post(call):
    global hisobot_bool
    hisobot_bool = True
    bot.send_message(call.message.chat.id, "Kanal nomini, silkasisini  vergul bilan ajratib kiriting .\nkanal_nomi,kanal_silkasi")



@bot.callback_query_handler(func= lambda call: call.data == "add_channel")
def channel_add_to_list(call):
    global add_channel_bool
    add_channel_bool = True
    bot.send_message(call.message.chat.id, "Kanal nomini, silkasisini va qo'shiluvchilar soni  vergul bilan ajratib kiriting .\nkanal_nomi,kanal_silkasi,100")


@bot.callback_query_handler(func= lambda call: call.data == "del_channel")
def channel_add_to_list(call):
    global del_channel_bool
    del_channel_bool = True
    bot.send_message(call.message.chat.id, "Kanal kodini kiriting.")

@bot.message_handler(func = lambda message: message.text == "📢Kanallar" and is_admin(message.chat.id))
def channel_list(message):
    keyboard = InlineKeyboardMarkup()
    button_add = InlineKeyboardButton(text="➕Kanal qo'shish", callback_data="add_channel")
    button_oth = InlineKeyboardButton(text="➕Post kanali", callback_data="oth_channel")
    button_del = InlineKeyboardButton(text="➖Kanal o'chrish", callback_data="del_channel")
    keyboard.add(button_oth)
    keyboard.add(button_add)
    keyboard.add(button_del)
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM followers")
    ch_list = cursor.fetchall()
    mm: str = ""
    for c in ch_list:
        mm += f"{c[0]}. {c[1]} , {c[2]} , {c[4]}\n"
    try:
        bot.send_message(message.chat.id, mm, reply_markup= keyboard)
    except:
        bot.send_message(message.chat.id, "Kanal qo'shing!", reply_markup= keyboard)

@bot.message_handler(func= lambda message: is_admin(message.chat.id) and add_channel_bool)
def addchannel(message):
    global add_channel_bool
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()

    m = message.text.split(",")
    try:
        cursor.execute("""
        INSERT OR IGNORE INTO followers (channel_name,channel_url, num_follower, now_follower)
        VALUES (?, ?, ?,?)
        """, (m[0],m[1],m[2],0))
        conn.commit()

        bot.send_message(message.chat.id, "✅Kanal muvoffaqiyatli qo'shildi.")
    except sqlite3.Error as e:
        bot.send_message(message.chat.id, f"⛔️Tizimda xatolik: {e}")
    finally:
        add_channel_bool = False
        conn.close()



@bot.message_handler(func= lambda message: is_admin(message.chat.id) and del_channel_bool)
def delchannel(message):
    global del_channel_bool
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM followers WHERE id = ?", (int(message.text),))
        conn.commit()

        bot.send_message(message.chat.id, "✅Kanal muvoffaqiyatli o'chirildi")
    except Exception as e:
        bot.send_message(message.chat.id, f"⛔️Tizimda xatolik: {e}")
    finally:
        del_channel_bool = False

@bot.message_handler(func = lambda message: is_admin(message.chat.id) and hisobot_bool)
def qosh_kanal(message):
    global hisobot_bool, nm_channel, CHANNEL_ID
    hisobot_bool = False
    try:
        ll = message.text.split(",")
        CHANNEL_ID = f"@{ll[1][13:]}"
        nm_channel = ll[0]
        bot.send_message(message.chat.id, "✅Kanal muvoffaqiyatli qo'shildi.")
    except:
        bot.send_message(message.chat.id, "⛔️Kanal o'rnamadi, iltimos qayta urining.")

url = f"https://api.telegram.org/bot{API_key}/sendPhoto"
def get_payload():
    global CAPTION,CHANNEL_ID,FILE_ID,BUTTON
    payload = {
        "chat_id": CHANNEL_ID,
        "photo": FILE_ID,
        "caption": CAPTION,
        "reply_markup": json.dumps(BUTTON)  # Inline keyboard markup must be JSON-encoded
    }
    return payload
#Admins tugmasi--------------------------------------
enable_add = False
enable_del = False
def send_demand1(message):
    bot.send_message(message.chat.id, "📃Admin qilmoqchi bo'lgan shaxsning 'username'ini  kiriting...")
def send_demand2(message):
    bot.send_message(message.chat.id, "🔢Admin raqamini jo'nating...")
@bot.callback_query_handler(func= lambda call: call.data == "add_admin")
def admin_add(call):
    global enable_add, enable_del
    enable_add = True
    enable_del = False
    send_demand1(call.message)

@bot.callback_query_handler(func= lambda call: call.data == "del_admin")
def admin_del(call):
    global enable_del, enable_add
    enable_del = True
    enable_add = False
    send_demand2(call.message)



@bot.message_handler( func= lambda message: message.text == "📋Adminlar" and is_admin(message.chat.id))
def show_admins(message):
    keyboard = InlineKeyboardMarkup()
    button_add = InlineKeyboardButton(text="➕Admin qo'shish", callback_data= "add_admin")
    button_del = InlineKeyboardButton(text="➖Admin o'chrish", callback_data= "del_admin")
    keyboard.add(button_add)
    keyboard.add(button_del)
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM admins""")
    adminlar = cursor.fetchall()
    mes_to_admin: str = ""
    for person in adminlar:

        mes_to_admin += f"{person[0]}."
        if person[2] != None:
            mes_to_admin += f" {person[2]},"
        if person[3] != None:
            mes_to_admin += f" {person[3]},"
        if person[4] != None:
            mes_to_admin += f" {person[4]},"
        mes_to_admin += "\n"
    try:
        bot.send_message(message.chat.id, mes_to_admin, reply_markup= keyboard)
    except:
        bot.send_message(message.chat.id, "Admin qo'shing !", reply_markup=keyboard)

@bot.message_handler(func= lambda message: is_admin(message.chat.id) and enable_add)
def search_admin(message):
    global enable_add

    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM users""")
    people = cursor.fetchall()
    try:
        num = int(message.text)
        for p in people:
            if p[0] == num:

                log_admin(p[1],p[2],p[3],p[4])
                bot.send_message(message.chat.id, "✅Yangi Admin o'rnatildi")
                break

        enable_add = False

    except ValueError:
        mes_to_admin: str = ""
        for person in people:

            if message.text in person:
                mes_to_admin += f"{person[0]}."
                if person[2] != None:
                    mes_to_admin += f" {person[2]},"
                if person[3] != None:
                    mes_to_admin += f" {person[3]},"
                if person[4] != None:
                    mes_to_admin += f" {person[4]},"
                mes_to_admin += "\n"
        bot.send_message(message.chat.id, f"Natijalar:\n{mes_to_admin}Ism oldidagi raqamni jo'nating")
    except Exception as e:
        bot.send_message(message.chat.id, f"⛔️Tizimda xatolik: {e}")
        enable_add = False


@bot.message_handler(func=lambda message: is_admin(message.chat.id) and enable_del)
def search_admin(message):
    global enable_del

    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM admins""")
    try:
        num = int(message.text)
        cursor.execute("DELETE FROM admins WHERE id = ?", (num,))
        conn.commit()
        enable_del = False
        bot.send_message(message.chat.id, "😎Adim muvoffaqiyatli o'chirildi.")
    except Exception as e:
        bot.send_message(message.chat.id, f"⛔️Tizimda xatolik: {e}")
        enable_del = False


#bot holati tugmasi----------------------------------
@bot.callback_query_handler(func= lambda call: call.data == "starts")
def startsbot(call):
    global holatbot
    holatbot = True
    switch(call.message)

def startbot(message):
    mes_key = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton(text= "✅Turn On" , callback_data= "starts")
    mes_key.add(but1)
    bot.send_message(message.chat.id, "⛔️Bot to'xtatildi.", reply_markup= mes_key)


@bot.callback_query_handler(func= lambda call: call.data == "stop")
def stops(call):
    global holatbot
    holatbot = False
    startbot(call.message)

@bot.message_handler(func = lambda message: message.text == "🤖Bot holati" and is_admin(message.chat.id))
def switch(message):
    global holatbot
    if is_admin(message.chat.id):
        keyboard = InlineKeyboardMarkup()
        if holatbot:
            hol = "Ishalamoqda"
        else:
            hol = "To'xtatilgan"
        button2 = InlineKeyboardButton(text="🚷Turn off", callback_data="stop")

        keyboard.add(button2)
        bot.send_message(message.chat.id, f"😇Bot holati: {hol}", reply_markup= keyboard )



#Back tugmasi---------------------------------------------
@bot.message_handler(func= lambda message: message.text == "◀️Orqaga")
def back(message):
    global get_anime, get_anime_nom,anime_del, anime_change, add_eng_bool, add_rus_bool, add_uz_bool
    get_anime = False
    get_anime_nom = False
    anime_del = False
    anime_change = False
    add_eng_bool, add_rus_bool, add_uz_bool = False, False, False
    bot.send_message(message.chat.id, "📋Bosh menyu", reply_markup= main_keyboard(message))



#Anime Izlash-------------------------------------------------------------------------------------------------------


@bot.callback_query_handler(func = lambda call:  call.data.startswith( "show_uz_anime:"))
def show_uz(call):
    message = call.message
    chat_id = message.chat.id

    # Retrieve the number from the user_data dictionary
    file_kod = int(call.data.split(":")[1])
    file_n_i = get_file(file_kod)
    k = -1
    for f in file_n_i:
        if f:
            saved_file_id, file_name, file_type = f
            k += 1
            # Send file using its file_id
            if file_type == 'photo':
                bot.send_photo(message.chat.id, saved_file_id, caption=file_name)

            elif file_type == 'video':
                bot.send_video(message.chat.id, saved_file_id, caption=f"{k} - qism")

            else:
                try:
                    bot.send_document(message.chat.id, saved_file_id, caption=f"{k} - qism")
                except:
                    bot.reply_to(message, "⭕️Unknown file type.")
        else:
            bot.reply_to(message, "⭕️File not found.")


@bot.callback_query_handler(func=lambda call:  call.data.startswith("show_eng_anime:"))
def show_eng(call):
    message = call.message
    chat_id = message.chat.id

    # Retrieve the number from the user_data dictionary
    file_kod = int(call.data.split(":")[1])
    file_n_i = get_file_eng(file_kod)
    k = -1
    for f in file_n_i:
        if f:
            saved_file_id, file_name, file_type = f
            k += 1
            # Send file using its file_id
            if file_type == 'photo':
                bot.send_photo(message.chat.id, saved_file_id, caption=file_name)

            elif file_type == 'video':
                bot.send_video(message.chat.id, saved_file_id, caption=f"Episode {k}")

            else:
                try:
                    bot.send_document(message.chat.id, saved_file_id, caption=f"Episode {k}")
                except:
                    bot.reply_to(message, "⭕️Unknown file type.")
        else:
            bot.reply_to(message, "⭕️File not found.")


@bot.callback_query_handler(func=lambda call:  call.data.startswith("show_rus_anime:"))
def show_rus(call):
    message = call.message
    chat_id = message.chat.id

    # Retrieve the number from the user_data dictionary
    file_kod = int(call.data.split(":")[1])
    file_n_i = get_file_rus(file_kod)
    k = -1
    for f in file_n_i:
        if f:
            saved_file_id, file_name, file_type = f
            k += 1
            # Send file using its file_id
            if file_type == 'photo':
                bot.send_photo(message.chat.id, saved_file_id, caption=file_name)

            elif file_type == 'video':
                bot.send_video(message.chat.id, saved_file_id, caption=f"{k} серия")

            else:
                try:
                    bot.send_document(message.chat.id, saved_file_id, caption=f"{k} серия")
                except:
                    bot.reply_to(message, "⭕️Unknown file type.")
        else:
            bot.reply_to(message, "⭕️File not found.")



@bot.message_handler(content_types=["text", "photo", "video", "audio", "document","sticker"], func= lambda message: holatbot)
def kod_check(message):
    global anime_kod, broadcast_mode
    if is_admin(message.chat.id) and broadcast_mode:
        conn = sqlite3.connect("bot_users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        peaple = cursor.fetchall()
        for user in peaple:

            try:
                user_id = user[1]
                if int(user_id) == 7651554989:
                    print("bo'timiz")
                elif message.content_type == "text":
                    bot.send_message(user_id, message.text)
                    # Broadcast photos
                elif message.content_type == "photo":
                    bot.send_photo(user_id, message.photo[-1].file_id, caption=message.caption)
                    # Broadcast videos
                elif message.content_type == "video":
                    bot.send_video(user_id, message.video.file_id, caption=message.caption)
                    # Broadcast audio
                elif message.content_type == "audio":
                    bot.send_audio(user_id, message.audio.file_id, caption=message.caption)
                    # Broadcast documents
                elif message.content_type == "document":
                    bot.send_document(user_id, message.document.file_id, caption=message.caption)
                elif message.content_type == "sticker":
                    bot.send_sticker(user_id, message.sticker.file_id)
            except Exception as e:
                print(f"⭕️️Bu userga xabar jo'natilmadi. {user}: {e}")
            finally:
                broadcast_mode = False
        bot.send_message(message.chat.id, "Xabar yuborib tugallandi.")
    else:
        try:
            file_kod = int(message.text)
            if file_kod <= anime_kod:
                keyboard = InlineKeyboardMarkup()
                button1 = InlineKeyboardButton(text="🇺🇿 Uzb", callback_data=f"show_uz_anime:{file_kod}")
                button2 = InlineKeyboardButton(text="🇬🇧 Eng", callback_data=f"show_eng_anime:{file_kod}")
                button3 = InlineKeyboardButton(text="🇷🇺 Rus", callback_data=f"show_rus_anime:{file_kod}")
                keyboard.add(button1, button2, button3)

                file_n_i = get_file(file_kod)
                f = file_n_i[0]
                saved_file_id, file_name, file_type = f
                if file_type == 'photo':
                    bot.send_photo(message.chat.id, saved_file_id, caption=file_name, reply_markup= keyboard)

            else:
                bot.send_message(message.chat.id, "🙁Bu kod bizning ro'yhatimizda topilmadi.")
        except ValueError:
            ani_res_list = get_ani_kod(message.text.lower())
            l  = ""
            for x in (ani_res_list):
                l += f"{x[1]}:  {x[2]}\n"
            bot.send_message(message.chat.id, l)


        except Exception as e:
            bot.send_message(message.chat.id, f"💥Tizimda xatolik vujudga keldi. Iltimos keyinroq qayta uruning: {e}")





def get_result(list1):
    results: list = []
    dont_rety: list = []
    for p in list1:
        if p[1] not in dont_rety:
            dont_rety.append(p[1])
            results.append(
                InlineQueryResultArticle(
                    id=str(p[0]),
                    title=p[2],
                    description=f"Anime is the best thing in the world 😇",
                    input_message_content=InputTextMessageContent(f"{p[1]}"),
                )
            )
    return results



@bot.inline_handler(lambda query: len(query.query) > 0)  # Only trigger when user types something
def inline_query_handler(query):
    print(get_ani_kod(query.query.lower()))
    results = get_result(get_ani_kod(query.query.lower()))



    bot.answer_inline_query(query.id, results, cache_time=1)






setup_block_user()
setup_database_followers()
setup_database_file()
setup_database_file_eng()
setup_database_file_rus()

setup_list_konkurs()
setup_yutuq()
setup_admin()
setup_database()
print("Your bot is running")
bot.infinity_polling(skip_pending= True)
