import { NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!
);

/**
 * GET /api/matches/last
 * Get the last match of the competition (for tiebreaker)
 */
export async function GET() {
  try {
    // Try to get match marked as last
    let { data, error } = await supabase
      .from('matches')
      .select('*')
      .eq('is_last_match', true)
      .single();

    // If not found, get the match with latest date
    if (error && error.code === 'PGRST116') {
      const response = await supabase
        .from('matches')
        .select('*')
        .order('data', { ascending: false })
        .limit(1)
        .single();
      
      data = response.data;
      error = response.error;
    }

    if (error) {
      if (error.code === 'PGRST116') {
        return NextResponse.json(
          { error: 'No matches found' },
          { status: 404 }
        );
      }
      throw error;
    }

    return NextResponse.json(data);
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    );
  }
}

// Made with Bob
