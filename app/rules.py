import re

CATEGORIES = (
    "Cards",
    "Accounts",
    "Loans",
    "Digital Banking",
    "Fraud",
    "Other",
)
URGENCIES = ("High", "Medium", "Low")

TEAM_BY_CATEGORY = {
    "Cards": "Card Services",
    "Accounts": "Account Services",
    "Loans": "Loan Department",
    "Digital Banking": "Digital Support",
    "Fraud": "Fraud and Risk",
    "Other": "Customer Service",
}

_FRAUD_PATTERN = re.compile(
    r"\b(?:fraud|stolen|lost\s+card|hacked|unauthorized|"
    r"did\s+not\s+make\s+this\s+payment|money\s+taken)\b",
    re.IGNORECASE,
)


def has_fraud_terms(text: str) -> bool:
    return _FRAUD_PATTERN.search(text) is not None