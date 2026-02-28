import sys


def main():
    COMPANIES = {
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Netflix': 'NFLX',
    'Tesla': 'TSLA',
    'Nokia': 'NOK'
    }

    STOCKS = {
    'AAPL': 287.73,
    'MSFT': 173.79,
    'NFLX': 416.90,
    'TSLA': 724.88,
    'NOK': 3.37
    }
    
    if len(sys.argv) != 2:
        return
    
    comp = sys.argv[1].capitalize()
    if comp in COMPANIES:
        print(STOCKS[COMPANIES[comp]])
    else:
        print("Unknown company")



if __name__ == "__main__":
    main()