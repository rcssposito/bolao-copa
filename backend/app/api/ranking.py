from fastapi import APIRouter, HTTPException
from typing import List
from app.models import RankingUser, RankingResponse
from app.database import supabase
from app.services.scoring import calculate_score_difference

router = APIRouter(prefix="/ranking", tags=["ranking"])


@router.get("/", response_model=RankingResponse)
async def get_ranking():
    """
    Get user ranking with tiebreaker logic.
    Users are sorted by:
    1. Total points (descending)
    2. Closest prediction to last match (ascending difference)
    """
    try:
        # Get all users
        users_response = supabase.table("users").select("*").execute()
        users = users_response.data
        
        # Get last match
        last_match_response = supabase.table("matches").select("*").eq("is_last_match", True).execute()
        last_match = last_match_response.data[0] if last_match_response.data else None
        
        # Calculate tiebreaker for each user
        ranking_users = []
        for user in users:
            diferenca_ultimo_jogo = None
            
            # Calculate difference from last match if available
            if (last_match and 
                last_match.get("placar_casa") is not None and 
                last_match.get("placar_fora") is not None and
                user.get("ultimo_palpite_casa") is not None and
                user.get("ultimo_palpite_fora") is not None):
                
                diferenca_ultimo_jogo = calculate_score_difference(
                    user["ultimo_palpite_casa"],
                    user["ultimo_palpite_fora"],
                    last_match["placar_casa"],
                    last_match["placar_fora"]
                )
            
            ranking_users.append({
                "id": user["id"],
                "nome": user["nome"],
                "pontos_total": user["pontos_total"],
                "ultimo_palpite_casa": user.get("ultimo_palpite_casa"),
                "ultimo_palpite_fora": user.get("ultimo_palpite_fora"),
                "grupo": user.get("grupo"),
                "pagou": user["pagou"],
                "diferenca_ultimo_jogo": diferenca_ultimo_jogo,
                "posicao": 0  # Will be set after sorting
            })
        
        # Sort by points (desc) and then by difference (asc)
        ranking_users.sort(
            key=lambda x: (
                -x["pontos_total"],  # Higher points first
                x["diferenca_ultimo_jogo"] if x["diferenca_ultimo_jogo"] is not None else float('inf')  # Lower difference first
            )
        )
        
        # Assign positions
        for i, user in enumerate(ranking_users, start=1):
            user["posicao"] = i
        
        return {
            "ranking": ranking_users,
            "total_usuarios": len(ranking_users)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/group/{group}", response_model=RankingResponse)
async def get_group_ranking(group: str):
    """Get ranking for a specific group"""
    try:
        # Get users from specific group
        users_response = supabase.table("users").select("*").eq("grupo", group).execute()
        users = users_response.data
        
        # Get last match
        last_match_response = supabase.table("matches").select("*").eq("is_last_match", True).execute()
        last_match = last_match_response.data[0] if last_match_response.data else None
        
        # Calculate tiebreaker for each user
        ranking_users = []
        for user in users:
            diferenca_ultimo_jogo = None
            
            if (last_match and 
                last_match.get("placar_casa") is not None and 
                last_match.get("placar_fora") is not None and
                user.get("ultimo_palpite_casa") is not None and
                user.get("ultimo_palpite_fora") is not None):
                
                diferenca_ultimo_jogo = calculate_score_difference(
                    user["ultimo_palpite_casa"],
                    user["ultimo_palpite_fora"],
                    last_match["placar_casa"],
                    last_match["placar_fora"]
                )
            
            ranking_users.append({
                "id": user["id"],
                "nome": user["nome"],
                "pontos_total": user["pontos_total"],
                "ultimo_palpite_casa": user.get("ultimo_palpite_casa"),
                "ultimo_palpite_fora": user.get("ultimo_palpite_fora"),
                "grupo": user.get("grupo"),
                "pagou": user["pagou"],
                "diferenca_ultimo_jogo": diferenca_ultimo_jogo,
                "posicao": 0
            })
        
        # Sort
        ranking_users.sort(
            key=lambda x: (
                -x["pontos_total"],
                x["diferenca_ultimo_jogo"] if x["diferenca_ultimo_jogo"] is not None else float('inf')
            )
        )
        
        # Assign positions
        for i, user in enumerate(ranking_users, start=1):
            user["posicao"] = i
        
        return {
            "ranking": ranking_users,
            "total_usuarios": len(ranking_users)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Made with Bob
