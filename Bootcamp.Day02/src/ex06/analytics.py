import os
from random import randint
import logging
import requests


class Research:
    class Calculations:
        def __init__(self, data):
            self.data = data
            logging.debug('Calculations object created')
            
        def counts(self):
            logging.debug('Calculating counts of heads and tails')
            heads, tails = 0, 0
            for h, t in self.data:
                heads += h
                tails += t
            return heads, tails
        
        def fractions(self, heads, tails):
            logging.debug('Calculating fractions of heads and tails')
            total = heads + tails
            if total == 0:
                logging.warning('No data available for fraction calculation')
                return 0.0, 0.0
            return (heads / total) * 100, (tails / total) * 100
        
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.header = ['head', 'tail']
        self.data = None
        logging.debug(f"Research object created with file: {file_path}")
        
    def _validate_data(self) -> None:
        logging.debug("Validating data structure")
        if len(self.data) < 2:
            error = 'Too few lines in file'
            logging.error(error)
            raise Exception(error)
        
        if len(self.header) != 2 or ('' in self.header):
            error = "Header must have exactly 2 columns"
            logging.error(error)
            raise Exception(error)
        
        for line in self.data:
            if len(line) != 2:
                error = 'The string must have exactly 2 values'
                logging.error(error)
                raise Exception(error)
            if not (line == ['0', '1'] or line == ['1', '0']):
                error = 'The values ​​must be only 0 or 1 and they must be different.'
                logging.error(error)
                raise Exception(error)
            
    def _data_formatting(self) -> None:
        logging.debug('Formatting data to integers')
        self.data = [list(map(int, line)) for line in self.data]
        
    def file_reader(self, has_header: bool = True):
        logging.debug(f"Reading file {self.file_path} with header={has_header}")
        if not os.path.exists(self.file_path):
            error = f"File {self.file_path} not found"
            logging.error(error)
            raise Exception(error)
        
        with open(self.file_path, 'r', encoding='utf-8') as f:
            text = f.read()
            
        self.data = [line.strip().split(',') for line in text.split('\n')]
        if has_header:
            self.header = self.data[0]
            self.data = self.data[1:]
            
        self._validate_data()
        self._data_formatting()
        
        return self.data
    
    def send_telegram_message(self, success: bool, webhook_url: str, chat_id: str) -> None:
        try:
            message = 'The report has been successfully created.' if success else "The report hasn't been created due to an error."
            
            logging.debug(f"Sending Telegram message: {message}")
            
            payload = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(webhook_url, data=payload, timeout=10)
            response.raise_for_status()
            
            logging.debug('Telegram message sent successfully')
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to send Telegram message: {e}")
        except Exception as e:
            logging.error(f"Unexpected error while sending Telegram message: {e}")
    

class Analytics(Research.Calculations):
    def __init__(self, data):
        super().__init__(data)
        logging.debug("Analytics object created")
        
    def predict_random(self, predictions_number):
        logging.debug(f"Generating {predictions_number} random predictions")
        predictions = []
        for _ in range(predictions_number):
            prediction = randint(0, 1)
            if prediction == 1:
                predictions.append([1, 0])
            else:
                predictions.append([0, 1])
        return predictions
    
    def predict_last(self):
        logging.debug('Getting last prediction')
        if self.data is None:
            logging.warning('No data available for last prediction')
            return []
        return self.data[-1]
        
    def save_file(self, data: str, file_name: str, file_expansion: str):
        logging.debug(f"Saving data to file {file_name}.{file_expansion}")
        with open(f"{file_name}.{file_expansion}", 'w', encoding='utf-8') as f:
            f.write(data)
        logging.debug('File saved successfully')
            