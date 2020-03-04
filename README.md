# TaobaoWebscrapper
TaobaoWebscrapper for internal use

## Procedure of the program
1. input the username to taobao website
1. check are there validation bar
1. if not send UA ( user-agent ) and tf2_password to the website, get that token
1. send the token to website and get the st code address
1. use the st code address to alibaba and apply the token
1. get the login cookie
1. serialize cookie ( if exist cookie ,  check the validation of cookie to get login
1. scraping the data from taobao, get the json file and save to excel

## stepup of the program

**python 3**
```
pip install xlrd
pip install openpyxl
pip install numpy
pip install pandas

git clone
cd TaobaoWebscrapper
python login.py #check the login system is working
python .\taobao_scrapper_extreme.py
```

## Example of Data
Please check the xlsx
