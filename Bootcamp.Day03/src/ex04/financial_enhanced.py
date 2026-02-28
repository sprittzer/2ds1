from bs4 import BeautifulSoup
import requests
import time
import sys
import urllib3

def main():
    if len(sys.argv) != 3:
        raise Exception("Pass the ticker symbol and the table field as arguments")
    token = sys.argv[1]
    table_field = sys.argv[2]
    
    headers = {
        "accept": "text/html",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.7151.132 Safari/537.36"
    }
    http = urllib3.PoolManager()
    url = f'https://finance.yahoo.com/quote/{token}/financials'
    response = http.request('GET', url, headers=headers)

    if response.status != 200:
        raise Exception(f"URL not accessible. HTTP status: {response.status}")

    page = response.data.decode('utf-8')
    
    soup = BeautifulSoup(page, "html.parser")
    
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
    