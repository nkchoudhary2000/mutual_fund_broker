import httpx
import os
from fastapi import HTTPException
import asyncpg
import httpx


RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")
DATABASE_URL = os.getenv("DATABASE_URL")

BASE_URL = "https://latest-mutual-fund-nav.p.rapidapi.com"

headers = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": RAPIDAPI_HOST
}

CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS fund_families (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);
"""

async def fetch_fund_families():
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        # Ensure table exists
        await conn.execute(CREATE_TABLE_QUERY)

        # Check if fund families already exist
        rows = await conn.fetch("SELECT name FROM fund_families")
        if rows:
            print("Loaded fund families from database.")
            return [row['name'] for row in rows]

        # If not found, fetch from API
        print("Fetching fund families from API...")
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}/latest",
                headers=headers,
                params={"Scheme_Type": "Open"}
            )

            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Failed to fetch schemes")

            mutual_fund_data = [mf['Mutual_Fund_Family'] for mf in response.json()]
            unique_fund_families = list(set(mutual_fund_data))

            # Store them in the database
            await conn.executemany(
                "INSERT INTO fund_families(name) VALUES($1) ON CONFLICT (name) DO NOTHING",
                [(name,) for name in unique_fund_families]
            )

            print("Stored fund families in database.")
            return unique_fund_families

    finally:
        await conn.close()

async def fetch_open_ended_schemes(fund_family: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/search_schemes",
            headers=headers,
            params={"fund_family": fund_family, "scheme_type": "Open Ended Schemes"}
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch schemes")
        return response.json()
