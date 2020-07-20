import telebot
import sqlite3

from config import CONFIG

bot = telebot.TeleBot(CONFIG['info']['token'])

@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id, CONFIG['info']['command'])

@bot.message_handler(commands=['adduniversity'])
def start_message(message):
	bot.send_message(message.chat.id, 'Введите следующие параметры: УНИВЕРСИТЕТ ФАКУЛЬТЕТ БАЛЛ\n\nПример: БНТУ Программное обеспечение информационных технологий 340')
	bot.register_next_step_handler(message, next_step_addUniversity)

def next_step_addUniversity(message):
	database("ADD_UNIVERSITY", message.text.split())

@bot.message_handler(commands=['universitys'])
def start_message(message):
	bot.send_message(message.chat.id, 'ВУЗ ФАКУЛЬТЕТ БАЛЛ')
	bot.send_message(message.chat.id, show_university())

	# ДОП. ФУНКЦИИ

def show_university():
	university = ''

	db = sqlite3.connect('university_git.db')
	sql = db.cursor()

	sql.execute("SELECT univer, faculty_score FROM university")
	result = sql.fetchall()

	for a in result:
		university += f"{a[0]} {a[1]}\n\n"

	db.close()

	return university

def database(operation, text):
	db = sqlite3.connect('university_git.db')
	sql = db.cursor()

	if operation == "ADD_UNIVERSITY":
		newFalulty_Score = " ".join(text[1:])
		sql.execute(f"INSERT INTO university (univer, faculty_score) VALUES ('{text[0]}', '{newFalulty_Score}')")

	db.commit()
	db.close()

if __name__ == '__main__':
	print('start')
	bot.polling(none_stop=True, interval=0)