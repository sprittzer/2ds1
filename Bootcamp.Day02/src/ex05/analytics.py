import os
from random import randint


class Research:
    class Calculations:
        def __init__(self, data):
            self.data = data
            
        def counts(self):
            heads, tails = 0, 0
            for h, t in self.data:
                heads += h
                tails += t
            return heads, tails
        
        def fractions(self, heads, tails):
            total = heads + tails
            if total == 0:
                return 0.0, 0.0
            return (heads / total) * 100, (tails / total) * 100
        
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.header = ['head', 'tail']
        self.data = None
        
    def _validate_data(self) -> None:
        if len(self.data) < 2:
            raise Exception("Too few lines in file")
        
        if len(self.header) != 2 or ('' in self.header):
            raise Exception("Header must have exactly 2 columns")
        
        for line in self.data:
            if len(line) != 2:
                raise Exception("The string must have exactly 2 values")
            if not (line == ['0', '1'] or line == ['1', '0']):
                raise Exception("The values ​​must be only 0 or 1 and they must be different.")
            
    def _data_formatting(self) -> None:
        self.data = [list(map(int, line)) for line in self.data]
        
    def file_reader(self, has_header: bool = True):
        if not os.path.exists(self.file_path):
            raise Exception(f"File {self.file_path} not found")
        
        with open(self.file_path, 'r', encoding='utf-8') as f:
            text = f.read()
            
        self.data = [line.strip().split(',') for line in text.split('\n')]
        if has_header:
            self.header = self.data[0]
            self.data = self.data[1:]
            
        self._validate_data()
        self._data_formatting()
        
        return self.data
    

class Analytics(Research.Calculations):
    def predict_random(self, predictions_number):
        predictions = []
        for _ in range(predictions_number):
            prediction = randint(0, 1)
            if prediction == 1:
                predictions.append([1, 0])
            else:
                predictions.append([0, 1])
        return predictions
    
    def predict_last(self):
        if self.data is None:
            return []
        return self.data[-1]
        
    def save_file(self, data: str, file_name: str, file_expansion: str):
        with open(f"{file_name}.{file_expansion}", 'w', encoding='utf-8') as f:
            f.write(data)
            