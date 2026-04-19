-- Run this in your Supabase SQL Editor

-- Song requests table
create table requests (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  artist text not null,
  votes int default 0,
  created_at timestamptz default now()
);

-- Vote tracking (one vote per voter per request)
create table request_votes (
  id uuid primary key default gen_random_uuid(),
  request_id uuid references requests(id) on delete cascade,
  voter_hash text not null,
  created_at timestamptz default now(),
  unique(request_id, voter_hash)
);

-- Helper function to increment votes
create or replace function increment_votes(row_id uuid)
returns void as $$
begin
  update requests set votes = votes + 1 where id = row_id;
end;
$$ language plpgsql;

-- Enable RLS
alter table requests enable row level security;
alter table request_votes enable row level security;

-- Allow public read/insert on requests
create policy "Anyone can read requests" on requests for select using (true);
create policy "Anyone can insert requests" on requests for insert with check (true);
create policy "Service can update requests" on requests for update using (true);

-- Allow public insert on votes, read for service
create policy "Anyone can insert votes" on request_votes for insert with check (true);
create policy "Anyone can read votes" on request_votes for select using (true);

-- Song reactions table (likes/dislikes per song)
create table song_reactions (
  id uuid primary key default gen_random_uuid(),
  song_id text not null,
  voter_hash text not null,
  reaction text not null check (reaction in ('like', 'dislike')),
  created_at timestamptz default now(),
  unique(song_id, voter_hash)
);

alter table song_reactions enable row level security;
create policy "Anyone can read song_reactions" on song_reactions for select using (true);
create policy "Anyone can insert song_reactions" on song_reactions for insert with check (true);
create policy "Anyone can update song_reactions" on song_reactions for update using (true);
create policy "Anyone can delete song_reactions" on song_reactions for delete using (true);
