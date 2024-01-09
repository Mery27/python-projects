#------------------------------------------------------------------------------
# projekt_1.py: první projekt do Engeto Online Python Akademie
# author: Jiří Merenda
# email: j.merenda@seznam.cz
# discord: .mery27
#------------------------------------------------------------------------------

# matematické funkce
import math

# kontrola souborů
import os

##-----------------------------------------------------------------------------
### Testování aplikace
##-----------------------------------------------------------------------------
# pokud je test = True, nebudou se brát v potaz inputy(), ale výchozí data
test = False

# výchozí data
user = "bob"
password = "123"
# který index v listu TEXTS se vezme pro testování
# u souboru se automaticky nastaví pro výběr první index
# zaleží na hodnotě v nastavení text_range_from
selected_text_index = "1"
# použít soubor pro testování
use_file = True
# který soubor se vezme pro test
file = "data.txt"

##-----------------------------------------------------------------------------
### Nastavení aplikace
##-----------------------------------------------------------------------------
# maximální délka řádku, pokud je menší, text se ořízne
# optimální je 50 a více a pro menší hodnoty už to nemusí být zcela přehledné
max_length = 60
# seznam znaků, které se mají v textu nahradit
# { co_se_nahradi: cim_se_nahradi }
list_replace_chars = {
    ".": "",
    ",": "",
    "?": "",
    "!": "",
    "'": "",
    "\"": "",
    "\n": " "
    }
# pro kolik textů se má zobrazovat seznam k výběru
# v opačném případě se zobrazí pouze rozsah např. od 1 po 20
# v případě, že by list TEXTS měl spoustu položek
# 1) První text k analýze... (345)
# 2) Druhý text k analýze... (234)
show_max_options = 10
# od jaké hodnoty se má zobrazovat seznam textů k analýze
# pro přehlednost je lepší volit 1 než 0, ale dá se nastavit i jiné číslo
text_range_from = 1
# vyhledá pouze soubory s .txt koncovkou
# dá se do listu přidat i další typ souborum který bude obsahovat pouze text
text_files = ["txt"]
# hlavička tabulky
table_head = ["LEN", "OCCURENCES", "NR."]
# oddělovač v tabulce
table_separator = "|"
# symbol pro vyjádření počtu slov v tabulce
char_for_graph = "*"
# výchozí hodnota pro rozšíření prostředního sloupce
# pro lepší přehlednost bude mít odsazení od třetího sloupce
# doporučená hodnota je do 10, pro větší texty se doporučuje menší hodnota
# jinak dojde k rozhození tabulky
more_space_for_midle_column = 2
# kolik nejpoužívanějších slov se má vypsat
number_most_used_words = 10
# výchozí text k analýze
TEXTS = [
    """Situated about 10 miles west of Kemmerer,
Fossil Butte is a ruggedly impressive
topographic feature that rises sharply
some 1000 feet above Twin Creek Valley
to an elevation of more than 7500 feet
above sea level. The butte is located just
north of US 30N and the Union Pacific Railroad,
which traverse the valley. """,
    """At the base of Fossil Butte are the bright
red, purple, yellow and gray beds of the Wasatch
Formation. Eroded portions of these horizontal
beds slope gradually upward from the valley floor
and steepen abruptly. Overlying them and extending
to the top of the butte are the much steeper
buff-to-white beds of the Green River Formation,
which are about 300 feet thick.""",
    """The monument contains 8198 acres and protects
a portion of the largest deposit of freshwater fish
fossils in the world. The richest fossil fish deposits
are found in multiple limestone layers, which lie some
100 feet below the top of the butte. The fossils
represent several varieties of perch, as well as
other freshwater genera and herring similar to those
in modern oceans. Other fish such as paddlefish,
garpike and stingray are also present.""",
]
# uživatelé
users = {
    "bob": "123",
    "ann": "pass123",
    "mike": "password123",
    "liz": "pass123",
}
##-----------------------------------------------------------------------------
### Definice pomocných funkcí
##-----------------------------------------------------------------------------
# výpočet, na kolik řádku se vleze text v závislosti na šířce řádku
# max_length se volí na začátku programu v Nastavení aplikace
def text_rows(text_value, text_max_length=max_length):
    rows = math.ceil((len(text_value)) / text_max_length)
    return rows

# ořezání stringu dle délky řádku
# není úplně nejšikovnější, dalo by se zpracovat, aby neořezávalo uprostřed slova
# TODO oříznutí celého slova a ne po písmenu
# jít po písmenu a pokud se má ořezávat a aktuální znak je písmeno
# vrátit zpět dokud nebude aktuální znak mezera a až pak oříznout
def print_max_length(
    text_value,
    text_max_length=max_length,
    end="\n"
    ):
    rows = text_rows(text_value)
    # vypíše text a pokud je potřeba text ořezat, tak text vypíše na více řádků
    for row in range(1, rows + 1):
        print(text_value[text_max_length * (row - 1) : (text_max_length * row)],
              end=end
              )
        
# čára, kterou si lze upravit dle potřeb
# title = uprostřed se zobrazí nadpis
# length = délka čáry, výchozí je rovna délce řádku
# separator = oddělovač, jaký vzhled bude mít čára
# delining = odřádkování, zda bude nějaká mezera nebo ne (zadá se "None")
#
# vzor separating_line("Nadpis", separator = "*")
#
# ************************** Nadpis **************************
#
def separating_line(
    title=None,
    length=max_length,
    separator="=",
    delining_top="\n",
    delining_bottom="None"
    ):
    delining_top = False if delining_top == "None" else delining_top
    delining_bottom = False if delining_bottom == "None" else delining_bottom

    print(delining_top) if delining_top else None
    if title is None:
        print("".center(length, separator))
    else:
        rows = text_rows(title)
        if rows > 1:
            print(f"".center(length, separator))
            print_max_length(title)
            print(f"".center(length, separator))
        else:
            print(f" {title} ".center(length, separator))
    print(delining_bottom) if delining_bottom else None

##-----------------------------------------------------------------------------
### Přihlášení
##-----------------------------------------------------------------------------
separating_line("Login")
user = input("Login name: ") if not test else user
password = input("Login password: ") if not test else password

if user not in users or password != users[user]:
    print("You are enter not valid data for login. Program will be stopped.")
    quit()
else:
    separating_line(
        title=f"Welcome to the app, {user.title()}.",
        delining_top="\n",
        separator="=",
        delining_bottom="\n",
    )
    allowed_files = ", ".join(text_files)
    # delší text, který se přizbůsobí délce řádku
    print_max_length(
        f"You can analyse text added in variable TEXTS (let next input empty) or you can add file name for analyse text in this file. File must be {allowed_files} format and must be in same directory as this .py file. If file dont exist in same folder, will be used default data."
    )

##-----------------------------------------------------------------------------
### Výběr textu k analýze
### Prvně je volba souboru a pokud se nezvolí, vyberou se výchozí data 
##-----------------------------------------------------------------------------
# absolutní cesta k tomuto souboru
# D:\wamp330\www\python\projekt_1
current_directory = os.path.dirname(os.path.realpath(__file__))

# absolutní cesta k složce projektu
# d:\wamp330\www\python
# current_directory = os.getcwd()

# seznam všech souborů ve složce
files_in_current_directory = os.listdir(current_directory)

# vytvoří seznam povolených textových souborů
files_for_analyse = []
for file_name in files_in_current_directory:
    # text_files se volí na začátku programu v Nastavení aplikace
    for allowed_files in text_files:
        if allowed_files in file_name:
            files_for_analyse.append(file_name)
        
# zadání jména souboru pro test
if test and use_file:
    file = file
    # soubor ma pouze jeden index
    # přepíše výchozí zadanou hodnotu pro test
    selected_text_index = str(text_range_from)
elif test and not use_file:
    # pokud se mají vzít výchozí data místo zvolení souboru pro test
    file = ""
else:
    # vypíše seznam dostupných a povolených souborů
    separating_line(separator=" ", delining_top="")
    print_max_length(f"Files in folder: {', '.join(files_for_analyse)}")
    # zadání názvu souboru
    file = input("Enter file name: ")

# pokud soubor existuje zpracuj ho, jinak zpracuj výchozí data
if file in files_for_analyse:
    with open(current_directory + "\\" + file, "r", encoding="utf-8") as f:
        # načte data ze souboru
        # readlines() čte data po řádcích
        raw_data_from_file = f.readlines()
        # zpracuje data ze souboru na jeden string
        # a odstraní odřádkování
        one_string = ("").join(raw_data_from_file).replace("\n", " ")
        # vytvoří list o jedné proměnné
        file_content = [one_string]
        # nastaví text ze souboru pro analýzu
        select_text_for_analyse = file_content
        separating_line("We successfully import data from your text file")
else:
    if file == "":
        # pokud uživatel nic nezadá, zpracují se výchozí data
        separating_line("You have chose used default data")
    else:
        separating_line("File dont exist, we used default data")
    # pokud neexistuje soubor, nastavi pro analýzu výchozí data
    select_text_for_analyse = TEXTS


# ukončí program, pokud existuje soubor, ale nebude žádný text k analýze
# žádný text = file_content = [""]
if not select_text_for_analyse[0]:
    separating_line(separator=" ", delining_top="")
    print_max_length("No data for analyse, file is empty. Program will be stopped.")
    quit()

##-----------------------------------------------------------------------------
### Výběr konkrétního textu ze všech možností
### Pro výchozí proměnnou TEXTS bude na výběr ze 3 možností
### Pro soubor bude na výběr pouze jeden text, tedy 1 možnost
##-----------------------------------------------------------------------------
# počet textu k analýze a nastavení rozsahu pro výběr
# např. od 1 po 3 nebo může být i od 0 po 2
text_count = len(select_text_for_analyse)
# text_range_from se volí na začátku programu v Nastavení aplikace
text_range_to = (text_range_from - 1) + text_count

separating_line(
    title=f"We have {text_count} texts to be analyzed",
    delining_top="\n",
    delining_bottom="\r",
)

# seznam se vypíše pouze pro zvolený počet položek show_max_options = 10
# show_max_options se volí na začátku programu v Nastavení aplikace
# v případě nalezení více textů k analýze než 10
# se seznam se pro přehlednost už nezobrazí
if text_count < show_max_options:
    # získá seznam všech textu v proměnné a vypíše tento seznam
    # bere potaz prvních 20 znaků, které se vypíši a zakončí ...
    # např. 1) Mauris tincidunt sem... (7500) = délka textu
    for index, text in enumerate(select_text_for_analyse, start=text_range_from):
        # ostraní počáteční a koncové mezery
        text_without_space = text.strip()
        output_text = (
            f"{index}) {text_without_space[:20]}... ({len(text_without_space)})"
        )

        # určení maximální délky pro separating_line pokud se text rozdělí
        # na více řádků
        if len(output_text) > max_length:
            sep_max_length = max_length
        else:
            sep_max_length = len(output_text)

        # pokud existuje pouze jedna možnost
        # TODO nefunguje zkrácení řádku a vždy se zobrazuje celý i mimo max_lentgh
        if index == text_range_from and text_count == 1:
            print_max_length(output_text)
        # první možnost
        elif index == text_range_from:
            print_max_length(output_text, end="")
        # poslední možnost
        elif index == text_range_to:
            separating_line(delining_top="\r",
                            separator="-",
                            length=(sep_max_length))
            print_max_length(output_text, end="")
            separating_line(separator=" ", delining_top="\r")
        # prostřední možnosti
        else:
            separating_line(delining_top="\r",
                            separator="-",
                            length=(sep_max_length))
            print_max_length(output_text, end="")

print_max_length("Select number for text which you want analyse.") if not test else None
selected_text_index = (
    input(
        f"Select number from {text_range_from} to {text_range_to} (def. is {text_range_from}): "
    )
    if not test
    else selected_text_index
)

# výchozí výběr textu, pokud uživatel nic nezadá je text_range_from
# např. "1" jako string, aby se provedl test níže
# pokud by byla 1 jako integer, tak isdigit() je jen pro string
# v případě výstupu z input() bude vždy string 
if selected_text_index == "":
    selected_text_index = str(text_range_from)

# pokud se nezadá číslo v povoleném rozsahu, program napíše chybu
# bude se opakovat dokud nebude zadaná správná hodnota
input_number_in_range = False
while input_number_in_range is not True:
        # # pokud se zadá něco jiného než číslo
        if not selected_text_index.isdigit():
            print("You set wrong character, only number is allowed!")
            selected_text_index = input("Enter number again: ")
        # # pokud uživatel zadá číslo mimo povolený rozsah, opakuj, dokud nezadá
        # # číslo z výběru
        elif (
            int(selected_text_index) < text_range_from
            or int(selected_text_index) > text_range_to
            ):
            print("You set wrong number, text for this number dosnt exist.")
            selected_text_index = input("Enter number again: ")
        else:
            input_number_in_range = True    

##-----------------------------------------------------------------------------
### Analýza textu
##-----------------------------------------------------------------------------
# uživatel vybere číslo textu, ktrý chce zpracovat selected_text_index
# vybrané číslo se převede na požadovaný index v listu
selected_text = select_text_for_analyse[int(selected_text_index) - text_range_from]

# Odstraní znaky v textu
# list_replace_chars se volí na začátku programu v Nastavení aplikace
for old_char, new_char in list_replace_chars.items():
    selected_text = selected_text.replace(old_char, new_char)

# převede text na slova, list se všemi slovy
selected_text_words = selected_text.split()

# počet slov
result_number_words = len(selected_text_words)

# délka textu
result_text_length = len(selected_text)

# počet slov s velkým začínajícím písmenem, začátek věty
# inicializace promennych
result_number_titlecase_word = 0
# TODO pokud by byl potřeba seznam těchto slov
# result_titlecase_word = []
result_number_uppercase_word = 0
# TODO pokud by byl potřeba seznam těchto slov
# result_uppercase_word = []
result_number_lowercase_word = 0
# TODO pokud by byl potřeba seznam těchto slov
# result_lowercase_word = []
result_number_numeric_string = 0
result_numeric_string = []

for word in selected_text_words:
    if word.istitle():
        result_number_titlecase_word += 1
        # result_titlecase_word.append(word)
    elif word.isupper():
        result_number_uppercase_word += 1
        # result_uppercase_word.append(word)
    elif word.islower():
        result_number_lowercase_word += 1
        # result_lowercase_word.append(word)
    elif word.isnumeric():
        result_number_numeric_string += 1
        result_numeric_string.append(int(word))
    else:
        print(f"On word {word} cant find any match")

# součet všech čísel v textu
result_sum_all_numeric_string = sum(result_numeric_string)

separating_line(f"Result for text number {selected_text_index}",
                delining_bottom="\r")

print_max_length(f"There are {result_number_words} words in the selected text.")
print_max_length(f"There are {result_number_titlecase_word} titlecase words.")
print_max_length(f"There are {result_number_uppercase_word} uppercase words.")
print_max_length(f"There are {result_number_lowercase_word} lowercase words.")
print_max_length(f"There are {result_number_numeric_string} numeric strings.")
print_max_length(f"The sum of all the numbers {result_sum_all_numeric_string}.")

##-----------------------------------------------------------------------------
### Délka slov a jejich počet, výskyt pro tabulku
##-----------------------------------------------------------------------------
# inicializace promenne
# slovník {delka_slova: pocet_slov_o_teto_delce}
list_of_words_with_length = dict()

# inicializace promenne
# maximální šířka sloupce
max_column_width = {}

# inicializace promenne
# rozdíl v délce názvu a hodnot v prvním sloupci pro správné formátování
diff_for_first_column = 0

# sestavení seznamu četnosti slov
# pro jednotlivé délky slova {delka_slova: počet_výskytu}
# např. {8: 5, 5: 12, 2: 9, 4: 11, 6: 3 ...}
for word in selected_text_words:
    word_length = len(word)
    if word_length in list_of_words_with_length:
        list_of_words_with_length[word_length] += 1
    else:
        list_of_words_with_length[word_length] = 1

# seřazení slov od nejkratších po nejdelší
# např. [(1, 1), (2, 9), (3, 6), (4, 11), (5, 12) ...]
result_list_of_words_with_length = sorted(list_of_words_with_length.items())

# najde v seznamu největší číslo pro určení šířky prvního sloupce
longest_word = max(list_of_words_with_length.keys())

# najde v seznamu nejvetší číslo pro určení nejširšího řádku 
# v prostředním sloupci
most_frequent_word_count = max(list_of_words_with_length.values())

# pro delší texty k analýze, je potřeba omezit šířku
# v závislosti na most_frequent_word_count, které může být i 100
# max_length se volí na začátku programu v colum_width Nastavení aplikace
# table_head se volí na začátku programu v Nastavení aplikace
# more_space_for_midle_column se volí na začátku programu v Nastavení aplikace
max_width_second_column = (
    max_length
    - int(len(table_head[0]))
    - int(len(table_head[2]))
    - more_space_for_midle_column
    - 2
)

# poměr vyjádření počtu slov v tabulce, vyhádření symbolem
ratio = 1
if most_frequent_word_count > max_width_second_column:
    ratio = math.ceil(most_frequent_word_count / max_width_second_column)
    
# sestavení listu s šířkami sloupců pro tabulku dle nalezených slov
colum_width = [
    len(str(longest_word)),
    int(most_frequent_word_count / ratio),
    len(str(most_frequent_word_count)),
]

# Výpočet šířky sloupců a nastavení proměné max_column_width
# {table_title: column_width}
# např: max_column_width = {'LEN': 3, 'OCCURENCES': 12, 'NR.': 3}
# table_head se volí na začátku programu v Nastavení aplikace
for index, title in enumerate(table_head):
    # vyrovnání prvního sloupce při delším názvu
    # např. pro "LEN"(delka 3) a nejdelší slovo o "11"(delka 2) znacích je to 1
    # pokud bude rozdíl > 1 není třeba přičítat větší hodnotu a stačí pouze 1
    if index == 0:
        diff_for_first_column = len(title) - colum_width[0]
    # vypočítá maximální délků sloupců
    max_column_width[title] = (
        len(title) if colum_width[index] < len(title) else colum_width[index]
    )
    # nastavit minimální šířku pro první sloupec
    # pro menší rozměr dojde k rozhození tabulky
    if max_column_width[table_head[0]] < 3:
        max_column_width[table_head[0]] = 3

##-----------------------------------------------------------------------------
### Sestavení tabulky
##-----------------------------------------------------------------------------
# result_list_of_words_with_length
# např. [(1, 1), (2, 9), (3, 6), (4, 11), (5, 12) ...]
for index, item in enumerate(result_list_of_words_with_length):
    # první hodnota z listu je délka slova vyjádřena v čísle
    word_lengt_number = item[0]
    # druhá hodnota z listu je počet slov o dané délce
    word_total_count = item[1]
    # šířky sloupců
    max_column_one_width = max_column_width[table_head[0]]
    max_column_two_width = max_column_width[table_head[1]]
    max_column_three_width = max_column_width[table_head[2]]
    # +4 zahrnuje mezery nezapočítené ve výpočtu při spojování stringů u printu
    total_table_width = max_column_one_width + max_column_two_width + more_space_for_midle_column + max_column_three_width + 4
    # sestavení hlavičky při prvním výpisu
    if index == 0:
        separating_line(separator="-",
                        delining_top="None",
                        length=total_table_width)
        # sestavení prvního sloupce, vezme nadpis z table_head viz Nastavení
        # přidá oddělovač tabulky z table_separator v Nastavení aplikace
        # table_separator se volí na začátku programu v Nastavení aplikace
        # zarovná a nastaví odsazení dle vypočítané hodnoty 
        # max_column_width[table_head[]]
        print(
            # první sloupec
            f"{table_head[0] + table_separator}".rjust(max_column_one_width),
            # druhý sloupec
            f"{table_head[1]} {'-- ratio ' + str(ratio) if ratio > 1 else ''}".center(
                max_column_two_width + more_space_for_midle_column
            ),
            # třetí sloupec
            f"{table_separator + table_head[2]}".ljust(max_column_three_width),
            sep=("\n" if max_length < 24 else " ")
        )
        separating_line(separator="-",
                        delining_top="None",
                        length=total_table_width)

    # sestavení řádků v tabulce
    print(
        # první sloupec
        # nastavení odsazení dle delší hodnoty buď délka názvu nebo délka čísel
        # přičte 1 pokud bude rozdíl mezi délkou názvu a délkou čísel > 0
        # pro správné zarovnání pri změně názvu
        f"{str(word_lengt_number) + table_separator}".rjust(
            max_column_one_width + (1 if diff_for_first_column > 0 else 0)
        ),
        # druhý sloupec
        f"{char_for_graph * int(word_total_count / ratio)}".ljust(
            max_column_two_width + more_space_for_midle_column
        ),
        #třetí sloupec
        f"{table_separator + str(word_total_count)}".ljust(
            max_column_three_width
        )
    )
    
##-----------------------------------------------------------------------------
### Sestavení tabulky se seznamem nejpoužinějších slov
##----------------------------------------------------------------------------- 
# number_most_used_words v Nastavení, výchozí je 10
most_used_words = {}
for used_word in selected_text_words:
    if used_word in most_used_words:
        most_used_words[used_word] += 1
    else:
        most_used_words[used_word] = 1

# seřazení slov podle počtu od nejpoužívanějších
sorted_most_used_words = sorted(most_used_words.items(),
                                reverse=True,
                                key=lambda x:x[1])[:number_most_used_words]

separating_line(f"List of most used words, top {number_most_used_words}",
                delining_bottom="\r")
for index, words in enumerate(sorted_most_used_words, start=1):
    print(index, "-", words[0].upper(), f"{words[1]}x")