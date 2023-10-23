import requests
from bs4 import BeautifulSoup


def get_page_html(url: str) -> str:
    # get the response object
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Could not fetch content of page {url}. {response.status_code}, {response.reason}")
    
    # return the response object
    return response.text


def strip_html(html: str):
    # parse html content
    soup = BeautifulSoup(html, "html.parser")
 
    for data in soup(['style', 'script']):
        # Remove tags
        data.decompose()
 
    # return data by retrieving the tag content
    return ' '.join(soup.stripped_strings)