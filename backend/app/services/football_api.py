import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime
from app.config import get_settings


class FootballDataAPI:
    """Client for Football-Data.org API"""
    
    BASE_URL = "https://api.football-data.org/v4"
    
    def __init__(self):
        self.settings = get_settings()
        self.api_key = self.settings.football_api_key
        self.headers = {"X-Auth-Token": self.api_key}
    
    async def fetch_world_cup_matches(self) -> List[Dict[str, Any]]:
        """
        Fetch all World Cup matches from the API.
        
        Returns:
            List of match dictionaries
        """
        url = f"{self.BASE_URL}/competitions/WC/matches"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                return data.get("matches", [])
            except httpx.HTTPError as e:
                print(f"Error fetching matches: {e}")
                return []
    
    def parse_match_data(self, api_match: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse API match data into our format.
        
        Args:
            api_match: Raw match data from API
        
        Returns:
            Parsed match dictionary
        """
        # Parse match date
        utc_date = api_match.get("utcDate")
        match_date = datetime.fromisoformat(utc_date.replace("Z", "+00:00")) if utc_date else None
        
        # Get team names
        home_team = api_match.get("homeTeam", {}).get("name", "Unknown")
        away_team = api_match.get("awayTeam", {}).get("name", "Unknown")
        
        # Get scores (if match is finished)
        score = api_match.get("score", {})
        full_time = score.get("fullTime", {})
        home_score = full_time.get("home")
        away_score = full_time.get("away")
        
        # Get status
        status = api_match.get("status", "SCHEDULED")
        
        return {
            "id_api": api_match.get("id"),
            "time_casa": home_team,
            "time_fora": away_team,
            "data": match_date,
            "placar_casa": home_score,
            "placar_fora": away_score,
            "status": status
        }
    
    async def get_parsed_matches(self) -> List[Dict[str, Any]]:
        """
        Fetch and parse all World Cup matches.
        
        Returns:
            List of parsed match dictionaries
        """
        raw_matches = await self.fetch_world_cup_matches()
        return [self.parse_match_data(match) for match in raw_matches]


# Singleton instance
football_api = FootballDataAPI()

# Made with Bob
