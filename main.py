from fastapi import FastAPI
from routers import expenses, analytics

app = FastAPI(title="Expense Manager API")

# Register Routers
app.include_router(expenses.router, prefix="/expenses", tags=["Expenses"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
