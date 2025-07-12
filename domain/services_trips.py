from domain.models import FlowStep


class TripsStepNavigationRules:
    """
    Checks for available navigation steps before building keyboard.
    existing without fsm cache , redo later
    """

    @staticmethod
    def can_go_next(step: FlowStep) -> bool:
        return bool(step.next_)

    @staticmethod
    def can_go_prev(step: FlowStep) -> bool:
        return bool(step.prev)

    @staticmethod
    def can_go_up(step: FlowStep) -> bool:
        return bool(step.parent)

    @staticmethod
    def has_children(step: FlowStep) -> bool:
        return bool(step.children)


class TripsStepValidator:
    """
    Checks if step instance has key to retrieve text from DB and button name label.
    """
    @staticmethod
    def is_valid_step(step: FlowStep) -> bool:
        return bool(step.response_key and step.label)
