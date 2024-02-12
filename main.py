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
    self.previos_page = None
    self.back = False

  def __str__(self):
    return f"user_id: {self.user_id}\nhistory: {self.history}\nprevios_page: {self.previos_page}\nback: {self.back}"

@testbot.message_handler(commands = ['start'])
def start_keyboard(message):
  keyboard = types.InlineKeyboardMarkup()

  button_ACB = types.InlineKeyboardButton(text = "Активная клиентская база", callback_data = "ACB")
  button_money = types.InlineKeyboardButton(text = "Деньги", callback_data = "money")
  button_sales = types.InlineKeyboardButton(text = "Продажи", callback_data = "sales")

  keyboard.add(button_ACB)
  keyboard.add(button_money, button_sales)

  testbot.send_message(message.chat.id, f"Привет, {message.from_user.first_name} ✌️\nЧто ты хочешь узнать?", reply_markup = keyboard)

  user_id = message.from_user.id
  user = User(user_id)
  user_dict[message.chat.id] = user

@testbot.message_handler(commands = ['debug'])
def debug(message):
  keyboard = types.InlineKeyboardMarkup()
  reload_btn = types.InlineKeyboardButton(text = "Обновить", callback_data = "reload")
  keyboard.add(reload_btn)
  testbot.send_message(message.chat.id, user_dict)
  testbot.send_message(message.chat.id, user_dict[message.chat.id], reply_markup = keyboard)

@testbot.callback_query_handler(func = lambda call: True)
def test_callback(call):
  if call.message:

    if call.data == "back":
      user = user_dict[call.message.chat.id]
      user.history.pop()
      call.data = user.previos_page
      length_of_history = len(user.history)
      if length_of_history <= 1:
        user.previos_page = None
      else:
        user.previos_page = user.history[-2]
      user.back = True
      testbot.answer_callback_query(call.id)

    # --> 1) Меню [Общая АКБ], [Новые], [Отток], [Возврат]
    if call.data == "ACB":
      keyboard = types.InlineKeyboardMarkup()

      button_total_ACB = types.InlineKeyboardButton(text = "Общая АКБ уникального абонента", callback_data = "total_ACB")
      button_new = types.InlineKeyboardButton(text = "Новые", callback_data = "new")
      button_outflow = types.InlineKeyboardButton(text = "Отток", callback_data = "outflow")
      button_return = types.InlineKeyboardButton(text = "Возврат", callback_data = "return")

      keyboard.add(button_total_ACB);
      keyboard.add(button_new, button_outflow, button_return);
      keyboard.add(inmenu)

      testbot.edit_message_text('Выберете пункт, по которому хотите получить результат:', call.message.chat.id, call.message.id, reply_markup = keyboard)

      user = user_dict[call.message.chat.id]
      if not user.back:
        user.history.append(call.data)
      else:
        user.back = False

      testbot.answer_callback_query(call.id)

    # --> 2) Меню [Поступления], [Реализация]
    elif call.data == "money":
      keyboard = types.InlineKeyboardMarkup()

      button_cash_receipts = types.InlineKeyboardButton(text = "Поступления", callback_data = "cash_receipts")
      button_implementation = types.InlineKeyboardButton(text = "Реализация", callback_data = "implementation")

      keyboard.add(button_cash_receipts, button_implementation);
      keyboard.add(inmenu)

      testbot.edit_message_text('Выберете пункт, по которому хотите получить результат:', call.message.chat.id, call.message.id, reply_markup = keyboard)

      user = user_dict[call.message.chat.id]
      if not user.back:
        user.history.append(call.data)
      else:
        user.back = False

      testbot.answer_callback_query(call.id)

    # --> 3) Меню [Услуги], [Оборудование]
    elif call.data == "sales":
      keyboard = types.InlineKeyboardMarkup()

      button_services = types.InlineKeyboardButton(text = "Услуги", callback_data = "services")
      button_equipment = types.InlineKeyboardButton(text = "Оборудование", callback_data = "equipment")

      keyboard.add(button_services, button_equipment);
      keyboard.add(inmenu)

      testbot.edit_message_text('Выберете пункт, по которому хотите получить результат:', call.message.chat.id, call.message.id, reply_markup = keyboard)

      user = user_dict[call.message.chat.id]
      if not user.back:
        user.history.append(call.data)
      else:
        user.back = False

      testbot.answer_callback_query(call.id)

    # --> Меню [МКД], [Общая], [Гепон]
    elif call.data == "total_ACB" or call.data == "new" or call.data == "outflow" or call.data == "return" or call.data == "cash_receipts" or call.data == "implementation":
      keyboard = types.InlineKeyboardMarkup()

      button_apartment = types.InlineKeyboardButton(text = "МКД (Многоквартирные дома)", callback_data = "apartment")
      button_general = types.InlineKeyboardButton(text = "Общая", callback_data = "general")
      button_gepon = types.InlineKeyboardButton(text = "Гепон", callback_data = "gepon")

      if call.data == "cash_receipts" or call.data == "implementation":
        button_apartment2 = types.InlineKeyboardButton(text = "МКД (Многоквартирные дома)", callback_data = "apartment_money")
        button_general2 = types.InlineKeyboardButton(text = "Общая", callback_data = "general_money")
        button_gepon2 = types.InlineKeyboardButton(text = "Гепон", callback_data = "gepon_money")

        keyboard.add(button_apartment2)
        keyboard.add(button_general2, button_gepon2)
      else:
        keyboard.add(button_apartment)
        keyboard.add(button_general, button_gepon)
      keyboard.add(back, inmenu)

      testbot.edit_message_text('Выберете пункт, по которому хотите получить результат:', call.message.chat.id, call.message.id, reply_markup = keyboard)
      user = user_dict[call.message.chat.id]
      if not user.back:
        user.previos_page = user.history[-1]
        user.history.append(call.data)
      else:
        user.back = False
      testbot.answer_callback_query(call.id)

    # --> Меню [Все города], [По городам], [По районам]
    elif call.data == "apartment" or call.data == "general" or call.data == "gepon" or call.data == "apartment_money" or call.data == "general_money" or call.data == "gepon_money":
      keyboard = types.InlineKeyboardMarkup()

      if call.data == "gepon_money" or call.data == "apartment_money" or call.data == "general_money":
        button_all_cities = types.InlineKeyboardButton(text = "Все города", callback_data = "oops")
        button_by_city = types.InlineKeyboardButton(text = "По городам", callback_data = "oops")
        button_by_district = types.InlineKeyboardButton(text = "По районам", callback_data = "oops")

        keyboard.add(button_all_cities, button_by_city, button_by_district)
      elif call.data == "gepon":
        button_all_cities = types.InlineKeyboardButton(text = "Все города", callback_data = "all_cities")
        button_by_city = types.InlineKeyboardButton(text = "По городам", callback_data = "by_city")
        button_by_district = types.InlineKeyboardButton(text = "По районам", callback_data = "by_district")

        keyboard.add(button_all_cities, button_by_city, button_by_district)
      else:
        button_all_cities = types.InlineKeyboardButton(text = "Все города", callback_data = "all_cities")
        button_by_city = types.InlineKeyboardButton(text = "По городам", callback_data = "by_city")
        button_by_district = types.InlineKeyboardButton(text = "По районам", callback_data = "by_district")

        keyboard.add(button_all_cities, button_by_city)
      keyboard.add(back, inmenu)

      testbot.edit_message_text('Выберете пункт, по которому хотите получить результат:', call.message.chat.id, call.message.id, reply_markup = keyboard)
      user = user_dict[call.message.chat.id]
      if not user.back:
        user.previos_page = user.history[-1]
        user.history.append(call.data)
      else:
        user.back = False
      testbot.answer_callback_query(call.id)

    # --> Меню [По статусу], [Платящая]
    elif call.data == "all_cities" or call.data == "by_city" or call.data == "by_district":
      keyboard = types.InlineKeyboardMarkup()

      button_by_status = types.InlineKeyboardButton(text = "По статусу", callback_data = "by_status")
      button_by_paying = types.InlineKeyboardButton(text = "Платящая", callback_data = "by_paying")

      keyboard.add(button_by_status, button_by_paying)
      keyboard.add(back, inmenu)

      testbot.edit_message_text('Выберете пункт, по которому хотите получить результат:', call.message.chat.id, call.message.id, reply_markup = keyboard)
      user = user_dict[call.message.chat.id]
      if not user.back:
        user.previos_page = user.history[-1]
        user.history.append(call.data)
      else:
        user.back = False
      testbot.answer_callback_query(call.id)

    # --> Меню [Предыдущий месяц], [Текущий год], [Статистика за 3 года]
    elif call.data == "by_status" or call.data == "by_paying" or call.data == "services" or call.data == "equipment":
      keyboard = types.InlineKeyboardMarkup()

      button_previous_month = types.InlineKeyboardButton(text = "Предыдущий месяц", callback_data = "previous_month")
      button_this_year = types.InlineKeyboardButton(text = "Текущий год", callback_data = "this_year")
      button_statistics_3years = types.InlineKeyboardButton(text = "Статистика за 3 года", callback_data = "statistics_3years")

      if call.data == "services" or call.data == "equipment":
        button_current_month2 = types.InlineKeyboardButton(text = "Текущий месяц", callback_data = "current_month2")
        button_previous_month2 = types.InlineKeyboardButton(text = "Предыдущий месяц", callback_data = "previous_month_2")
        button_this_year2 = types.InlineKeyboardButton(text = "Текущий год", callback_data = "this_year_2")
        button_statistics_3years2 = types.InlineKeyboardButton(text = "Статистика за 3 года", callback_data = "statistics_3years_2")
        keyboard.add(button_current_month2, button_previous_month2)
        keyboard.add(button_this_year2, button_statistics_3years2)
      else:
        button_previous_month = types.InlineKeyboardButton(text = "Предыдущий месяц", callback_data = "previous_month")
        button_this_year = types.InlineKeyboardButton(text = "Текущий год", callback_data = "this_year")
        button_statistics_3years = types.InlineKeyboardButton(text = "Статистика за 3 года", callback_data = "statistics_3years")
        keyboard.add(button_previous_month, button_this_year, button_statistics_3years)
      keyboard.add(back, inmenu)

      testbot.edit_message_text('Выберете пункт, по которому хотите получить результат:', call.message.chat.id, call.message.id, reply_markup = keyboard)
      user = user_dict[call.message.chat.id]
      if not user.back:
        user.previos_page = user.history[-1]
        user.history.append(call.data)
      else:
        user.back = False
      testbot.answer_callback_query(call.id)

      # --> Меню [По всем каналам], [Выбор канала]
    elif call.data == "current_month2" or call.data == "previous_month_2" or call.data == "this_year_2" or call.data == "statistics_3years_2":
      keyboard = types.InlineKeyboardMarkup()

      button_all_channels = types.InlineKeyboardButton(text = "По всем каналам", callback_data = "all_channels")
      button_selection_channel = types.InlineKeyboardButton(text = "Выбор канала", callback_data = "selection_channel")

      keyboard.add(button_all_channels, button_selection_channel)
      keyboard.add(back, inmenu)

      testbot.edit_message_text('Выберете пункт, по которому хотите получить результат:', call.message.chat.id, call.message.id, reply_markup = keyboard)
      user = user_dict[call.message.chat.id]
      if not user.back:
        user.previos_page = user.history[-1]
        user.history.append(call.data)
      else:
        user.back = False
      testbot.answer_callback_query(call.id)

    # --> Меню [Таблица], [Диаграмма], [Эксель]
    elif call.data == "previous_month" or call.data == "this_year" or call.data == "statistics_3years" or call.data == "oops":
      keyboard = types.InlineKeyboardMarkup()

      button_table = types.InlineKeyboardButton(text = "Таблица", callback_data = "table")
      button_diagram = types.InlineKeyboardButton(text = "Диаграмма", callback_data = "diagram")
      button_excel = types.InlineKeyboardButton(text = "Эксель", callback_data = "excel")

      keyboard.add(button_table, button_diagram, button_excel)
      keyboard.add(back, inmenu)

      testbot.edit_message_text('Выберете пункт, по которому хотите получить результат:', call.message.chat.id, call.message.id, reply_markup = keyboard)
      user = user_dict[call.message.chat.id]
      if not user.back:
        user.previos_page = user.history[-1]
        user.history.append(call.data)
      else:
        user.back = False
      testbot.answer_callback_query(call.id)

    elif call.data == "inmenu":
      keyboard = types.InlineKeyboardMarkup()

      button_ACB = types.InlineKeyboardButton(text = "Активная клиентская база", callback_data = "ACB")
      button_money = types.InlineKeyboardButton(text = "Деньги", callback_data = "money")
      button_sales = types.InlineKeyboardButton(text = "Продажи", callback_data = "sales")

      keyboard.add(button_ACB)
      keyboard.add(button_money, button_sales)

      testbot.edit_message_text("Вы вернулись в главное меню. Выберите раздел:", call.message.chat.id, call.message.id, reply_markup = keyboard)

      user_dict[call.message.chat.id].history.clear()
      user_dict[call.message.chat.id].previos_page = None

      testbot.answer_callback_query(call.id)

    elif call.data == "reload":
      keyboard = types.InlineKeyboardMarkup()
      reload_btn = types.InlineKeyboardButton(text = "Обновить", callback_data = "reload")
      keyboard.add(reload_btn)
      testbot.edit_message_text(user_dict[call.message.chat.id], call.message.chat.id, call.message.id, reply_markup = keyboard)
      testbot.answer_callback_query(call.id)

    else:
      testbot.send_message(call.message.chat.id, "Error. Data: " + call.data)
      testbot.answer_callback_query(call.id)

testbot.infinity_polling()