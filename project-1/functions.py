import math
from settings import *

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