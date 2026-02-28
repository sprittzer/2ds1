class Research:
    def file_reader(self):
        with open('../data.csv', 'r', encoding='utf-8') as f:
            data = f.read()
        return data
        
        
if __name__ == "__main__":
    obj = Research()
    print(obj.file_reader())