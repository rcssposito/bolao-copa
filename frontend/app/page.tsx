export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            🏆 Bolão Copa 2026
          </h1>
          <p className="text-xl text-gray-600">
            Sistema de apostas da Copa do Mundo
          </p>
        </header>

        {/* Status Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          {/* Pote Total */}
          <div className="bg-white rounded-lg shadow-lg p-6 border-t-4 border-green-500">
            <div className="text-sm text-gray-600 mb-2">💰 Pote Total</div>
            <div className="text-3xl font-bold text-gray-900">R$ 0,00</div>
            <div className="text-sm text-gray-500 mt-2">0 participantes</div>
          </div>

          {/* Jogos Disponíveis */}
          <div className="bg-white rounded-lg shadow-lg p-6 border-t-4 border-blue-500">
            <div className="text-sm text-gray-600 mb-2">⚽ Jogos Disponíveis</div>
            <div className="text-3xl font-bold text-gray-900">0</div>
            <div className="text-sm text-gray-500 mt-2">Para apostar</div>
          </div>

          {/* Sua Posição */}
          <div className="bg-white rounded-lg shadow-lg p-6 border-t-4 border-purple-500">
            <div className="text-sm text-gray-600 mb-2">🏅 Sua Posição</div>
            <div className="text-3xl font-bold text-gray-900">-</div>
            <div className="text-sm text-gray-500 mt-2">0 pontos</div>
          </div>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Jogos */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">
                ⚽ Jogos Disponíveis
              </h2>
              <div className="text-center py-12 text-gray-500">
                <p className="text-lg mb-2">Nenhum jogo disponível</p>
                <p className="text-sm">
                  Execute a sincronização para buscar os jogos da Copa
                </p>
              </div>
            </div>
          </div>

          {/* Ranking */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">
                🏆 Ranking
              </h2>
              <div className="text-center py-12 text-gray-500">
                <p className="text-lg mb-2">Ranking vazio</p>
                <p className="text-sm">
                  Adicione usuários para começar
                </p>
              </div>
            </div>
          </div>
        </div>


        {/* Footer */}
        <footer className="mt-12 text-center text-gray-600">
          <p className="text-sm">
            Desenvolvido para a Copa do Mundo 2026 🌎⚽
          </p>
        </footer>
      </div>
    </main>
  )
}

// Made with Bob
