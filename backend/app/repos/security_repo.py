from sqlalchemy import insert

from app.database import get_db
from app.schemas.db_schemas import Security


def insert_security_ohlc_prices(db, security_ohlc_prices_dict):
    query = insert(Security).values(security_ohlc_prices_dict)
    db.execute(query)
    db.commit()
