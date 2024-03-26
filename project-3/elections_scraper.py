'''
Projekt 3 Election scraper
election_scraper.py: třetí projekt do Engeto Online Python Akademie

author: Jiří Merenda
email: j.merenda@seznam.cz
discord: .mery27
'''

import sys
import csv
import os
import time

import program_functions as pf

# Check if URL has all 3 parameters, name program, url from website and file name
if len(sys.argv) != 3:
    pf.separator_line()
    print(f"Missing argument{'s' if len(sys.argv) == 1 else ''}, program will be stoped.")
    quit()

# Take from URL only text after last "/"
# user_url = sys.argv[1].split("/")[-1]
user_url = pf.get_last_text_in_url(sys.argv[1])

if user_url.find("xnumnuts") == -1 and not user_url == pf.world_url:
    pf.separator_line()
    print("You enter wrong format URL adress, missing some paramater 'kraj=' or 'xnumnuts='.")
    quit()

user_file = sys.argv[2]
user_file = user_file if os.path.splitext(user_file)[-1][-3:] == "csv" else user_file + ".csv"
file = os.path.dirname(os.path.realpath(__file__)) + os.sep + user_file

pf.separator_line()
print("Download data from url:")
print(pf.create_url(user_url))
pf.separator_line()

result_villages = {}
start_time = time.time()
# list of all villages with url adress which we need to process
if user_url == pf.world_url:
    list_villages = pf.get_international_village(user_url).items()
    header = pf.header_countries
else:
    list_villages = pf.get_data_select_village(user_url).items()
    header = pf.header
# COMPLETE RESULT FROM ALL VILLAGES(CITIES) AND DISTRICT into result_villages variable
for index_village, (title, village) in enumerate(list_villages):
    result_villages[title] = village
    village_url = village[pf.title_url_link]
    # If url parameter "vyber" or "svetadil" is in url you get direct election result page
    if village_url.find("vyber") >= 0 or village_url.find("svetadil") >= 0:
        result_villages[title][pf.title_election_results] = pf.get_result_election(village_url)
        pf.progress_bar(
            total_from = index_village,
            total_to = len(list_villages),
            district_from = 0,
            distric_to = 0,
            start_time = start_time
            )
    else:
        # If region city has some district process them
        list_of_districts = pf.get_data_select_district(village_url).values()
        for index_disctrict, district_url in enumerate(list_of_districts):
            result_for_disctrict = pf.get_result_election(district_url)
            if index_disctrict == 0:
                result_villages[title][pf.title_election_results] = result_for_disctrict
            else:
                for key, value in result_for_disctrict.items():
                    if key == pf.title_election_candidates:
                        for candidate in result_for_disctrict[key]:
                            result_villages[title][pf.title_election_results][pf.title_election_candidates][candidate] += (
                                int(result_for_disctrict[pf.title_election_candidates][candidate]))
                    else:
                        result_villages[title][pf.title_election_results][key] += int(result_for_disctrict[key])
            pf.progress_bar(
                total_from = index_village,
                total_to = len(list_villages),
                district_from = index_disctrict,
                distric_to = len(list_of_districts),
                start_time = start_time
                )

# Exted header with all candidates which we get from first item in result result_villages
first_result_election_candidates = next(iter(result_villages.values()))[pf.title_election_results]
all_election_candidates = first_result_election_candidates.get(pf.title_election_candidates).keys()
header.extend(all_election_candidates)

pf.separator_line(space_top=True)
print("Saving data to te file: ", user_file)

result = []
# CREATE ROWS FOR CSV FILE
for index, village in enumerate(result_villages.values()):
    # Progres bar
    print(f"\rProgress: {index + 1}/{len(result_villages)}", end='', flush=True)
    # Fill row with numbers for length of header
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

pf.separator_line(space_top=True)
print("I'm ending the program")