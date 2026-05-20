import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';
import { validateBetTiming } from '@/lib/scoring';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!
);

/**
 * POST /api/bets
 * Create or update a bet for a match.
 * Users can only bet before the match starts.
 */
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { usuario_id, jogo_id, palpite_casa, palpite_fora, resultado_radio } = body;

    // Get match to check timing
    const { data: match, error: matchError } = await supabase
      .from('matches')
      .select('*')
      .eq('id', jogo_id)
      .single();

    if (matchError || !match) {
      return NextResponse.json(
        { error: 'Match not found' },
        { status: 404 }
      );
    }

    const matchDate = new Date(match.data);
    const currentDate = new Date();

    // Validate timing
    if (!validateBetTiming(matchDate, currentDate)) {
      return NextResponse.json(
        { error: 'Cannot bet after match has started' },
        { status: 400 }
      );
    }

    // Check if bet already exists
    const { data: existingBet } = await supabase
      .from('bets')
      .select('*')
      .eq('usuario_id', usuario_id)
      .eq('jogo_id', jogo_id)
      .single();

    const betData = {
      usuario_id,
      jogo_id,
      palpite_casa,
      palpite_fora,
      resultado_radio
    };

    let result;
    if (existingBet) {
      // Update existing bet
      const { data, error } = await supabase
        .from('bets')
        .update(betData)
        .eq('id', existingBet.id)
        .select()
        .single();
      
      if (error) throw error;
      result = data;
    } else {
      // Create new bet
      const { data, error } = await supabase
        .from('bets')
        .insert(betData)
        .select()
        .single();
      
      if (error) throw error;
      result = data;
    }

    // Update user's last bet for tiebreaker
    if (match.is_last_match) {
      await supabase
        .from('users')
        .update({
          ultimo_palpite_casa: palpite_casa,
          ultimo_palpite_fora: palpite_fora
        })
        .eq('id', usuario_id);
    }

    return NextResponse.json(result);
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    );
  }
}

// Made with Bob
