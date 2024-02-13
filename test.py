import telebot
from telebot import types

testbot = telebot.TeleBot("6454477981:AAFT67o3MnnNlXtjzGZezpOkLaNkw819N_E")
inmenu = types.InlineKeyboardButton(text = "Главное меню", callback_data = "inmenu")
back = types.InlineKeyboardButton(text = "Назад", callback_data = "back")

user_dict = {}

class User:
  def __init__(self, user_id):
    self.user_id = user_id
    self.history = []
    self.back = False

  def __str__(self):
    return f"user_id: {self.user_id}\nhistory: {self.history}\nback: {self.back}"

# Обозначение кнопки
def record_button(text_button, callback):
  return types.InlineKeyboardButton(text = text_button, callback_data = callback)

def record_func(user, data):
  if not user.back:
    user.history.append(data)
  else:
    user.back = False

# Запуск бота + отправка номера телефона ------------------------------------ (Доделать)
@testbot.message_handler(commands = ['start'])
def start_message(message):
  keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
  reg_button = types.KeyboardButton(text = "Отправить номер телефона", request_contact = True)
  keyboard.add(reg_button)
  testbot.send_message(message.chat.id, 'Привет! Я — корпоративный бот-аналитик для сотрудников Е-Лайт-Телеком.\nЯ предоставляю им структурированную информацию по выбранным категориям в виде отчётов, графиков, эксель-таблицы.\n\nОтправь мне свой номер телефона, чтобы я проверил, а действительно ли ты наш работник.', reply_markup=keyboard)
# ---------------------------------------------------------------------------------

@testbot.message_handler(content_types = ['contact'])
def echo(message):
  testbot.send_message(message.chat.id, message.contact.phone_number, reply_markup = types.ReplyKeyboardRemove())

# Запуск бота [/Start] + Главное меню ---> {АКБ}, {Деньги}, {Продажи}
@testbot.message_handler(commands = ['menu'])
def start_keyboard(message):
  keyboard = types.InlineKeyboardMarkup()

  button_ACB = record_button("Активная клиентская база", "ACB")
  button_money = record_button("Деньги", "money")
  button_sales = record_button("Продажи", "sales")

  keyboard.add(button_ACB)
  keyboard.add(button_money, button_sales)

  testbot.send_message(message.chat.id, "Какую информацию ты хочешь узнать? 💬", reply_markup = keyboard)

  # Присвоение класса [User]
  if user_dict.get(message.chat.id) == None:
    user_id = message.from_user.id
    user = User(user_id)
    user_dict[message.chat.id] = user
  else: user.history.clear()

# -----------------------------------------------------
  
@testbot.message_handler(commands = ['debug'])
def debug(message):
  keyboard = types.InlineKeyboardMarkup()
  reload_btn = types.InlineKeyboardButton(text = "Обновить", callback_data = "reload")
  keyboard.add(reload_btn)
  text = ""
  for item in user_dict:
    text += f"\n{item};"
  testbot.send_message(message.chat.id, f"Текущие пользователи:\n{text}\n---------------------\nТекущий сеанс:\n\n{user_dict[message.chat.id]}", reply_markup = keyboard)

# Навигация в меню - [Обработки]
@testbot.callback_query_handler(func = lambda call: True)
def test_callback(call):
  if call.message:

    keyboard = types.InlineKeyboardMarkup()
    chat_id = call.message.chat.id
    msg_id = call.message.id
    user = user_dict[chat_id]

    # Вернуться на один раздел назад
    if call.data == "back":
      user.history.pop()

      call.data = user.history[-1] if len(user.history) != 0 else "inmenu"

      user.back = True

      testbot.answer_callback_query(call.id)

    if call.data == "reload":
      try:
        reload_btn = record_button("Обновить", "reload")
        keyboard.add(reload_btn)

        text = ""
        for item in user_dict:
          text += f"\n{item};"

        testbot.edit_message_text(f"Текущие пользователи:\n{text}\n---------------------\nТекущий сеанс:\n\n{user}", chat_id, msg_id, reply_markup = keyboard)

        testbot.answer_callback_query(call.id)
      except:
        testbot.answer_callback_query(call.id)

    # АКБ ---> {Общая АКБ}, {Новые}, {Отток}, {Возврат}
    if call.data == "ACB":
      button_total_ACB = record_button("Общая АКБ уникального абонента", "total_ACB")
      button_new = record_button("Новые", "new")
      button_outflow = record_button("Отток", "outflow")
      button_return = record_button("Возврат", "return")

      keyboard.add(button_total_ACB)
      keyboard.add(button_new, button_outflow, button_return)
      keyboard.add(inmenu)

      testbot.edit_message_text('Выбери пункт, по которому хочешь получить результат:', chat_id, msg_id, reply_markup = keyboard)

      record_func(user, call.data)

      testbot.answer_callback_query(call.id)
    # -----------------------------------------------------

    # Деньги ---> {Поступления}, {Реализация}
    elif call.data == "money":
      button_cash_receipts = record_button("Поступления", "cash_receipts")
      button_implementation = record_button("Реализация", "implementation")

      keyboard.add(button_cash_receipts, button_implementation)
      keyboard.add(inmenu)

      testbot.edit_message_text('Выбери пункт, по которому хочешь получить результат:', chat_id, msg_id, reply_markup = keyboard)

      record_func(user, call.data)

      testbot.answer_callback_query(call.id)
    # -----------------------------------------------------

    # Продажи ---> {Услуги}, {Оборудование}
    elif call.data == "sales":
      button_services = record_button("Услуги", "services")
      button_equipment = record_button("Оборудование", "equipment")

      keyboard.add(button_services, button_equipment);
      keyboard.add(inmenu)

      testbot.edit_message_text('Выбери пункт, по которому хочешь получить результат:', chat_id, msg_id, reply_markup = keyboard)

      record_func(user, call.data)

      testbot.answer_callback_query(call.id)
    # -----------------------------------------------------

    # {МКД}, {Общая}, {Гепон}
    elif call.data in ["total_ACB", "new", "outflow", "return", "cash_receipts", "implementation", "all_channels", "selection_channel"]:
      button_apartment = record_button("МКД (Многоквартирные дома)", "apartment")
      button_general = record_button("Общая", "general")
      button_gepon = record_button("Гепон", "gepon")

      if call.data in ["all_channels", "selection_channel"]:
        keyboard.add(button_apartment, button_gepon)
      else:
        keyboard.add(button_apartment)
        keyboard.add(button_general, button_gepon)
      keyboard.add(back, inmenu)

      testbot.edit_message_text('Выбери пункт, по которому хочешь получить результат:', chat_id, msg_id, reply_markup = keyboard)

      record_func(user, call.data)

      testbot.answer_callback_query(call.id)
    # -----------------------------------------------------

    # {Все города}, {По городам}, {По районам}
    elif user.history[0] != "sales" and call.data in ["apartment", "general", "gepon"]:
      button_all_cities = record_button("Все города", "all_cities")
      button_by_city = record_button("По городам", "by_city")
      button_by_district = record_button("По районам", "by_district")

      if user.history[0] == "ACB" and call.data != "gepon":
        keyboard.add(button_all_cities, button_by_city)
      else:
        keyboard.add(button_all_cities, button_by_city, button_by_district)
      keyboard.add(back, inmenu)

      testbot.edit_message_text('Выбери пункт, по которому хочешь получить результат:', chat_id, msg_id, reply_markup = keyboard)

      record_func(user, call.data)

      testbot.answer_callback_query(call.id)
    # -----------------------------------------------------

    # {По статусу}, {Платящая}
    elif user.history[0] == "ACB" and call.data in ["all_cities", "by_city", "by_district"]:
      button_by_status = record_button("По статусу", "by_status")
      button_by_paying = record_button("Платящая", "by_paying")

      keyboard.add(button_by_status, button_by_paying)
      keyboard.add(back, inmenu)

      testbot.edit_message_text('Выбери пункт, по которому хочешь получить результат:', chat_id, msg_id, reply_markup = keyboard)

      record_func(user, call.data)

      testbot.answer_callback_query(call.id)
    # -----------------------------------------------------

    # {Текущий месяц}, {Предыдущий месяц}, {Текущий год}, {Статистика за 3 года}
    elif call.data in ["by_status", "by_paying", "services", "equipment"]:
      button_current_month = record_button("Текущий месяц", "current_month")
      button_previous_month = record_button("Предыдущий месяц", "previous_month")
      button_this_year = record_button("Текущий год", "this_year")
      button_statistics_3years = record_button("Статистика за 3 года", "statistics_3years")

      if user.history[0] == "ACB":
        keyboard.add(button_previous_month, button_this_year, button_statistics_3years)
      else:
        keyboard.add(button_current_month, button_previous_month)
        keyboard.add(button_this_year, button_statistics_3years)
      keyboard.add(back, inmenu)

      testbot.edit_message_text('Выбери пункт, по которому хочешь получить результат:', chat_id, msg_id, reply_markup = keyboard)

      record_func(user, call.data)

      testbot.answer_callback_query(call.id)
    # -----------------------------------------------------

    # {По всем каналам}, {Выбор канала}
    elif (user.history[0] == "sales") and call.data in ["current_month", "previous_month", "this_year", "statistics_3years"]:
      button_all_channels = record_button("По всем каналам", "all_channels")
      button_selection_channel = record_button("Выбор канала", "selection_channel")

      keyboard.add(button_all_channels, button_selection_channel)
      keyboard.add(back, inmenu)

      testbot.edit_message_text('Выбери пункт, по которому хочешь получить результат:', chat_id, msg_id, reply_markup = keyboard)

      record_func(user, call.data)

      testbot.answer_callback_query(call.id)
    # -----------------------------------------------------

    # {Таблица}, {Диаграмма}, {Эксель}
    elif  (user.history[0] == "ACB" and call.data in ["previous_month", "this_year", "statistics_3years"]) or (user.history[0] == "money" and call.data in ["all_cities", "by_city", "by_district"]) or (user.history[0] == "sales" and call.data in ["apartment", "gepon"]):
      button_table = record_button("Таблица", "table")
      button_diagram = record_button("Диаграмма", "diagram")
      button_excel = record_button("Эксель", "excel")

      keyboard.add(button_table, button_diagram, button_excel)
      keyboard.add(back, inmenu)

      testbot.edit_message_text('Выбери пункт, по которому хочешь получить результат:', chat_id, msg_id, reply_markup = keyboard)

      record_func(user, call.data)

      testbot.answer_callback_query(call.id)
    # -----------------------------------------------------

    elif call.data == "inmenu":
      button_ACB = record_button("Активная клиентская база", "ACB")
      button_money = record_button("Деньги", "money")
      button_sales = record_button("Продажи", "sales")

      keyboard.add(button_ACB)
      keyboard.add(button_money, button_sales)

      testbot.edit_message_text("Вы вернулись в главное меню.\n Какую информацию ты хочешь узнать? 💬", chat_id, msg_id, reply_markup = keyboard)

      user.history.clear()

      testbot.answer_callback_query(call.id)

    else:
      if call.data != 'reload':
        testbot.send_message(chat_id, "Error. Data: " + str(call.data))
        testbot.answer_callback_query(call.id)

testbot.infinity_polling()