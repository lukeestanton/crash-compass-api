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

def store_series(series_id, category):
    # Fetch metadata
    info = fred.get_series_info(series_id)
    series = Series(
        series_id=series_id,
        name=info.get("title"),
        frequency=info.get("frequency_short"),
        units=info.get("units_short"),
        category=category,
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


SERIES_TO_LOAD = {
    # Labor Market
    "UNRATE": "Labor Market",
    "PAYEMS": "Labor Market",
    "AHETPI": "Labor Market",
    "IC4WSA": "Labor Market",
    
    # Consumers
    "PCE": "Consumers",
    "DSPIC96": "Consumers",
    "CPIAUCSL": "Consumers",
    "CPILFESL": "Consumers",
    "CSCICP03USM665S": "Consumers",
    
    # Financial Conditions
    "FEDFUNDS": "Financial Conditions",
    "GS10": "Financial Conditions",
    "T10Y2Y": "Financial Conditions",
    "DGS10": "Financial Conditions",
    "GS1": "Financial Conditions",
    "AAA10Y": "Financial Conditions",
    "M2REAL": "Financial Conditions",
    "WM2NS": "Financial Conditions",
    
    # Production
    "INDPRO": "Production",
    "IPMAN": "Production",
    "WPSFD49207": "Production",
    
    # Housing
    "HOUST": "Housing",
    "PERMIT": "Housing"
}

for series_id, category in SERIES_TO_LOAD.items():
    try:
        store_series(series_id, category)
    except Exception as e:
        print(f"Failed to store {series_id}: {e}")