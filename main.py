import telebot
import sqlite3
import ast

import random

import keyboards

bot = telebot.TeleBot("")


def check_sub_channel(chat_member):
    if chat_member.status != 'left':
        return True
    else:
        return False


@bot.message_handler(commands=['start'])
def start(message):#Обработка /start
    conn = sqlite3.connect('Users.db')
    cursor = conn.cursor()
    channel = cursor.execute(f"SELECT * FROM admin").fetchall()
    print(channel)
    conn.commit()
    conn.close()
    if all(check_sub_channel(bot.get_chat_member(chat_id=x[0], user_id=message.chat.id)) for x in channel):
        try:
            try:
                ref_user = message.text.split()[1]
            except IndexError:
                conn = sqlite3.connect('Users.db')
                cursor = conn.cursor()
                cursor.execute(f"INSERT INTO users (id, money, ref_user, username) VALUES ('{message.from_user.id}', 0, 'NULL','{message.from_user.username}')").fetchall()
                conn.commit()
                conn.close()
                bot.send_message(message.chat.id, 'Добро пожаловать в бот',reply_markup=keyboards.markup)
            except:
                bot.send_message(message.chat.id,'Пожалуйста добавьте username и попробуйте еще раз!')
            else:
                conn = sqlite3.connect('Users.db')
                cursor = conn.cursor()
                cursor.execute(
                    f"INSERT INTO users (id, money, ref_user, username) VALUES ('{message.from_user.id}', 0, '{ref_user}','{message.from_user.username}')").fetchall()
                cursor.execute(f"UPDATE users SET money=money+1 WHERE id = '{ref_user}'")
                conn.commit()
                conn.close()
                bot.send_message(message.chat.id, 'Добро пожаловать в бот',reply_markup=keyboards.markup)
        except:
            bot.send_message(message.chat.id,'Вы уже зарегистрировались',reply_markup=keyboards.markup)
    else:
        text = "\n".join([x[0] for x in channel])
        bot.send_message(message.chat.id,f'Подпишитесь на все каналы:\n\n{text}')


@bot.message_handler(commands=["topbotSpasiboAndreuiFreinu1234"])
def admin(message):#Обработка /start
    bot.send_message(message.chat.id,'Добро пожаловать в админ панель',reply_markup=keyboards.markup_admin)
    a = bot.send_message(message.chat.id,'Какую функцию хотите использовать')
    bot.register_next_step_handler(a,admin_text)


def admin_text(message):
    if message.text == 'Рассылка':
        a = bot.send_message(message.chat.id,'Напишите текст для рассылки')
        bot.register_next_step_handler(a,newsletter)
    if message.text == 'Пополнить баланс юзеру':
        a = bot.send_message(message.chat.id, 'Напишите username пользователя без @')
        bot.register_next_step_handler(a, user_plus_1)
    if message.text == 'Забрать баланс юзера':
        a = bot.send_message(message.chat.id, 'Напишите username пользователя без @')
        bot.register_next_step_handler(a, user_menos_1)
    if message.text == 'Удалить канал спонсора':
        a = bot.send_message(message.chat.id, 'Отправьте канал спонсора в таком ввиде:\n@channel')
        bot.register_next_step_handler(a, delete_channel)
    if message.text == 'Добавить канал спонсора':
        a = bot.send_message(message.chat.id, 'Отправьте канал спонсора в таком ввиде:\n@channel')
        bot.register_next_step_handler(a, add_channel)
    if message.text == 'Спонсорские каналы':
        conn = sqlite3.connect('Users.db')
        cursor = conn.cursor()
        url = cursor.execute(f"SELECT * FROM admin").fetchall()
        conn.close()
        bot.send_message(message.chat.id,"\n".join(x[0] for x in url))
    if message.text == 'Статистика':
        conn = sqlite3.connect('Users.db')
        cursor = conn.cursor()
        amount = cursor.execute(f"SELECT id FROM users").fetchall()
        bot.send_message(message.chat.id, f'Количество юзеров бота: {(amount.index(amount[-1])) + 1}')
        conn.close()
    if message.text == 'Назад':
        a = bot.send_message(message.chat.id,'Админ панель',reply_markup=keyboards.markup_admin)
        bot.register_next_step_handler(a, admin_text)


def add_channel(message):
    if message.text != "Назад":
        conn = sqlite3.connect('Users.db')
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO admin (url) VALUES ('{message.text}')")
        conn.commit()
        conn.close()
        bot.send_message(message.chat.id,'Канал добавлен')
    else:
        a = bot.send_message(message.chat.id, 'Админ панель', reply_markup=keyboards.markup_admin)
        bot.register_next_step_handler(a, admin_text)


def delete_channel(message):
    if message.text != "Назад":
        try:
            conn = sqlite3.connect('Users.db')
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM admin WHERE url = '{message.text}'")
            conn.commit()
            conn.close()
            bot.send_message(message.chat.id,'Канал удален')
        except:
            bot.send_message(message.chat.id,'Канал не был добавлен')
    else:
        a = bot.send_message(message.chat.id, 'Админ панель', reply_markup=keyboards.markup_admin)
        bot.register_next_step_handler(a, admin_text)


def user_menos_1(message):
    if message.text != "Назад":
        try:
            conn = sqlite3.connect('Users.db')
            cursor = conn.cursor()
            money = cursor.execute(f"SELECT money FROM users WHERE username = '{message.text}'").fetchall()[0][0]
            conn.commit()
            conn.close()
            a = bot.send_message(message.chat.id,f'Количество голды у пользователя:\n{money}\nНапишите сколько голды забрать у пользователя')
            bot.register_next_step_handler(a,user_menos_2,message.text)
        except:
            bot.send_message(message.chat.id,'Что-то пошло не так. Проверьте правильность информации')
    else:
        a = bot.send_message(message.chat.id,'Админ панель',reply_markup=keyboards.markup_admin)
        bot.register_next_step_handler(a, admin_text)


def user_menos_2(message,user):
    if message.text != "Назад":
        try:
            conn = sqlite3.connect('Users.db')
            cursor = conn.cursor()
            cursor.execute(f"UPDATE users SET money=money-{int(message.text)} WHERE username = '{str(user)}'")
            conn.commit()
            conn.close()
            bot.send_message(message.chat.id,f'Вы забрали голду у пользователя с username:{user}')
        except:
            bot.send_message(message.chat.id,'Что-то пошло не так. Проверьте правильность информации')
    else:
        a = bot.send_message(message.chat.id,'Админ панель',reply_markup=keyboards.markup_admin)
        bot.register_next_step_handler(a,admin_text)


def user_plus_1(message):
    if message.text != "Назад":
        try:
            conn = sqlite3.connect('Users.db')
            cursor = conn.cursor()
            money = cursor.execute(f"SELECT money FROM users WHERE username = '{message.text}'").fetchall()[0][0]
            conn.commit()
            conn.close()
            a = bot.send_message(message.chat.id,
                                 f'Количество голды у пользователя:\n{money}\nНапишите на сколько голды хотите пополнили баланс у пользователя')
            bot.register_next_step_handler(a, user_plus_2, message.text)
        except:
            bot.send_message(message.chat.id, 'Что-то пошло не так. Проверьте правильность информации')
    else:
        a = bot.send_message(message.chat.id,'Админ панель',reply_markup=keyboards.markup_admin)
        bot.register_next_step_handler(a, admin_text)


def user_plus_2(message,user):
    if message.text != "Назад":
        try:
            conn = sqlite3.connect('Users.db')
            cursor = conn.cursor()
            cursor.execute(f"UPDATE users SET money=money+{int(message.text)} WHERE username = '{str(user)}'")
            conn.commit()
            conn.close()
            bot.send_message(message.chat.id,f'Вы пополнили баланс пользователя с username:\n{user} \nНа {message.text} голды')
        except:
            bot.send_message(message.chat.id,'Что-то пошло не так. Проверьте правильность информации')
    else:
        a = bot.send_message(message.chat.id,'Админ панель',reply_markup=keyboards.markup_admin)
        bot.register_next_step_handler(a,admin_text)


def newsletter(message):
    if message.text != "Назад":
        conn = sqlite3.connect('Users.db')
        cursor = conn.cursor()
        users = [int(x) for x in cursor.execute(f"SELECT id FROM users WHERE id !='{message.chat.id}'").fetchall()[0]]
        conn.close()
        for i in users:
            bot.send_message(i,message.text)
        bot.send_message(message.chat.id,'Рассылка прошла успешна')
    else:
        a = bot.send_message(message.chat.id,'Админ панель',reply_markup=keyboards.markup_admin)
        bot.register_next_step_handler(a,admin_text)


@bot.message_handler(content_types=["text"])
def start(message):
    conn = sqlite3.connect('Users.db')
    cursor = conn.cursor()
    balance = cursor.execute(f"SELECT * FROM users WHERE id = '{message.chat.id}'").fetchall()[0][1]
    conn.commit()
    conn.close()
    if message.text == 'Профиль':
        bot.send_message(message.chat.id,f'Ваш баланс:\n{balance} голды')
    elif message.text == 'Отзывы по выводу':
        bot.send_message(message.chat.id,'Канал с отзывами:\n\n')
    elif message.text == 'Поддержка':
        bot.send_message(message.chat.id,'Аккаунт тех.поддержки:\n')
    elif message.text == 'Рефка':
        bot.send_message(message.chat.id,f"Вот ваша рефка: \nhttp://t.me/___?start={message.chat.id}")#Название бота
    elif message.text == 'Сапер':
        a = bot.send_message(message.chat.id,'Сколько вы хотите сделать ставку?')
        bot.register_next_step_handler(a,saper)
    elif message.text == 'Пополнить баланс':
        text = 'Отправьте деньги на любую из карт: \n\nCбер:\n____\nТиньк:\n_____\n\nТак же отправьте чек и скрины сюда \n@___\n\nКурс: 1г = 0.7 руб'
        bot.send_message(message.chat.id,text)
    elif message.text == 'Вывод':
        a = bot.send_message(message.chat.id,'Какую сумму вы хотите вывести?\nНапишите число\nВывод возможен от 100 голды')
        bot.register_next_step_handler(a,vivod)
    else:
        bot.send_message(message.chat.id,'Я вас не понял',reply_markup=keyboards.markup)


def saper(message):
        # Отправляем первое сообщение с клавиатурой
        minefield = [[f"n {y} {x}" for x in range(5)] for y in range(5)]
        # Размещаем мины случайным образом
        mine_positions = random.sample(range(5 * 5), 5)
        keyboard = keyboards.keyboard(minefield,mine_positions)
        try:
            conn = sqlite3.connect('Users.db')
            cursor = conn.cursor()
            minefield = str(minefield).replace("'", '"')
            cursor.execute(
                f"INSERT INTO mine (id, field, x, stavka) VALUES ('{message.from_user.id}','{minefield}','1',{int(message.text)})").fetchall()
            cursor.execute(f"UPDATE users SET money = money-{int(message.text)} WHERE id = {message.chat.id}")
            conn.commit()
            conn.close()
        except:
            conn = sqlite3.connect('Users.db')
            cursor = conn.cursor()
            minefield = str(minefield).replace("'", '"')
            cursor.execute(f"UPDATE mine SET field = '{minefield}' WHERE id = {message.chat.id}")
            cursor.execute(f"UPDATE users SET money = money-{int(message.text)} WHERE id = {message.chat.id}")
            cursor.execute(f"UPDATE mine SET stavka = {int(message.text)} WHERE id = {message.chat.id}")
            conn.commit()
            conn.close()
        bot.send_message(message.chat.id, "Добро пожаловать в игру в сапёр! Нажмите на клетку, чтобы открыть её.",
                         reply_markup=keyboard)



def vivod(message):
    try:
        if int(message.text)>=100:
            try:
                conn = sqlite3.connect('Users.db')
                cursor = conn.cursor()
                cursor.execute(f"UPDATE users SET money=money-{int(message.text)} WHERE id = '{message.chat.id}'")
                conn.commit()
                conn.close()
                bot.send_message(message.chat.id,'Выстовите скин которого не больше 6000 на рынке. И отправьте скрин сюда:\n@maksik_tag')
            except:
                bot.send_message(message.chat.id,'Накопите больше голды для вывода')
        else:
            bot.send_message(message.chat.id,'Нельзя выводить меньше 100 голды')
    except:
        bot.send_message(message.chat.id,'Вы ввели не число')



@bot.callback_query_handler(func=lambda call:True)
def but1_pressed(call):
    if 'n' in call.data:
        conn = sqlite3.connect('Users.db')
        cursor = conn.cursor()
        minefield = ast.literal_eval(cursor.execute(f"SELECT field FROM mine WHERE id = '{call.message.chat.id}'").fetchall()[0][0])
        minefield[int(call.data.split()[1])][int(call.data.split()[2])] = "NULL"
        coefficient = [1, 1.20, 1.5, 1.92, 2.49, 3.26, 4.34, 5.9, 8.16, 11.56, 16.82, 25.21, 39.23, 63.74, 109.26,
                       200.3,
                       400.59,
                       901.31, 2403.5, 8412.25, 50473.5]
        keyboard = keyboards.keyboard_call(minefield)
        minefield = str(minefield).replace("'", '"')
        cursor.execute(f"UPDATE mine SET field = '{minefield}' WHERE id = {call.message.chat.id}")
        x = cursor.execute(f"SELECT x FROM mine WHERE id = {call.message.chat.id}").fetchall()[0][0]
        cursor.execute(f"UPDATE mine SET x = '{coefficient[coefficient.index(float(x))+1]}' WHERE id = {call.message.chat.id}")
        conn.commit()
        conn.close()
        try:
            bot.edit_message_text(text=f"Ваш выигрыш умножен на {coefficient[coefficient.index(float(x))+1]}\nСледующее попадание умножит выигрыш на {coefficient[coefficient.index(float(x))+2]}",chat_id=call.message.chat.id, message_id=call.message.id,reply_markup=keyboard)
        except:
            bot.edit_message_text(
                text=f"Ваш выигрыш умножен на {coefficient[coefficient.index(float(x))+1]}\nВы собрали максимальный X",
                chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=keyboard)
    elif call.data == 'NULL':
        bot.send_message(call.message.chat.id,'Вы уже открывали эту ячейку')
    elif call.data == 'stop':
        conn = sqlite3.connect('Users.db')
        cursor = conn.cursor()
        x = cursor.execute(f"SELECT x FROM mine WHERE id = {call.message.chat.id}").fetchall()[0][0]
        stavka = cursor.execute(f"SELECT stavka FROM mine WHERE id = {call.message.chat.id}").fetchall()[0][0]
        cursor.execute(
            f"DELETE FROM mine WHERE id = {call.message.chat.id}")
        cursor.execute(f"UPDATE users SET money = money+{int(float(x)*int(stavka))} WHERE id = {call.message.chat.id}")
        conn.commit()
        conn.close()
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id, text=f'Ваш выигрыш умножен на {x}')


    else:
        conn = sqlite3.connect('Users.db')
        cursor = conn.cursor()
        cursor.execute(
            f"DELETE FROM mine WHERE id = {call.message.chat.id}")
        conn.commit()
        conn.close()
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id, text="Вы проиграли!")


while True:
    try:
        bot.polling(none_stop=True)
    except:
        pass

