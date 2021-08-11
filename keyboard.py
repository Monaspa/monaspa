from aiogram import types


menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(
    types.KeyboardButton('👑 Admin Panel')
)

adm = types.ReplyKeyboardMarkup(resize_keyboard=True)
adm.add(
    types.KeyboardButton('👿 შავი სია'),
    types.KeyboardButton('✅ შავ სიაში დამატება'),
    types.KeyboardButton('❎ შავი სიიდან წაშლა')
)
adm.add(types.KeyboardButton('💬 სპამი'))
adm.add('⏪ უკან')

back = types.ReplyKeyboardMarkup(resize_keyboard=True)
back.add(
    types.KeyboardButton('⏪ გაუქმება')
)


def fun(user_id):
    quest = types.InlineKeyboardMarkup(row_width=3)
    quest.add(
        types.InlineKeyboardButton(text='💬 პასუხი', callback_data=f'{user_id}-ans'),
        types.InlineKeyboardButton(text='❎ წაშლა', callback_data='ignor')
    )
    return quest