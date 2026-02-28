class Must_Read:
    with open('../data.csv', 'r', encoding='utf-8') as f:
        data = f.read()
    print(data)
        
        
if __name__ == "__main__":
    Must_Read()