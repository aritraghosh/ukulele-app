import songsData from '@/data/songs.json';
import { SongEntry, Song, Level } from '@/types';

const songs: SongEntry[] = songsData as SongEntry[];

export function getAllSongs(): SongEntry[] {
  return songs;
}

export function getSongById(id: string): SongEntry | undefined {
  return songs.find((s) => s.id === id);
}

export function getSongAtLevel(entry: SongEntry, level: Level): Song {
  return entry[level];
}

export function searchSongs(query: string): SongEntry[] {
  const q = query.toLowerCase().trim();
  if (!q) return songs;
  return songs.filter(
    (s) =>
      s.title.toLowerCase().includes(q) ||
      s.artist.toLowerCase().includes(q)
  );
}
