# app/routers/fred.py
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.get_fred_data import get_series_db

router = APIRouter(prefix="/api/v1/fred", tags=["FRED"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/series/{series_id}")
def series(series_id: str, start: str = None, end: str = None, db: Session = Depends(get_db)):
    try:
        data = get_series_db(series_id=series_id, start=start, end=end, session=db)
        return data
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))