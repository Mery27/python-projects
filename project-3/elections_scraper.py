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
world = "ps36?xjazyk=CZ"
request_timeout_seconds = 120
title_code = "code"
title_location = "location"
title_continent = "continent"
title_countries = "countries"
title_city = "city"
title_count_district = "count_district"
title_registred = "registred"
title_envelops = "envelops"
title_valid = "valid"
title_election_results = "election_results"
title_election_candidates = "election_candidates"
title_url_link = "url"
# list of election candidates will be added on the end of the header
header = [title_code, title_location, title_registred, title_envelops, title_valid]
header_countries = [title_continent, title_countries, title_city, title_registred, title_envelops, title_valid] 


def create_url(website_url: str) -> str:
    return base_url + "/" + website_url


def get_response(url: str) -> requests.models.Response|None:
    '''
    Try connection to the url, if it fails in any case, program will be stopped.
    '''
    try:
        response = requests.get(url, timeout=request_timeout_seconds)
        if response.status_code != 200:
            separator_line(space_top=True)
            print(f"Request to {url} failed with {response.status_code} status code.")
            quit()

    except requests.exceptions.Timeout:
        separator_line(space_top=True)
        print(f"Request timed out. Timeout set to: {request_timeout_seconds} seconds.")
        quit()

    except requests.exceptions.RequestException as e:
        separator_line(space_top=True)
        print(f"Request give us error: {e}")
        quit()

    else:
        return response


def get_content_from_url(website_url: str) -> bs:
    '''
    Return html content from url.
    '''
    response = get_response(create_url(website_url))

    return bs(response.content, features="html.parser")


def get_data_select_village(website_url: str) -> dict:
    '''
    Get dict with all cities for select.

    Return:
        {
            'Praha': {\n
                'city_name': 'Praha',\n
                'code': 'CZ0100',\n
                'url': 'ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100'\n
                },\n
            'Benešov': {....\n
    '''
    html_page = get_content_from_url(website_url)
    rows = html_page.select("table tr:nth-child(n+3)")
    
    dict_of_results = {}
    for row in rows:
        if row.select("td:nth-child(1)")[0].get_text().isnumeric():
            code = row.select("td:nth-child(1)")[0].get_text()
            title = row.select("td:nth-child(2)")[0].get_text()
            url = row.select("td:last-child a")[0].attrs["href"]

            dict_of_results[title] = {
                title_location: title,
                title_code: code,
                title_url_link: url,
                title_election_results : {} }

    return dict_of_results


def get_data_select_district(website_url: str) -> dict:
    '''
    Get result from table, only for "vyber okrsku"

    Return:
        {"code": "url"}
    '''
    html_page: bs = get_content_from_url(website_url)
    rows = html_page.select("table tr:nth-child(n+2)")
    
    dict_of_results = {}
    for row in rows:
        for column in row.find_all("td", class_="cislo"):
            code = column.get_text()
            url = column.select("a")[0].attrs["href"]
            
            dict_of_results[code] = url

    return dict_of_results


def get_international_village(website_url: str) -> dict:
    '''
    Get dict with all countries for select.

    Return:
        {0: 
            {
                'election_results': {},
                'city': 'Tirana',
                'count_district': '1',
                'continent': 'Evropa',
                'url': 'ps311?xjazyk=CZ&xkraj=2&xobec=999997&xsvetadil=EV&xzeme=8&xokrsek=1',
                'countries': 'Albánie'
            },
    '''
    html_page = get_content_from_url(website_url)
    rows = html_page.select("table tr:nth-child(n+2)")
    
    current_continent = ""
    current_countries = ""
    dict_of_results = {}
    for index, row in enumerate(rows):
        if row.select_one("td[headers='s1'] a"):
            current_continent = row.select_one("td[headers='s1'] a").get_text().replace("\n", "")
        if row.select_one("td[headers='s2']"):
            current_countries = row.select_one("td[headers='s2']").get_text().replace("\n", "")
        city = row.select_one("td[headers='s3']").get_text()
        count_district = row.select_one("td[headers='s4']").get_text().replace("\n","")
        url = row.select_one("td:last-child a").attrs["href"]

        dict_of_results[index] = {
            title_continent: current_continent,
            title_countries: current_countries,
            title_city: city,
            title_count_district: count_district,
            title_url_link: url,
            title_election_results : {} }

    return dict_of_results


def get_result_election(website_url: str) -> dict:
    '''
    Get result as registred, envelops, valid and all election candidates

    Return:
        {'election_candidates': {
            'ANO 2011': '32',
            'Blok proti islam.-Obran.domova': '0',
            ...and others
            },
        'envelops': '145',
        'registred': '205',
        'valid': '144'
        }
    '''
    html_page: bs = get_content_from_url(website_url)
    table_sum_election = html_page.select("#publikace > table tr:last-child")

    result_sum_election = {title_registred: 0,
                            title_envelops: 0,
                            title_valid: 0,
                            title_election_candidates : {} }
    
    for col in table_sum_election:
        result_sum_election[title_registred] = int(col.select(
            "td[headers='sa2']")[0].get_text().replace("\xa0", ""))
        result_sum_election[title_envelops] = int(col.select(
            "td[headers='sa3']")[0].get_text().replace("\xa0", ""))
        result_sum_election[title_valid] = int(col.select(
            "td[headers='sa6']")[0].get_text().replace("\xa0", ""))
    
    table_election_candidate = html_page.select("#outer table tr:nth-child(n+3)")
    for row in table_election_candidate:
        if row.select("td:nth-child(1)")[0].get_text().isnumeric():
            title = row.select("td:nth-child(2)")[0].get_text()
            votes = row.select("td:nth-child(3)")[0].get_text().replace("\xa0", "")
            result_sum_election[title_election_candidates][title] = int(votes)

    return result_sum_election


def progress_bar(total_from: str|int, total_to: str|int,
                 district_from: str|int, distric_to: str|int,
                 start_time: time,
                 timer_format: str = '%M:%S'):
    '''
    Return progress bar in format.\n
    Progress: total 2/57  - disctrict 10/109  - time 00:14\n
    Some space on the end in time line, clear screen from previous longer line
    '''
    print(f"\rProgress:",
            f"total {total_from + 1}/{total_to}",
            f" - disctrict {district_from}/{distric_to}",
            f" - time {time.strftime(timer_format,time.gmtime(time.time() - start_time))}  ",
            end='', flush=True)


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

if user_url.find("xnumnuts") == -1 and not user_url == world:
    separator_line()
    print("You enter wrong format URL adress, missing some paramater 'kraj=' or 'xnumnuts='.")
    quit()

user_file = sys.argv[2]
user_file = user_file if os.path.splitext(user_file)[-1][-3:] == "csv" else user_file + ".csv"
file = os.path.dirname(os.path.realpath(__file__)) + os.sep + user_file

separator_line()
print("Download data from url:")
print(create_url(user_url))
separator_line()

result_villages = {}
start_time = time.time()
# list of all villages with url adress which we need to process
if user_url == world:
    list_villages = get_international_village(user_url).items()
    header = header_countries
else:
    list_villages = get_data_select_village(user_url).items()
# COMPLETE RESULT FROM ALL VILLAGES(CITIES) AND DISTRICT into result_villages variable
for index_village, (title, village) in enumerate(list_villages):
    result_villages[title] = village
    village_url = village[title_url_link]
    # if url parameter "vyber" or "svetadil" is in url you get direct election result page
    if village_url.find("vyber") >= 0 or village_url.find("svetadil") >= 0:
        result_villages[title][title_election_results] = get_result_election(village_url)
        progress_bar(index_village, len(list_villages), 0, 0, start_time)
    else:
        list_of_districts = get_data_select_district(village_url).values()
        for index_disctrict, district_url in enumerate(list_of_districts):
            result_for_disctrict = get_result_election(district_url)
            if index_disctrict == 0:
                result_villages[title][title_election_results] = result_for_disctrict
            else:
                for key, value in result_for_disctrict.items():
                    if key == title_election_candidates:
                        for candidate in result_for_disctrict[key]:
                            result_villages[title][title_election_results][title_election_candidates][candidate] += (
                                int(result_for_disctrict[title_election_candidates][candidate]))
                    else:
                        result_villages[title][title_election_results][key] += int(result_for_disctrict[key])
            progress_bar(index_village, len(list_villages), index_disctrict,
                         len(list_of_districts), start_time)

# Exted header with all candidates which we get from first item in result result_villages
first_result_election_candidates = next(iter(result_villages.values()))[title_election_results]
all_election_candidates = first_result_election_candidates.get(title_election_candidates).keys()
header.extend(all_election_candidates)

separator_line(space_top=True)
print("Saving data to te file: ", user_file)

result = []
# CREATE ROWS FOR CSV FILE
for index, village in enumerate(result_villages.values()):
    # Progres bar
    print(f"\rProgress: {index + 1}/{len(result_villages)}", end='', flush=True)
    # fill row with numbers for length of header
    row = [i for i in range(len(header))]
    for key_1_lvl, value_1_lvl in village.items():
        # if key in header, write to header in same index
        if key_1_lvl in header:
            row[header.index(key_1_lvl)] = village.get(key_1_lvl)
        if key_1_lvl not in header and isinstance(value_1_lvl, dict):
            for key_2_lvl, value_2_lvl in village.get(key_1_lvl).items():
                if key_2_lvl in header:
                    row[header.index(key_2_lvl)] = village.get(
                        key_1_lvl, {}).get(key_2_lvl, {})
                if key_2_lvl not in header and isinstance(value_2_lvl, dict):
                    for key_3_lvl, value_3_lvl in village.get(key_1_lvl).get(key_2_lvl).items():
                        if key_3_lvl in header:
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