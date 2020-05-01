#!/usr/bin/env python3

import argparse
import logging
import time

import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Script that loads data from dominos.ua')
parser.add_argument('--lang', type=str, default='ru', metavar='', help='site and data language')
parser.add_argument('-b', '--browser',  type=str, choices=['chrome', 'firefox'],
                    default='chrome', metavar='', help='webdriver (chrome by default)')
parser.add_argument('--log-level',  type=str, choices=['debug', 'info', 'warning', 'error'],
                    default='debug', metavar='', help='debug/info/warning/error')
required_args = parser.add_argument_group('required arguments')
required_args.add_argument('-l', '--login', type=str, metavar='', help='user\'s login or email', required=True)
required_args.add_argument('-p', '--password', type=str, metavar='', help='user\'s password', required=True)

args = parser.parse_args()

log_level_map = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR
}

logging.basicConfig(format='[%(asctime)s - %(levelname)-8s] %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

logger = logging.getLogger('extractor')
logger.setLevel(log_level_map[args.log_level])

logger.debug('Script is started ...')

driver = webdriver.Chrome() if args.browser == 'chrome' else webdriver.Firefox()
driver.delete_all_cookies()

try:
    main_page_url = 'https://dominos.ua/en/kyiv/'
    driver.get(main_page_url)
    logger.debug(f'Page {main_page_url} has been opened')

    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    logger.debug(f'Esc key has been pressed')

    logger.debug(f'Looking for "Sign in" button ...')
    sign_button = driver.find_element_by_class_name('fake-header__sing-in-block')
    sign_button.click()
    logger.debug(f'"Sign in" button has been clicked')

    logger.debug(f'Looking for login/password inputs ...')
    login_input = driver.find_element_by_name('email')
    password_input = driver.find_element_by_name('password')

    login_input.send_keys(args.login)
    password_input.send_keys(args.password)
    logger.debug(f'Credentials have been set')

    logger.debug(f'Looking for "Sign in" button ...')
    login_button_xpath = "//button[contains(concat(' ', normalize-space(@class),' '), ' dp-btn ') and text()='Sign in']"
    login_button = driver.find_element_by_xpath(login_button_xpath)
    login_button.click()
    logger.debug(f'"Sign in" button has been clicked')
    time.sleep(5)

    history_page_url = f'https://dominos.ua/{args.lang}/kyiv/user/history/'
    driver.get(history_page_url)
    logger.debug(f'Page {history_page_url} has been opened')

    if args.browser == 'chrome':
        logger.debug(f'Waiting for town confirm button ...')
        wait = WebDriverWait(driver, 15)
        town_confirm_button_xpath = "//button[contains(concat(' ', normalize-space(@class),' '), ' dp-btn ')]"
        wait.until(EC.visibility_of_element_located((By.XPATH, town_confirm_button_xpath)))
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        logger.debug(f'Esc key has been pressed')
    else:
        time.sleep(5)

    logger.debug(f'Looking for order nodes...')
    order_nodes = driver.find_elements_by_xpath("//div[contains(concat(' ', normalize-space(@class),' '), ' tbody ')]")

    if len(order_nodes) == 0:
        raise Exception('Zero order nodes!')

    logger.info(f'{len(order_nodes)} order nodes have been found')

    orders = []

    for order_node in tqdm(order_nodes):

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

    logger.info(f'All orders data has been processed')
    orders = pd.DataFrame(orders)
    tsv_path = 'dist/dominos_pizza_orders.tsv.gz'
    orders.to_csv(tsv_path, sep='\t', compression='gzip')
    logger.info(f'Orders data has been saved to {tsv_path}')
except Exception as e:
    logger.exception(e)
finally:
    driver.quit()
    logger.debug('Webdriver has been closed')
