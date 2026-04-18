import { createClient } from '@supabase/supabase-js';
import { headers } from 'next/headers';
import { createHash } from 'crypto';

function getSupabase() {
  return createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY!
  );
}

function hashVoter(ip: string, voterId: string): string {
  return createHash('sha256').update(`${ip}-${voterId}`).digest('hex');
}

export async function POST(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const body = await request.json();
  const voterId = body.voterId || '';
  const headersList = await headers();
  const ip = headersList.get('x-forwarded-for') || '127.0.0.1';
  const voterHash = hashVoter(ip, voterId);
  const supabase = getSupabase();

  // Try to insert vote (unique constraint prevents doubles)
  const { error: voteError } = await supabase
    .from('request_votes')
    .insert({ request_id: id, voter_hash: voterHash });

  if (voteError) {
    if (voteError.code === '23505') {
      return Response.json({ error: 'Already voted' }, { status: 409 });
    }
    return Response.json({ error: voteError.message }, { status: 500 });
  }

  // Increment vote count
  const { error: updateError } = await supabase.rpc('increment_votes', {
    row_id: id,
  });

  if (updateError) {
    // Fallback: manual increment
    const { data: req } = await supabase.from('requests').select('votes').eq('id', id).single();
    if (req) {
      await supabase.from('requests').update({ votes: req.votes + 1 }).eq('id', id);
    }
  }

  return Response.json({ success: true });
}
