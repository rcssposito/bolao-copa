from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from app.models import Match
from app.database import supabase

router = APIRouter(prefix="/matches", tags=["matches"])


@router.get("/", response_model=List[Match])
async def get_available_matches():
    """
    Get all matches available for betting.
    Returns matches that are SCHEDULED and haven't started yet.
    """
    try:
        current_time = datetime.utcnow().isoformat()
        response = supabase.table("matches").select("*").eq("status", "SCHEDULED").gte("data", current_time).order("data").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/upcoming", response_model=List[Match])
async def get_upcoming_matches():
    """
    Get all future matches (for visualization only).
    Returns all matches that haven't finished yet.
    """
    try:
        response = supabase.table("matches").select("*").neq("status", "FINISHED").order("data").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/finished", response_model=List[Match])
async def get_finished_matches():
    """Get all finished matches with scores"""
    try:
        response = supabase.table("matches").select("*").eq("status", "FINISHED").order("data", desc=True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{match_id}", response_model=Match)
async def get_match(match_id: str):
    """Get a specific match by ID"""
    try:
        response = supabase.table("matches").select("*").eq("id", match_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Match not found")
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/last/match", response_model=Match)
async def get_last_match():
    """Get the last match of the competition (for tiebreaker)"""
    try:
        response = supabase.table("matches").select("*").eq("is_last_match", True).execute()
        if not response.data:
            # If not marked, get the match with latest date
            response = supabase.table("matches").select("*").order("data", desc=True).limit(1).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="No matches found")
        
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Made with Bob
