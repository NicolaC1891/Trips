from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

REGIONS = {
    "Брестская": "brest",
    "Витебская": "vitebsk",
    "Гомельская": "gomel",
    "Гродненская": "grodno",
    "Минская": "minsk",
    "Могилевская": "mogilev"}


def make_region_kb(direction):
    keyboard = []
    for name, callback in REGIONS.items():
        button = InlineKeyboardButton(text=name, callback_data=f"{direction}:{callback}")
        keyboard.append([button])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return markup


def make_cities_kb(city_dict, direction):
    keyboard = []
    for cityname, city in city_dict.items():
        button = InlineKeyboardButton(text=cityname, callback_data=f"{direction}:{cityname}")
        keyboard.append([button])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return markup


def resulting_kb():
    keyboard = []
    keyboard.append([InlineKeyboardButton(text="🗺 Показать информацию", callback_data="planner_core")])
    keyboard.append([InlineKeyboardButton(text="🔄  Выбрать заново", callback_data="planner_start")])
    keyboard.append([InlineKeyboardButton(text="🏠  В меню", callback_data="to_main")])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return markup


def final_kb():
    keyboard = []
    keyboard.append([InlineKeyboardButton(text="🔄  Выбрать заново", callback_data="planner_start")])
    keyboard.append([InlineKeyboardButton(text="🏠  В меню", callback_data="to_main")])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return markup
