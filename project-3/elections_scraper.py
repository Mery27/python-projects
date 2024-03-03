'''
Get data from websie https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ
Choose regional unit and get voting results for all elections villages.
Save this data as cvs file.

'''

import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import sys


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
    return requests.get(url)


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
        result_sum_election["registred"] = col.select("td[headers='sa2']")[0].get_text().replace("\xa0", "")
        result_sum_election["envelops"] = col.select("td[headers='sa5']")[0].get_text().replace("\xa0", "")
        result_sum_election["valid"] = col.select("td[headers='sa6']")[0].get_text().replace("\xa0", "")
    
    table_election_candidate = html_page.select(
        "#outer table tr:nth-child(n+3)"
        )
    for row in table_election_candidate:
        if row.select("td:nth-child(1)")[0].get_text().isnumeric():
            title = row.select("td:nth-child(2)")[0].get_text()
            votes = row.select("td:nth-child(3)")[0].get_text().replace("\xa0", "")
            result_sum_election["election_candidates"][title] = votes

    return result_sum_election
