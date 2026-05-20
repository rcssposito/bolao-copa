from datetime import datetime
from typing import List, Dict, Any
from app.database import supabase
from app.services.football_api import football_api
from app.services.scoring import calculate_points, calculate_score_difference


async def sync_matches() -> Dict[str, Any]:
    """
    Sync matches from Football-Data.org API to database.
    Updates existing matches and creates new ones.
    
    Returns:
        Dictionary with sync results
    """
    try:
        # Fetch matches from API
        api_matches = await football_api.get_parsed_matches()
        
        if not api_matches:
            return {
                "success": False,
                "matches_updated": 0,
                "message": "No matches fetched from API"
            }
        
        matches_updated = 0
        
        for match_data in api_matches:
            # Check if match exists
            existing = supabase.table("matches").select("*").eq("id_api", match_data["id_api"]).execute()
            
            if existing.data:
                # Update existing match
                supabase.table("matches").update({
                    "time_casa": match_data["time_casa"],
                    "time_fora": match_data["time_fora"],
                    "data": match_data["data"].isoformat() if match_data["data"] else None,
                    "placar_casa": match_data["placar_casa"],
                    "placar_fora": match_data["placar_fora"],
                    "status": match_data["status"],
                    "updated_at": datetime.utcnow().isoformat()
                }).eq("id_api", match_data["id_api"]).execute()
            else:
                # Insert new match
                supabase.table("matches").insert({
                    "id_api": match_data["id_api"],
                    "time_casa": match_data["time_casa"],
                    "time_fora": match_data["time_fora"],
                    "data": match_data["data"].isoformat() if match_data["data"] else None,
                    "placar_casa": match_data["placar_casa"],
                    "placar_fora": match_data["placar_fora"],
                    "status": match_data["status"]
                }).execute()
            
            matches_updated += 1
        
        return {
            "success": True,
            "matches_updated": matches_updated,
            "message": f"Successfully synced {matches_updated} matches"
        }
    
    except Exception as e:
        return {
            "success": False,
            "matches_updated": 0,
            "message": f"Error syncing matches: {str(e)}"
        }


async def calculate_all_bets() -> int:
    """
    Calculate points for all bets on finished matches.
    Updates bet points and user total points.
    
    Returns:
        Number of bets calculated
    """
    try:
        # Get all finished matches
        finished_matches = supabase.table("matches").select("*").eq("status", "FINISHED").execute()
        
        bets_calculated = 0
        
        for match in finished_matches.data:
            if match["placar_casa"] is None or match["placar_fora"] is None:
                continue
            
            # Get all bets for this match
            bets = supabase.table("bets").select("*").eq("jogo_id", match["id"]).execute()
            
            for bet in bets.data:
                # Calculate points
                points = calculate_points(
                    bet["palpite_casa"],
                    bet["palpite_fora"],
                    match["placar_casa"],
                    match["placar_fora"]
                )
                
                # Update bet points
                supabase.table("bets").update({
                    "pontos": points
                }).eq("id", bet["id"]).execute()
                
                bets_calculated += 1
        
        return bets_calculated
    
    except Exception as e:
        print(f"Error calculating bets: {e}")
        return 0


async def update_user_totals() -> int:
    """
    Update total points for all users by summing their bet points.
    
    Returns:
        Number of users updated
    """
    try:
        # Get all users
        users = supabase.table("users").select("id").execute()
        
        users_updated = 0
        
        for user in users.data:
            # Sum all bet points for this user
            bets = supabase.table("bets").select("pontos").eq("usuario_id", user["id"]).execute()
            
            total_points = sum(bet["pontos"] for bet in bets.data)
            
            # Update user total
            supabase.table("users").update({
                "pontos_total": total_points
            }).eq("id", user["id"]).execute()
            
            users_updated += 1
        
        return users_updated
    
    except Exception as e:
        print(f"Error updating user totals: {e}")
        return 0


async def mark_last_match() -> bool:
    """
    Identify and mark the last match of the competition.
    Used for tiebreaker calculation.
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Reset all matches
        supabase.table("matches").update({"is_last_match": False}).neq("id", "00000000-0000-0000-0000-000000000000").execute()
        
        # Get the match with the latest date
        matches = supabase.table("matches").select("*").order("data", desc=True).limit(1).execute()
        
        if matches.data:
            last_match = matches.data[0]
            supabase.table("matches").update({"is_last_match": True}).eq("id", last_match["id"]).execute()
            return True
        
        return False
    
    except Exception as e:
        print(f"Error marking last match: {e}")
        return False


async def full_sync() -> Dict[str, Any]:
    """
    Perform a complete sync: update matches, calculate bets, update totals, mark last match.
    
    Returns:
        Dictionary with complete sync results
    """
    # Sync matches from API
    match_result = await sync_matches()
    
    if not match_result["success"]:
        return match_result
    
    # Calculate bet points
    bets_calculated = await calculate_all_bets()
    
    # Update user totals
    users_updated = await update_user_totals()
    
    # Mark last match
    await mark_last_match()
    
    return {
        "success": True,
        "matches_updated": match_result["matches_updated"],
        "bets_calculated": bets_calculated,
        "users_updated": users_updated,
        "message": "Full sync completed successfully"
    }

# Made with Bob
