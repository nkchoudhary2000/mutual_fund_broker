from fastapi import APIRouter, Depends, HTTPException
from app.services import mutual_fund
from app.core.security import get_current_user
from app.db.models.user import User

router = APIRouter(prefix="/funds", tags=["Mutual Funds"])

@router.get("/families")
async def get_fund_families(current_user: User = Depends(get_current_user)):
    """
    Get list of mutual fund families from RapidAPI.
    Protected by JWT.
    """
    try:
        print("Fetching fund families...")
        return await mutual_fund.fetch_fund_families()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/schemes")
async def get_schemes(fund_family: str, current_user: User = Depends(get_current_user)):
    """
    Get schemes for a specific fund family.
    Protected by JWT.
    """
    try:
        return await mutual_fund.fetch_open_ended_schemes(fund_family)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
