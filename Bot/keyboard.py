from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_stop_word = KeyboardButton('Добавить запрещенное слово')
button_delete_old_word = KeyboardButton('Удалить сообщения с запрещенными словами')
button_delete_msg_user = KeyboardButton('Удалить сообщения по пользователю')
button_setting = KeyboardButton('Настройки')

button_list = ReplyKeyboardMarkup()
button_list.add(button_stop_word).add(button_delete_old_word).add(button_delete_msg_user).add(button_setting)

button_cancel = ReplyKeyboardMarkup().add(KeyboardButton('/admin'))

