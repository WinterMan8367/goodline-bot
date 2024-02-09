import telebot
from telebot import types

testbot = telebot.TeleBot("6454477981:AAFT67o3MnnNlXtjzGZezpOkLaNkw819N_E")
inmenu = types.InlineKeyboardButton(text = "В главное меню", callback_data = "inmenu")

@testbot.message_handler(commands = ['start'])
def start_keyboard(message):
  keyboard = types.InlineKeyboardMarkup()
  ACB = types.InlineKeyboardButton(text = "Активная клиентская база", callback_data = "ACB")
  money = types.InlineKeyboardButton(text = "Деньги", callback_data = "money")
  sells = types.InlineKeyboardButton(text = "Продажи", callback_data = "sells")
  keyboard.add(ACB, money, sells)
  testbot.send_message(message.chat.id, f"Привет, {message.from_user.first_name} {message.from_user.last_name} ✌️\nЭто тестовый бот. Выберите раздел:", reply_markup = keyboard)

@testbot.callback_query_handler(func=lambda call: True)
def test_callback(call):
  if call.message:
    if call.data == "inmenu":
      keyboard = types.InlineKeyboardMarkup()
      ACB = types.InlineKeyboardButton(text = "Активная клиентская база", callback_data = "ACB")
      money = types.InlineKeyboardButton(text = "Деньги", callback_data = "money")
      sells = types.InlineKeyboardButton(text = "Продажи", callback_data = "sells")
      keyboard.add(ACB, money, sells)
      testbot.edit_message_text("Вы вернулись в главное меню. Выберите раздел:", call.message.chat.id, call.message.id, reply_markup = keyboard)
      testbot.answer_callback_query(call.id)
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
      testbot.answer_callback_query(call.id)
    elif call.data == "money":
      keyboard = types.InlineKeyboardMarkup()
      receipts = types.InlineKeyboardButton(text = "Поступления", callback_data = "receipts")
      production = types.InlineKeyboardButton(text = "Реализация", callback_data = "production")
      keyboard.row(receipts, production)
      keyboard.row(inmenu)
      testbot.edit_message_text("Выберите подраздел:", call.message.chat.id, call.message.id, reply_markup = keyboard)
      testbot.answer_callback_query(call.id)
    else:
      testbot.send_message(call.message.chat.id, "Error. Data: " + call.data)
      testbot.answer_callback_query(call.id)

testbot.infinity_polling()