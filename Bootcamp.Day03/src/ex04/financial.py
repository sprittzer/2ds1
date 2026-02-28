from bs4 import BeautifulSoup
import requests
import time
import sys

def main():
    if len(sys.argv) != 3:
        raise Exception("Pass the ticker symbol and the table field as arguments")
    token = sys.argv[1]
    table_field = sys.argv[2]
    
    headers = {
        "accept": "text/html",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.7151.132 Safari/537.36"
    }
    url = f'https://finance.yahoo.com/quote/{token}/financials'
    page = requests.get(url, headers=headers)
    
    if page.status_code != 200:
        raise Exception(f"URL not accessible. The ticker may be incorrect.")
    
    soup = BeautifulSoup(page.text, "html.parser")
    
    article_tag = soup.find('article')
    if not article_tag:
        raise Exception(f"Ticker '{token}' seems to be incorrect")
    
    field = soup.find('div', title=table_field)
    if not field:
        raise Exception(f"Field '{table_field}' not found")
    
    row = field.find_parent('div', class_='row')
    result = tuple(filter(lambda x: x != '', [el.text.strip() for el in row.contents]))

    print(result)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
    