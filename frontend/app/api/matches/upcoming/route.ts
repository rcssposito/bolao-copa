import { NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!
);

/**
 * GET /api/matches/upcoming
 * Get all future matches (for visualization only).
 * Returns all matches that haven't finished yet.
 */
export async function GET() {
  try {
    const { data, error } = await supabase
      .from('matches')
      .select('*')
      .neq('status', 'FINISHED')
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
