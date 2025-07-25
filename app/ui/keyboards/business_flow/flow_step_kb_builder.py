from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.application.entities.flow_step_entity import FlowStep


class FlowStepUIBuilder:

    BTN_PREV = "⬅  Назад"
    BTN_NEXT = "➡  Дальше"
    BTN_UP = "⬆  К разделу"
    BTN_MENU = "🏠  В меню"

    def __init__(self, child_labels: list | None, step: FlowStep):
        self.child_labels = child_labels
        self.step = step

    def build_kb(self) -> InlineKeyboardMarkup:

        keyboard = []

        if self.step.children:
            for child, label in zip(self.step.children, self.child_labels):
                keyboard.append(
                    [
                        InlineKeyboardButton(
                            text=label, callback_data=child
                        )
                    ]
                )


        sideways_block = []
        if self.step.prev:
            sideways_block.append(
                InlineKeyboardButton(text=self.BTN_PREV, callback_data=self.step.prev)
            )
        if self.step.next_:
            sideways_block.append(
                InlineKeyboardButton(text=self.BTN_NEXT, callback_data=self.step.next_)
            )
        if sideways_block:
            keyboard.append(sideways_block)

        bottom_block = []
        if self.step.parent:
            bottom_block.append(
                InlineKeyboardButton(text=self.BTN_UP, callback_data=self.step.parent)
            )
        bottom_block.append(
            InlineKeyboardButton(text=self.BTN_MENU, callback_data="to_main")
        )
        keyboard.append(bottom_block)

        markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return markup
