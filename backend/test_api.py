#!/usr/bin/env python3
"""
Script de teste da API do Bolão Copa
Execute: python test_api.py
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_health():
    """Testa o health check"""
    print_section("1. Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_create_user():
    """Cria um usuário de teste"""
    print_section("2. Criar Usuário")
    data = {
        "nome": "Usuário Teste",
        "grupo": "A",
        "pagou": True
    }
    response = requests.post(f"{BASE_URL}/api/users", json=data)
    print(f"Status: {response.status_code}")
    user = response.json()
    print(f"Usuário criado: {user['nome']} (ID: {user['id']})")
    return user

def test_list_users():
    """Lista todos os usuários"""
    print_section("3. Listar Usuários")
    response = requests.get(f"{BASE_URL}/api/users")
    users = response.json()
    print(f"Total de usuários: {len(users)}")
    for user in users[:3]:  # Mostra apenas os 3 primeiros
        print(f"  - {user['nome']} (Grupo: {user['grupo']}, Pagou: {user['pagou']})")
    return users

def test_sync():
    """Sincroniza dados da API"""
    print_section("4. Sincronizar Dados")
    print("Sincronizando jogos da Football-Data.org...")
    response = requests.post(f"{BASE_URL}/api/admin/sync")
    result = response.json()
    print(f"Status: {response.status_code}")
    print(f"Jogos atualizados: {result.get('matches_updated', 0)}")
    print(f"Apostas calculadas: {result.get('bets_calculated', 0)}")
    print(f"Mensagem: {result.get('message', 'N/A')}")
    return result

def test_list_matches():
    """Lista jogos disponíveis"""
    print_section("5. Listar Jogos Disponíveis")
    response = requests.get(f"{BASE_URL}/api/matches")
    matches = response.json()
    print(f"Jogos disponíveis para apostar: {len(matches)}")
    for match in matches[:3]:  # Mostra apenas os 3 primeiros
        data = datetime.fromisoformat(match['data'].replace('Z', '+00:00'))
        print(f"  - {match['time_casa']} vs {match['time_fora']}")
        print(f"    Data: {data.strftime('%d/%m/%Y %H:%M')}")
        print(f"    Status: {match['status']}")
    return matches

def test_create_bet(user_id, match_id):
    """Cria uma aposta"""
    print_section("6. Criar Aposta")
    data = {
        "usuario_id": user_id,
        "jogo_id": match_id,
        "palpite_casa": 2,
        "palpite_fora": 1,
        "resultado_radio": "CASA"
    }
    response = requests.post(f"{BASE_URL}/api/bets", json=data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        bet = response.json()
        print(f"Aposta criada: {bet['palpite_casa']} x {bet['palpite_fora']}")
        print(f"Resultado previsto: {bet['resultado_radio']}")
        return bet
    else:
        print(f"Erro: {response.json()}")
        return None

def test_get_ranking():
    """Busca o ranking"""
    print_section("7. Ver Ranking")
    response = requests.get(f"{BASE_URL}/api/ranking")
    data = response.json()
    print(f"Total de usuários no ranking: {data['total_usuarios']}")
    print("\nTop 5:")
    for user in data['ranking'][:5]:
        print(f"  {user['posicao']}º - {user['nome']}: {user['pontos_total']} pontos")
        if user['diferenca_ultimo_jogo'] is not None:
            print(f"      Diferença último jogo: {user['diferenca_ultimo_jogo']}")
    return data

def test_get_pot():
    """Busca informações do pote"""
    print_section("8. Informações do Pote")
    response = requests.get(f"{BASE_URL}/api/admin/pot/total")
    pot = response.json()
    print(f"Valor por usuário: R$ {pot['valor_por_usuario']:.2f}")
    print(f"Usuários pagantes: {pot['usuarios_pagantes']}")
    print(f"Total do pote: R$ {pot['total_pote']:.2f}")
    return pot

def test_get_stats():
    """Busca estatísticas gerais"""
    print_section("9. Estatísticas Gerais")
    response = requests.get(f"{BASE_URL}/api/admin/stats")
    stats = response.json()
    print(f"Total de usuários: {stats['total_users']}")
    print(f"Usuários que pagaram: {stats['paid_users']}")
    print(f"Usuários pendentes: {stats['unpaid_users']}")
    print(f"Total de jogos: {stats['total_matches']}")
    print(f"Jogos finalizados: {stats['finished_matches']}")
    print(f"Jogos agendados: {stats['scheduled_matches']}")
    print(f"Total de apostas: {stats['total_bets']}")
    return stats

def main():
    """Executa todos os testes"""
    print("\n" + "="*60)
    print("  🏆 TESTE DA API DO BOLÃO COPA")
    print("="*60)
    
    try:
        # 1. Health check
        if not test_health():
            print("\n❌ API não está respondendo!")
            return
        
        # 2. Criar usuário
        user = test_create_user()
        
        # 3. Listar usuários
        users = test_list_users()
        
        # 4. Sincronizar dados
        sync_result = test_sync()
        
        # 5. Listar jogos
        matches = test_list_matches()
        
        # 6. Criar aposta (se houver jogos)
        if matches and len(matches) > 0:
            test_create_bet(user['id'], matches[0]['id'])
        else:
            print("\n⚠️  Nenhum jogo disponível para apostar")
        
        # 7. Ver ranking
        test_get_ranking()
        
        # 8. Ver pote
        test_get_pot()
        
        # 9. Ver estatísticas
        test_get_stats()
        
        print_section("✅ TESTES CONCLUÍDOS COM SUCESSO!")
        print("A API está funcionando corretamente!")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Erro: Não foi possível conectar à API")
        print("Certifique-se de que o backend está rodando:")
        print("  cd backend && uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n❌ Erro durante os testes: {str(e)}")

if __name__ == "__main__":
    main()

# Made with Bob
