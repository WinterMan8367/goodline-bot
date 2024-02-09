import telebot
from telebot import types

testbot = telebot.TeleBot("6454477981:AAFT67o3MnnNlXtjzGZezpOkLaNkw819N_E")
inmenu = types.InlineKeyboardButton(text = "В главное меню", callback_data = "inmenu")
back = types.InlineKeyboardButton(text = "Назад", callback_data = "back")

user_dict = {}

class User:
  def __init__(self, user_id):
    self.user_id = user_id
    self.history = []
    self.previos_page = None

  def __str__(self):
    return f"user_id: {self.user_id}\nhistory: {self.history}\nprevios_page: {self.previos_page}"

@testbot.message_handler(commands = ['start'])
def start_keyboard(message):
  keyboard = types.InlineKeyboardMarkup()
  ACB = types.InlineKeyboardButton(text = "Активная клиентская база", callback_data = "ACB")
  money = types.InlineKeyboardButton(text = "Деньги", callback_data = "money")
  sells = types.InlineKeyboardButton(text = "Продажи", callback_data = "sells")
  keyboard.add(ACB, money, sells)
  testbot.send_message(message.chat.id, f"Привет, {message.from_user.first_name} {message.from_user.last_name} ✌️\nЭто тестовый бот.\nВыберите раздел:", reply_markup = keyboard)
  user_id = message.from_user.id
  user = User(user_id)
  user_dict[message.chat.id] = user

@testbot.message_handler(commands = ['debug'])
def debug(message):
  testbot.send_message(message.chat.id, user_dict)
  testbot.send_message(message.chat.id, user_dict[message.chat.id])

@testbot.callback_query_handler(func=lambda call: True)
def test_callback(call):
  if call.message:
    if call.data == "inmenu":
      keyboard = types.InlineKeyboardMarkup()
      ACB = types.InlineKeyboardButton(text = "Активная клиентская база", callback_data = "ACB")
      money = types.InlineKeyboardButton(text = "Деньги", callback_data = "money")
      sells = types.InlineKeyboardButton(text = "Продажи", callback_data = "sells")
      keyboard.add(ACB, money, sells)
      testbot.edit_message_text("Вы вернулись в главное меню.\nВыберите раздел:", call.message.chat.id, call.message.id, reply_markup = keyboard)
      user_dict[call.message.chat.id].history.clear()
      user_dict[call.message.chat.id].previos_page = None
      testbot.answer_callback_query(call.id)
    elif call.data == "back":
      print()
    elif call.data == "ACB":
      keyboard = types.InlineKeyboardMarkup()
      totalACB = types.InlineKeyboardButton(text = "Общая АКБ уникального абонента", callback_data = "totalACB")
      news = types.InlineKeyboardButton(text = "Новые", callback_data = "news")
      outflow = types.InlineKeyboardButton(text = "Отток", callback_data = "outflow")
      rtrn = types.InlineKeyboardButton(text = "Возврат", callback_data = "rtrn")
      keyboard.row(totalACB)
      keyboard.row(news, outflow, rtrn)
      keyboard.row(inmenu)
      testbot.edit_message_text("Выберите подраздел:", call.message.chat.id, call.message.id, reply_markup = keyboard)
      user = user_dict[call.message.chat.id]
      user.history.append(call.data)
      testbot.answer_callback_query(call.id)
    elif call.data == "totalACB":
      keyboard = types.InlineKeyboardMarkup()
      apartment = types.InlineKeyboardButton(text = "МКД", callback_data = "apartment")
      general = types.InlineKeyboardButton(text = "Общая", callback_data = "general")
      gepon = types.InlineKeyboardButton(text = "GePON", callback_data = "gepon")
      keyboard.row(apartment, general, gepon)
      keyboard.row(back, inmenu)
      testbot.edit_message_text("Выберите подраздел:", call.message.chat.id, call.message.id, reply_markup = keyboard)
      user = user_dict[call.message.chat.id]
      user.previos_page = user.history[-1]
      user.history.append(call.data)
      testbot.answer_callback_query(call.id)
    elif call.data == "money":
      keyboard = types.InlineKeyboardMarkup()
      receipts = types.InlineKeyboardButton(text = "Поступления", callback_data = "receipts")
      production = types.InlineKeyboardButton(text = "Реализация", callback_data = "production")
      keyboard.row(receipts, production)
      keyboard.row(inmenu)
      testbot.edit_message_text("Выберите подраздел:", call.message.chat.id, call.message.id, reply_markup = keyboard)
      user = user_dict[call.message.chat.id]
      user.history.append(call.data)
      testbot.answer_callback_query(call.id)
    else:
      testbot.send_message(call.message.chat.id, "Error. Data: " + call.data)
      testbot.answer_callback_query(call.id)

testbot.infinity_polling()