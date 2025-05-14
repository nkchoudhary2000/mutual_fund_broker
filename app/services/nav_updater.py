from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models.investment import Investment
import httpx
import os
import asyncio

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")
BASE_URL = "https://latest-mutual-fund-nav.p.rapidapi.com"

headers = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": RAPIDAPI_HOST
}

async def fetch_latest_nav(scheme_name: str) -> float:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/scheme_nav",
            headers=headers,
            params={"scheme_name": scheme_name}
        )
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and data:
                return float(data[0]["nav"])
    return None  # fallback

def update_navs():
    print("Updating NAVs...")
    db: Session = SessionLocal()
    try:
        investments = db.query(Investment).all()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        for inv in investments:
            new_nav = loop.run_until_complete(fetch_latest_nav(inv.scheme_name))
            if new_nav:
                inv.nav = new_nav
        db.commit()
    except Exception as e:
        print(f"Error in NAV update: {e}")
    finally:
        db.close()

def start_nav_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_navs, "interval", hours=1)
    scheduler.start()
    print("NAV update scheduler started.")
