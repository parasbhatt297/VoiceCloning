
import re
from num2words import num2words


def normalize_numbers(text, lang="en"):
    def replace_number(match):
        number = match.group().replace(",", "")

        if "." in number:
            whole, decimal = number.split(".", 1)

            whole_words = num2words(int(whole), lang=lang)
            decimal_words = " ".join(
                num2words(int(digit), lang=lang)
                for digit in decimal
            )

            return f"{whole_words} point {decimal_words}"

        return num2words(int(number), lang=lang)

    pattern = r"(?<!\w)\d[\d,]*(?:\.\d+)?(?!\w)"
    return re.sub(pattern, replace_number, text)
