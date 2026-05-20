import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!
);

/**
 * GET /api/admin/users/group/[group]
 * Get all users in a specific group (admin only)
 */
export async function GET(
  request: NextRequest,
  { params }: { params: { group: string } }
) {
  try {
    const { data, error } = await supabase
      .from('users')
      .select('*')
      .eq('grupo', params.group)
      .order('nome');

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
