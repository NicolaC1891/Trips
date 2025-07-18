class MenuItem:
    def __init__(self, response_key, label):
        self.response_key = response_key
        self.label = label


BUSINESS_ITEMS = [
    MenuItem(response_key="home_0", label="🇧🇾  ПО БЕЛАРУСИ  🇧🇾"),
#   MenuItem(response_key="abroad_0", label="🌎  ЗА ГРАНИЦУ  🌎"),
    MenuItem(response_key="advance_today_0_0", label="🔥  Авансовый отчет"),
    MenuItem(response_key="manual", label="ℹ️  Как пользоваться ботом"),
]

HELP_ITEMS = [
    MenuItem(response_key="help", label="🆘  Помощь"),
    MenuItem(response_key="office_cat", label="🐈‍⬛  Идея!"),
]
