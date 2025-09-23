def make_region_kb():
    kb = InlineKeyboardBuilder()
    for key, title in REGIONS.items():
        kb.button(text=title, callback_data=f"region:{key}")
    kb.adjust(2)
    return kb.as_markup()


def make_city_kb(region_key, stage):
    kb = InlineKeyboardBuilder()
    for city in CITIES.get(region_key, []):
        kb.button(text=city, callback_data=f"{stage}:{city}")
    kb.adjust(2)
    return kb.as_markup()
