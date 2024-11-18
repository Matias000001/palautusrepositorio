from entities.user import User
from repositories.user_repository import (
    user_repository as default_user_repository
)


class UserInputError(Exception):
    pass


class AuthenticationError(Exception):
    pass


class UserService:
    def __init__(self, user_repository=default_user_repository):
        self._user_repository = user_repository

    def check_credentials(self, username, password):
        if not username or not password:
            raise UserInputError("Username and password are required")

        user = self._user_repository.find_by_username(username)

        if not user or user.password != password:
            raise AuthenticationError("Invalid username or password")

        return user

    def create_user(self, username, password, password_confirmation):
        self.validate(username, password, password_confirmation)

        user = self._user_repository.create(
            User(username, password)
        )

        return user

    def validate(self, username, password, password_confirmation):
        # Tarkistetaan, että käyttäjätunnus ja salasana eivät ole tyhjiä
        if not username or not password:
            raise UserInputError("Username and password are required.")

        # Käyttäjätunnus: vähintään 3 merkkiä ja vain kirjaimia
        if len(username) < 3 or not username.isalpha():
            raise UserInputError("Username is too short")

        # Tarkistetaan, että käyttäjätunnus ei ole jo käytössä
        if self._user_repository.find_by_username(username):
            raise UserInputError("Username is already in use.")

        # Salasana: vähintään 8 merkkiä ja ei pelkkiä kirjaimia
        if len(password) < 8 or password.isalpha():
            raise UserInputError("Password is too short")

        # Varmistetaan, että salasana ja vahvistus ovat samat
        if password != password_confirmation:
            raise UserInputError("Passwords do not match.")

        return None
user_service = UserService()
