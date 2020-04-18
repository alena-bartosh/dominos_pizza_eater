#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description='Script that loads data from dominos.ua')
parser.add_argument('--lang', type=str, default='ru', help='Site and data language')
parser.add_argument('-l', '--login', type=str, help='User\'s login or email')
parser.add_argument('-p', '--password', type=str, help='User\'s password')

args = parser.parse_args()

print(args)