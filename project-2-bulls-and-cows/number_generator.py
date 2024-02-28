'''
Generator random numbers 
    - all numbers are generated default as list[int]

generate_random_number()
    - you can choose length of number
    - range of digits in number
    - if digits can repeat self
    - if number can start with zero

generate_unique_number()
    - use function generate_random_number() for generate number
    - in this function you can only choose how many digts be in number
    - this function generate only uniq number if is posible, for this method
    functin using file when save generate numbers
    - calculates how many options there are for generating a number based
    on its settings (for 1 digit numbers without 0 are 9 posible options)
'''

from random import randint

import file_functions as ff


# where we save file, in def same folder as this file
default_file_with_numbers: str = "used_numbers.txt"
# how long number we want guesses, '1234'
default_number_digits: int = 5
# range for set use only from 0 to 9
default_range_from: int = 0
# range for set use only from 0 to 9
default_range_to: int = 9
default_first_digit_is_null: bool = False
default_repeat_digit: bool = False



def generate_unique_number(total_digits: int = default_number_digits,
                      file: str = default_file_with_numbers
                      ) -> list[str]:
    '''
    You can generate uniq number if is posible to generate him. If max possible
    variatns is over, function clear data and generate numbers again.
    In this function you can choose only how many digits will be in number.
    For random number using function generate_radnom_number() which has more
    options for settings.
    
        Parameters:
            total_difits (int)  --  how many digits the number has
            file (str)  --  file name where you save generated numbers

        Return:
            uniq_number (list)  --  ["1", "2", "3", "4"]

        Example:
            For 1 digit number you can generated only 9 uniq numbers if is set
            range from 0 to 9 and first number is not be 0.
            So if you generate all this number, list will be cleared
            and you can generate again new 9 uniq numbers.
    '''
    
    uniq_number = generate_random_number(total_digits)
    last_item_in_file = ff.get_last_item_from_file(file)
    
    # if previsou number has difference digts
    # clear the file
    if len(uniq_number) != len(last_item_in_file):
        ff.clear_file(file)
    
    list_of_used_numbers = get_used_numbers(file)

    if not is_available_options(list_of_used_numbers):
        # clear file and reset list_of_used_numbers
        ff.clear_file(file)
        list_of_used_numbers = []

    while is_number_used(uniq_number, list_of_used_numbers):
        uniq_number = generate_random_number(total_digits)
    else:
        # save_number(uniq_number, ff.create_abs_path(file))
        ff.append_to_file(file, list_to_string(uniq_number))
        return uniq_number


def generate_random_number(total_digits: int = default_number_digits,
                           range_from: int = default_range_from,
                           range_to: int = default_range_to,
                           firt_digit_is_null: bool = default_first_digit_is_null,
                           repeat_digit: bool = default_repeat_digit
                           ) -> list[str]:
    '''
    Generate random numbers.
    You can set how long of the number will be, range for digits in number, if
    first number can be null, if numbers can reapeat self.
    If you set total_digits more than range and repeat_digit it will be False
    you get error.

        Parameters:
            tota_digits (int) -- total digits in the number\n
            range_from (int)  -- from which digit you can generate
            range_to (int)  --  to digit you can generate
            first_number_is_null (bool) -- if can be first number null\n
            repeat_digit (bool) -- can number contain same number more than one\n

        Return:
            List[int] example ["1", "2", "3", "4"] for 4 digits
            or ["1", "2", "3"] for 3 digts\n

        Example:


    '''

    check_settings(total_digits, range_from, range_to, repeat_digit)

    range_from = abs(range_from)
    range_to = abs(range_to)
    
    random_number = []
    
    for digit in range(total_digits):
        number = randint(range_from, range_to)
        # generate one random number if first number cant be null
        if not firt_digit_is_null and digit == 0:
            range_from_first_digit = range_from if range_from > 1 else 1
            random_number.append(str(randint(range_from_first_digit, range_to)))
        # generate one uniq number
        elif not repeat_digit:
            while str(number) in random_number:
                number = randint(range_from, range_to)
            random_number.append(str(number))
        # generate one random number
        else:    
            random_number.append(str(number))

    return random_number


def is_number_used(number: list[str|int], list_numbers: list[str]) -> bool:
    '''
    Check if the number is used in list. For right result we need use data parameters of same type.
    '''
    return True if list_to_string(number) in list_numbers else False    



def get_used_numbers(file: str) -> list[str]:
    '''
    Get used numbers from file and save them as list. If file with numbers dont
    exit create this file
    '''
    
    if not ff.is_file(file):
        # in this situation this crete new file
        ff.clear_file(file)

    return ff.remove_new_line_from_list(ff.get_lines_from_file(file))


def list_to_string(list: list) -> str:
    '''
    Convert list to string
    '''

    number = ""
    for char in list:
        number += str(char)
    
    return number


def get_max_range(range_from: int, range_to: int) -> int:
    '''
    Get max range from two absolute numbers
    '''

    return (abs(range_to) + 1) - abs(range_from)


def check_settings(digits: int, range_from: int,
                   range_to: int, repeat_digit: bool = False
                   ) -> bool|None:
    '''
    Cheking if you can generate number for spicific range and length number.
    Its olny for situation when you cant reapet same digit in number.

        Return:
            True  --  if setting its ok
            quit()  --  if setting its not ok, quit program and write error message
    '''

    max_range = get_max_range(range_from, range_to)

    # If you can reapeat digits and you can choose at least 1 digit
    # you can generate number example ["1", "1", "1", "1"]
    if repeat_digit and max_range > 0:
        return True

    # If you cant repeat digits and you want generate number for more digits
    # as you cant use because you set low max range
    if digits > max_range and not repeat_digit:
            print("")
            print("Setting error:")
            print(f"For {digits} digit number you have allowed only range")
            print(f"from {range_from} to {range_to}. This is to low, because give only")
            print(f"{max_range} uniq digits and you need {digits}.")
            print("")
            print("The program has been stopped")
            quit()

    return True


def get_max_available_options(digits: int = default_number_digits,
                              firt_digit_is_null: bool = default_first_digit_is_null,
                              range_from: int = default_range_from,
                              range_to: int = default_range_to,
                              repeat_digit: bool = default_repeat_digit
                              ) -> int:
    '''
    Calculate max available options for specific length number and settings how
    number will be look.
    (if numbers can repeat, range of numbers, if first digit can be null)
    
        Example:
            For default settings: If we dont use 0 on begining the number first
            position of number will be only 9 and other 10.
            Next option always -1 of previous range because we dont want duplicite numbers.
            Max options for 4 digits, first 1-9, second 0-8, third 0-7, four 0-6.
            Result: will be 4536 options for 4 digit number
    '''

    check_settings(digits, range_from, range_to, repeat_digit)
    
    max_range = get_max_range(range_from, range_to)
    range_for_first_digit = max_range if firt_digit_is_null else max_range - 1
    
    max_options = range_for_first_digit
    if digits > 1:
        for index in range(1, digits):
            if not repeat_digit:
                max_options *= (max_range - index)
            else:
                max_options *= max_range
    
    return max_options


def is_available_options(list_used_numbers: list) -> bool:
    '''
    Check if we can create another uniq number or if we used all
    '''
    
    max = get_max_available_options()
    current = list_used_numbers

    if len(current) >= max:
        print("Numbers in the file reached maximum limit so we cleared file.")
        return False
    
    return True


if __name__ == "__main__":
    print("Uniq number: ", generate_unique_number())
    print("Used numbers from previous session: ", get_used_numbers(default_file_with_numbers))
    print("Total generated numbers", len(get_used_numbers()))
    print(f"Max available uniq options for {default_number_digits} digit number")
    print(f"and range from {default_range_from} to {default_range_to} is: ", get_max_available_options())
    print("Can genereate another uniq number: ", is_available_options())