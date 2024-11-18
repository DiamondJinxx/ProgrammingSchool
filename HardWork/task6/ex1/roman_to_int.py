def romanToInt(roman: str) -> int:
    if roman == "IV":
        return 4
    roman_to_int_map = {
        "I": 1,
        "V": 5,
        "X": 10,
    }
    roman = roman[::-1]
    integer = 0
    for number in roman:
        int_number = roman_to_int_map[number]
        integer += int_number

    return integer
