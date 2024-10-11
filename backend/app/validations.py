from datetime import datetime
import logging

class Validation:
    def __init__(self, data):
        self.data = data
        
        
    def is_valid(self, security_ohlc_prices_dict):
        
        validators = [
            self.is_json,
            self.validate_date,
            self.validate_json_data_columns
        ]
        
        errors = []
        is_valid = True

        for validation in validators:
            v = validation(security_ohlc_prices_dict)

            if not v['status']:
                is_valid = False
                errors.append(v['error'])

        logging.info(f"errorssss, {errors}")
        return {
            'valid': is_valid,
            'errors': errors,
        };
        
    def validate_json_data_columns(self, security_ohlc_prices_dict):
        try:
            if "Date" in security_ohlc_prices_dict and "Open" in security_ohlc_prices_dict and "High" in security_ohlc_prices_dict and "Low" in security_ohlc_prices_dict and "Close" in security_ohlc_prices_dict and "Volume" in security_ohlc_prices_dict:
                return {"error": "", "status": True}
            else:
                return {"error": "Json data is not in valid format. Required columns: Date(DD-MM-YYYY), Open(Price), High(Price), Low(Price), Close(Price), Volume", "status": False}
        except Exception as e:
            return {"error": str(e), "status": False}


    def validate_date(self, security_ohlc_prices_dict):
        try:
            # check if the date is in format DD-MM-YYYY
            if datetime.strptime(security_ohlc_prices_dict['Date'], '%m-%d-%Y'):
                return {"error": "", "status": True}
            else:
                return {"error": "Date is not in valid format", "status": False}
            
        except Exception as e:
            return {"error": str(e), "status": False}
        
        
    def is_json(self, data):
        try:
            if isinstance(data, dict):
                return {"error": "", "status": True}
            else:
                return {"error": "Data is not in valid format", "status": False}
        except Exception as e:
            return {"error": str(e), "status": False}
