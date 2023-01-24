import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver

def get_mobile_numbers(html):
    numbers = []

    # Case: 1234567890
    numbers += re.findall(r'[>\s]\d{10}\D', html)
    # Case: 12345 67890 or 12345-67890
    numbers += re.findall(r'[>\s]\d{5}[-\.\s]\d{5}\D', html)
    # Case: 123 456 7890 or 123-456-7890
    numbers += re.findall(r'[>\s]\d{3}[-\.\s]\d{3}[-\.\s]\d{4}\D', html)
    # Case: +911234567890 +91 1234567890
    numbers += re.findall(r'[>\s]\+91[-\s]\d{10}\D', html)
    # Case: +91 12345 67890 or +91-12345-67890
    numbers += re.findall(r'[>\s]\+91[-\s]\d{5}[-\.\s]\d{5}\D', html)
    # Case: +91 123 456 7890 or +91-123-456-7890
    numbers += re.findall(r'[>\s]\+91[-\s]\d{3}[-\.\s]\d{3}[-\.\s]\d{4}\D', html)

    for i in range(len(numbers)):
        numbers[i] = numbers[i][1:-2]

    return numbers

website = input("Enter the website URL: ")

opt = int(input(" 1. Requests\n 2. Selenium\n Select a library: "))

if opt == 1:
    # Requests Code
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
    }
    html_data = requests.get(website, headers=headers).content

elif opt == 2:
    # Selenium Code
    driver = webdriver.Chrome()
    driver.get(website)

    html_data = driver.page_source
    driver.close()

soup = BeautifulSoup(html_data, 'html.parser')
raw_html = soup.prettify()

# print(raw_html)
print(get_mobile_numbers(raw_html))