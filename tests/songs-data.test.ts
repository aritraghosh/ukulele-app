import { describe, it, expect } from 'vitest';
import songsData from '../data/songs.json';
import { SongEntry, ChordFingering } from '../types';

const songs = songsData as SongEntry[];
const LEVELS = ['easy', 'medium', 'advanced'] as const;

describe('Song Data Integrity', () => {
  it('should have at least 25 songs', () => {
    expect(songs.length).toBeGreaterThanOrEqual(25);
  });

  it('every song should have a unique id', () => {
    const ids = songs.map((s) => s.id);
    expect(new Set(ids).size).toBe(ids.length);
  });

  it('every song should have title and artist', () => {
    for (const song of songs) {
      expect(song.title).toBeTruthy();
      expect(song.artist).toBeTruthy();
    }
  });

  it('every song should have all 3 difficulty levels', () => {
    for (const song of songs) {
      for (const level of LEVELS) {
        expect(song[level]).toBeDefined();
        expect(song[level].level).toBe(level);
        expect(song[level].title).toBe(song.title);
        expect(song[level].artist).toBe(song.artist);
      }
    }
  });

  it('every level should have at least 1 chord', () => {
    for (const song of songs) {
      for (const level of LEVELS) {
        expect(song[level].chords.length).toBeGreaterThan(0);
      }
    }
  });

  it('every chord should have valid frets (4 values, -1 to 15)', () => {
    for (const song of songs) {
      for (const level of LEVELS) {
        for (const chord of song[level].chords) {
          expect(chord.frets).toHaveLength(4);
          for (const fret of chord.frets) {
            expect(fret).toBeGreaterThanOrEqual(-1);
            expect(fret).toBeLessThanOrEqual(15);
          }
        }
      }
    }
  });

  it('every chord should have valid fingers (4 values, 0-4)', () => {
    for (const song of songs) {
      for (const level of LEVELS) {
        for (const chord of song[level].chords) {
          expect(chord.fingers).toHaveLength(4);
          for (const finger of chord.fingers) {
            expect(finger).toBeGreaterThanOrEqual(0);
            expect(finger).toBeLessThanOrEqual(4);
          }
        }
      }
    }
  });

  it('every chord should have a name', () => {
    for (const song of songs) {
      for (const level of LEVELS) {
        for (const chord of song[level].chords) {
          expect(chord.name).toBeTruthy();
          expect(typeof chord.name).toBe('string');
        }
      }
    }
  });

  it('every level should have a strumming pattern', () => {
    for (const song of songs) {
      for (const level of LEVELS) {
        expect(song[level].strummingPattern).toBeTruthy();
        // Pattern should only contain valid characters
        const beats = song[level].strummingPattern.trim().split(/\s+/);
        for (const beat of beats) {
          expect(['D', 'U', 'x', '-']).toContain(beat);
        }
      }
    }
  });

  it('every level should have lyrics with chord markers', () => {
    for (const song of songs) {
      for (const level of LEVELS) {
        expect(song[level].lyrics).toBeTruthy();
        expect(song[level].lyrics).toMatch(/\[.+?\]/); // at least one chord marker
      }
    }
  });

  it('advanced should have >= as many chords as easy', () => {
    for (const song of songs) {
      expect(song.advanced.chords.length).toBeGreaterThanOrEqual(
        song.easy.chords.length
      );
    }
  });
});
