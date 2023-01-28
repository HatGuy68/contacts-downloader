from bs4 import BeautifulSoup
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path
import re
import requests

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.absolute() / "static"),
    name="static",
)

def scan_website(url):
    print("Requesting", url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
    }
    html_data = requests.get(url, headers=headers).content
    soup = BeautifulSoup(html_data, 'html.parser')
    raw_html = soup.prettify()
    print("request done")
    print("Parsing")
    numbers = []

    # Case: 1234567890
    numbers += re.findall(r'[>\s]\d{10}\D', raw_html)
    # Case: 12345 67890 or 12345-67890
    numbers += re.findall(r'[>\s]\d{5}[-\.\s]\d{5}\D', raw_html)
    # Case: 123 456 7890 or 123-456-7890
    numbers += re.findall(r'[>\s]\d{3}[-\.\s]\d{3}[-\.\s]\d{4}\D', raw_html)
    # Case: 1234 567 890 or 1234-567-890
    numbers += re.findall(r'[>\s]\+91[-\s]\d{4}[-\.\s]\d{3}[-\.\s]\d{3}\D', raw_html)
    # Case: +911234567890 +91 1234567890
    numbers += re.findall(r'[>\s]\+91[-\s]\d{10}\D', raw_html)
    # Case: +91 12345 67890 or +91-12345-67890
    numbers += re.findall(r'[>\s]\+91[-\s]\d{5}[-\.\s]\d{5}\D', raw_html)
    # Case: +91 123 456 7890 or +91-123-456-7890
    numbers += re.findall(r'[>\s]\+91[-\s]\d{3}[-\.\s]\d{3}[-\.\s]\d{4}\D', raw_html)
    # Case: +91 1234 567 890 or +91-1234-567-890
    numbers += re.findall(r'[>\s]\+91[-\s]\d{4}[-\.\s]\d{3}[-\.\s]\d{3}\D', raw_html)

    for i in range(len(numbers)):
        numbers[i] = numbers[i][1:-2]
        numbers[i] = numbers[i].replace(" ","")
        numbers[i] = numbers[i].replace("-","")

    numbers = list(set(numbers))

    return {"numbers": numbers}

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    url = None
    context = {'request': request, 'url': url}
    return templates.TemplateResponse("index.html", context)

@app.post("/")
def read_root(request: Request, url: str = Form()):
    print(url)
    numbers = scan_website(url)
    print(url, numbers)
    context = {'request': request, 'url': url, 'numbers': numbers}
    return templates.TemplateResponse("index.html", context)