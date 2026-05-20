#!/bin/bash
# Script para iniciar o backend no Mac

echo "🚀 Iniciando Bolão Copa Backend..."

# Verificar se está no diretório correto
if [ ! -f "requirements.txt" ]; then
    echo "❌ Erro: Execute este script da pasta backend/"
    exit 1
fi

# Verificar se as dependências estão instaladas
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "📦 Instalando dependências..."
    python3 -m pip install -r requirements.txt
fi

# Iniciar o servidor
echo "✅ Iniciando servidor na porta 8000..."
echo "📝 Documentação: http://localhost:8000/docs"
echo ""

python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Made with Bob
