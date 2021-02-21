#!/usr/bin/env python3

from selenium import webdriver
import os

driver = webdriver.Chrome(os.curdir + "/chromedriver")


driver.get("https://ausopen.com/match/2021-daniil-medvedev-vs-stefanos-tsitsipas-ms602")
