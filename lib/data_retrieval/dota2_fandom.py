import requests
from bs4 import BeautifulSoup


def get_heroes_bad_against(hero_name):
    soup = return_beautiful_soup_parser_from_hero_counters_page(hero_name)
    divs_between = find_divs_between_elements_by_id( "Bad_against...", "Good_against...", soup)
    names_of_heroes_bad_against = get_names_of_heroes_from_filtered_divs(divs_between)
    return names_of_heroes_bad_against


def get_heroes_good_against(hero_name):
    soup = return_beautiful_soup_parser_from_hero_counters_page(hero_name)
    divs_between = find_divs_between_elements_by_id("Good_against...", "Works_well_with...", soup)
    names_of_heroes_good_against = get_names_of_heroes_from_filtered_divs(divs_between)
    return names_of_heroes_good_against


def get_names_of_heroes_from_filtered_divs(divs_between):
    names_of_heroes_bad_against = []
    for div in divs_between:
        a = div.find("a")
        if a.get_text(strip=True):
            names_of_heroes_bad_against.append(a.get_text(strip=True))
    return names_of_heroes_bad_against


def find_divs_between_elements_by_id(start_id, end_id, soup):
    start = soup.find(id=start_id)
    end = soup.find(id=end_id)
    divs_between = []
    for el in start.find_all_next():
        if el == end:  # stop when reaching the end marker
            break
        if el.name == "div":
            divs_between.append(el)
    return divs_between


def return_beautiful_soup_parser_from_hero_counters_page(hero_name):
    response = requests.get("https://dota2.fandom.com/wiki/" + hero_name.title() + "/Counters")
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup
