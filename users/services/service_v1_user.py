from users.models import User


class UserService:
    def __init__(self, user: User) -> None:
        self.user = user

    def change_user_mode(self):
        self.user.is_host = not self.user.is_host
        self.user.save()
