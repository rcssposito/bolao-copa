import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!
);

/**
 * GET /api/matches
 * Get all matches available for betting.
 * Returns matches that are SCHEDULED and haven't started yet.
 */
export async function GET(request: NextRequest) {
  try {
    const currentTime = new Date().toISOString();
    const { data, error } = await supabase
      .from('matches')
      .select('*')
      .eq('status', 'SCHEDULED')
      .gte('data', currentTime)
      .order('data');

    if (error) throw error;

    return NextResponse.json(data);
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    );
  }
}

// Made with Bob
