class User:
    """
    A simple user class
    """

    def __init__(self, user_id: int, username: str, full_name: str) -> None:
        self.id = user_id
        self.username = username
        self.full_name = full_name
