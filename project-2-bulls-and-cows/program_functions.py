'''
My custom functions for main program
'''

import math
from datetime import datetime
from termcolor import colored
import inflect

import settings as s
import file_functions as ff


p = inflect.engine()



def separator_line(max_line_width: int =50, sep: str ="-", color: str = "white"):
    '''
    Separator line

        Parameters:
            max_line_width (int)  --  set max line width
            separator = "-"  --  how separator looks like
            color_fg (str)  --  text color
            color_bg (str)  --  background color

        Available color:
            black, red, green, yellow, blue, magenta, cyan, white,
            light_grey, dark_grey, light_red, light_green, light_yellow, light_blue,
            light_magenta, light_cyan.

        Example:
            colored('Hello, World!', 'green')
    '''

    print(colored(sep.center(max_line_width, sep), color = color))



def cprint(message, color):
    '''
    Print color text

        Parameters:
            message (str)  --  content for print
            color (str)  --  text color

        Available color:
            black, red, green, yellow, blue, magenta, cyan, white,
            light_grey, dark_grey, light_red, light_green, light_yellow, light_blue,
            light_magenta, light_cyan.

        Example:
            colored('Hello, World!', 'green')
    '''

    print(colored(message, color = color))


def welcome_message(user_name: str, digits: int):
    '''
    Create wellcome message.

        Return:
            Hi there, Jirka!\n
            Welcome back! Its time to play again.\n
            Your last game was 22-02-2024 00:08\n
            
            I've generated a random 3 digit number for you.\n
            Let's play a bulls and cows game.
    '''
    separator_line()
    print(f"Hi there{', ' + user_name.title() if has_user_file(user_name) else '' }!")

    if has_user_file(user_name):
        print("Welcome back! Its time to play again.")
        last_game = get_last_result_from_user_file(user_name)
        if last_game["date"]:
            print(f"Your last game was {last_game['date']}")
    else:
        print("Welcome in your first game")

    separator_line()
    print(f"I've generated a random {digits} digit number for you.")
    print("Let's play a bulls and cows game.")
    separator_line()


def str_from_list(list: list[int|str], sep: str = ", ") -> str:
    '''
    Return string from list with custom separator from list of integer or string numbers.
    '''

    string = sep.join(str(number) for number in list)

    return string


def show_secret_number(number: str):
    '''
    Print message with secret number.

        Return:
            *********************\n
            Secret number is 1873\n
            *********************
    '''

    separator_line(sep="*", color="light_green")
    cprint(f"Secret number is {number}", "light_green")
    separator_line(sep="*", color="light_green")

def get_current_datetime_raw() -> str:
    '''
    Get current datetime in raw format.
    Format is default for datetime.now() - 2024-02-20 10:14:37.975139
    '''

    return datetime.now()


def get_current_datetime_format() -> str:
    '''
    Get current datetime in human format.
    Format is "%d-%m-%Y %H:%M" - 18-02-2024 10:14

    Return:
        datetime (str)  --  in "%d-%m-%Y %H:%M" format
    '''

    now = datetime.now()

    return now.strftime("%d-%m-%Y %H:%M")


def create_log_message(number: str|int,
                       status: str,
                       guesses: int,
                       total_time: str,
                       datetime_now: str = get_current_datetime_format()
                       ) -> str:
    '''
    Create log message which you can save in file.

    Return:
                    --  number, status, guesses, total_time, datetime_now
        message (str)  --  710, success, 3, 00:12, 18-02-2024 10:14
    '''

    message = f"{number}{s.default_separator}{status}{s.default_separator}{guesses}{s.default_separator}{total_time}{s.default_separator}{datetime_now}"
    
    return message


def get_total_time(datetime_from: str, datetime_to:str) -> dict:
    '''
    Get differnet datetime in raw format and human format.

    Return:
        total time (dict)  --  {
            "raw_format": "2024-02-18 10:14:37.975139",
            "human_format": "18-02-2024 10:14"
        }
    '''

    total_time = datetime_to - datetime_from
    total_time_format = str(total_time)[2:7]

    return dict({
        "raw_format": total_time,
        "human_format": total_time_format
        })


def help_menu(settings: dict, items_on_row: int = 2,
              sep: str = " | ", color: str = "light_cyan"):
    '''
    Create help menu with text you can write and which do some actions

        Parameters:
            settings (dict)  --  settigns from main_settings() in settings.py
            items_on_row (int)  --  how many items will be in row
            sep (str)  --  separator items in row
            color (str)  --  color for text and separator

        Return:
            **************************************************\n
            You try find number which has 3 digit and you cant\n
            repeat same number again. Your result will be save\n
            in file jirka_log.txt.\n
            -\n
            (q)uit - end program | (h)elp - print help\n
            (s)how - show secret number | (c)clear - my log file\n
            **************************************************
    '''
    separator_line(sep="*", color=color)

    cprint(f'''\
You try find number which has {settings["default_digits"]} digit and you cant 
repeat same number again. Your result will be save
in file {create_user_file_name(settings["default_name"])}.

    ''', color)

    length = len((menu := settings["default_help_menu_items"]))
    if length > items_on_row:
        help_range = math.ceil(length/items_on_row)
        for index in range(help_range):
            item_from = items_on_row * index
            item_to = item_from + items_on_row
            cprint(sep.join(menu[item_from:item_to]), color)
    else:
        cprint(sep.join(menu), color)

    separator_line(sep="*", color=color)
     

def get_inflection_str(string: str, quantity: int):
    '''
    Get inflection string from "string" and "quantity" and result is string
    in correct format for singular or plural.
    Using inflection library https://pypi.org/project/inflect/ 
    '''

    if p:
        return p.plural(string, quantity)
    else:
        return string if abs(quantity) == 1 else string + "s" 


def find_match(user_number: str, random_number: list[str]) -> dict:
    '''
    Find match (same number on same position as bulls) in list for each number
    in string and create dict with result.
    If find match create value in dict as 1 other result give 0.

        Parameters:
            user_number (str)  --  number as string
            random_number (list)  --  number as list[str]

        Return:
            dict {0: 0, 1: 0, 2: 0, 3: 0}
            keys is index of digit number
            values is result 1 = match, 0 = unmatch
    '''

    match = {}
    for number in range(len(user_number)):
        if user_number[number] == str(random_number[number]):
            match[number] = 1
        else:
            match[number] = 0

    return match


def find_same_number(user_number: str, random_number: str|list[str]) -> int:
    '''
    Find same number from string on the list (cow).

        Return: 
            sum_same_numbers (int)  --  count same numbers
    '''
    if isinstance(random_number, list):
        random_number = str_from_list(random_number)

    sume_same_numbers = 0
    for number in user_number:
        # if number in random_number:
        if random_number.find(number) != -1:
            sume_same_numbers += 1

    return sume_same_numbers


def get_match_result(user_number: str, random_number: list[str]) -> dict:
    '''
    Get the result from the found bulls and cows. Bulls has high priority
    so we need substract cows with bulls and get correct result cows.
    If you find 1 bull and 3 cows you need the bull substract from cows
    and you get result 1 bull 2 cows.
    
        Return:
            dict() example { "bulls": 1, "cows": 2 }
    '''

    bulls = sum(find_match(user_number, random_number).values())
    cows = find_same_number(user_number, random_number)

    return {"bulls": bulls, "cows": abs(cows - bulls) }


def find_duplicate_number(user_number: str) -> set:
    '''
    Find duplicate values save their in set() for reduce if find more than one
    diplicate number.
    Create set() with duplicates or empty set() if dont find any duplicate number.

        Return:
            Set() save only uniq duplicate values.
    '''

    duplicates = set([number for number in user_number if user_number.count(number) > 1])
    
    return duplicates


def is_duplicate_number(user_number: list|set|tuple|dict) -> bool:
    '''
    Check if find some duplicate number.
    
        Return:
            True if contain at least one duplicates.
            False if not cantain duplicates.
    '''

    return bool(find_duplicate_number(user_number))


def create_path_for_user_file(user_name: str) -> str:
    '''
    Create rel path to file, create file name from user name and add default_dir
    from settings.py.
    '''
    user_file = create_user_file_name(user_name)
    path_to_user_file = ff.create_rel_path(s.default_dir, user_file)

    return path_to_user_file


def create_user_file_name(user_name: str) -> str:
    '''
    Create user file name for save his result. If user name dont exist or is 
    same as default_name in settings.py set name as default_log_file in settings.py.

        Return
            file_name (str)  --  username_log.txt
    '''

    if not user_name or user_name == s.default_name:
        return s.default_log_file 

    file_name = ff.create_file_name(file_name="log", extension="txt", prefix=user_name)
    
    return file_name


def get_last_result_from_user_file(user_name: str) -> dict:
    '''
    Get last result in user file.
    Get path for user file from name and get last item in user file.

        Return:
            dict 
            key is header[column] from default_log_header in settings.py\n
            value is file[column] from format in set on create_log_message()\n
        
        Return example:
            {
                'number': '842',\n
                'status': 'user quit',\n
                'guesses': '0',\n
                'total_time': '02:08',\n
                'date': '22-02-2024 00:08'\n
            }
    '''

    last_game = ff.get_last_item_from_file(create_path_for_user_file(user_name))
    
    log_header = s.default_log_header.split(",")
    
    data_last_game = {}
    if last_game:
        log_data = last_game.split(s.default_separator)
        data_last_game = {log_header[i] : log_data[i] for i in range(len(log_header))}

    return data_last_game


def clear_user_file(user_name: str):
    '''
    Clear user file.
    '''

    user_file = create_path_for_user_file(user_name)
    ff.clear_file(user_file)

    print(f"File {user_file} has been cleared.")


def save_result_default(message: str):
    '''
    Save result in the file with default name, path is created from
    default_log_file and default_dir in settings.py.
    If file dont exists create new one and if exist add result in the file.
    '''
    
    if not ff.is_dir(s.default_dir):
        ff.create_dir(s.default_dir)
    
    file = ff.create_rel_path(s.default_dir, s.default_log_file)

    if not ff.is_file(file):
        ff.write_to_file(file, message, s.default_log_header)
    else:
        ff.append_to_file(file, message)

    print(f"All result you can see in {file}")


def save_result_for_user(user: str, message: str):
    '''
    Save result in the file with user name, path is created from
    create_user_file_name() and default_dir in settings.py.
    If file dont exists create new one and if exist add result in the file.
    If dir dont exist, create new one.
    '''

    if not ff.is_dir(s.default_dir):
        ff.create_dir(s.default_dir)
    
    file_name = create_user_file_name(user)
    file = ff.create_rel_path(s.default_dir, file_name)

    if not ff.is_file(file) or not get_last_result_from_user_file(user):
        ff.write_to_file(file, message, s.default_log_header)
    else:
        ff.append_to_file(file, message)

    print(f"We save your result in file {file}")


def is_user(settings: dict) -> bool:
    '''
    Check if user enter his name or he play as Guest.

        Return:
            True (bool)  --  user exist
            False (bool)  --  user dont exist or you play as Guest
    '''
    if settings:
        if settings["default_name"] != s.default_name:
            return True

    return False


def has_user_file(user_name: str):
    '''
    Check if user has created his file. Return False if user is defaul name in
    settings or empty string.

        Return:
            True  --  if file exists\n
            False  --  if user dont exist or you play as Guest and if file dont exist
    '''
    if not user_name or user_name == s.default_name:
        return False

    user_file = create_user_file_name(user_name)
    file = ff.create_rel_path(s.default_dir, user_file)

    if not ff.is_file(file):
        return False
    
    return True



if __name__ == "__main__":
    print(get_last_result_from_user_file("jirka"))
    pass
    # user_number = "4263"
    # random_number = [1,2,3,4]
    # print(find_match(user_number, random_number))
    # print(find_same_number(user_number, random_number))
    # print(get_match_result(user_number, random_number))
    # print(is_duplicate_number(user_number))