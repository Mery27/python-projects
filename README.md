
# Python projekt 1 - Textový analyzátor

Může načíst jednoduchý textový (.txt) soubor, který se nachází ve stejném adresáři jako python soubor nebo zpracuje data v proměnné TEXTS.
Ze souboru převede text do jedné proměnné. U výchozí proměnné, která je list, lze vybrat, kterou část chcete analyzovat.

## Funkce

- Analyzuje text a vypíše celkový počet slov, slova začínající velkým písmenem, slova pouze velkým písmem, slova pouze malým písmem, čísla a jejich celkový součet.
- Vytvoří tabulku s jednotlivými délkami slov a jejich celkovým výskytem v textu. (tabulka se přizpůsobí počtu nalezených slov, vytvoří se poměr při velkém počtu slov)
- Najde nejpoužívanější slova. (nastavitelný počet slov, které chceme zobrazit)

## Nastavení

Na začátku programu si lze v proměnných nastavit:
- maximální šířku řádku, text se podle šířky ořízne, max_length = 60
- které znaky se mají z textu odebrat, popřípadě nahradit, list_replace_chars = .,?!'"\n
- do kolika textů v proměnné TEXTS se má zobrazit i slovní nábídka pro výběr, show_max_options = 10 např. 1) První text k analýze... (345) 2) Druhý text k analýze... (234)
- jaké soubory jsou povolené pro načtení textů, text_files = [\"txt\"]
- hlavička tabulky, table_head = ["LEN", "OCCURENCES", "NR."]
- oddělovač v tabulce, table_separator = "|"
- symbol pro vyjádření počtu slov v tabulce, char_for_graph = "*"
- kolik nejpoužívanějších slov se má vypsat, number_most_used_words = 10

## Testování bez zadávání dat v inputech

Pro rychlejší testování lze nastavit proměnou test = True a vyřadí se zadávání dat přes input(). V proměných si lze nastavit co chcete testovat.