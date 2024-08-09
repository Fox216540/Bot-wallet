from telebot import types as typ

markup = typ.ReplyKeyboardMarkup(True,None,None)
item1 = typ.KeyboardButton('Профиль')
item2 = typ.KeyboardButton('Отзывы по выводу')
item3 = typ.KeyboardButton('Поддержка')
item4 = typ.KeyboardButton('Рефка')
item5 = typ.KeyboardButton('Сапер')
item6 = typ.KeyboardButton('Ежедневный бонус')
item7 = typ.KeyboardButton('Пополнить баланс')
item8 = typ.KeyboardButton('Вывод')


markup.add(item1,item2,item3)
markup.add(item4,item5,item8)
markup.add(item7)

markup_admin = typ.ReplyKeyboardMarkup(True,one_time_keyboard=True)
item1 = typ.KeyboardButton('Рассылка')
item2 = typ.KeyboardButton('Пополнить баланс юзеру')
item3 = typ.KeyboardButton('Забрать баланс юзера')
item4 = typ.KeyboardButton('Удалить канал спонсора')
item5 = typ.KeyboardButton('Добавить канал спонсора')
item6 = typ.KeyboardButton('Спонсорские каналы')
item7 = typ.KeyboardButton('Назад')
item8 = typ.KeyboardButton('Статистика')


markup_admin.add(item1,item2)
markup_admin.add(item3,item4)
markup_admin.add(item5,item6)
markup_admin.add(item7)
markup_admin.add(item8)

def keyboard(minefield,mine_positions):
    keyboard = typ.InlineKeyboardMarkup()
    stop = typ.InlineKeyboardButton(text=f"stop", callback_data=f"stop")
    for pos in mine_positions:
        row, col = divmod(pos, 5)
        minefield[row][col] = f"y {row} {col}"
    for x in minefield:
        # добавляем на нее две кнопки
        button1 = typ.InlineKeyboardButton(text=f"⬜️", callback_data=f"{x[0]}")
        button2 = typ.InlineKeyboardButton(text=f"⬜️", callback_data=f"{x[1]}")
        button3 = typ.InlineKeyboardButton(text=f"⬜️", callback_data=f"{x[2]}")
        button4 = typ.InlineKeyboardButton(text=f"⬜️", callback_data=f"{x[3]}")
        button5 = typ.InlineKeyboardButton(text=f"⬜️", callback_data=f"{x[4]}")
        keyboard.row(button1, button2, button3, button4, button5)
    keyboard.add(stop)
    return keyboard

def keyboard_call(minefield):
    keyboard = typ.InlineKeyboardMarkup()
    stop = typ.InlineKeyboardButton(text=f"stop", callback_data=f"stop")
    for x in minefield:
        button1 = typ.InlineKeyboardButton(text=f"⬜️", callback_data=f"{x[0]}")
        button2 = typ.InlineKeyboardButton(text=f"⬜️", callback_data=f"{x[1]}")
        button3 = typ.InlineKeyboardButton(text=f"⬜️", callback_data=f"{x[2]}")
        button4 = typ.InlineKeyboardButton(text=f"⬜️", callback_data=f"{x[3]}")
        button5 = typ.InlineKeyboardButton(text=f"⬜️", callback_data=f"{x[4]}")
        if x[0] == 'NULL':
            button1 = typ.InlineKeyboardButton(text=f"🌟", callback_data=f"NULL")
        if x[1] == 'NULL':
            button2 = typ.InlineKeyboardButton(text=f"🌟", callback_data=f"NULL")
        if x[2] == 'NULL':
            button3 = typ.InlineKeyboardButton(text=f"🌟", callback_data=f"NULL")
        if x[3] == 'NULL':
            button4 = typ.InlineKeyboardButton(text=f"🌟", callback_data=f"NULL")
        if x[4] == 'NULL':
            button5 = typ.InlineKeyboardButton(text=f"🌟", callback_data=f"NULL")
        keyboard.row(button1, button2, button3, button4, button5)
    keyboard.add(stop)
    return keyboard


