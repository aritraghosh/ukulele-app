'use client';

import Link from 'next/link';
import { SongEntry } from '@/types';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Heart } from 'lucide-react';

const ACCENT_COLORS = [
  'from-primary/15 to-chart-5/10',
  'from-chart-2/15 to-chart-4/10',
  'from-accent/20 to-chart-3/10',
  'from-chart-4/15 to-chart-2/10',
  'from-chart-5/15 to-accent/10',
  'from-chart-1/15 to-primary/10',
];

const BORDER_COLORS = [
  'hover:border-primary/40',
  'hover:border-chart-2/40',
  'hover:border-accent/40',
  'hover:border-chart-4/40',
  'hover:border-chart-5/40',
  'hover:border-chart-1/40',
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
      <Card className={`cursor-pointer hover:shadow-xl transition-all duration-300 h-full flex flex-col border-2 border-transparent ${BORDER_COLORS[ci]} hover:-translate-y-1 bg-gradient-to-br ${ACCENT_COLORS[ci]}`}>
        <CardHeader className="pb-2 flex-1">
          <div className="flex items-start justify-between">
            <div>
              <CardTitle className="text-base font-bold">{song.title}</CardTitle>
              <p className="text-sm text-muted-foreground">{song.artist}</p>
            </div>
            {isFavorite && <Heart className="h-4 w-4 fill-primary text-primary" />}
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
