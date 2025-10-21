# scripts/fetch_and_store
import os
from datetime import date
from dotenv import load_dotenv
from fredapi import Fred

from app.db.session import SessionLocal
from app.db.models import Series, Observation

load_dotenv()
fred = Fred(api_key=os.environ["FRED_API_KEY"])
session = SessionLocal()

def store_series(series_id):
    # Fetch metadata
    info = fred.get_series_info(series_id)
    series = Series(
        series_id=series_id,
        name=info.get("title"),
        frequency=info.get("frequency_short"),
        units=info.get("units_short"),
        updated_at=date.today()
    )
    session.merge(series)

    # Remove old observations for this series
    session.query(Observation).filter_by(series_id=series_id).delete()

    # Fetch data
    data = fred.get_series(series_id)
    for d, v in data.items():
        if v is not None:
            obs = Observation(series_id=series_id, date=d.date(), value=float(v))
            session.add(obs)

    session.commit()
    print(f"Stored {series_id}: {len(data)} rows")

# Series to store on script run
SERIES_TO_LOAD = ["UNRATE", "CPIAUCSL", "T10Y2Y", "AHETPI", "PERMIT", "FEDFUNDS"]

for series_id in SERIES_TO_LOAD:
    try:
        store_series(series_id)
    except Exception as e:
        print(f"Failed to store {series_id}: {e}")