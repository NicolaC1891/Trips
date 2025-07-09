from dataclasses import dataclass


@dataclass
class Month:
    """
    Represents a month with its number and abbreviated Russian name.

    Attributes:
    - number (int): The numeric representation of the month (1–12).
    - name (str): The abbreviated Russian name of the month (e.g., "янв", "фев").
    """

    number: int
    name: str


@dataclass
class Day:
    """
    Represents a day of the week with its number and abbreviated Russian name.

    Attributes:
    - number (int): The numeric representation of the day (1–7), where 1 is Monday and 7 is Sunday.
    - name (str): The abbreviated Russian name of the day (e.g., "Пн", "Вт").
    """

    number: int
    name: str


MONTHS_RU: list[Month] = [
    Month(1, "янв"),
    Month(2, "фев"),
    Month(3, "мар"),
    Month(4, "апр"),
    Month(5, "май"),
    Month(6, "июн"),
    Month(7, "июл"),
    Month(8, "авг"),
    Month(9, "сен"),
    Month(10, "окт"),
    Month(11, "ноя"),
    Month(12, "дек"),
]


DAYS_RU: list[Day] = [
    Day(1, "Пн"),
    Day(2, "Вт"),
    Day(3, "Ср"),
    Day(4, "Чт"),
    Day(5, "Пт"),
    Day(6, "Сб"),
    Day(7, "Вс"),
]
