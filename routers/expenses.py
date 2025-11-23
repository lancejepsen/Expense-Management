from fastapi import APIRouter, HTTPException
from datetime import date
from typing import List
from schemas.expense import Expense, ExpenseCreate
from schemas.monthly import MonthlyExpense
from db.queries import (
    fetch_expenses_for_date,
    insert_expense,
    delete_expenses_for_date,
    fetch_expenses_by_month,
)
from utils.logger import logger

router = APIRouter()

@router.get("/date/{expense_date}", response_model=List[Expense])
def get_expenses_by_date(expense_date: date):
    logger.info(f"Fetching expenses for date: {expense_date}")
    results = fetch_expenses_for_date(expense_date)
    return results


@router.post("/date/{expense_date}")
def add_or_update_expenses(expense_date: date, expenses: List[ExpenseCreate]):
    logger.info(f"Updating expenses for date: {expense_date}")
    delete_expenses_for_date(expense_date)

    for exp in expenses:
        insert_expense(expense_date, exp.amount, exp.category, exp.notes)

    return {"message": "Expenses updated successfully"}


@router.get("/monthly", response_model=list[MonthlyExpense])
def get_expenses_monthly():
    logger.info("Fetching monthly expense summary")
    return fetch_expenses_by_month()
