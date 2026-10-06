import re

_EMAIL_PATTERN = re.compile(
    r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE
)
_BANGLADESHI_PHONE_PATTERN = re.compile(
    r"(?<![0-9])(?:\+?880|00880|0)?[ ]?1[3-9](?:[ -]?[0-9]){8}(?![0-9])"
)
_LONG_NUMBER_PATTERN = re.compile(r"(?<![0-9])(?:[0-9][ ]*){7,}[0-9](?![0-9])")


def mask_personal_data(text: str) -> str:
    text = _EMAIL_PATTERN.sub("[email]", text)
    text = _BANGLADESHI_PHONE_PATTERN.sub("[phone]", text)
    return _LONG_NUMBER_PATTERN.sub("****", text)