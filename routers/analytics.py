from fastapi import APIRouter, HTTPException
from schemas.analytics import DateRange
from db.queries import fetch_expense_summary
from utils.logger import logger

router = APIRouter()

@router.post("/summary")
def analytics_summary(date_range: DateRange):
    logger.info("Generating expense summary analytics")

    data = fetch_expense_summary(date_range.start_date, date_range.end_date)
    if not data:
        raise HTTPException(status_code=404, detail="No data found")

    # Compute totals
    total = sum(row["total"] for row in data)

    breakdown = {
        row["category"]: {
            "total": row["total"],
            "percentage": round((row["total"] / total) * 100, 2) if total > 0 else 0,
        }
        for row in data
    }

    return breakdown
