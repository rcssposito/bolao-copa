from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from app.models import Bet, BetCreate, BetUpdate
from app.database import supabase
from app.services.scoring import validate_bet_timing

router = APIRouter(prefix="/bets", tags=["bets"])


@router.post("/", response_model=Bet)
async def create_or_update_bet(bet: BetCreate):
    """
    Create or update a bet for a match.
    Users can only bet before the match starts.
    """
    try:
        # Get match to check timing
        match_response = supabase.table("matches").select("*").eq("id", bet.jogo_id).execute()
        if not match_response.data:
            raise HTTPException(status_code=404, detail="Match not found")
        
        match = match_response.data[0]
        match_date = datetime.fromisoformat(match["data"].replace("Z", "+00:00"))
        current_date = datetime.utcnow().replace(tzinfo=match_date.tzinfo)
        
        # Validate timing
        if not validate_bet_timing(match_date, current_date):
            raise HTTPException(status_code=400, detail="Cannot bet after match has started")
        
        # Check if bet already exists
        existing_bet = supabase.table("bets").select("*").eq("usuario_id", bet.usuario_id).eq("jogo_id", bet.jogo_id).execute()
        
        bet_data = {
            "usuario_id": bet.usuario_id,
            "jogo_id": bet.jogo_id,
            "palpite_casa": bet.palpite_casa,
            "palpite_fora": bet.palpite_fora,
            "resultado_radio": bet.resultado_radio
        }
        
        if existing_bet.data:
            # Update existing bet
            response = supabase.table("bets").update(bet_data).eq("id", existing_bet.data[0]["id"]).execute()
        else:
            # Create new bet
            response = supabase.table("bets").insert(bet_data).execute()
        
        # Update user's last bet for tiebreaker
        if match.get("is_last_match"):
            supabase.table("users").update({
                "ultimo_palpite_casa": bet.palpite_casa,
                "ultimo_palpite_fora": bet.palpite_fora
            }).eq("id", bet.usuario_id).execute()
        
        return response.data[0]
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user/{user_id}", response_model=List[Bet])
async def get_user_bets(user_id: str):
    """Get all bets for a specific user"""
    try:
        response = supabase.table("bets").select("*").eq("usuario_id", user_id).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/match/{match_id}", response_model=List[Bet])
async def get_match_bets(match_id: str):
    """Get all bets for a specific match"""
    try:
        response = supabase.table("bets").select("*").eq("jogo_id", match_id).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{bet_id}", response_model=Bet)
async def get_bet(bet_id: str):
    """Get a specific bet by ID"""
    try:
        response = supabase.table("bets").select("*").eq("id", bet_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Bet not found")
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{bet_id}")
async def delete_bet(bet_id: str):
    """Delete a bet (only before match starts)"""
    try:
        # Get bet and match to check timing
        bet_response = supabase.table("bets").select("*, matches(*)").eq("id", bet_id).execute()
        if not bet_response.data:
            raise HTTPException(status_code=404, detail="Bet not found")
        
        bet = bet_response.data[0]
        match = bet.get("matches")
        
        if match:
            match_date = datetime.fromisoformat(match["data"].replace("Z", "+00:00"))
            current_date = datetime.utcnow().replace(tzinfo=match_date.tzinfo)
            
            if not validate_bet_timing(match_date, current_date):
                raise HTTPException(status_code=400, detail="Cannot delete bet after match has started")
        
        supabase.table("bets").delete().eq("id", bet_id).execute()
        return {"message": "Bet deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Made with Bob
