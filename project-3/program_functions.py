from bs4 import BeautifulSoup as bs
import requests
import time

import test_data


base_url = "https://volby.cz/pls/ps2017nss"
request_timeout_seconds = 120

world_url = "ps36?xjazyk=CZ"

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


def get_last_text_in_url(url: str) -> bool:
    '''
    Check right format url. If format its enter with https://... format it will be
    cut and it will be taken only text after last "/". 

    Parameters:
        url (str) - url adrress

    Return:
        Get short version url, this mean all text after last "/"
    '''
    result_url = url if url.startswith("ps") else url.split("/")[-1]

    return result_url


def create_url(website_url: str) -> str:
    '''
    Create URL from base_url and website_url. If you put long format URL, function
    take only last part of this long format after last "/".

    Parameters:
        website_url (str) - short version of url, this mean all text after last / in url
        example: ps33?xjazyk=CZ&xkraj=14&xobec=598925

    Return:
        Get dict with all cities(villages) in choosen regional city.

    '''
    return base_url + "/" + get_last_text_in_url(website_url)


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
    Return html content from url in BeautifulSoup format.

    Parameters:
        website_url (str) - short version of url, this mean all text after last / in url
        example: ps33?xjazyk=CZ&xkraj=14&xobec=598925

    Return:
        Get HTML content of website in BeautifulSoup format.
    '''
    response = get_response(create_url(website_url))

    return bs(response.content, features="html.parser")


def get_test_data_from_string(content):
    return bs(content, features="html.parser")


def get_text_by_selector(soup: bs,
                         selector: str,
                         remove: str = None,
                         default: str = ""
                         ) -> str:
    '''
    Get text by CSS selector from html tag.

    Parameters:
        soup (BeautifulSoup as bs) - HTML content in bs format
        selector (str) - CSS selector for find HTML tag
        default (str) - return default string if not get any result

    Return:
        Get plain text from HTML tag.
    '''
    element = soup.select_one(selector)

    if element:
        text = element.get_text(strip=True)
        result = text.replace(remove, "") if remove else text
    else:
        result = default

    return result


def get_text_from_attributes_by_selector(soup: bs,
                         selector: str,
                         attributes: str,
                         default: str = "",
                         ) -> str:
    '''
    Get value from attributes in html tag.

    Parameters:
        soup (BeautifulSoup as bs) - HTML content in bs format
        selector (str) - CSS selector for find HTML tag with some attributes (href, rel, data...)
        default (str) - return default string if not get any result

    Return:
        Get plain text from attribute in HTML tag.
    '''
    element = soup.select_one(selector)

    return element.attrs[attributes] if element else default


def get_data_select_village(website_url: str) -> dict:
    '''
    Get dict with all cities for select.

    Parameters:
        website_url (str) - short version of url, this mean all text after last / in url
        example: ps33?xjazyk=CZ&xkraj=14&xobec=598925

    Return:
        Get dict with all cities(villages) in choosen regional city.

    Return example:
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
        if get_text_by_selector(row, "td:nth-child(1) a").isnumeric():
            code = get_text_by_selector(row, "td:nth-child(1) a")
            title = get_text_by_selector(row, "td:nth-child(2)")
            url = get_text_from_attributes_by_selector(row, "td:last-child a", "href")

            dict_of_results[title] = {
                title_location: title,
                title_code: code,
                title_url_link: url,
                title_election_results : {} }

    return dict_of_results


def get_data_select_district(website_url: str) -> dict:
    '''
    Get result from table, only for page "vyber okrsku". In result we get urls for
    table with election result.

    Parameters:
        website_url (str) - short version of url, this mean all text after last / in url
        example: ps33?xjazyk=CZ&xkraj=14&xobec=598925

    Return:
        List of district in dict in format {"code": "url"}.
    
    Return example:
        {
            '1': 'ps311?xjazyk=CZ&xkraj=14&xobec=598925&xokrsek=1&xvyber=8103',
            '2': 'ps311?xjazyk=CZ&xkraj=14&xobec=598925&xokrsek=2&xvyber=8103'
        }
    '''
    html_page: bs = get_content_from_url(website_url)
    rows = html_page.select("table tr:nth-child(n+2)")
    
    dict_of_results = {}
    for row in rows:
        for column in row.find_all("td", class_="cislo"):
            code = column.get_text()
            url = get_text_from_attributes_by_selector(column, "a", "href")
            
            dict_of_results[code] = url

    return dict_of_results


def get_international_village(website_url: str) -> dict:
    '''
    Get dict with all countries for select.

    Parameters:
        website_url (str) - short version of url, this mean all text after last / in url
        example: ps33?xjazyk=CZ&xkraj=14&xobec=598925

    Return:
        Create dict with all countries in table from website url.

    Return example:
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
        if get_text_by_selector(row, "td[headers='s1'] a"):
            current_continent = get_text_by_selector(row, "td[headers='s1'] a", remove="\n")
        if row.select_one("td[headers='s2']"):
            current_countries = get_text_by_selector(row, "td[headers='s2'] a", remove="\n")
        city = get_text_by_selector(row, "td[headers='s3'] a")
        count_district = get_text_by_selector(row, "td[headers='s4'] a", remove="\n")
        url = get_text_from_attributes_by_selector(row, "td:last-child a", "href")

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

    Parameters:
        website_url (str) - short version of url, this mean all text after last / in url
        example: ps33?xjazyk=CZ&xkraj=14&xobec=598925 

    Return:
        Return dict with election results.

    Return exmaple:
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
        result_sum_election[title_registred] = int(
            get_text_by_selector(col, "td[headers='sa2']", remove="\xa0"))
        result_sum_election[title_envelops] = int(
            get_text_by_selector(col, "td[headers='sa3']", remove="\xa0"))
        result_sum_election[title_valid] = int(
            get_text_by_selector(col, "td[headers='sa6']", remove="\xa0"))
    
    table_election_candidate = html_page.select("#outer table tr:nth-child(n+3)")
    for row in table_election_candidate:
        if get_text_by_selector(row, "td:nth-child(1)").isnumeric():
            title = get_text_by_selector(row, "td:nth-child(2)")
            votes = get_text_by_selector(row, "td:nth-child(3)", remove="\xa0")
            result_sum_election[title_election_candidates][title] = int(votes)

    return result_sum_election


def progress_bar(total_from: str|int, total_to: str|int,
                 district_from: str|int, distric_to: str|int,
                 start_time: time,
                 timer_format: str = '%M:%S'):
    '''
    Return progress bar in format.\n
    Some space on the end in time line, clear screen from previous longer line

    Parameters:
        total_from (str|int) - set current number in range (1 = 1/20)\n
        total_to (str|int) - set total number in range (20 = 1/20)\n
        district_from (str|int) - set current number in range (1 = 1/20)\n
        distric_to (str|int) - set total number in range (20 = 1/20)\n
        start_time (time) - the time from which it starts counting, time in seconds
        since the Epoch\n
        time_format (str) - in time format for function time.strftime()\n

    Return:
        Return current status in process in numbers with total time.

        Progress: total 2/57  - disctrict 10/109  - time 00:14\n
    '''
    print(f"\rProgress:",
            f"total {total_from + 1}/{total_to}",
            f" - disctrict {district_from}/{distric_to}",
            f" - time {time.strftime(timer_format,time.gmtime(time.time() - start_time))}  ",
            end='', flush=True)


def separator_line(space_top: bool = False):
    print("") if space_top else None
    print("-"*60)


if __name__ == "__main__":
    list_of_cities = get_content_from_url("ps32?xjazyk=CZ&xkraj=14&xnumnuts=8103")
    list_of_district = get_data_select_district("ps33?xjazyk=CZ&xkraj=14&xobec=598925")
    table_result = get_result_election("ps311?xjazyk=CZ&xkraj=14&xobec=598925&xokrsek=1&xvyber=8103")

    print(table_result)
