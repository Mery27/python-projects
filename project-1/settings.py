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