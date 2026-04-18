'use client';

import Link from 'next/link';
import { SongEntry } from '@/types';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Heart } from 'lucide-react';

const ACCENT_COLORS = [
  'from-pink-400/20 to-purple-400/10',
  'from-blue-400/20 to-cyan-400/10',
  'from-amber-400/20 to-orange-400/10',
  'from-green-400/20 to-teal-400/10',
  'from-violet-400/20 to-indigo-400/10',
  'from-rose-400/20 to-red-400/10',
];

const BORDER_COLORS = [
  'hover:border-pink-300',
  'hover:border-blue-300',
  'hover:border-amber-300',
  'hover:border-green-300',
  'hover:border-violet-300',
  'hover:border-rose-300',
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
