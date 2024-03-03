'''
Get data from websie https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ
Choose regional unit and get voting results for all elections villages.
Save this data as cvs file.

'''

import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import sys
import csv
import os
import time



base_url = "https://volby.cz/pls/ps2017nss"
# základní stránka pro výběr - 1 úroveň
url_uzemni_uroven = "ps3?xjazyk=CZ"
# 2 úroveň - jen příklad
url_vyber_obce = "ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103"
# 3 úroveň - jen příklad - má jen některá obec
url_vyber_okrsku = "ps33?xjazyk=CZ&xkraj=1&xobec=500054"
# vysledky - jen příklad - finalni stránka
url_vysledky = "ps311?xjazyk=CZ&xkraj=1&xobec=500054&xokrsek=1001&xvyber=1100"


def create_url(base_url: str, join_url: str) -> str:
    return base_url + "/" + join_url


def get_response(url: str) -> requests.models.Response:
    return requests.get(url, timeout=120)


def get_response_code(response: requests.models.Response) -> int:
    '''
    Return status code from requests.get().
    More info on this url https://developer.mozilla.org/en-US/docs/Web/HTTP/Status

        Return:
        -------
            status_code (int)\n
            200 = Ok\n
            204 = Not content\n
            400 = Bad request\n
            404 = Not Found\n
            403 = Forbiden\n
    '''
    return response.status_code


def get_content_from_url(response: requests.models.Response) -> bs:
    '''
    Return content from url if response status code return 200 else return
    warning and quit the program.
    '''
    if get_response_code(response) == 200:
        return bs(response.content, features="html.parser")
    
    else:
        print("We cannot get content from web site.")
        print(f"Get status code: {get_response_code(response)}")
        quit()


def get_table_data_from_url(html_page: bs) -> dict:
    '''
    Get dict with all cities for select.
    select table 3 tr and all after
    
    Pro první dvě úrovně
    - výběr uzemní úrovně
    - výběr obce
    table tr:nth-child(3n+0)

    Example:
        500054    Praha 1    URL

    Return:
    -------
        {
            'Praha': {\n
                'city_name': 'Praha',\n
                'code': 'CZ0100',\n
                'url': 'ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100'\n
                },\n
            'Benešov': {\n
                'city_name': 'Benešov',\n
                'code': 'CZ0201',\n
                'url': 'ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101'\n
                },\n
        }
    '''
    rows = html_page.select(
        "table tr:nth-child(n+3)"
        )
    
    dict_of_results = {}
    for row in rows:
        if row.select("td:nth-child(1)")[0].get_text().isnumeric():
            code = row.select("td:nth-child(1)")[0].get_text()
            title = row.select("td:nth-child(2)")[0].get_text()
            url = row.select("td:last-child a")[0].attrs["href"]

            dict_of_results[title] = {
                "location": title,
                "code": code,
                "url": url,
                "election_results" : {}
                }

    return dict_of_results


def get_data_select_village(url: str) -> dict:
    '''
    Get result from table, only for "uzemni uroven" and "vyber obce".
    '''
    return get_table_data_from_url(
            get_content_from_url(
                get_response(
                    create_url(base_url, url)
                    )))


def get_data_select_district(url: str) -> dict:
    '''
    Get result from table, only for "vyber okrsku"

    Example:
        1001	1002	1003	1004

    Result:
        {"code": "url"}
    '''
    html_page: bs = get_content_from_url(get_response(create_url(base_url, url)))
    rows = html_page.select(
        "table tr:nth-child(n+2)"
        )
    
    dict_of_results = {}
    for row in rows:
        for column in row.find_all("td", class_="cislo"):
            code = column.get_text()
            url = column.select("a")[0].attrs["href"]
            
            dict_of_results[code] = url

    return dict_of_results


def get_result_election(url: str) -> dict:
    '''
    Get result as registred, envelops, valid and all election candidates

    Result example:
        {'election_candidate': {
            'ANO 2011': '32',
            'Blok proti islam.-Obran.domova': '0',
            'CESTA ODPOVĚDNÉ SPOLEČNOSTI': '0',
            'Dobrá volba 2016': '0',
            ...and others
            },
        'envelops': '145',
        'registred': '205',
        'valid': '144'
        }
    '''
    html_page: bs = get_content_from_url(get_response(create_url(base_url, url)))
    table_sum_election = html_page.select(
        "#publikace > table tr:last-child"
    )

    result_sum_election = {
        "registred": 0,
        "envelops": 0,
        "valid": 0,
        "election_candidates" : {}
        }
    for col in table_sum_election:
        result_sum_election["registred"] = col.select(
            "td[headers='sa2']")[0].get_text().replace("\xa0", "")
        result_sum_election["envelops"] = col.select(
            "td[headers='sa3']")[0].get_text().replace("\xa0", "")
        result_sum_election["valid"] = col.select(
            "td[headers='sa6']")[0].get_text().replace("\xa0", "")
    
    table_election_candidate = html_page.select(
        "#outer table tr:nth-child(n+3)"
        )
    for row in table_election_candidate:
        if row.select("td:nth-child(1)")[0].get_text().isnumeric():
            title = row.select("td:nth-child(2)")[0].get_text()
            votes = row.select("td:nth-child(3)")[0].get_text().replace("\xa0", "")
            result_sum_election["election_candidates"][title] = votes

    return result_sum_election


def progress_bar(total_from: str|int,
                 total_to: str|int,
                 district_from: str|int,
                 distric_to: str|int,
                 start_time: time,
                 timer_format: str = '%M:%S'
                ):
    '''
    Return progress bar in format.
    Progress: total 2/57  - disctrict 10/109  - time 00:14
    '''
    print(f"\rProgress:",
            f"total {total_from + 1}/{total_to}",
            f" - disctrict {district_from}/{distric_to}",
            f" - time {time.strftime(timer_format,time.gmtime(time.time() - start_time))}",
            end='',
            flush=True
            )


def separator_line():
    print("-"*50)


if len(sys.argv) != 3:
    separator_line()
    print(f"Missing argument{'s' if len(sys.argv) == 1 else ''}, program will be stoped.")
    quit()

# TODO: check if user_url is right url, caintan all parameters
user_url = sys.argv[1]
user_file = sys.argv[2]

'''
'Bartošovice': {
    'code': '599212',
        'election_results': {
        'election_candidates': {
            'ANO 2011': 281,
            'Blok proti islam.-Obran.domova': 0,
            'CESTA ODPOVĚDNÉ SPOLEČNOSTI': 0,
            'Dobrá volba 2016': 1,
            'Dělnic.str.sociální spravedl.': 2,
            'Komunistická str.Čech a Moravy': 104,
            'Křesť.demokr.unie-Čs.str.lid.': 23,
            'Občanská demokratická aliance': 0,
            'Občanská demokratická strana': 39,
            'REALISTÉ': 1,
            'ROZUMNÍ-stop migraci,diktát.EU': 2,
            'Radostné Česko': 2,
            'Referendum o Evropské unii': 0,
            'SPORTOVCI': 3,
            'SPR-Republ.str.Čsl. M.Sládka': 2,
            'STAROSTOVÉ A NEZÁVISLÍ': 6,
            'Strana Práv Občanů': 2,
            'Strana svobodných občanů': 9,
            'Strana zelených': 13,
            'Svob.a př.dem.-T.Okamura (SPD)': 140,
            'TOP 09': 7,
            'Česká národní fronta': 0,
            'Česká pirátská strana': 38,
            'Česká str.sociálně demokrat.': 56,
            'Česká strana národně sociální': 0,
            'Řád národa - Vlastenecká unie': 3
            },
        'envelops': 735,
        'registred': 1341,
        'valid': 734},
    'title': 'Bartošovice',
    'url': 'ps33?xjazyk=CZ&xkraj=14&xobec=599212'
    }}
'''
all_villages = {}
# list of all adres on 1.level (seznam mest)
list_of_villages = get_data_select_village(user_url).items()

separator_line()
print("Download data from url: ", user_url)
separator_line()

start_time = time.time()
for index_village, (title, village) in enumerate(list_of_villages):
    '''
    {'code': '599247',
    'title': 'Bílovec',
    'url': 'ps33?xjazyk=CZ&xkraj=14&xobec=599247'}
    '''
    # complete_url = 0 if index == 0 else complete_url + 1
    all_villages[title] = village
    # url: [url]
    village_url = village["url"]
    if village_url.find("vyber") > 1:
        all_villages[title]["election_results"] = get_result_election(village_url)
        # Progres bar
        progress_bar(index_village, len(list_of_villages), 0, 0, start_time)

    # If vyber is not in url, need lead others url with okrsek
    if village_url.find("vyber") == -1:
        list_of_districts = get_data_select_district(village_url).values()
        for index_disctrict, district_url in enumerate(list_of_districts):
            '''
            python elections_scraper.py "ps32?xjazyk=CZ&xkraj=14&xnumnuts=8104" "file.csv"

            ['ps311?xjazyk=CZ&xkraj=14&xobec=568741&xvyber=8104',
            'ps311?xjazyk=CZ&xkraj=14&xobec=599212&xokrsek=1&xvyber=8104',
            'ps311?xjazyk=CZ&xkraj=14&xobec=599212&xokrsek=2&xvyber=8104',
            'ps311?xjazyk=CZ&xkraj=14&xobec=568481&xvyber=8104',
            'ps311?xjazyk=CZ&xkraj=14&xobec=546984&xvyber=8104',
            'ps311?xjazyk=CZ&xkraj=14&xobec=599247&xokrsek=1&xvyber=8104',
            .....
            '''
            result_for_disctrict = get_result_election(district_url)
            if index_disctrict == 0:
                all_villages[title]["election_results"] = result_for_disctrict
            else:
                for key, value in result_for_disctrict.items():
                    if key == "election_candidates":
                        for candidate in result_for_disctrict[key]:
                            all_villages[title]["election_results"]["election_candidates"][candidate] = int(
                                all_villages[title]["election_results"]["election_candidates"][candidate]
                                ) + int(result_for_disctrict["election_candidates"][candidate])
                    else:
                        all_villages[title]["election_results"][key] = int(
                            all_villages[title]["election_results"][key]
                            ) + int(result_for_disctrict[key])
                        # Progres bar
            progress_bar(index_village,
                         len(list_of_villages),
                         index_disctrict,
                         len(list_of_districts),
                         start_time)

'''
set result dict to correct data, remove url
'''

file = os.path.dirname(os.path.realpath(__file__)) + os.sep + user_file

first_result_election_candidates = next(iter(all_villages.values()))["election_results"]
election_candidates = first_result_election_candidates.get("election_candidates").keys()

header = ["code", "location", "registred", "envelops", "valid", *election_candidates]

result = []

separator_line()
print("Saving data to te file: ", user_file)

for index, village in enumerate(all_villages.values()):
    # Progres bar
    print(f"\rProgress: {index + 1}/{len(all_villages)}", end='', flush=True)
    # předvyplníme, aby se správně vkládali data ze slovníku
    row = [i for i in range(len(header))]
    for key_1_lvl in village:
        # přeskočí url ve slovníku, nepotřebujeme
        if key_1_lvl == "url":
            continue
        # pokud klíče v první úrovní zanoření slovníku odpovídají hodnotě ze headeru
        # zapiš je do listu na pořadí, ve kterém se nacházejí v headeru
        if key_1_lvl in header:
            row[header.index(key_1_lvl)] = village.get(key_1_lvl)
        elif not village.get(key_1_lvl, {}):
            # pokud hodnota co není v headeru je ve slovníků, ale je to prázný dict
            # ověření, aby se neprováděla smyčka v prázdém dictu
            continue
        else:
            for key_2_lvl in village.get(key_1_lvl):
                # pokud klíče ve druhé úrovní zanoření slovníku ....
                if key_2_lvl in header:
                    row[header.index(key_2_lvl)] = village.get(
                        key_1_lvl, {}).get(key_2_lvl, {})
                elif not village.get(key_1_lvl, {}).get(key_2_lvl, {}):
                    # pokud hodnota co není v headeru je ve slovníků, ale je to prázný dict
                    # ověření, aby se neprováděla smyčka v prázdém dictu
                    continue
                else:
                    for key_3_lvl in village.get(key_1_lvl).get(key_2_lvl):
                    # pokud klíče ve třetím úrovní zanoření slovníku ....
                        row[header.index(key_3_lvl)] = village.get(
                            key_1_lvl, {}).get(key_2_lvl, {}).get(key_3_lvl, {})
            
    result.append(row)

with open(file, mode="w", encoding="UTF_8", newline="") as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=",")
    spamwriter.writerow(header)
    for file_row in result:
        spamwriter.writerow(file_row)

print("")
separator_line()
print("I'm ending the program")