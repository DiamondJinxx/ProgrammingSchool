
def romanToInt(roman: str) -> int:
    roman_to_int_map = {
        "I": 1,
        "V": 5,
        "X": 10,
        "L": 50,
        "C": 100,
        "D": 500,
        "M": 1000,
    }
    roman = roman[::-1]
    integer = 0
    prev = -1
    for number in roman:
        int_number = roman_to_int_map[number]
        if int_number < prev:
            integer -= int_number
            prev = int_number
            continue
        integer += int_number
        prev = int_number

    return integer
