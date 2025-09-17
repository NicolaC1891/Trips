class MenuItem:
    def __init__(self, response_key, label):
        self.response_key = response_key
        self.label = label


BUSINESS_ITEMS = [
    MenuItem(response_key="menu_trips", label="🧳  КОМАНДИРОВКИ"),
    MenuItem(response_key="repexp_0", label="💸  ПРЕДСТАВИТЕЛЬСКИЕ РАСХОДЫ"),
    MenuItem(response_key="advance_today_0_0", label="🧾  АВАНСОВЫЙ ОТЧЕТ"),
    MenuItem(response_key="menu_manual", label="ℹ️  Как пользоваться ботом"),
]

HELP_ITEMS = [
    MenuItem(response_key="menu_help", label="🆘  Помощь"),
    MenuItem(response_key="office_cat", label="🐈‍⬛  Бонус :)"),
]
