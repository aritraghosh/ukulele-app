import { describe, it, expect, beforeEach } from 'vitest';
import { getAllSongs, getSongById, searchSongs, getSongAtLevel } from '../lib/songs';

describe('Song Search & Filter', () => {
  it('getAllSongs returns all songs', () => {
    const songs = getAllSongs();
    expect(songs.length).toBeGreaterThanOrEqual(25);
  });

  it('getSongById returns correct song', () => {
    const songs = getAllSongs();
    const first = songs[0];
    const found = getSongById(first.id);
    expect(found).toBeDefined();
    expect(found!.title).toBe(first.title);
  });

  it('getSongById returns undefined for invalid id', () => {
    expect(getSongById('nonexistent-song-id')).toBeUndefined();
  });

  it('searchSongs finds by title', () => {
    const results = searchSongs('imagine');
    expect(results.length).toBeGreaterThan(0);
    expect(results.some((s) => s.title.toLowerCase().includes('imagine'))).toBe(true);
  });

  it('searchSongs finds by artist', () => {
    const results = searchSongs('beatles');
    expect(results.length).toBeGreaterThan(0);
    expect(results.some((s) => s.artist.toLowerCase().includes('beatles'))).toBe(true);
  });

  it('searchSongs returns all for empty query', () => {
    const all = getAllSongs();
    const results = searchSongs('');
    expect(results.length).toBe(all.length);
  });

  it('searchSongs is case insensitive', () => {
    const r1 = searchSongs('HALLELUJAH');
    const r2 = searchSongs('hallelujah');
    expect(r1.length).toBe(r2.length);
    expect(r1.length).toBeGreaterThan(0);
  });

  it('getSongAtLevel returns correct level', () => {
    const songs = getAllSongs();
    const entry = songs[0];
    const easy = getSongAtLevel(entry, 'easy');
    expect(easy.level).toBe('easy');
    const adv = getSongAtLevel(entry, 'advanced');
    expect(adv.level).toBe('advanced');
  });
});
