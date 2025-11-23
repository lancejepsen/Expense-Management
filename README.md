# Expense Manager — FastAPI + Streamlit + MySQL

A modern, full-stack expense management system built with:

- **FastAPI** backend  
- **Streamlit** frontend  
- **MySQL** database  
- Secure `.env` configuration  
- Modular, production-ready project structure  

---

## 🚀 Features

### Backend (FastAPI)
- Add / update daily expenses
- Fetch daily expenses
- Category analytics (percentage breakdown)
- Monthly expense summary
- Clean router-based architecture
- Secure DB credentials using `.env`

### Frontend (Streamlit)
- Modern UI for entering expenses
- Analytics dashboard
- Monthly bar chart
- Category-level breakdown
- Live API integration

## 📁 Project Structure
your_project/
│
├── main.py
├── .env
├── requirements.txt
│
├── routers/
│ ├── expenses.py
│ └── analytics.py
│
├── db/
│ ├── connection.py
│ └── queries.py
│
├── schemas/
│ ├── expense.py
│ ├── analytics.py
│ └── monthly.py
│
├── utils/
│ └── logger.py
│
└── frontend/
└── app.py

---

## 🔐 Environment Variables (`.env`)

Run MySQL server to get your database info req below.

Create a `.env` file in the project root:

DB_HOST=localhost
DB_USER=[YOUR DB USER ID]
DB_PASSWORD=[YOUR DATABASE PASSWORD]
DB_NAME=[YOUR DATABASE NAME]
DB_PORT=[YOUR DATABASE PORT NUMBER]


**Never commit `.env` to GitHub** — the `.gitignore` already prevents this.

---

## 🛠 Install Dependencies

pip install -r requirements.txt

---

## ▶️ Running the Project

### 1️⃣ Start FastAPI backend

uvicorn main:app --reload

Backend runs at:
http://localhost:8000

Swagger docs:
http://localhost:8000/docs

---

### 2️⃣ Start Streamlit frontend

streamlit run frontend/app.py


Frontend opens in a browser.

---

## 🗄 Database Schema

Expected MySQL table:

```sql
CREATE TABLE expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    expense_date DATE NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    category VARCHAR(255),
    notes VARCHAR(255)
);

---

Author: Created by Lance Jepsen
