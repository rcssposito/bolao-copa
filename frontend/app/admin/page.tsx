'use client';

import { useState, useEffect } from 'react';

interface User {
  id: string;
  nome: string;
  grupo: string | null;
  pagou: boolean;
  pontos_total: number;
  created_at: string;
}

export default function AdminPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [newUserName, setNewUserName] = useState('');
  const [newUserGroup, setNewUserGroup] = useState('');
  const [editingUser, setEditingUser] = useState<string | null>(null);
  const [editGroup, setEditGroup] = useState('');

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    try {
      const response = await fetch('/api/admin/users');
      const data = await response.json();
      setUsers(data);
    } catch (error) {
      console.error('Erro ao carregar usuários:', error);
    } finally {
      setLoading(false);
    }
  };

  const createUser = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newUserName.trim()) return;

    try {
      const response = await fetch('/api/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          nome: newUserName,
          grupo: newUserGroup || null,
          pagou: false
        })
      });

      if (response.ok) {
        setNewUserName('');
        setNewUserGroup('');
        loadUsers();
      }
    } catch (error) {
      console.error('Erro ao criar usuário:', error);
    }
  };

  const togglePaid = async (userId: string, currentStatus: boolean) => {
    try {
      await fetch(`/api/admin/users/${userId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pagou: !currentStatus })
      });
      loadUsers();
    } catch (error) {
      console.error('Erro ao atualizar pagamento:', error);
    }
  };

  const updateGroup = async (userId: string) => {
    try {
      await fetch(`/api/admin/users/${userId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ grupo: editGroup || null })
      });
      setEditingUser(null);
      setEditGroup('');
      loadUsers();
    } catch (error) {
      console.error('Erro ao atualizar grupo:', error);
    }
  };

  const deleteUser = async (userId: string) => {
    if (!confirm('Tem certeza que deseja deletar este usuário?')) return;

    try {
      await fetch(`/api/users/${userId}`, {
        method: 'DELETE'
      });
      loadUsers();
    } catch (error) {
      console.error('Erro ao deletar usuário:', error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-xl text-gray-600">Carregando...</div>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <header className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            ⚙️ Administração
          </h1>
          <p className="text-gray-600">
            Gerencie usuários, grupos e pagamentos
          </p>
        </header>

        {/* Add User Form */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            ➕ Adicionar Usuário
          </h2>
          <form onSubmit={createUser} className="flex gap-4">
            <input
              type="text"
              placeholder="Nome do usuário"
              value={newUserName}
              onChange={(e) => setNewUserName(e.target.value)}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
            <input
              type="text"
              placeholder="Grupo (opcional)"
              value={newUserGroup}
              onChange={(e) => setNewUserGroup(e.target.value)}
              className="w-48 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <button
              type="submit"
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
            >
              Adicionar
            </button>
          </form>
        </div>

        {/* Users List */}
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
            <h2 className="text-2xl font-bold text-gray-900">
              👥 Usuários ({users.length})
            </h2>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Nome
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Grupo
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Pontos
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Pagamento
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Ações
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {users.map((user) => (
                  <tr key={user.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">
                        {user.nome}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {editingUser === user.id ? (
                        <div className="flex gap-2">
                          <input
                            type="text"
                            value={editGroup}
                            onChange={(e) => setEditGroup(e.target.value)}
                            className="px-2 py-1 border border-gray-300 rounded text-sm"
                            placeholder="Grupo"
                          />
                          <button
                            onClick={() => updateGroup(user.id)}
                            className="text-green-600 hover:text-green-800 text-sm"
                          >
                            ✓
                          </button>
                          <button
                            onClick={() => {
                              setEditingUser(null);
                              setEditGroup('');
                            }}
                            className="text-red-600 hover:text-red-800 text-sm"
                          >
                            ✗
                          </button>
                        </div>
                      ) : (
                        <div className="flex items-center gap-2">
                          <span className="text-sm text-gray-900">
                            {user.grupo || '-'}
                          </span>
                          <button
                            onClick={() => {
                              setEditingUser(user.id);
                              setEditGroup(user.grupo || '');
                            }}
                            className="text-blue-600 hover:text-blue-800 text-xs"
                          >
                            ✏️
                          </button>
                        </div>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">
                        {user.pontos_total}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <button
                        onClick={() => togglePaid(user.id, user.pagou)}
                        className={`px-3 py-1 rounded-full text-xs font-medium ${
                          user.pagou
                            ? 'bg-green-100 text-green-800'
                            : 'bg-red-100 text-red-800'
                        }`}
                      >
                        {user.pagou ? '✓ Pago' : '✗ Não Pago'}
                      </button>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <button
                        onClick={() => deleteUser(user.id)}
                        className="text-red-600 hover:text-red-800 font-medium"
                      >
                        🗑️ Deletar
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {users.length === 0 && (
            <div className="text-center py-12 text-gray-500">
              <p className="text-lg">Nenhum usuário cadastrado</p>
              <p className="text-sm mt-2">
                Adicione o primeiro usuário usando o formulário acima
              </p>
            </div>
          )}
        </div>

        {/* Back to Home */}
        <div className="mt-8 text-center">
          <a
            href="/"
            className="inline-block px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors font-medium"
          >
            ← Voltar para Home
          </a>
        </div>
      </div>
    </main>
  );
}

// Made with Bob
