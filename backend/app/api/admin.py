from fastapi import APIRouter, HTTPException
from typing import List
from app.models import User, AdminUserUpdate, ConfigUpdate, ConfigItem, PotResponse, SyncResponse
from app.database import supabase
from app.services.sync import full_sync

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=List[User])
async def get_all_users():
    """Get all users with their details (admin only)"""
    try:
        response = supabase.table("users").select("*").order("nome").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/users/{user_id}", response_model=User)
async def update_user_admin(user_id: str, user_update: AdminUserUpdate):
    """Update user group and payment status (admin only)"""
    try:
        update_data = {}
        if user_update.grupo is not None:
            update_data["grupo"] = user_update.grupo
        if user_update.pagou is not None:
            update_data["pagou"] = user_update.pagou
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        response = supabase.table("users").update(update_data).eq("id", user_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="User not found")
        
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/users/group/{group}", response_model=List[User])
async def get_users_by_group(group: str):
    """Get all users in a specific group (admin only)"""
    try:
        response = supabase.table("users").select("*").eq("grupo", group).order("nome").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/config/pot", response_model=ConfigItem)
async def get_pot_config():
    """Get pot value configuration"""
    try:
        response = supabase.table("config").select("*").eq("key", "pot_value").execute()
        if not response.data:
            # Return default if not set
            return {"key": "pot_value", "value": "50", "updated_at": None}
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/config/pot", response_model=ConfigItem)
async def update_pot_config(config: ConfigUpdate):
    """Update pot value configuration (admin only)"""
    try:
        # Check if config exists
        existing = supabase.table("config").select("*").eq("key", "pot_value").execute()
        
        if existing.data:
            # Update existing
            response = supabase.table("config").update({"value": config.value}).eq("key", "pot_value").execute()
        else:
            # Insert new
            response = supabase.table("config").insert({"key": "pot_value", "value": config.value}).execute()
        
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pot/total", response_model=PotResponse)
async def get_pot_total():
    """Calculate total pot value based on users who paid"""
    try:
        # Get pot value
        pot_config = supabase.table("config").select("*").eq("key", "pot_value").execute()
        pot_value = float(pot_config.data[0]["value"]) if pot_config.data else 50.0
        
        # Count users who paid
        users_response = supabase.table("users").select("id").eq("pagou", True).execute()
        usuarios_pagantes = len(users_response.data)
        
        total_pote = pot_value * usuarios_pagantes
        
        return {
            "valor_por_usuario": pot_value,
            "usuarios_pagantes": usuarios_pagantes,
            "total_pote": total_pote
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sync", response_model=SyncResponse)
async def trigger_sync():
    """Manually trigger data synchronization (admin only)"""
    try:
        result = await full_sync()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_stats():
    """Get general statistics (admin only)"""
    try:
        # Count users
        users = supabase.table("users").select("id, pagou").execute()
        total_users = len(users.data)
        paid_users = len([u for u in users.data if u["pagou"]])
        
        # Count matches
        matches = supabase.table("matches").select("id, status").execute()
        total_matches = len(matches.data)
        finished_matches = len([m for m in matches.data if m["status"] == "FINISHED"])
        
        # Count bets
        bets = supabase.table("bets").select("id").execute()
        total_bets = len(bets.data)
        
        return {
            "total_users": total_users,
            "paid_users": paid_users,
            "unpaid_users": total_users - paid_users,
            "total_matches": total_matches,
            "finished_matches": finished_matches,
            "scheduled_matches": total_matches - finished_matches,
            "total_bets": total_bets
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Made with Bob
