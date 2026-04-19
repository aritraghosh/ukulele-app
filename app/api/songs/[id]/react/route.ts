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

async function getCounts(supabase: ReturnType<typeof getSupabase>, songId: string, voterHash: string) {
  const { data: reactions } = await supabase
    .from('song_reactions')
    .select('reaction, voter_hash')
    .eq('song_id', songId);

  let likes = 0;
  let dislikes = 0;
  let userReaction: 'like' | 'dislike' | null = null;

  for (const r of reactions || []) {
    if (r.reaction === 'like') likes++;
    else if (r.reaction === 'dislike') dislikes++;
    if (r.voter_hash === voterHash) userReaction = r.reaction as 'like' | 'dislike';
  }

  return { likes, dislikes, userReaction };
}

export async function GET(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const url = new URL(request.url);
  const voterId = url.searchParams.get('voterId') || '';
  const headersList = await headers();
  const ip = headersList.get('x-forwarded-for') || '127.0.0.1';
  const voterHash = hashVoter(ip, voterId);
  const supabase = getSupabase();

  const counts = await getCounts(supabase, id, voterHash);
  return Response.json(counts);
}

export async function POST(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const body = await request.json();
  const voterId = body.voterId || '';
  const reaction = body.reaction as 'like' | 'dislike';

  if (!['like', 'dislike'].includes(reaction)) {
    return Response.json({ error: 'Invalid reaction' }, { status: 400 });
  }

  const headersList = await headers();
  const ip = headersList.get('x-forwarded-for') || '127.0.0.1';
  const voterHash = hashVoter(ip, voterId);
  const supabase = getSupabase();

  // Check existing reaction
  const { data: existing } = await supabase
    .from('song_reactions')
    .select('id, reaction')
    .eq('song_id', id)
    .eq('voter_hash', voterHash)
    .single();

  if (existing) {
    if (existing.reaction === reaction) {
      // Toggle off — delete
      await supabase.from('song_reactions').delete().eq('id', existing.id);
    } else {
      // Switch reaction
      await supabase.from('song_reactions').update({ reaction }).eq('id', existing.id);
    }
  } else {
    // New reaction
    await supabase.from('song_reactions').insert({
      song_id: id,
      voter_hash: voterHash,
      reaction,
    });
  }

  const counts = await getCounts(supabase, id, voterHash);
  return Response.json(counts);
}
