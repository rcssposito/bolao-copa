import { NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!
);

/**
 * GET /api/admin/pot
 * Calculate total pot value based on users who paid
 */
export async function GET() {
  try {
    // Get pot value from config
    const { data: potConfig } = await supabase
      .from('config')
      .select('*')
      .eq('key', 'pot_value')
      .single();

    const potValue = potConfig ? parseFloat(potConfig.value) : 50.0;

    // Count users who paid
    const { data: users, error } = await supabase
      .from('users')
      .select('id')
      .eq('pagou', true);

    if (error) throw error;

    const usuariosPagantes = users.length;
    const totalPote = potValue * usuariosPagantes;

    return NextResponse.json({
      valor_por_usuario: potValue,
      usuarios_pagantes: usuariosPagantes,
      total_pote: totalPote
    });
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    );
  }
}

// Made with Bob
