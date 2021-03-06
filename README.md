# Domino's pizza eater :pizza:
I really like pizza but even more I like data analysis. 
If you feel the same way, automatically extract data about your orders in the Domino's with this script and get the analysis!
[Quick demo.](https://github.com/alena-bartosh/dominos_pizza_eater/blob/master/ipynb/analyzer.ipynb)
 
### Setup
1. Install [Selenium driver](https://selenium-python.readthedocs.io/installation.html)
2. Run commands
```sh
git clone https://github.com/alena-bartosh/dominos_pizza_eater.git && cd dominos_pizza_eater/
python3 -m venv .env
echo 'export PATH=$(pwd)/src:$PATH' >> .env/bin/activate
source .env/bin/activate
pip install -r requirements.txt
python3 -m ipykernel install --user --name=.env
```

### Run
(in the virtual environment)
```sh
extractor.py --login YOUR_LOGIN --password YOUR_PASSWORD
transformer.py
jupyter notebook ./ipynb/analyzer.ipynb
```

### Usage
```
extractor.py --help

usage: extractor.py [-h] [--lang] [-b] [--log-level] -l  -p

Script that extracts data from dominos.ua

optional arguments:
  -h, --help        show this help message and exit
  --lang            site and data language
  -b , --browser    webdriver (chrome by default)
  --log-level       debug/info/warning/error

required arguments:
  -l , --login      user's login or email
  -p , --password   user's password
```

### How it works
[![dominos_pizza_eater](https://img.youtube.com/vi/NGUPQketHSU/0.jpg)](https://youtu.be/NGUPQketHSU)
