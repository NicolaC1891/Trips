from domain.flow_logic import FlowStep

FLOW_TRIPS_HOME = {

    "home_0": FlowStep(response_key="home_travel", children=("home_1", "home_2", "home_3", "home_4",),
                       prev=None, next_=None,
                       parent="to_main", label='Командировки по РБ'),

    "home_1": FlowStep(response_key="home_module", children=None,
                       prev=None, next_="home_2",
                       parent=None, label='1. С чего начать"'),

    "home_2": FlowStep(response_key="home_memo", children=("home_21", "home_22", "home_23", "home_24",),
                       prev="home_1", next_="home_21",
                       parent=None, label='2. Оформление заявки'),

    "home_21": FlowStep(response_key="home_memo_fill", children=None,
                        prev="home_1", next_="home_22",
                        parent="home_2", label='2.1. Карточка в модуле'),

    "home_22": FlowStep(response_key="home_memo_upload", children=None,
                        prev="home_21", next_="home_23",
                        parent="home_2", label='2.2. Выгрузка в СЭД "Канцлер"'),

    "home_23": FlowStep(response_key="home_memo_final", children=None,
                        prev="home_22", next_="home_24",
                        parent="home_2", label='2.3. Дополнение в СЭД "Канцлер"'),

    "home_24": FlowStep(response_key="home_memo_approve", children=None,
                        prev="home_23", next_="home_3",
                        parent="home_2", label='2.4. Согласование в СЭД "Канцлер"'),

    "home_3": FlowStep(response_key="home_order", children=None,
                       prev="home_24", next_="home_4",
                       parent=None, label='3. Оформление приказа'),

    "home_4": FlowStep(response_key="home_report", children=None,
                       prev="home_3", next_=None,
                       parent=None, label='4. Авансовый отчет'),
}
