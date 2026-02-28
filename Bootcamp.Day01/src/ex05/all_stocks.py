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
    
    els = list(map(lambda x: x.strip(), sys.argv[1].split(',')))
    if any(el == '' for el in els):
        return
    
    
    for el in els:
        el_f = el.capitalize()
        if el_f in COMPANIES:
            print(f"{el_f} stock price is {STOCKS[COMPANIES[el_f]]}")
            continue
        el_f = el.upper()
        if el_f in COMPANIES_REVERSE:
            print(f"{el_f} is a ticker symbol for {COMPANIES_REVERSE[el_f]}")
        else:
            print(f"{el} is an unknown company or an unknown ticker symbol")

if __name__ == "__main__":
    main()