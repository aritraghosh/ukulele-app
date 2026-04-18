'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { Level, Song } from '@/types';
import { getSongById, getSongAtLevel } from '@/lib/songs';
import { toggleFavorite, isFavorite } from '@/lib/storage';
import { ChordDiagram } from '@/components/ChordDiagram';
import { StrummingPattern } from '@/components/StrummingPattern';
import { LyricsDisplay } from '@/components/LyricsDisplay';
import { LevelSelector } from '@/components/LevelSelector';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Heart, Download, ArrowLeft } from 'lucide-react';
import Link from 'next/link';

export default function SongPage() {
  const params = useParams();
  const id = params.id as string;
  const [level, setLevel] = useState<Level>('easy');
  const [fav, setFav] = useState(false);

  const entry = getSongById(id);

  useEffect(() => {
    if (entry) setFav(isFavorite(entry.id));
  }, [entry]);

  if (!entry) {
    return (
      <main className="max-w-5xl mx-auto px-4 py-16 text-center space-y-4">
        <p className="text-5xl">🌺</p>
        <p className="text-muted-foreground text-lg">Song not found.</p>
        <Link href="/" className="text-primary font-semibold underline underline-offset-2">
          Back to library
        </Link>
      </main>
    );
  }

  const song: Song = getSongAtLevel(entry, level);

  function handleFavorite() {
    const result = toggleFavorite(entry!.id);
    setFav(result);
  }

  function handleDownload() {
    const content = [
      `${song.title} - ${song.artist}`,
      `Level: ${song.level}`,
      '',
      `Chords: ${song.chords.map((c) => c.name).join(', ')}`,
      '',
      `Strumming: ${song.strummingPattern}`,
      song.strummingDescription,
      '',
      '--- Lyrics & Chords ---',
      song.lyrics,
    ].join('\n');

    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${song.title} - ${song.artist} (${song.level}).txt`;
    a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <main className="max-w-5xl mx-auto px-4 py-8 space-y-6">
      <Link href="/" className="inline-flex items-center gap-1.5 text-sm text-muted-foreground hover:text-primary transition-colors font-medium">
        <ArrowLeft className="h-4 w-4" />
        Back to library
      </Link>

      {/* Song header */}
      <div className="bg-gradient-to-r from-primary/10 via-chart-5/15 to-accent/30 rounded-2xl p-6 sm:p-8">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-extrabold tracking-tight">{song.title}</h1>
            <p className="text-lg text-muted-foreground">{song.artist}</p>
          </div>
          <div className="flex items-center gap-2 flex-wrap">
            <Button
              variant="outline"
              size="sm"
              onClick={handleFavorite}
              className="rounded-full"
            >
              <Heart className={`mr-1.5 h-4 w-4 ${fav ? 'fill-pink-500 text-pink-500' : ''}`} />
              {fav ? 'Saved' : 'Save'}
            </Button>
            <Button variant="outline" size="sm" onClick={handleDownload} className="rounded-full">
              <Download className="mr-1.5 h-4 w-4" />
              Download
            </Button>
          </div>
        </div>
        <div className="mt-4">
          <LevelSelector value={level} onChange={setLevel} />
        </div>
      </div>

      {/* Chords */}
      <Card className="border-2 overflow-hidden">
        <div className="bg-gradient-to-r from-primary/5 to-transparent px-6 py-3 border-b">
          <h3 className="text-sm font-bold uppercase tracking-wider text-primary">
            🎸 Chords
          </h3>
        </div>
        <CardContent className="pt-6">
          <div className="flex flex-wrap gap-6 justify-center sm:justify-start">
            {song.chords.map((chord) => (
              <ChordDiagram key={chord.name} chord={chord} size={110} />
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Strumming */}
      <Card className="border-2 overflow-hidden">
        <div className="bg-gradient-to-r from-chart-2/10 to-transparent px-6 py-3 border-b">
          <h3 className="text-sm font-bold uppercase tracking-wider text-chart-2">
            🥁 Strumming Pattern
          </h3>
        </div>
        <CardContent className="pt-6">
          <StrummingPattern
            pattern={song.strummingPattern}
            description={song.strummingDescription}
          />
        </CardContent>
      </Card>

      {/* Lyrics */}
      <Card className="border-2 overflow-hidden">
        <div className="bg-gradient-to-r from-chart-3/10 to-transparent px-6 py-3 border-b">
          <h3 className="text-sm font-bold uppercase tracking-wider text-chart-3">
            🎤 Lyrics & Chords
          </h3>
        </div>
        <CardContent className="pt-6">
          <div className="bg-muted/20 rounded-xl p-6 border border-border/50">
            <LyricsDisplay lyrics={song.lyrics} />
          </div>
        </CardContent>
      </Card>
    </main>
  );
}
