from pydantic import BaseModel
from datetime import date

class DateRange(BaseModel):
    start_date: date
    end_date: date
