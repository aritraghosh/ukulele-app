'use client';

import { useState, useEffect, useMemo } from 'react';
import { SongEntry } from '@/types';
import { getAllSongs, searchSongs } from '@/lib/songs';
import { getFavorites } from '@/lib/storage';
import { SongCard } from '@/components/SongCard';
import { Input } from '@/components/ui/input';
import { Search } from 'lucide-react';

export default function Home() {
  const [query, setQuery] = useState('');
  const [favorites, setFavorites] = useState<string[]>([]);

  useEffect(() => {
    setFavorites(getFavorites());
  }, []);

  const songs = useMemo(() => searchSongs(query), [query]);

  return (
    <main className="max-w-5xl mx-auto px-4 py-10 space-y-8">
      {/* Hero */}
      <div className="text-center space-y-3">
        <h1 className="text-4xl font-extrabold tracking-tight bg-gradient-to-r from-primary via-chart-5 to-chart-2 bg-clip-text text-transparent">
          Song Library
        </h1>
        <p className="text-muted-foreground text-lg">
          {getAllSongs().length} songs with chords at every level — pick one and start strumming!
        </p>
      </div>

      {/* Search */}
      <div className="relative max-w-lg mx-auto">
        <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
        <Input
          placeholder="Search songs or artists..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="pl-11 py-6 text-base rounded-full border-2 border-border focus:border-primary shadow-sm"
        />
      </div>

      {songs.length === 0 ? (
        <div className="text-center py-16 space-y-2">
          <p className="text-4xl">🎵</p>
          <p className="text-muted-foreground text-lg">
            No songs found. Try a different search or{' '}
            <a href="/requests" className="text-primary font-semibold underline underline-offset-2">
              request a song
            </a>
            !
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {songs.map((song, i) => (
            <SongCard
              key={song.id}
              song={song}
              isFavorite={favorites.includes(song.id)}
              colorIndex={i}
            />
          ))}
        </div>
      )}
    </main>
  );
}
