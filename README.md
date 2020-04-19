# Domino's pizza eater :pizza:
I really like pizza but even more I like data analysis. 
If you feel the same way, automatically upload data about your orders in the Domino's with this script and get the analysis!

### Setup
1. Install [Selenium driver](https://selenium-python.readthedocs.io/installation.html)
2. Run commands
```sh
git clone https://github.com/alena-bartosh/dominos_pizza_eater.git && cd dominos_pizza_eater/
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```

### Run
(in the virtual environment)
```sh
./src/loader.py --login YOUR_LOGIN --password YOUR_PASSWORD
```

### Usage
```
./src/loader.py --help

usage: loader.py [-h] [--lang] [-b] [--log-level] [-l] [-p]

Script that loads data from dominos.ua

optional arguments:
  -h, --help        show this help message and exit
  --lang            site and data language
  -b , --browser    webdriver (chrome by default)
  --log-level       debug/info/warning/error
  -l , --login      user's login or email
  -p , --password   user's password
```
