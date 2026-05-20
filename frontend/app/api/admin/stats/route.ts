import { NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!
);

/**
 * GET /api/admin/stats
 * Get general statistics (admin only)
 */
export async function GET() {
  try {
    // Count users
    const { data: users, error: usersError } = await supabase
      .from('users')
      .select('id, pagou');

    if (usersError) throw usersError;

    const totalUsers = users.length;
    const paidUsers = users.filter(u => u.pagou).length;

    // Count matches
    const { data: matches, error: matchesError } = await supabase
      .from('matches')
      .select('id, status');

    if (matchesError) throw matchesError;

    const totalMatches = matches.length;
    const finishedMatches = matches.filter(m => m.status === 'FINISHED').length;

    // Count bets
    const { data: bets, error: betsError } = await supabase
      .from('bets')
      .select('id');

    if (betsError) throw betsError;

    const totalBets = bets.length;

    return NextResponse.json({
      total_users: totalUsers,
      paid_users: paidUsers,
      unpaid_users: totalUsers - paidUsers,
      total_matches: totalMatches,
      finished_matches: finishedMatches,
      scheduled_matches: totalMatches - finishedMatches,
      total_bets: totalBets
    });
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    );
  }
}

// Made with Bob
