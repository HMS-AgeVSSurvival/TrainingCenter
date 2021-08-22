def get_letter(number, first_call=True):
    number = int(number)  # Since 1 -> A

    if first_call:
        number -= 1

    if number < 26:
        return chr(ord("A") + number)
    else:
        return get_letter(number // 26 - 1, first_call=False) + get_letter(
            number % 26, first_call=False
        )
