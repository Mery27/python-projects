
# Python projekt 2 - Bulls and Cows

Bull & Cows - hra postavená na hádání 4 ciferného čísla

## Instalace doplňkových modulů

V projektu jsou použity následující doplňkové moduly.

```bash
pip install inflect
pip install termcolor
```

```bash
annotated-types = 0.6.0
inflect = 7.0.0
pydantic = 2.6.3
pydantic_core = 2.16.3
termcolor = 2.4.0
typing_extensions = 4.10.0
```

## Funkce

- Program obsahuje generátor náhodných čísel, který může generovat libovolné náhodná a unikátní čísla
- V programu si lze defaultně vybrat, zda chceme vygenerovat 1, 2, 3, 4, 5 nebo 6 ciferné číslo
- Pokud se zadá jméno, výsledek se uloží do souboru pro konkrétního uživatele např. jirka_log.txt
- Každý výsledek se zvlášť ukládá do hlavního logu - log.txt

- Základní menu, které vyvoláme zadáním písmene "h" nebo "help"
    - (q) quit - Ukončení programu
    - (s) show - Ukáže vygenerované číslo
    - (c ) clear -  Uživatel si může smazat vlastní výsledky ze souboru

## Settings .py

V souboru si lze v nastavit:
```sh
default_digits = 4  --  výchozí délka čísla
default_range_digits = [1, 2, 3, 4, 5, 6]  --  rozsah možnosti délky čísla
default_dir = "data"  --  název složky, kde se budou ukládat data
default_log_file = "log.txt"  --  název hlavního logu
default_separator = ","  --  pro logy
```

Tyto proměnné jsou automaticky načteny přes funkci get_default_settings() do hlavního programu.
Dále jsou načteny všechny uživatelské funkce, které přepisují defaultní proměnné.

Uživatelské funkce musí být uložené v souboru settings .py.
Výstup této funkce musí být stejného typu jako je defaultní proměnná, jinak se nepoužije.
Funkce se musí jmenovat `set_user_` následovano jménem proměnné, kterou chceme změnit například
`default_name`, název funkce tedy bude `set_user_default_name()`.

>Například:
>`default_name = Guest`
>Vytvoříme funkci `set_user_default_name()`, která bude mít v sobě input, který bude
>po uživateli chtít zadat jeho jméno. Funkce se automaticky načte při spuštění programu
>a bude po uživateli chtít zadat jeho jméno. Po zadání se výchozí hodnota proměnné
>přepíše na hodnotu zadanou uživatelem a přepíše se ve slovníku se všemi proměnnými.

```sh
def set_user_default_name() -> str:

    pf.separator_line()
    name = input("Whats your name? ")
    pf.separator_line()
    
    return name
```

## Number generator .py

V souboru si lze v nastavit:
```sh

default_file_with_numbers = "used_numbers/numbers.txt"  --  soubor, kde se ukládájí vygenerované čísla
default_different_file_name: bool = True  --  jestli se budou vygenerované čísla ukladat do jednoho souboru, který se vždy přepíše při změně počtu číslic nebo pro každou délku vygenerovaného čísla se vytvoří vlastní soubor
default_number_digits = 4  --  přepíše se v hlavním programu (jak dlouhé číslo se bude generovat)
default_range_from = 0  --  od jakého čísla se budou generovat hodnoty
default_range_to = 9  --  do jakého čísla se budou generovat hodnoty
default_first_digit_is_null = False  --  jestli se má generovat číslo s nulou na začátku
default_repeat_digit = False  --  jestli se mají opakovat čísla
```

### generator_random_number()

Generuje náhodné číslo dle proměnných. Před generování se provedé kontrola, která ověří
zda lze dle nastavení číslo vygenerovat.

>Například:
>Pokud zvolíme `default_range_from = 0`, `default_range_to = 2` a `default_repeat_digit = False` pro 
>`default_number_digits = 4` nebude možné číslo vygenerovat, protože není stanoven dostatečný rozsah číslic.
>Program vypíše chybu `Settings error` a zastaví program.

### generator_unique_number()

Je mu předáno číslo z `generator_random_number()` a pro zaručení unikátnosti se každé vygenerované číslo
ukládá do souboru `default_file_with_numbers = "used_numbers/numbers.txt"`. Pokud v souboru číslo už existuje, tak
se generuje nové. Zde dochází ke kontrole, zda pro danou délku čísla existuje ještě možnost unikátního čísla.
Funkce `get_max_available_options` propočítává dle zadaných proměnných maximální počet možností, které lze
vygenerovat a ověřuje se s vygenerovanými čísly. Pokud bylo dosaženo limutu a už nelze generovat unikántí
číslo, tak se musí soubor promazat a začne se zase od začátku.

>Například:
>Pokud zvolíme `default_range_from = 0`, `default_range_to = 9`, `default_repeat_digit = False` a
>`default_first_digit_is_null: bool = False` pro `default_number_digits = 4` bude maximální počet možnosti
>unikátních čísel rovný 4536. Tato kontrola se využije hlavně při jednom nebo dvoumístmém čísle.

### uložení vygenerovaných čísel
`default_different_file_name` - určuje jak se budou úkládat vygenerované čísla  
Pokud je nastaveno **True** pro každou délku vygenerovaného čísla se vytvoří vlastní soubor s prefixem např. 2_digit_ a z proměnné `default_file_with_numbers` se vezme název souboru, konečný soubor bude 2_digit_numbers.txt uložený ve složce used_numbers.

Pokud je nastaveno **False** čísla se budou ukládat vždy do stejného souboru  
**Pokud se změní délka čísla například z 3-číselného na 4-číselné, dojde k přepsání souboru s uloženými čísly.**