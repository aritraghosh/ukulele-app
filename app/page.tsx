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
    <main className="max-w-5xl mx-auto px-4 py-8 space-y-6">
      <div>
        <h1 className="text-2xl font-bold mb-1">Song Library</h1>
        <p className="text-muted-foreground text-sm">
          {getAllSongs().length} songs with chords at every level
        </p>
      </div>

      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <Input
          placeholder="Search songs or artists..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="pl-9"
        />
      </div>

      {songs.length === 0 ? (
        <p className="text-muted-foreground text-center py-12">
          No songs found. Try a different search or request a song!
        </p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {songs.map((song) => (
            <SongCard
              key={song.id}
              song={song}
              isFavorite={favorites.includes(song.id)}
            />
          ))}
        </div>
      )}
    </main>
  );
}
