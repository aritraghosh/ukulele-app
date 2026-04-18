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
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
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
      <main className="max-w-5xl mx-auto px-4 py-8">
        <p className="text-muted-foreground">Song not found.</p>
        <Link href="/" className="text-primary underline text-sm mt-2 inline-block">
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
      <Link href="/" className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground">
        <ArrowLeft className="h-4 w-4" />
        Back to library
      </Link>

      <Card>
        <CardHeader>
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div>
              <CardTitle className="text-xl">{song.title}</CardTitle>
              <p className="text-muted-foreground">{song.artist}</p>
            </div>
            <div className="flex items-center gap-2 flex-wrap">
              <LevelSelector value={level} onChange={setLevel} />
              <Button
                variant="outline"
                size="sm"
                onClick={handleFavorite}
              >
                <Heart className={`mr-1 h-4 w-4 ${fav ? 'fill-primary text-primary' : ''}`} />
                {fav ? 'Saved' : 'Save'}
              </Button>
              <Button variant="outline" size="sm" onClick={handleDownload}>
                <Download className="mr-1 h-4 w-4" />
                Download
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-8">
          {/* Chords */}
          <div>
            <h3 className="text-sm font-semibold mb-3 text-muted-foreground uppercase tracking-wide">
              Chords
            </h3>
            <div className="flex flex-wrap gap-4">
              {song.chords.map((chord) => (
                <ChordDiagram key={chord.name} chord={chord} />
              ))}
            </div>
          </div>

          {/* Strumming */}
          <div>
            <h3 className="text-sm font-semibold mb-3 text-muted-foreground uppercase tracking-wide">
              Strumming Pattern
            </h3>
            <StrummingPattern
              pattern={song.strummingPattern}
              description={song.strummingDescription}
            />
          </div>

          {/* Lyrics */}
          <div>
            <h3 className="text-sm font-semibold mb-3 text-muted-foreground uppercase tracking-wide">
              Lyrics & Chords
            </h3>
            <div className="bg-muted/30 rounded-lg p-6">
              <LyricsDisplay lyrics={song.lyrics} />
            </div>
          </div>
        </CardContent>
      </Card>
    </main>
  );
}
