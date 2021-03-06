from aiogram import types


menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(
    types.KeyboardButton('๐ Admin Panel')
)

adm = types.ReplyKeyboardMarkup(resize_keyboard=True)
adm.add(
    types.KeyboardButton('๐ฟ แจแแแ แกแแ'),
    types.KeyboardButton('โ แจแแ แกแแแจแ แแแแแขแแแ'),
    types.KeyboardButton('โ แจแแแ แกแแแแแ แฌแแจแแ')
)
adm.add(types.KeyboardButton('๐ฌ แกแแแแ'))
adm.add('โช แฃแแแ')

back = types.ReplyKeyboardMarkup(resize_keyboard=True)
back.add(
    types.KeyboardButton('โช แแแฃแฅแแแแ')
)


def fun(user_id):
    quest = types.InlineKeyboardMarkup(row_width=3)
    quest.add(
        types.InlineKeyboardButton(text='๐ฌ แแแกแฃแฎแ', callback_data=f'{user_id}-ans'),
        types.InlineKeyboardButton(text='โ แฌแแจแแ', callback_data='ignor')
    )
    return quest