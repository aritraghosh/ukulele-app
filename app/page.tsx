'use client';

import { useState, useEffect, useMemo } from 'react';
import { SongEntry } from '@/types';
import { getAllSongs, searchSongs } from '@/lib/songs';
import { getFavorites } from '@/lib/storage';
import { SongCard } from '@/components/SongCard';
import { Input } from '@/components/ui/input';
import { Search, ChevronLeft, ChevronRight } from 'lucide-react';

const PAGE_SIZE = 24;

export default function Home() {
  const [query, setQuery] = useState('');
  const [page, setPage] = useState(1);
  const [favorites, setFavorites] = useState<string[]>([]);

  useEffect(() => {
    setFavorites(getFavorites());
  }, []);

  // Reset to page 1 when search changes
  useEffect(() => {
    setPage(1);
  }, [query]);

  const songs = useMemo(() => searchSongs(query), [query]);
  const totalPages = Math.ceil(songs.length / PAGE_SIZE);
  const paginated = songs.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);

  return (
    <main className="max-w-5xl mx-auto px-4 py-10 space-y-8">
      {/* Hero */}
      <div className="text-center space-y-3">
        <h1 className="text-4xl font-extrabold tracking-tight bg-gradient-to-r from-primary via-chart-5 to-chart-3 bg-clip-text text-transparent">
          🌺 Song Library 🌴
        </h1>
        <p className="text-muted-foreground text-lg">
          {getAllSongs().length} songs with chords at every level — grab your uke and strum along!
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
          <p className="text-4xl">🌺</p>
          <p className="text-muted-foreground text-lg">
            No songs found. Try a different search or{' '}
            <a href="/requests" className="text-primary font-semibold underline underline-offset-2">
              request a song
            </a>
            !
          </p>
        </div>
      ) : (
        <>
          {/* Results count */}
          <div className="flex items-center justify-between text-sm text-muted-foreground">
            <span>
              Showing {(page - 1) * PAGE_SIZE + 1}–{Math.min(page * PAGE_SIZE, songs.length)} of {songs.length} songs
            </span>
            <span>Page {page} of {totalPages}</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {paginated.map((song, i) => (
              <SongCard
                key={song.id}
                song={song}
                isFavorite={favorites.includes(song.id)}
                colorIndex={(page - 1) * PAGE_SIZE + i}
              />
            ))}
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex items-center justify-center gap-2 pt-4">
              <button
                onClick={() => { setPage(p => Math.max(1, p - 1)); window.scrollTo({ top: 0, behavior: 'smooth' }); }}
                disabled={page === 1}
                className="p-2 rounded-full hover:bg-muted disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
              >
                <ChevronLeft className="h-5 w-5" />
              </button>

              {Array.from({ length: totalPages }, (_, i) => i + 1)
                .filter(p => p === 1 || p === totalPages || Math.abs(p - page) <= 2)
                .reduce<(number | 'ellipsis')[]>((acc, p, idx, arr) => {
                  if (idx > 0 && p - (arr[idx - 1]) > 1) acc.push('ellipsis');
                  acc.push(p);
                  return acc;
                }, [])
                .map((item, idx) =>
                  item === 'ellipsis' ? (
                    <span key={`e-${idx}`} className="px-1 text-muted-foreground">...</span>
                  ) : (
                    <button
                      key={item}
                      onClick={() => { setPage(item); window.scrollTo({ top: 0, behavior: 'smooth' }); }}
                      className={`w-10 h-10 rounded-full text-sm font-semibold transition-all ${
                        page === item
                          ? 'bg-primary text-primary-foreground shadow-md'
                          : 'hover:bg-muted text-muted-foreground'
                      }`}
                    >
                      {item}
                    </button>
                  )
                )}

              <button
                onClick={() => { setPage(p => Math.min(totalPages, p + 1)); window.scrollTo({ top: 0, behavior: 'smooth' }); }}
                disabled={page === totalPages}
                className="p-2 rounded-full hover:bg-muted disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
              >
                <ChevronRight className="h-5 w-5" />
              </button>
            </div>
          )}
        </>
      )}
    </main>
  );
}
