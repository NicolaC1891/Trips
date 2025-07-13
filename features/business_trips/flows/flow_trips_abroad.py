from domain.flow_logic import FlowStep

FLOW_TRIPS_ABROAD = {

    "abroad_0": FlowStep(response_key="abroad_travel", children=("abroad_1", "abroad_2", "abroad_3", "abroad_4",),
                         prev=None, next_=None,
                         parent="to_main", label='Командировки по РБ'),

    "abroad_1": FlowStep(response_key="abroad_module", children=None,
                       prev=None, next_="abroad_2",
                       parent=None, label='1. С чего начать"'),

    "abroad_2": FlowStep(response_key="abroad_memo", children=("abroad_21", "abroad_22", "abroad_23", "abroad_24",),
                       prev="abroad_1", next_="abroad_21",
                       parent=None, label='2. Оформление заявки'),

    "abroad_21": FlowStep(response_key="abroad_memo_fill", children=None,
                        prev="abroad_1", next_="abroad_22",
                        parent="abroad_2", label='2.1. Карточка в модуле'),

    "abroad_22": FlowStep(response_key="abroad_memo_upload", children=None,
                        prev="abroad_21", next_="home_23",
                        parent="abroad_2", label='2.2. Выгрузка в СЭД "Канцлер"'),

    "abroad_23": FlowStep(response_key="abroad_memo_final", children=None,
                        prev="abroad_22", next_="abroad_24",
                        parent="abroad_2", label='2.3. Дополнение в СЭД "Канцлер"'),

    "abroad_24": FlowStep(response_key="abroad_memo_approve", children=None,
                        prev="abroad_23", next_="abroad_3",
                        parent="abroad_2", label='2.4. Согласование в СЭД "Канцлер"'),

    "abroad_3": FlowStep(response_key="abroad_order", children=None,
                       prev="abroad_24", next_="abroad_4",
                       parent=None, label='3. Оформление приказа'),

    "abroad_4": FlowStep(response_key="abroad_report", children=None,
                       prev="abroad_3", next_=None,
                       parent=None, label='4. Авансовый отчет'),
}