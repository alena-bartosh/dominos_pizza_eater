#!/usr/bin/env python3

import argparse
import time

import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

parser = argparse.ArgumentParser(description='Script that loads data from dominos.ua')
parser.add_argument('--lang', type=str, default='ru', help='Site and data language')
parser.add_argument('--wait', action='store_true', help='Wait for town confirm popup')
parser.add_argument('-l', '--login', type=str, help='User\'s login or email')
parser.add_argument('-p', '--password', type=str, help='User\'s password')

args = parser.parse_args()
driver = webdriver.Chrome()
driver.delete_all_cookies()

try:
    driver.get('https://dominos.ua/en/kyiv/')

    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

    sign_button = driver.find_element_by_class_name('fake-header__sing-in-block')
    sign_button.click()

    login_input = driver.find_element_by_name('email')
    password_input = driver.find_element_by_name('password')

    login_input.send_keys(args.login)
    password_input.send_keys(args.password)

    login_button_xpath = "//button[contains(concat(' ', normalize-space(@class),' '), ' dp-btn ') and text()='Sign in']"
    login_button = driver.find_element_by_xpath(login_button_xpath)
    login_button.click()
    time.sleep(5)

    driver.get(f'https://dominos.ua/{args.lang}/kyiv/user/history/')

    if args.wait:
        wait = WebDriverWait(driver, 15)
        town_confirm_button_xpath = "//button[contains(concat(' ', normalize-space(@class),' '), ' dp-btn ')]"
        wait.until(EC.visibility_of_element_located((By.XPATH, town_confirm_button_xpath)))
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    else:
        time.sleep(5)

    order_nodes = driver.find_elements_by_xpath("//div[contains(concat(' ', normalize-space(@class),' '), ' tbody ')]")

    orders = []

    for order_node in order_nodes:
        order = {}

        order_id = order_node.find_element_by_class_name('order').text
        date = order_node.find_element_by_class_name('date').text
        price = order_node.find_element_by_class_name('price').text

        item_nodes = order_node.find_elements_by_class_name('order-details-item')

        for item_node in item_nodes:
            count = item_node.find_element_by_class_name('quantity').get_attribute('innerHTML').strip()
            title = item_node.find_element_by_class_name('order-detatils-info__title').\
                get_attribute('innerHTML').strip()
            details = item_node.find_element_by_class_name('order-detatils-info__data').\
                get_attribute('innerHTML').strip()

            orders.append(dict(order_id=order_id, date=date, price=price, count=count, title=title, details=details))

    orders = pd.DataFrame(orders)
    orders.to_csv('dist/dominos_pizza_orders.tsv.gz', sep='\t', compression='gzip')

finally:
    driver.quit()
