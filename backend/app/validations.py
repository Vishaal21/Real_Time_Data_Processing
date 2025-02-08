import json
import logging
from datetime import datetime


class SecurityDictListValidation:
    def __init__(self, security_ohlc_prices_dict_list: list, file_metadata_id: str):
        self.file_metadata_id = file_metadata_id
        self.security_ohlc_prices_dict_list = security_ohlc_prices_dict_list

    def is_security_data_valid(self):
        from celery_files.tasks.process_security_json_data import (
            send_message_to_websocket_queue,
        )

        for index, security_data in enumerate(self.security_ohlc_prices_dict_list):
            validation = Validation(security_data, index)

            validation_result = validation.is_valid()

            if not validation_result["valid"]:
                for error in validation_result["errors"]:
                    send_message_to_websocket_queue.delay(
                        json.dumps({"message": error, "is_valid": False})
                    )

                return

            else:
                security_data["file_metadata_id"] = self.file_metadata_id


class Validation:
    def __init__(self, security_ohlc_prices_dict: dict, index):
        self.security_index = index
        self.security_ohlc_prices_dict = security_ohlc_prices_dict

    def is_valid(self) -> dict:
        validators = [self.is_json, self.validate_date, self.validate_json_data_columns]
        errors = []
        is_valid = True

        for validator in validators:
            v = validator()
            if not v["status"]:
                is_valid = False
                errors.append(v["error"])
                logging.error(
                    f"failed to process security_ohlc_prices_dict at index {self.security_index}, {errors}"
                )

        return {
            "valid": is_valid,
            "errors": errors,
        }

    def validate_json_data_columns(self):
        try:
            # Define the required columns (case-insensitive)
            required_columns = {"date", "open", "high", "low", "close", "volume"}

            # Normalize the keys in the dictionary to lowercase
            actual_columns = {
                key.lower() for key in self.security_ohlc_prices_dict.keys()
            }

            # Find missing columns
            missing_columns = required_columns - actual_columns

            if not missing_columns:
                return {"error": "", "status": True}
            else:
                return {
                    "error": "Json data is not in valid format. Required columns: Date(DD-MM-YYYY), Open(Price), High(Price), Low(Price), Close(Price), Volume",
                    "status": False,
                }

        except Exception as e:
            return {"error": str(e), "status": False}

    def validate_date(self):
        try:
            # check if the date is in format DD-MM-YYYY
            if datetime.strptime(self.security_ohlc_prices_dict["Date"], "%m-%d-%Y"):
                return {"error": "", "status": True}
            else:
                return {"error": "Date is not in valid format", "status": False}

        except Exception as e:
            return {"error": str(e), "status": False}

    def is_json(self):
        try:
            if isinstance(self.security_ohlc_prices_dict, dict):
                return {"error": "", "status": True}
            else:
                return {"error": "Data is not in valid json format", "status": False}
        except Exception as e:
            return {"error": str(e), "status": False}
