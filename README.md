# Domino's pizza eater :pizza:

### Setup
1. Install [Chrome Selenium driver](https://selenium-python.readthedocs.io/installation.html)
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
```sh
./src/loader.py --help

usage: loader.py [-h] [--lang] [--wait] [-l] [-p]

Script that loads data from dominos.ua

optional arguments:
  -h, --help        show this help message and exit
  --lang            site and data language
  --wait            wait for town confirm popup
  -l , --login      user's login or email
  -p , --password   user's password
```
