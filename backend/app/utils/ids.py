import random
import string


def generate_swasthya_id() -> str:
    digits = "".join(random.choices(string.digits, k=6))
    return f"SW-{digits}"
