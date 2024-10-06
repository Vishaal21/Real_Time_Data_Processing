from pydantic import BaseModel
from datetime import date

class SecurityCreate(BaseModel):
    name: str
    open_price: str
    close_price: str
    high_price: str
    low_price: str
    volume: str
    date: date
    
class FileMetadataCreate(BaseModel):
    file_name: str
    file_path: str
    file_size: str
    file_type: str
    upload_date: date
    is_valid: bool
    validation_message: str
    

    


