from django.core.validators import RegexValidator
from rest_framework.exceptions import ValidationError

WRONG_USERNAME_LIST = ["me", "Me", "ME"]
WRONG_USERNAME = '"me", "Me", "ME" - недопустимое имя пользователя!'


def name_validator(value):
    """
    username != 'me'
    username includes only letters, digits and @/./+/-/_
    """
    if value in WRONG_USERNAME_LIST:
        raise ValidationError(WRONG_USERNAME)
    return value


name_valid = RegexValidator(r'^[a-zA-Z0-9]*$',
                            'Недопустимые символы в названии.')
