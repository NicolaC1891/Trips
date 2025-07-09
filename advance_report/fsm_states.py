from aiogram.fsm.state import State, StatesGroup


class AdvReportStates(StatesGroup):
    """
    Finite State Machine (FSM) states for the advance report feature.

    This class defines the state used during interaction with the user
    when they are selecting a date of return from the business trip.
    """

    date_selection = State()
    """
    State where the user is prompted to select a date
    for calculating the report deadline.
    """
