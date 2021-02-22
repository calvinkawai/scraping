#!/usr/bin/env python3

"""
Create following structure match data

{
    "Set 1": [
        {
            "Server": "D. Medvedev is serving game 10",
            "Description": "D. Medvedev wins the set",
            "Game Score": "6-4",
            "Score Details": [
                {
                    "Point Score": "Game"
                    "Dscription": "D. Medvedev wins the point with a Service Winner"
                }
            ]
        }
    ]
}
"""


from selenium import webdriver
from helper import *
from pprint import pprint
import os
import json

match_commentaries_xpath = "//*[@class='match-detail-container -live']//*[@class='filter-dropdown__select']//option"
select_set_xpath = "//*[@class='match-detail-container -live']//select"
match_data_xpath = "//*[@class='mc-commentary__container']/div"


driver = webdriver.Chrome(os.curdir + "/chromedriver")


def get_game_description(point_ele):
    return point_ele.find_element_by_xpath(f".//div[@class='mc-commentary__header__middle-column']//span").text + \
        point_ele.find_element_by_xpath(f".//div[@class='mc-commentary__header__middle-column']/h2").text

def get_game_score(point_ele):
    return point_ele.find_element_by_xpath(f".//div[@class='mc-commentary__header__right-column']/div").text

def get_point_description(elem):
    return elem.find_element_by_xpath(f".//div[@class='mc-commentary__commentary__middle-column']/p").text

def get_point_score(elem):
    return elem.find_element_by_xpath(f".//div[@class='mc-commentary__commentary__right-column']/span").text

def scrap_match_data(match_url):
    result = {}
    result["url"] = match_url
    output_file_name = "AO-2021/" + match_url.split("-")[-1] + ".json"
    driver.get(match_url)

    match_commentaries = wait_for_elems_by_xpath(driver, match_commentaries_xpath)
    choose_set_button = wait_for_elem_by_xpath(driver, select_set_xpath)

    for set_elem in match_commentaries:
        choose_set_button.click()
        set_elem.click()
        current_set = set_elem.text.strip()
        result[current_set] = []
        try:
            # the player retired after on current set
            match_data = wait_for_elems_by_xpath(driver, match_data_xpath)
        except Exception as e:
            with open(output_file_name, "w") as fp:
                json.dump(result, fp, indent=4)
            return
        current_game = None
        for md in match_data:
            if "mc-commentary__header" in md.get_attribute("class"):
                if current_game:
                    result[current_set] = [current_game] + result[current_set]
                current_game = dict()
                try:
                    current_game["Game Score"] = get_game_score(md)
                    current_game["Description"] = get_game_description(md)
                except Exception as e:
                    current_game["Description"] = get_game_description(md)
                current_game["Score Details"] = list()
            else:
                # if no heading, one of the player is retired
                if not current_game:
                    current_game = dict()
                    current_game["Game Score"] = "Game is not finished"
                    current_game["Description"] = "Game is not finished"
                    current_game["Score Details"] = list()
                current_point = {}
                try:
                    current_point["Point Score"] = get_point_score(md)
                    current_point["Description"] = get_point_description(md)
                    current_game["Score Details"] = [current_point] + current_game["Score Details"]
                except Exception as e:
                    current_game["Server"] = get_point_description(md)
        result[current_set] = [current_game] + result[current_set]

    with open(output_file_name, "w") as fp:
        json.dump(result, fp, indent=4)
