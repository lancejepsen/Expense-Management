from pydantic import BaseModel

class MonthlyExpense(BaseModel):
    year_month: str
    total_expenses: float
