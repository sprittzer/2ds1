import sys, os


class Research:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = None
        
    def _validate_file(self) -> None:
        if len(self.data) < 2:
            raise Exception("Too few lines in file")
        
        if len(self.data[0]) != 2 or ('' in self.data[0]):
            raise Exception("Header must have exactly 2 columns")
        
        for line in self.data[1:]:
            if len(line) != 2:
                raise Exception("The string must have exactly 2 values")
            if not (line == ['0', '1'] or line == ['1', '0']):
                raise Exception("The values ​​must be only 0 or 1 and they must be different.")
        
    def file_reader(self) -> str:
        if not os.path.exists(self.file_path):
            raise Exception(f"File {self.file_path} not found")
        
        with open(self.file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        self.data = [line.strip().split(',') for line in text.split('\n')]
        self._validate_file()
        return text
        
        
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 first_constructor.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    obj = Research(file_path)
    try:
        print(obj.file_reader())
    except Exception as e:
        print(f"Error: {e}")