# Uke Practice

Ukulele chord practice app with a curated library of songs at 3 difficulty levels and community song request voting.

## Tech Stack
- **Next.js 16** (App Router) + **Tailwind CSS** + **shadcn/ui**
- **Supabase** for shared song request voting
- **Static JSON** for pre-built song library (`data/songs.json`)

## Getting Started

```bash
npm install
npm run dev        # http://localhost:3000
```

## Environment Variables

Copy `.env.local.example` or set:

```
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

## Project Structure

```
app/
  page.tsx                 # Home: song library grid with search
  song/[id]/page.tsx       # Song detail: chords, strumming, lyrics
  requests/page.tsx        # Community request board with voting
  api/requests/            # Supabase-backed request/vote API
components/
  ChordDiagram.tsx         # SVG ukulele chord fingering diagrams
  StrummingPattern.tsx     # Visual D/U strumming notation
  LyricsDisplay.tsx        # Lyrics with inline chord markers
  LevelSelector.tsx        # Easy/Medium/Advanced toggle
  SongCard.tsx             # Song grid card
  NavBar.tsx               # Site navigation
data/
  songs.json               # Pre-generated song library
lib/
  songs.ts                 # Song data access (search, filter)
  storage.ts               # localStorage helpers (favorites, voter ID)
  supabase.ts              # Supabase client
scripts/
  seed-songs.ts            # One-time song generation via Claude API
  fill-remaining.ts        # Batch song data population
types/
  index.ts                 # TypeScript interfaces
```

## Testing

```bash
npm test               # Run all tests
npm run test:watch     # Watch mode
```

Tests cover:
- Song data integrity (valid JSON, all fields present, chord fingerings valid)
- Storage utilities (favorites, voter ID)
- Song search/filter logic
- Component rendering

## Adding Songs

Songs live in `data/songs.json`. Each entry has `easy`, `medium`, `advanced` variants with:
- `chords`: array of `{ name, frets: [G,C,E,A], fingers: [0-4] }`
- `strummingPattern`: D/U/x/- notation
- `lyrics`: text with `[ChordName]` inline markers

Run `scripts/fill-remaining.ts` as a template for batch additions.

## Deployment

Deployed on Vercel. Push to `main` triggers auto-deploy.

Supabase setup: run `supabase-setup.sql` in the SQL Editor.
