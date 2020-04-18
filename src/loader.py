#!/usr/bin/env python3

import argparse
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

parser = argparse.ArgumentParser(description='Script that loads data from dominos.ua')
parser.add_argument('--lang', type=str, default='ru', help='Site and data language')
parser.add_argument('-l', '--login', type=str, help='User\'s login or email')
parser.add_argument('-p', '--password', type=str, help='User\'s password')
parser.add_argument('-n', '--no-close', action='store_true')

args = parser.parse_args()

driver = webdriver.Chrome()
driver.get('https://dominos.ua/en/kyiv/')

webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

sign_button = driver.find_element_by_class_name('fake-header__sing-in-block')
sign_button.click()

login_input = driver.find_element_by_name('email')
password_input = driver.find_element_by_name('password')

login_input.send_keys(args.login)
password_input.send_keys(args.password)

login_button_xpath = "//button[contains(concat(' ',normalize-space(@class),' '),' dp-btn ') and text()='Sign in']"
login_button = driver.find_element_by_xpath(login_button_xpath)
login_button.click()
time.sleep(5)

profile_button = driver.find_element_by_class_name('fake-header__sing-in-block')
profile_button.click()
time.sleep(2)

history_button = driver.find_element_by_xpath('//li[text()="History"]')
history_button.click()

if not args.no_close:
    driver.close()
