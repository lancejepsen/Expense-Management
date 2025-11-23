from db.connection import get_cursor
from utils.logger import logger

def fetch_expenses_for_date(expense_date):
    logger.info(f"Fetching expenses for date: {expense_date}")
    with get_cursor() as cur:
        cur.execute(
            "SELECT * FROM expenses WHERE expense_date = %s",
            (expense_date,),
        )
        return cur.fetchall()


def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert expense")
    with get_cursor(commit=True) as cur:
        cur.execute(
            """INSERT INTO expenses (expense_date, amount, category, notes)
               VALUES (%s, %s, %s, %s)""",
            (expense_date, amount, category, notes),
        )


def delete_expenses_for_date(expense_date):
    logger.info(f"Delete expense for date: {expense_date}")
    with get_cursor(commit=True) as cur:
        cur.execute(
            "DELETE FROM expenses WHERE expense_date = %s",
            (expense_date,),
        )


def fetch_expenses_by_month():
    with get_cursor() as cur:
        sql = (
            "SELECT YEAR(expense_date) AS yr, "
            "MONTH(expense_date) AS mo, "
            "SUM(amount) AS total_expenses "
            "FROM expenses "
            "GROUP BY yr, mo "
            "ORDER BY yr, mo"
        )

        cur.execute(sql)
        rows = cur.fetchall()

        # Convert yr + mo → "YYYY-MM"
        result = []
        for row in rows:
            year = row["yr"]
            month = row["mo"]
            ym = f"{year}-{month:02d}"
            result.append({
                "year_month": ym,
                "total_expenses": row["total_expenses"]
            })

        return result



def fetch_expense_summary(start_date, end_date):
    logger.info("Fetching expense summary")
    with get_cursor() as cur:
        cur.execute("""
            SELECT category, SUM(amount) AS total
            FROM expenses
            WHERE expense_date BETWEEN %s AND %s
            GROUP BY category;
        """, (start_date, end_date))
        return cur.fetchall()
