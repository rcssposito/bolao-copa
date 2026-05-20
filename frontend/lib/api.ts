import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Types
export interface User {
  id: string
  nome: string
  pontos_total: number
  ultimo_palpite_casa: number | null
  ultimo_palpite_fora: number | null
  grupo: string | null
  pagou: boolean
  created_at: string
}

export interface Match {
  id: string
  id_api: number
  time_casa: string
  time_fora: string
  data: string
  placar_casa: number | null
  placar_fora: number | null
  status: 'SCHEDULED' | 'FINISHED' | 'LIVE' | 'POSTPONED'
  is_last_match: boolean
  created_at: string
  updated_at: string
}

export interface Bet {
  id: string
  usuario_id: string
  jogo_id: string
  palpite_casa: number
  palpite_fora: number
  resultado_radio: 'CASA' | 'EMPATE' | 'FORA'
  pontos: number
  created_at: string
}

export interface RankingUser extends User {
  posicao: number
  diferenca_ultimo_jogo: number | null
}

export interface PotInfo {
  valor_por_usuario: number
  usuarios_pagantes: number
  total_pote: number
}

// API Functions

// Users
export const getUsers = () => api.get<User[]>('/users')
export const getUser = (id: string) => api.get<User>(`/users/${id}`)
export const createUser = (data: Partial<User>) => api.post<User>('/users', data)
export const updateUser = (id: string, data: Partial<User>) => api.put<User>(`/users/${id}`, data)

// Matches
export const getAvailableMatches = () => api.get<Match[]>('/matches')
export const getUpcomingMatches = () => api.get<Match[]>('/matches/upcoming')
export const getFinishedMatches = () => api.get<Match[]>('/matches/finished')
export const getMatch = (id: string) => api.get<Match>(`/matches/${id}`)

// Bets
export const createBet = (data: {
  usuario_id: string
  jogo_id: string
  palpite_casa: number
  palpite_fora: number
  resultado_radio: 'CASA' | 'EMPATE' | 'FORA'
}) => api.post<Bet>('/bets', data)

export const getUserBets = (userId: string) => api.get<Bet[]>(`/bets/user/${userId}`)
export const getMatchBets = (matchId: string) => api.get<Bet[]>(`/bets/match/${matchId}`)

// Ranking
export const getRanking = () => api.get<{ ranking: RankingUser[]; total_usuarios: number }>('/ranking')
export const getGroupRanking = (group: string) => 
  api.get<{ ranking: RankingUser[]; total_usuarios: number }>(`/ranking/group/${group}`)

// Admin
export const getAllUsers = () => api.get<User[]>('/admin/users')
export const updateUserAdmin = (id: string, data: { grupo?: string; pagou?: boolean }) =>
  api.put<User>(`/admin/users/${id}`, data)
export const getUsersByGroup = (group: string) => api.get<User[]>(`/admin/users/group/${group}`)
export const getPotTotal = () => api.get<PotInfo>('/admin/pot/total')
export const updatePotValue = (value: string) => api.put('/admin/config/pot', { value })
export const triggerSync = () => api.post('/admin/sync')
export const getStats = () => api.get('/admin/stats')

export default api

// Made with Bob
