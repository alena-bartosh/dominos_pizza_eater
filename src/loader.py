#!/usr/bin/env python3

import argparse
from selenium import webdriver

parser = argparse.ArgumentParser(description='Script that loads data from dominos.ua')
parser.add_argument('--lang', type=str, default='ru', help='Site and data language')
parser.add_argument('-l', '--login', type=str, help='User\'s login or email')
parser.add_argument('-p', '--password', type=str, help='User\'s password')
parser.add_argument('-n', '--no-close', action='store_true')

args = parser.parse_args()

driver = webdriver.Chrome()
driver.get(f'https://dominos.ua/{args.lang}/kyiv/')

if not args.no_close:
    driver.close()
