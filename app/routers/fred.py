# app/routers/fred.py
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.get_fred_data import get_series_db, get_categories_with_series

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

@router.get("/categories")
def get_categories():
    try:
        return get_categories_with_series()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/dial_score")
def get_dial_score():
    try:
        return 35.8
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))