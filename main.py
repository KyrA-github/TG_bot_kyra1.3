import telebot
import sqlite3
import config
import random
from telebot import types


bot = telebot.TeleBot(config.TOKEN)
conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS balances
                  (user_id INTEGER PRIMARY KEY,
                    balance REAL,
                    user_name text)''')

user_id = 0
amount = 0.0
user_name = ""

@bot.message_handler(commands=['start'])
# старт
def start(message):
    global user_name
    global user_id
    user_id = message.from_user.id
    user_name = message.from_user.username
    # print(user_name)
    # print(user_id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Меню")
    markup.add(btn1, )
    bot.send_message(message.chat.id,
                    text="Привет, {0.first_name}! я бот который с тобой будет играть в игру угадай число. Начнем? ".format(
                        message.from_user), reply_markup=markup)
    # print("start")

    update_balance(user_id, amount)
# проверка пользователя
def update_balance(user_id, amount):
    # Проверка, существует ли пользователь в таблице balances
    cursor.execute('''SELECT balance
                      FROM balances
                      WHERE user_id = ?''', (user_id,))
    # print("Pn")

    result = cursor.fetchall()
    # print(result)

    if result:
        cursor.execute(f"SELECT balance FROM balances WHERE user_id = {user_id}")
        new = cursor.fetchone()
        # print(new)
        new_balance = new[0]
        # print(new_balance)
        cursor.execute('''UPDATE balances
                          SET balance = ?
                          WHERE user_id = ?''', (new_balance, user_id))
        # print("Пользователь уже существует")
    else:
        # Создаем нового пользователя с начальным балансом
        cursor.execute('''INSERT INTO balances (user_id, balance, user_name)
                          VALUES (?, ?, ?)''', (user_id, amount, user_name))
        # print("Создаем нового пользователя")
        cursor.execute(f"SELECT balance FROM balances WHERE user_id = {user_id}")
        new = cursor.fetchone()
        # print(new)
        new_balance = new[0]
        # print(new_balance)
    conn.commit()
@bot.message_handler(commands=['kyra'])
def kyra_admin(message):
    try:
        msg = bot.send_message(message.chat.id, text="Введите пароль чтобы войти как: Admin".format(message.from_user))
        bot.register_next_step_handler(msg, admin)
    except TypeError:
        bot.send_message(message.chat.id, "Erorr нажмите /start")
def admin(message):
    try:
        if message.text == "kyra":
            bot.send_message(message.chat.id, text="Вы вошли как: Admin".format(message.from_user))
            y = cursor.execute("SELECT * FROM balances")
            new = y.fetchall()
            bot.send_message(message.chat.id, f'Пользователи которые содержуться в базе: {new}')
        else:
            bot.send_message(message.chat.id, 'Проль не верный')
            menu(message)
    except TypeError:
        bot.send_message(message.chat.id, "Erorr нажмите /start")

@bot.message_handler(content_types=['text'])
def text(message):
    global user_id
# меню
    try:
        if message.text == "Меню":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Простой")
            btn2 = types.KeyboardButton("Сложный")
            btn3 = types.KeyboardButton("Тех.потдержка")
            btn4 = types.KeyboardButton("X2")
            btn5 = types.KeyboardButton("Баланс")
            # btn6 = types.KeyboardButton("Case")
            markup.add(btn1, btn2, btn3, btn4, btn5, )
            bot.send_message(message.chat.id,
                             text="{0.first_name} ты в меню. Уровни сложности ПРОСТОЙ ОТ 1-3, СЛОЖНЫЙ 1-9".
                             format(message.from_user), reply_markup=markup)
            # простой уровень
        elif message.text == "Простой":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn0 = types.KeyboardButton("3")
            btn1 = types.KeyboardButton("1")
            btn2 = types.KeyboardButton("2")
            markup.add(btn1, btn2, btn0)
            msg = bot.send_message(message.chat.id, text="{0.first_name} выбери число".format(message.from_user),
                             reply_markup=markup)
            user_id = message.from_user.id
            bot.register_next_step_handler(msg, game1)
            #сложный уровень
        elif message.text == "Тех.потдержка":
            bot.send_message(message.chat.id,
                             text="Если вы заметели ошибку напишите нам на почту   artemskoll3423@gmail.com".
                             format(message.from_user))
        elif message.text == "Баланс":
            try:
                user_id = message.from_user.id
                cursor.execute(f"SELECT balance FROM balances WHERE user_id = {user_id}")
                new = cursor.fetchone()
                new_balance = new[0]
                bot.send_message(message.chat.id, new_balance)
            except TypeError:
                bot.send_message(message.chat.id, "У вас нет баланса нажмите /start")
        elif message.text == "Сложный":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("1")
            btn2 = types.KeyboardButton("2")
            btn3 = types.KeyboardButton("3")
            btn4 = types.KeyboardButton("4")
            btn5 = types.KeyboardButton("5")
            btn6 = types.KeyboardButton("6")
            btn7 = types.KeyboardButton("7")
            btn8 = types.KeyboardButton("8")
            btn9 = types.KeyboardButton("9")
            markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9)
            msg = bot.send_message(message.chat.id, text="{0.first_name}! выбери число".format(message.from_user),
                             reply_markup=markup)
            bot.register_next_step_handler(msg, game2)
        elif message.text == "X2":
            cursor.execute(f"SELECT balance FROM balances WHERE user_id = {user_id}")
            new = cursor.fetchone()
            new_balance = new[0]
            if new_balance > 1.0:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("Играем")
                btn2 = types.KeyboardButton("Меню")
                markup.add(btn1, btn2)
                msg = bot.send_message(message.chat.id,
                                       text="Оплата 200, при выйграше удвоится баланс. Играем?".format(message.from_user),
                                       reply_markup=markup)
                bot.register_next_step_handler(msg, game_money)
            elif new_balance <= 0.0:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn123 = types.KeyboardButton("Меню")
                markup.add(btn123)
                bot.send_message(message.chat.id,
                                 text="Твой баланс меньше либо равен 0.0 игра не состоиться.".format(
                                     message.from_user), reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Я тебя не понимаю((((")
    except TypeError:
        bot.send_message(message.chat.id, "У вас нет баланса нажмите /start")
# X2

def game_money(message):
    try:
        if message.text == "Играем":

                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("1")
                btn2 = types.KeyboardButton("2")
                btn3 = types.KeyboardButton("3")
                markup.add(btn1, btn2, btn3)
                msg = bot.send_message(message.chat.id, text="{0.first_name} выбери число".format(message.from_user),
                                 reply_markup=markup)
                bot.register_next_step_handler(msg, game_money_pl)

        elif message.text == "Меню":
            text(message)
    except ValueError:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn123 = types.KeyboardButton("Меню")
        markup.add( btn123)
        bot.send_message(message.chat.id,
                         text="Я тебя не понимаю((((".format(
                             message.from_user), reply_markup=markup)
def game_money_pl(message):
    try:
        v = int(message.text)
        rando = random.randint(1, 3)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn3 = types.KeyboardButton("Меню")
        markup.add(btn3)
        bot.send_message(message.chat.id,
                         text="Твой результат:".format(
                             message.from_user), reply_markup=markup)
        if rando == v:
            bot.send_message(message.chat.id, 'Ты выйграл')
            game_money_v(message)
        elif rando != v:
            bot.send_message(message.chat.id, 'Ты проиграл', )
            bot.send_message(message.chat.id, 'Повезет в следуйсчий раз')
            game_money_p(message)
    except ValueError:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn123 = types.KeyboardButton("Меню")
        markup.add(btn123)
        bot.send_message(message.chat.id,
                         text="Я тебя не понимаю((((".format(
                             message.from_user), reply_markup=markup)
#игры

def game1(message):
    try:
        v = int(message.text)
        rando = random.randint(1, 3)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Простой")
        btn2 = types.KeyboardButton("Сложный")
        btn3 = types.KeyboardButton("Меню")
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id,
                         text="{0.first_name} ты в меню. Уровни сложности ПРОСТОЙ ОТ 1-3, СЛОЖНЫЙ 1-9".format(
                             message.from_user), reply_markup=markup)
        if rando == v:
            bot.send_message(message.chat.id, 'Ты выйграл')
            max1_bal(message)
        elif rando != v:
            bot.send_message(message.chat.id, 'Ты проиграл', )
            bot.send_message(message.chat.id, 'Я загадывал число')
            bot.send_message(message.chat.id, str(rando) )
            min_bal(message)
        # bot.send_message(message.chat.id, f'твой баланс {balans}')
    except ValueError:
        bot.send_message(message.chat.id,
                         text="Я тебя не понимаю((((".format(
                             message.from_user))
        menu(message)
def game2(message):
    try:
        v = int(message.text)
        rando = random.randint(1, 9)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Простой")
        btn2 = types.KeyboardButton("Сложный")
        btn3 = types.KeyboardButton("Меню")
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id,
                         text="{0.first_name} ты в меню. Уровни сложности ПРОСТОЙ ОТ 1-3, СЛОЖНЫЙ 1-9".format(
                             message.from_user), reply_markup=markup)
        if rando == v:
            bot.send_message(message.chat.id, 'Ты выйграл')
            max2_bal(message)
        elif rando != v:
            bot.send_message(message.chat.id, 'Ты проиграл', )
            bot.send_message(message.chat.id, 'Я загадывал число')
            bot.send_message(message.chat.id, str(rando))
            min_bal(message)
    except ValueError:
        bot.send_message(message.chat.id,
                         text="Я тебя не понимаю((((".format(
                             message.from_user))
        menu(message)
#меню 2
def menu(message):
    # меню
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Простой")
    btn2 = types.KeyboardButton("Сложный")
    btn3 = types.KeyboardButton("Тех.потдержка")
    btn4 = types.KeyboardButton("X2")
    btn5 = types.KeyboardButton("Баланс")
    # btn6 = types.KeyboardButton("Case")
    markup.add(btn1, btn2, btn3, btn4, btn5,)
    bot.send_message(message.chat.id,
                     text="{0.first_name} ты в меню. Уровни сложности ПРОСТОЙ ОТ 1-3, СЛОЖНЫЙ 1-9".format(
                         message.from_user), reply_markup=markup)
# балансы
def max2_bal(message):
    try:
        user_id = message.from_user.id
        # Добовляем 250 к балансу
        cursor.execute(f"SELECT balance FROM balances WHERE user_id = {user_id}")
        new = cursor.fetchone()
        new_balance = new[0]
        new_value = new_balance + 250
        cursor.execute('''UPDATE balances
                          SET balance = ?
                          WHERE user_id = ?''', (new_value, user_id))
        bot.send_message(message.chat.id, f'твой баланс {new_value}')
        conn.commit()
    except TypeError:
        bot.send_message(message.chat.id, "У вас нет баланса нажмите /start")
def max1_bal(message):
    try:
        user_id = message.from_user.id
        # Добавляем 100 к балансу
        cursor.execute(f"SELECT balance FROM balances WHERE user_id = {user_id}")
        new = cursor.fetchone()
        new_balance = new[0]
        new_value = new_balance + 100
        cursor.execute('''UPDATE balances
                          SET balance = ?
                          WHERE user_id = ?''', (new_value, user_id))
        bot.send_message(message.chat.id, f'твой баланс {new_value}')
        conn.commit()
    except TypeError:
        bot.send_message(message.chat.id, "У вас нет баланса нажмите /start")
def min_bal(message):
    try:
        user_id = message.from_user.id
        # Отнимаем 10 с баланса
        cursor.execute(f"SELECT balance FROM balances WHERE user_id = {user_id}")
        new = cursor.fetchone()
        new_balance = new[0]
        new_value = new_balance - 10
        cursor.execute('''UPDATE balances
                          SET balance = ?
                          WHERE user_id = ?''', (new_value, user_id))
        bot.send_message(message.chat.id, f'твой баланс {new_value}')
        conn.commit()
    except TypeError:
        bot.send_message(message.chat.id, "У вас нет баланса нажмите /start")
def game_money_v(message):
    try:
        user_id = message.from_user.id
        # Отнимаем 10 с баланса
        cursor.execute(f"SELECT balance FROM balances WHERE user_id = {user_id}")
        new = cursor.fetchone()
        new_balance = new[0]
        new_value = new_balance * 2
        cursor.execute('''UPDATE balances
                          SET balance = ?
                          WHERE user_id = ?''', (new_value, user_id))
        bot.send_message(message.chat.id, f'твой баланс {new_value}')
        conn.commit()
    except TypeError:
        bot.send_message(message.chat.id, "У вас нет баланса нажмите /start")
# игры X2
def game_money_p(message):
    try:
        user_id = message.from_user.id
        # Отнимаем 10 с баланса
        cursor.execute(f"SELECT balance FROM balances WHERE user_id = {user_id}")
        new = cursor.fetchone()
        new_balance = new[0]
        new_value = new_balance - 200
        cursor.execute('''UPDATE balances
                          SET balance = ?
                          WHERE user_id = ?''', (new_value, user_id))
        bot.send_message(message.chat.id, f'твой баланс {new_value}')
        conn.commit()
    except TypeError:
        bot.send_message(message.chat.id, "У вас нет баланса нажмите /start")



bot.polling(none_stop=True)
conn.close()
