# 🏦 Mutual Fund Broker

A FastAPI-based mutual fund broker web application that fetches mutual fund data from RapidAPI, stores unique fund families in PostgreSQL, and presents a basic dashboard UI.

---

## 📦 Tech Stack

- **Backend**: FastAPI, HTTPX (async)
- **Database**: PostgreSQL
- **ORM & Migrations**: SQLAlchemy, Alembic
- **Authentication**: JWT (`python-jose`)
- **Frontend**: HTML, CSS, JS (served via FastAPI)
- **Environment Handling**: `python-dotenv`
- **Async DB Driver**: asyncpg

---

## 🧰 Requirements

- Python 3.10+
- PostgreSQL
- pip / pip-tools
- virtualenv (recommended)

---

## 🔧 Project Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/mutual_fund_broker.git
cd mutual_fund_broker

```Create Virtual Environment
python -m venv venv
source venv/bin/activate        # For Linux/macOS
venv\Scripts\activate           # For Windows


```Create Database
CREATE DATABASE mutualfund;


```Install Dependency
pip install -r requirements.txt


```Run Application
uvicorn app.main:app --reload
