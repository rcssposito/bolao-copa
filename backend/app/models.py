from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class MatchStatus(str, Enum):
    """Match status enum"""
    SCHEDULED = "SCHEDULED"
    FINISHED = "FINISHED"
    LIVE = "LIVE"
    POSTPONED = "POSTPONED"


class ResultadoRadio(str, Enum):
    """Bet result radio options"""
    CASA = "CASA"
    EMPATE = "EMPATE"
    FORA = "FORA"


# User Models
class UserBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100)
    grupo: Optional[str] = Field(None, max_length=50)
    pagou: bool = False


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=1, max_length=100)
    grupo: Optional[str] = Field(None, max_length=50)
    pagou: Optional[bool] = None


class User(UserBase):
    id: str
    pontos_total: int = 0
    ultimo_palpite_casa: Optional[int] = None
    ultimo_palpite_fora: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Match Models
class MatchBase(BaseModel):
    id_api: int
    time_casa: str = Field(..., max_length=100)
    time_fora: str = Field(..., max_length=100)
    data: datetime
    status: MatchStatus = MatchStatus.SCHEDULED


class MatchCreate(MatchBase):
    pass


class MatchUpdate(BaseModel):
    placar_casa: Optional[int] = None
    placar_fora: Optional[int] = None
    status: Optional[MatchStatus] = None
    is_last_match: Optional[bool] = None


class Match(MatchBase):
    id: str
    placar_casa: Optional[int] = None
    placar_fora: Optional[int] = None
    is_last_match: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Bet Models
class BetBase(BaseModel):
    palpite_casa: int = Field(..., ge=0)
    palpite_fora: int = Field(..., ge=0)
    resultado_radio: ResultadoRadio


class BetCreate(BetBase):
    usuario_id: str
    jogo_id: str


class BetUpdate(BetBase):
    pass


class Bet(BetBase):
    id: str
    usuario_id: str
    jogo_id: str
    pontos: int = 0
    created_at: datetime

    class Config:
        from_attributes = True


# Config Models
class ConfigItem(BaseModel):
    key: str
    value: str
    updated_at: datetime


class ConfigUpdate(BaseModel):
    value: str


# Ranking Models
class RankingUser(BaseModel):
    id: str
    nome: str
    pontos_total: int
    ultimo_palpite_casa: Optional[int]
    ultimo_palpite_fora: Optional[int]
    grupo: Optional[str]
    pagou: bool
    posicao: int
    diferenca_ultimo_jogo: Optional[float] = None


class RankingResponse(BaseModel):
    ranking: list[RankingUser]
    total_usuarios: int


# Pot Models
class PotResponse(BaseModel):
    valor_por_usuario: float
    usuarios_pagantes: int
    total_pote: float


# Admin Models
class AdminUserUpdate(BaseModel):
    grupo: Optional[str] = None
    pagou: Optional[bool] = None


# Sync Response
class SyncResponse(BaseModel):
    success: bool
    matches_updated: int
    bets_calculated: int
    message: str

# Made with Bob
