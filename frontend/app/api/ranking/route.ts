import { NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';
import { calculateScoreDifference } from '@/lib/scoring';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!
);

/**
 * GET /api/ranking
 * Get user ranking with tiebreaker logic.
 * Users are sorted by:
 * 1. Total points (descending)
 * 2. Closest prediction to last match (ascending difference)
 */
export async function GET() {
  try {
    // Get all users
    const { data: users, error: usersError } = await supabase
      .from('users')
      .select('*');

    if (usersError) throw usersError;

    // Get last match
    const { data: lastMatchData } = await supabase
      .from('matches')
      .select('*')
      .eq('is_last_match', true)
      .single();

    const lastMatch = lastMatchData || null;

    // Calculate tiebreaker for each user
    const rankingUsers = users.map(user => {
      let diferenca_ultimo_jogo = null;

      // Calculate difference from last match if available
      if (
        lastMatch &&
        lastMatch.placar_casa !== null &&
        lastMatch.placar_fora !== null &&
        user.ultimo_palpite_casa !== null &&
        user.ultimo_palpite_fora !== null
      ) {
        diferenca_ultimo_jogo = calculateScoreDifference(
          user.ultimo_palpite_casa,
          user.ultimo_palpite_fora,
          lastMatch.placar_casa,
          lastMatch.placar_fora
        );
      }

      return {
        id: user.id,
        nome: user.nome,
        pontos_total: user.pontos_total,
        ultimo_palpite_casa: user.ultimo_palpite_casa,
        ultimo_palpite_fora: user.ultimo_palpite_fora,
        grupo: user.grupo,
        pagou: user.pagou,
        diferenca_ultimo_jogo,
        posicao: 0 // Will be set after sorting
      };
    });

    // Sort by points (desc) and then by difference (asc)
    rankingUsers.sort((a, b) => {
      // Higher points first
      if (b.pontos_total !== a.pontos_total) {
        return b.pontos_total - a.pontos_total;
      }
      // Lower difference first (null values go to end)
      const aDiff = a.diferenca_ultimo_jogo ?? Infinity;
      const bDiff = b.diferenca_ultimo_jogo ?? Infinity;
      return aDiff - bDiff;
    });

    // Assign positions
    rankingUsers.forEach((user, index) => {
      user.posicao = index + 1;
    });

    return NextResponse.json({
      ranking: rankingUsers,
      total_usuarios: rankingUsers.length
    });
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    );
  }
}

// Made with Bob
