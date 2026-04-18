'use client';

import Link from 'next/link';
import { SongEntry } from '@/types';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Heart } from 'lucide-react';

interface SongCardProps {
  song: SongEntry;
  isFavorite?: boolean;
}

export function SongCard({ song, isFavorite }: SongCardProps) {
  const chordNames = song.easy.chords.map((c) => c.name).join(' · ');

  return (
    <Link href={`/song/${song.id}`}>
      <Card className="cursor-pointer hover:shadow-md transition-shadow h-full">
        <CardHeader className="pb-2">
          <div className="flex items-start justify-between">
            <div>
              <CardTitle className="text-base">{song.title}</CardTitle>
              <p className="text-sm text-muted-foreground">{song.artist}</p>
            </div>
            {isFavorite && <Heart className="h-4 w-4 fill-primary text-primary" />}
          </div>
        </CardHeader>
        <CardContent>
          <p className="text-xs text-muted-foreground">{chordNames}</p>
        </CardContent>
      </Card>
    </Link>
  );
}
