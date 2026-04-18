'use client';

import Link from 'next/link';
import { SongEntry } from '@/types';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Heart } from 'lucide-react';

const ACCENT_COLORS = [
  'from-orange-400/20 to-rose-300/10',
  'from-cyan-400/20 to-teal-300/10',
  'from-amber-300/20 to-yellow-300/10',
  'from-emerald-400/20 to-green-300/10',
  'from-orange-300/20 to-amber-300/10',
  'from-sky-400/20 to-cyan-300/10',
];

const BORDER_COLORS = [
  'hover:border-orange-300',
  'hover:border-cyan-300',
  'hover:border-amber-300',
  'hover:border-emerald-300',
  'hover:border-orange-300',
  'hover:border-sky-300',
];

interface SongCardProps {
  song: SongEntry;
  isFavorite?: boolean;
  colorIndex?: number;
}

export function SongCard({ song, isFavorite, colorIndex = 0 }: SongCardProps) {
  const chordNames = song.easy.chords.map((c) => c.name).join(' · ');
  const ci = colorIndex % ACCENT_COLORS.length;

  return (
    <Link href={`/song/${song.id}`}>
      <Card className={`cursor-pointer hover:shadow-xl transition-all duration-300 h-full border-2 border-transparent ${BORDER_COLORS[ci]} hover:-translate-y-1 bg-gradient-to-br ${ACCENT_COLORS[ci]}`}>
        <CardHeader className="pb-2">
          <div className="flex items-start justify-between">
            <div>
              <CardTitle className="text-base font-bold">{song.title}</CardTitle>
              <p className="text-sm text-muted-foreground">{song.artist}</p>
            </div>
            {isFavorite && <Heart className="h-4 w-4 fill-pink-500 text-pink-500" />}
          </div>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-1.5">
            {song.easy.chords.slice(0, 5).map((c) => (
              <span
                key={c.name}
                className="text-xs px-2 py-0.5 rounded-full bg-primary/10 text-primary font-semibold"
              >
                {c.name}
              </span>
            ))}
          </div>
        </CardContent>
      </Card>
    </Link>
  );
}
