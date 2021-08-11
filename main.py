import logging
from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN, admin
import keyboard as kb
import functions as func
import sqlite3
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import Throttled

storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
connection = sqlite3.connect('data.db')
q = connection.cursor()

class st(StatesGroup):
	item = State()
	item2 = State()
	item3 = State()
	item4 = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	if result[0] == 0:
		if message.chat.id == admin:
			await message.answer('გაგიმარჯოს შე ყლეო!', reply_markup=kb.menu)
		else:
			await message.answer( f'გამარჯობა! {message.from_user.first_name} \nMonaspa - კიბერ უსაფრთხოების, ანონიმურობისა და კონფიდენციალურობის დაცვის კომპანიაა. დაარსებულია შვეიცარიაში.🇨🇭 \nდაწერეთ თქვენი შეკითხვა, დაგვიტოვეთ შეტყობინება ან გააფორმეთ შეკვეთა და ჩვენ დაგიკავშირდებით!')
	else:
		await message.answer('თქვენ დაბლოკილი ხართ!')


@dp.message_handler(content_types=['text'], text='👑 Admin Panel')
async def handfler(message: types.Message, state: FSMContext):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	if result[0] == 0:
		if message.chat.id == admin:
			await message.answer('კეთილი იყოს შენი მობრძანება ადმინ-პანელში.', reply_markup=kb.adm)

@dp.message_handler(content_types=['text'], text='⏪ უკან')
async def handledr(message: types.Message, state: FSMContext):
	await message.answer('გამარჯობა.', reply_markup=kb.menu)

@dp.message_handler(content_types=['text'], text='👿 შავი სია')
async def handlaer(message: types.Message, state: FSMContext):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	if result[0] == 0:
		if message.chat.id == admin:
			q.execute(f"SELECT * FROM users WHERE block == 1")
			result = q.fetchall()
			sl = []
			for index in result:
				i = index[0]
				sl.append(i)

			ids = '\n'.join(map(str, sl))
			await message.answer(f'შავ სიაში მყოფი მომხმარებლების ID:\n{ids}')

@dp.message_handler(content_types=['text'], text='✅ შავ სიაში დამატება')
async def hanadler(message: types.Message, state: FSMContext):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	if result[0] == 0:
		if message.chat.id == admin:
			await message.answer('შეიყვანეთ იმ მომხმარებლის ID, რომლის დაბლოკვაც გსურთ. \nდააჭირეთ ქვემო ღილაკს ოპერაციის გასაუქმებლად', reply_markup=kb.back)
			await st.item3.set()

@dp.message_handler(content_types=['text'], text='❎ შავი სიიდან წაშლა')
async def hfandler(message: types.Message, state: FSMContext):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	if result[0] == 0:
		if message.chat.id == admin:
			await message.answer('შეიყვანეთ იმ მომხმარებლის ID, რომლის განბლოკვა გსურთ.\nდააჭირეთ ქვემო ღილაკს ოპერაციის გასაუქმებლად', reply_markup=kb.back)
			await st.item4.set()

@dp.message_handler(content_types=['text'], text='💬 სპამი')
async def hangdler(message: types.Message, state: FSMContext):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	if result[0] == 0:
		if message.chat.id == admin:
			await message.answer('შეიყვანეთ ტექსტი გაგზავნისთვის.\n\nდააჭირეთ ქვემო ღილაკს ოპერაციის გასაუქმებლად', reply_markup=kb.back)
			await st.item.set()

@dp.message_handler(content_types=['text'])
@dp.throttled(func.antiflood, rate=3)
async def h(message: types.Message, state: FSMContext):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	if result[0] == 0:
		if message.chat.id == admin:
			pass
		else:
			await message.answer('თქვენი შეტყობინება გაგზავნილია. გიპასუხებთ მომავალში.')
			await bot.send_message(admin, f"<b>მიღებულია ახლაი წერილი!</b>\n<b>წერილის ავტორი:</b> {message.from_user.mention}\nID: {message.chat.id}\n<b>წერილი:</b> {message.text}", reply_markup=kb.fun(message.chat.id), parse_mode='HTML')
	else:
		await message.answer('თქვენ დაბლოკილი ხართ ბოტში!')


@dp.callback_query_handler(lambda call: True) # Inline ნაწილი
async def cal(call, state: FSMContext):
	if 'ans' in call.data:
		a = call.data.index('-ans')
		ids = call.data[:a]
		await call.message.answer('შეიყვანეთ პასუხი მომხმარებლისთვის:', reply_markup=kb.back)
		await st.item2.set() # ადმინი პასუხობს მომხმარებელს
		await state.update_data(uid=ids)
	elif 'ignor' in call.data:
		await call.answer('წაშლილია')
		await bot.delete_message(call.message.chat.id, call.message.message_id)
		await state.finish()

@dp.message_handler(state=st.item2)
async def proc(message: types.Message, state: FSMContext):
	if message.text == '⏪ გაუქმება':
		await message.answer('გაუქმება! უკან ვაბრუნებ.', reply_markup=kb.menu)
		await state.finish()
	else:
		await message.answer('Შეტყობინება გაგზავნილია.', reply_markup=kb.menu)
		data = await state.get_data()
		id = data.get("uid")
		await state.finish()
		await bot.send_message(id, 'თქვენ მიიღეთ პასუხი ადმინისტრატორისგან:\n\nტექსტი: {}'.format(message.text))

@dp.message_handler(state=st.item)
async def process_name(message: types.Message, state: FSMContext):
	q.execute(f'SELECT user_id FROM users')
	row = q.fetchall()
	connection.commit()
	text = message.text
	if message.text == '⏪ გაუქმება':
		await message.answer('გაუქმება!ვაბრუნებ უკან.', reply_markup=kb.adm)
		await state.finish()
	else:
		info = row
		await message.answer('სპამი დაწყებულია!', reply_markup=kb.adm)
		for i in range(len(info)):
			try:
				await bot.send_message(info[i][0], str(text))
			except:
				pass
		await message.answer('სპამი დასრულებულია!', reply_markup=kb.adm)
		await state.finish()


@dp.message_handler(state=st.item3)
async def proce(message: types.Message, state: FSMContext):
	if message.text == '⏪ გაუქმება':
		await message.answer('გაუქმება! ვაბრუნებ უკან.', reply_markup=kb.adm)
		await state.finish()
	else:
		if message.text.isdigit():
			q.execute(f"SELECT block FROM users WHERE user_id = {message.text}")
			result = q.fetchall()
			connection.commit()
			if len(result) == 0:
				await message.answer('მონაცემთა ბაზაში ასეთი მომხმარებელი არ მოიძებნა.', reply_markup=kb.adm)
				await state.finish()
			else:
				a = result[0]
				id = a[0]
				if id == 0:
					q.execute(f"UPDATE users SET block = 1 WHERE user_id = {message.text}")
					connection.commit()
					await message.answer('მომხმარებელი წარმატები დაიმატა შავ სიაში.', reply_markup=kb.adm)
					await state.finish()
					await bot.send_message(message.text, 'თქვენ დაბლოკილი ხართ ბოტში.')
				else:
					await message.answer('ეს მომხმარებელი შავ სიაშია დამატებული!', reply_markup=kb.adm)
					await state.finish()
		else:
			await message.answer('ბრძანება არასწორია!...\nშეიყვანეთ ID')

@dp.message_handler(state=st.item4)
async def proc(message: types.Message, state: FSMContext):
	if message.text == '⏪ გაუქმება':
		await message.answer('გაუქმება! ვაბრუნებ უკან.', reply_markup=kb.adm)
		await state.finish()
	else:
		if message.text.isdigit():
			q.execute(f"SELECT block FROM users WHERE user_id = {message.text}")
			result = q.fetchall()
			connection.commit()
			if len(result) == 0:
				await message.answer('მონაცემთა ბაზაში ასეთი მომხმარებელი არ მოიძებნა.', reply_markup=kb.adm)
				await state.finish()
			else:
				a = result[0]
				id = a[0]
				if id == 1:
					q.execute(f"UPDATE users SET block = 0 WHERE user_id = {message.text}")
					connection.commit()
					await message.answer('მომხმარებელი წარმატებით განიბლოკა.', reply_markup=kb.adm)
					await state.finish()
					await bot.send_message(message.text, 'თქვენ განბლოკილი ხართ ადმინისტრაციის მიერ.')
				else:
					await message.answer('მომხმარებელმა არ დაიბლოკა.', reply_markup=kb.adm)
					await state.finish()
		else:
			await message.answer('ბრძანება არასწორია!...\nშეიყვანეთ ID')

if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)