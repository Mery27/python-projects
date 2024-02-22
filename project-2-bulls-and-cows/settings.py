'''
Default settings in variables.
If you want you can overwrite default variables with own functions.

Custom function which overwrites default variable must have name start with "set_user_"
and after that follow with name variable you want overwrite example "default_name".

Example:
If you want to overwrite dafault_name variable so you must create function
with name "set_user_default_name()" wchich must return same result as default variable.
Users custom function must return same data type as default variable or they dont 
will be used.
'''

from textwrap import dedent

import program_functions as pf


# Default wariables
default_name = "Guest"
default_digits = 4
default_range_digits = [1, 2, 3, 4, 5, 6]
default_quit = "quit"
# file where will be saved all generated numbers for Guest
default_file = "used_numbers.txt"
default_help_menu_items = ["(q)uit - end program",
                           "(h)elp - print help",
                           "(s)how - show secret number",
                           "(c)clear - my log file"]
default_dir = "data"
default_log_header = "number,status,guesses,total_time,date"
default_log_file = "log.txt"
default_separator = ","


def get_default_settings() ->dict:
    '''
    Return dict from defined variables in settings.py file which start with name default_.
    
    Return:
        dict {
            "default_name": Guest,\n
            "default_digits": 4,\n
            "default_range_digits": [1, 2, 3, 4, 5, 6],\n
            "default_quit": "quit"\n
            "default_file": "used_numbers.txt"\n
        }
    '''

    default_settings = {}
    for variable in globals():
        if variable[:8] == "default_":
            default_settings[str(variable)] = eval(variable)

    return default_settings


def set_user_default_range_digits() -> list[int]:
    '''
    Testovací funkce na přepsání hodnot pro výběr délky čísla pro hádáni.
    Změna se projeví v main_program.py, ale range se volá už tady v souboru
    set_user_default_digits(), takže se změna neprojeví vizuálně a dále není už 
    v programu tato proměná použita.
    '''
    my_range = [2, 4, 6]

    return my_range


def set_user_default_name() -> str:
    '''
    Custom function which overwrite default_name.
    This function create input for user name.

    Name must start with set_user_ and after that name follow with variable you
    want overwrite. So in this case dafault_name and finally result
    will be set_user_default_name()

        Return:
            name (str)  --  user name
    '''

    pf.separator_line()
    name = input("Whats your name? ")
    pf.separator_line()
    
    return name


def set_user_default_digits(default_digits: int = default_digits,
                            deafault_range_digits: list = default_range_digits
                            ) -> int:
    '''
    Custom function which overwrite variable default_digits.
    This function create input for number of digits.

    Name must start with set_user_ and after that name follow with variable you
    want overwrite. So in this case dafault_digits and finally result
    will be set_user_default_digits()

        Parameters:
            default_digits (int)  --  how many digits has a number
            deafault_range_digits (list)  --  options with digits you can choose

        Return:
            number_digits (int)  --  how long number you want guesses
    '''

    print(dedent(f'''\
    Default long number for guesses is {default_digits}, but you can
    choice from {pf.str_from_list(default_range_digits, " ")} anything else 
    is give default value.'''))
    pf.separator_line(max_line_width=1)
    
    # Defined number_digits variable
    number_digits = input("How long a number you want to guess? ")
    if number_digits.isdigit() and int(number_digits) in deafault_range_digits:
        number_digits = int(number_digits)
    else:
        number_digits = default_digits
        print("We set default digits because you enter wrong value.")
        pf.separator_line()

    return number_digits


def get_user_settings() -> dict:
    '''
    Get all function in settings.py file with name start set_user_ and create dict with their results as value in dict. Key in dict is name function after set_user_.
    If not imported this func in main_settings() it will be used default settings from variables.

        set_user_default_name() - example of function
            Function can defined user name as input.\n
            Result in dict {"default_name": result from the function (str)}
        
        set_user_default_digits() - example of function
            User can defined how long number he want guesses.\n
            Result in dict {"default_digits": result from the function (int)}

        Return:
            dict {"default_name": Joe, "default_digits": 4}
    '''

    user_settings = {}
    for user_func in globals():
        if user_func[:9] == "set_user_":
            user_settings[str(user_func[9:])] = eval(user_func+'()')

    return user_settings


def main_settings(enable_user_settings: bool = True) -> dict:
    '''
    Create main settings from default_settings() and user_settings().
    If user settings is enabled (True), default settigns will be overwritten with user data.
    User data must by same type as default data.

        Parameters:
            enable_user_settings (bool)  --  if is True default settings will be overwritten 

        Return:
            settings (dict)  --  return default parameters from file the settings.py

        Example for default:
            dict = {\n
            'default_name': 'Guest',\n
            'default_digits': 4,\n
            'default_range_digits': [1, 2, 3, 4, 5, 6],\n
            'default_quit': 'quit',\n
            'default_file': 'used_numbers.txt',\n
            'default_help_menu_items': ['(q)uit - end program', '(h)elp - print help'...,\n
            'default_dir': 'data',\n
            'default_log_header': 'number,\n
            status, gues...time, date',\n
            'default_log_file': 'log.txt',\n
            'default_separator': ','\n
            }\n
    '''

    if enable_user_settings:
        defaul_settings = get_default_settings()
        user_settings = get_user_settings()
        # if user custom function result is other type as default variable dont use them
        for key in user_settings:
            if type(user_settings[key]) == type(defaul_settings[key]):
                defaul_settings[key] = user_settings[key]
                
        return defaul_settings
    else:
        return get_default_settings()


if __name__ == "__main__":
    # print(get_user_settings())
    print(main_settings(True))