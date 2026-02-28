import sys


def main():
    COMPANIES = {
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Netflix': 'NFLX',
    'Tesla': 'TSLA',
    'Nokia': 'NOK'
    }
    
    COMPANIES_REVERSE = {v: k for k, v in COMPANIES.items()}

    STOCKS = {
    'AAPL': 287.73,
    'MSFT': 173.79,
    'NFLX': 416.90,
    'TSLA': 724.88,
    'NOK': 3.37
    }
    
    if len(sys.argv) != 2:
        return
    
    ticker = sys.argv[1].upper()
    if ticker in STOCKS:
        print(f'{COMPANIES_REVERSE[ticker]} {STOCKS[ticker]}')
    else:
        print("Unknown ticker")


if __name__ == "__main__":
    main()