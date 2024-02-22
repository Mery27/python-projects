'''
Projekt 2 Bulls and Cows
main_program.py: druhý projekt do Engeto Online Python Akademie

author: Jiří Merenda
email: j.merenda@seznam.cz
discord: .mery27

main_program.py
---------------
sestavení programu

settings.py
-----------
nastavení pro program

program_function.py
-------------------
funkce samotného programu

number_generator.py
-------------------
modul pro generování čísla buď náhodného čísla dle nastavení
nebo unikátního čísla, tedy čísla, které se nebude opakovat pokud existuje možnost
vygenerování dalšího unikátního čísla

file_function.py
----------------
funkce pro práci se soubory

'''

import settings as s
import program_functions as pf

# from number_generator import generate_unique_number
import number_generator

# Load settings from file settings.py
# enable_user_settings = you can type your name for save your result in own file
# and choice number length
settings = s.main_settings(enable_user_settings=True)

# Variables for main program
guesses = 0
game_run = True
datetime_start = pf.get_current_datetime_raw()
datetime_start_format = pf.get_current_datetime_format()


random_number = number_generator.generate_unique_number(settings["default_digits"])
random_number_string = pf.str_from_list(random_number, sep="")

# If user set his name file be saved with his name
# None as Guest, dont save result on special file
user = settings["default_name"] if pf.is_user(settings) else None

pf.welcome_message(user_name=settings["default_name"], digits=settings["default_digits"])

while game_run:

    user_tip = input("Enter a number or (h)elp: " if guesses == 0 else "Enter a number: ")
    pf.separator_line()

    if user_tip == "show" or user_tip == "s":
        pf.show_secret_number(random_number_string)
        continue

    if user_tip == "help" or user_tip == "h":
        pf.help_menu(settings)
        continue

    if user_tip == "c" or user_tip == "clear":
        if user:
            pf.clear_user_file(user)
            pf.separator_line()
        else:
            pf.cprint("As Guest you cannot cleared file.", "light_red")
            pf.separator_line()
        continue
    
    if user_tip == settings["default_quit"] or user_tip == settings["default_quit"][0]:
        pf.cprint(f"You quit the game after {guesses} guesses.", "light_green")

        datetime_quit = pf.get_current_datetime_raw()
        datetime_quit_format = pf.get_current_datetime_format()
        
        total_time = pf.get_total_time(datetime_start, datetime_quit)
        
        message = pf.create_log_message(
            number=random_number_string,
            status="user quit",
            guesses=guesses,
            total_time=total_time["human_format"],
            datetime_now=datetime_quit_format
            )
        
        if user:
            pf.save_result_for_user(user, message)

        pf.save_result_default(message)
        
        game_run = False


    elif not user_tip:
        pf.cprint(f"You dont enter any value.", "light_red")
        pf.separator_line()

    elif user_tip[0] == "0" or not number_generator.default_first_digit_is_null:
        pf.cprint(f"The number cannot start with zero.", "light_red")
        pf.separator_line()

    elif not user_tip.isdigit() or not len(user_tip) == settings["default_digits"]:
        pf.cprint(f"You must write only {settings['default_digits']} digit number.", "light_red")
        pf.separator_line()

    elif pf.is_duplicate_number(user_tip):
        duplicates = ", ".join(pf.find_duplicate_number(user_tip))
        inflection_number = pf.get_inflection_str('number', len(duplicates))
        pf.cprint(f"You are enter duplicate {inflection_number} {duplicates}", "light_red")
        print("Please enter number without repeating same number.")
        pf.separator_line()

    else:
        result = pf.get_match_result(user_tip, random_number)
        bulls = result["bulls"]
        cows = result["cows"]
        guesses += 1

        if result['bulls'] == settings["default_digits"]:
            pf.cprint(f"Correct, you've guessed the right number in {guesses} guesses!", "light_green")

            datetime_success = pf.get_current_datetime_raw()
            datetime_success_format = pf.get_current_datetime_format()
            
            total_time = pf.get_total_time(datetime_start, datetime_success)
            
            message = pf.create_log_message(
                number=random_number_string,
                status="success",
                guesses=guesses,
                total_time=total_time["human_format"],
                datetime_now=datetime_success_format
                )
            
            if user:
                pf.save_result_for_user(user, message)

            pf.save_result_default(message)

            game_run = False
        
        else:
            print(bulls, pf.get_inflection_str("bull", bulls), 
                  "," , 
                  cows, pf.get_inflection_str("cow", cows))
            pf.separator_line()
