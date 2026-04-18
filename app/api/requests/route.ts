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

export async function GET(request: Request) {
  const url = new URL(request.url);
  const voterId = url.searchParams.get('voterId') || '';
  const headersList = await headers();
  const ip = headersList.get('x-forwarded-for') || '127.0.0.1';
  const voterHash = hashVoter(ip, voterId);
  const supabase = getSupabase();

  const { data: requests, error } = await supabase
    .from('requests')
    .select('*')
    .order('votes', { ascending: false });

  if (error) {
    return Response.json({ error: error.message }, { status: 500 });
  }

  // Check which ones this voter has voted on
  const { data: votes } = await supabase
    .from('request_votes')
    .select('request_id')
    .eq('voter_hash', voterHash);

  const votedIds = new Set((votes || []).map((v: { request_id: string }) => v.request_id));

  const result = (requests || []).map((r: { id: string; title: string; artist: string; votes: number; created_at: string }) => ({
    ...r,
    hasVoted: votedIds.has(r.id),
  }));

  return Response.json(result);
}

export async function POST(request: Request) {
  const body = await request.json();

  if (!body.title?.trim() || !body.artist?.trim()) {
    return Response.json({ error: 'Title and artist required' }, { status: 400 });
  }

  const supabase = getSupabase();

  const { data, error } = await supabase
    .from('requests')
    .insert({ title: body.title.trim(), artist: body.artist.trim() })
    .select()
    .single();

  if (error) {
    return Response.json({ error: error.message }, { status: 500 });
  }

  return Response.json(data);
}
