'''
Projekt 3 Election scraper
election_scraper.py: třetí projekt do Engeto Online Python Akademie

author: Jiří Merenda
email: j.merenda@seznam.cz
discord: .mery27
'''

import requests
from bs4 import BeautifulSoup as bs

import sys
import csv
import os
import time


base_url = "https://volby.cz/pls/ps2017nss"
request_timeout_seconds = 120
# list of election candidates will be added on the end of the header
header = ["code", "location", "registred", "envelops", "valid"]
election_results = "election_results"
election_candidates = "election_candidates"
url_link = "url"


def create_url(base_url: str, join_url: str) -> str:
    return base_url + "/" + join_url


def get_response(url: str) -> requests.models.Response|bool:
    '''
    Try connection to the url, if it fails in any case, program will be stopped.
    '''
    try:
        response = requests.get(url, timeout=request_timeout_seconds)
        if response.status_code != 200:
            print(f"Request to {url} failed with {response.status_code} status code.")
            quit()

    except requests.exceptions.Timeout:
        print(f"Request timed out. Timeout set to: {request_timeout_seconds} seconds.")
        quit()

    except requests.exceptions.RequestException as e:
        print(f"Request give us error: {e}")
        quit()

    else:
        return response


def get_content_from_url(response: requests.models.Response) -> bs:
    '''
    Return html content from url.
    '''
    return bs(response.content, features="html.parser")


def get_table_data_from_url(html_page: bs) -> dict:
    '''
    Get dict with all cities for select.

    Return:
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
                header[1]: title,
                header[0]: code,
                url_link: url,
                election_results : {}
                }

    return dict_of_results


def get_data_select_village(url: str) -> dict:
    '''
    Get result from table, only for "uzemni uroven" and "vyber obce".

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
    return get_table_data_from_url(
            get_content_from_url(
                get_response(
                    create_url(base_url, url)
                    )))


def get_data_select_district(url: str) -> dict:
    '''
    Get result from table, only for "vyber okrsku"

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
        header[2]: 0,
        header[3]: 0,
        header[4]: 0,
        election_candidates : {}
        }
    for col in table_sum_election:
        result_sum_election[header[2]] = int(col.select(
            "td[headers='sa2']")[0].get_text().replace("\xa0", ""))
        result_sum_election[header[3]] = int(col.select(
            "td[headers='sa3']")[0].get_text().replace("\xa0", ""))
        result_sum_election[header[4]] = int(col.select(
            "td[headers='sa6']")[0].get_text().replace("\xa0", ""))
    
    table_election_candidate = html_page.select(
        "#outer table tr:nth-child(n+3)"
        )
    for row in table_election_candidate:
        if row.select("td:nth-child(1)")[0].get_text().isnumeric():
            title = row.select("td:nth-child(2)")[0].get_text()
            votes = row.select("td:nth-child(3)")[0].get_text().replace("\xa0", "")
            result_sum_election[election_candidates][title] = int(votes)

    return result_sum_election


def progress_bar(total_from: str|int,
                 total_to: str|int,
                 district_from: str|int,
                 distric_to: str|int,
                 start_time: time,
                 timer_format: str = '%M:%S'
                ):
    '''
    Return progress bar in format.\n
    Progress: total 2/57  - disctrict 10/109  - time 00:14\n
    Some space on the end in time line, clear screen from previous longer line
    '''
    print(f"\rProgress:",
            f"total {total_from + 1}/{total_to}",
            f" - disctrict {district_from}/{distric_to}",
            f" - time {time.strftime(timer_format,time.gmtime(time.time() - start_time))}  ",
            end='',
            flush=True
            )


def separator_line(space_top: bool = False):
    print("") if space_top else None
    print("-"*60)


#-------------
# MAIN PROGRAM
#-------------
if len(sys.argv) != 3:
    separator_line()
    print(f"Missing argument{'s' if len(sys.argv) == 1 else ''}, program will be stoped.")
    quit()

user_url = sys.argv[1].split("/")[-1]

if user_url.find("kraj") == -1 or user_url.find("xnumnuts") == -1:
    separator_line()
    print("You enter wrong format URL adress, missing some paramater 'kraj=' or 'xnumnuts='.")
    quit()

user_file = sys.argv[2]
file = os.path.dirname(os.path.realpath(__file__)) + os.sep + user_file

separator_line()
print("Download data from url: ", user_url)
separator_line()

# initialization variable for all villages with election data
result_villages = {}
start_time = time.time()
# list of all villages with url adress which we need to process
list_villages = get_data_select_village(user_url).items()
# complete region result from all villages and distrcit into result_villages variable
for index_village, (title, village) in enumerate(list_villages):
    result_villages[title] = village
    village_url = village[url_link]
    # if url parameter "vyber" is in url you get election result page
    if village_url.find("vyber") > 1:
        result_villages[title][election_results] = get_result_election(village_url)
        progress_bar(index_village, len(list_villages), 0, 0, start_time)
    else:
        list_of_districts = get_data_select_district(village_url).values()
        for index_disctrict, district_url in enumerate(list_of_districts):
            result_for_disctrict = get_result_election(district_url)
            if index_disctrict == 0:
                result_villages[title][election_results] = result_for_disctrict
            else:
                for key, value in result_for_disctrict.items():
                    if key == election_candidates:
                        for candidate in result_for_disctrict[key]:
                            result_villages[title][election_results][election_candidates][candidate] += (
                                int(result_for_disctrict[election_candidates][candidate]))
                    else:
                        result_villages[title][election_results][key] += int(result_for_disctrict[key])
                        # Progres bar
            progress_bar(index_village, len(list_villages), index_disctrict,
                         len(list_of_districts), start_time)


first_result_election_candidates = next(iter(result_villages.values()))[election_results]
all_election_candidates = first_result_election_candidates.get(election_candidates).keys()
header.extend(all_election_candidates)

separator_line(space_top=True)
print("Saving data to te file: ", user_file)


result = []
for index, village in enumerate(result_villages.values()):
    # Progres bar
    print(f"\rProgress: {index + 1}/{len(result_villages)}", end='', flush=True)
    # fill row with numbers for length of header
    row = [i for i in range(len(header))]
    for key_1_lvl in village:
        # we dont need url in result
        if key_1_lvl == url_link:
            continue
        # if key in header, write to header in same index
        if key_1_lvl in header:
            row[header.index(key_1_lvl)] = village.get(key_1_lvl)
        elif not village.get(key_1_lvl, {}):
            # dont loop throw empy dict
            continue
        else:
            for key_2_lvl in village.get(key_1_lvl):
                if key_2_lvl in header:
                    row[header.index(key_2_lvl)] = village.get(
                        key_1_lvl, {}).get(key_2_lvl, {})
                elif not village.get(key_1_lvl, {}).get(key_2_lvl, {}):
                    continue
                else:
                    for key_3_lvl in village.get(key_1_lvl).get(key_2_lvl):
                        row[header.index(key_3_lvl)] = village.get(
                            key_1_lvl, {}).get(key_2_lvl, {}).get(key_3_lvl, {})

    result.append(row)


with open(file, mode="w", encoding="UTF_8", newline="") as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=",")
    spamwriter.writerow(header)
    for file_row in result:
        spamwriter.writerow(file_row)

separator_line(space_top=True)
print("I'm ending the program")