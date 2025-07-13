class FlowStep:
    """
    Represents a single step in the business trips instruction flow.

    Attributes:
        response_key (str): Key used to fetch the message content for this step.
        children (tuple[str] | None): Tuple of keys representing child steps (sub-steps).
        prev (str): Key of the previous step in the sequence, or None if there is none.
        next_ (Optional[str]): Key of the next step in the sequence, or None if there is none.
        parent (Optional[str]): Key of the parent step (higher-level step), or None if top-level.
        label (str): Human-readable label/title of the step.
    """

    def __init__(
        self,
        response_key: str,
        children: tuple[str, ...] | None,
        prev: str | None,
        next_: str | None,
        parent: str | None,
        label: str,
    ):
        self.response_key = response_key
        self.children = children
        self.prev = prev
        self.next_ = next_
        self.parent = parent
        self.label = label
        self.content = None


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


class FlowStepValidator:
    """
    Checks if step instance has key to retrieve text from DB and button name label.
    """

    @staticmethod
    def is_valid_step(step: FlowStep) -> bool:
        return bool(step.response_key and step.label)
