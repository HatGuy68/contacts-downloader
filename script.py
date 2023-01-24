import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver


website = input("Enter the website URL: ")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
}
html_data = requests.get(website, headers=headers).content

soup = BeautifulSoup(html_data, 'html.parser')
raw_html = soup.prettify()

# print(raw_html)
print(raw_html)