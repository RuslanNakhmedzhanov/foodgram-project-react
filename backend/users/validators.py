import re

from rest_framework.exceptions import ValidationError

WRONG_USERNAME_LIST = ["me", "Me", "ME"]
WRONG_USERNAME = '"me", "Me", "ME" - недопустимое имя пользователя!'
WRONG_SYMBOLS = "Недопустимые символы: {}"


def name_validator(value):
    """
    username != 'me'
    username includes only letters, digits and @/./+/-/_
    """
    if value in WRONG_USERNAME_LIST:
        raise ValidationError(WRONG_USERNAME)
    if not re.fullmatch(r'^[\w.@+-]+', value):
        raise ValidationError(
            WRONG_SYMBOLS.format(
                "".join(set(re.findall(r"[^\w.@+-]", value)))
            )
        )
    return value
