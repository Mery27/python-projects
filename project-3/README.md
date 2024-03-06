# Python projekt 3 - Election sraper

Projekt do Python Akademie od Engeta.

## Popis projektu

Tento projekt slouží k extrahování výsledků z parlamentích voleb v roce 2017. Odkaz na stránky [zde](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ).

## Instalace knihoven

V projektu jsou použity doplňkové knihovny a jejich seznam je uložen v souboru `requirements.txt`.
Pro instalaci s manažerem `pip` použijte následující příklady:
```bash
$ pip --version                     # ověření verze manažeru
$ pip install -r requirements.txt   # instalace veškerých knihoven
```
V našem případě byli použitý knihovny [requests](https://pypi.org/project/requests/) a [beautifulsoup4](https://pypi.org/project/beautifulsoup4/):
```bash
$ pip install requests              # knihovna pro stažení obsahu stránky
$ pip install beautifulsoup4        # knihovna pro usnadnění scrapování z webových stránek
```

## Spuštění projektu

Spuštění souboru `elections_scraper.py` v příkazovém řádků vyžaduje dva povinné argumenty.

```bash
$ python elections_scraper.py <url_uzemniho_celku> <nazev_vysledneho_souboru>
```

`url_uzemniho_celku`    - může být ve formátu celé URL adresy nebo jen částečné, například:
- https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100
- ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100

Seznam všech uzemních celků naleznete [zde](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ)

`nazev_souboru` - může být ve formátu s koncovkou nebo bez ní
- praha.csv
- praha

Po skončení programu se vám výsledky uloží do zadaného souboru `praha.csv`

**V případě, že se vám bude vyskytovat chyba popsané níže, lze si zvýšit `request_timeout_seconds = 120` na vyšší hodnotu, která je udávaná v sekundách.**
```bash
Request timed out. Timeout set to: 120 seconds.
```
## Ukázka projektu

Výsledky hlasování pro okres Prostějov:

1. argument: `https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103`
2. argument: `prostejov`

Spuštění programu:

```bash
$ python elections_scraper.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" "prostejov"
```

Průběh stahování:

```bash
Download data from url:
https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103
------------------------------------------------------------
Progress: total 97/97  - disctrict 0/0  - time 01:54
------------------------------------------------------------
Saving data to te file:  prostejov.csv
Progress: 97/97
------------------------------------------------------------
I'm ending the program
```

Částečný výstup:

code,location,registred,envelops,valid,Občanská demokratická strana,Řád národa - Vlastenecká unie a další
506761,Alojzov,205,145,144,29,0,0,9,0,5,17,4,1,1,0,0,18,0,5,32,0,0,6,0,0,1,1,15,0
589268,Bedihošť,834,527,524,51,0,0,28,1,13,123,2,2,14,1,0,34,0,6,140,0,0,26,0,0,0,0,82,1
589276,Bílovice-Lutotín,431,279,275,13,0,0,32,0,8,40,1,0,4,0,0,30,0,3,83,0,0,22,0,0,0,1,38,0