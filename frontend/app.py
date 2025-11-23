import streamlit as st
from datetime import datetime
import requests
import pandas as pd

API_URL = "http://localhost:8000"

st.title("Expense Management System")

# Custom CSS
st.markdown("""
<style>
.stDateInput > div > div {
    width: 150px !important;
}
</style>
""", unsafe_allow_html=True)

categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

tab1, tab2, tab3 = st.tabs(["Add/Update Expenses", "Analytics By Category", "Analytics By Month"])


# =====================================================
# TAB 1: ADD / UPDATE EXPENSES FOR A DATE
# =====================================================
with tab1:

    selected_date = st.date_input(
        "Enter Date:",
        datetime(2024, 8, 1),
        label_visibility="collapsed"
    )
    date_str = selected_date.strftime("%Y-%m-%d")

    # GET existing expenses for this date
    response = requests.get(f"{API_URL}/expenses/date/{date_str}")
    existing_expenses = response.json() if response.status_code == 200 else []

    key_prefix = date_str.replace("-", "")

    with st.form("expense_form"):
        col1, col2, col3 = st.columns(3)
        col1.markdown("**Amount**")
        col2.markdown("**Category**")
        col3.markdown("**Notes**")

        expenses = []

        for i in range(5):
            # Pre-fill existing data
            if i < len(existing_expenses):
                amount = existing_expenses[i]["amount"]
                category = existing_expenses[i]["category"]
                notes = existing_expenses[i]["notes"]
            else:
                amount = 0.0
                category = "Other"
                notes = ""

            c1, c2, c3 = st.columns(3)

            amount_input = c1.number_input(
                "Amount",
                min_value=0.0,
                value=float(amount),
                key=f"amount_{i}_{key_prefix}",
                label_visibility="collapsed"
            )

            category_input = c2.selectbox(
                "Category",
                categories,
                index=categories.index(category),
                key=f"category_{i}_{key_prefix}",
                label_visibility="collapsed"
            )

            notes_input = c3.text_input(
                "Notes",
                value=notes,
                key=f"notes_{i}_{key_prefix}",
                label_visibility="collapsed"
            )

            expenses.append({
                "amount": amount_input,
                "category": category_input,
                "notes": notes_input
            })

        submit_button = st.form_submit_button("Save Expenses")

        if submit_button:
            filtered = [exp for exp in expenses if exp["amount"] > 0]

            post_response = requests.post(
                f"{API_URL}/expenses/date/{date_str}",
                json=filtered
            )

            if post_response.status_code == 200:
                st.success("Expenses updated successfully")
            else:
                st.error(f"Failed to update expenses: {post_response.text}")


# =====================================================
# TAB 2: ANALYTICS — CATEGORY BREAKDOWN
# =====================================================
with tab2:

    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input("Start Date", datetime(2024, 8, 1))
    with col2:
        end_date = st.date_input("End Date", datetime(2024, 8, 5))

    if st.button("Get Analytics"):

        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }

        response = requests.post(f"{API_URL}/analytics/summary", json=payload)

        if response.status_code != 200:
            st.error(f"Error: {response.text}")
        else:
            result = response.json()

            df = pd.DataFrame({
                "Category": list(result.keys()),
                "Total": [result[c]["total"] for c in result],
                "Percentage": [result[c]["percentage"] for c in result]
            })

            df_sorted = df.sort_values(by="Percentage", ascending=False)

            st.subheader("Expense Breakdown by Category")
            st.bar_chart(df_sorted.set_index("Category")["Percentage"])

            df_sorted["Percentage"] = df_sorted["Percentage"].apply(lambda x: f"{x:.2f}%")
            st.table(df_sorted)


# =====================================================
# TAB 3: ANALYTICS — MONTHLY SUMMARY
# =====================================================
with tab3:
    st.subheader("Expense Breakdown by Month")

    response = requests.get(f"{API_URL}/expenses/monthly")

    if response.status_code != 200:
        st.error(f"Status: {response.status_code}, Error: {response.text}")
    else:
        df = pd.DataFrame(response.json())

        if "year_month" in df.columns:
            # Bar chart first
            st.bar_chart(df.set_index("year_month")["total_expenses"])

        # Then the table below it
        st.dataframe(df)
