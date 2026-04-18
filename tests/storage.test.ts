import { describe, it, expect, beforeEach } from 'vitest';

// Mock localStorage
const localStorageMock = (() => {
  let store: Record<string, string> = {};
  return {
    getItem: (key: string) => store[key] || null,
    setItem: (key: string, value: string) => { store[key] = value; },
    removeItem: (key: string) => { delete store[key]; },
    clear: () => { store = {}; },
  };
})();

Object.defineProperty(globalThis, 'localStorage', { value: localStorageMock });

// Mock crypto.randomUUID
Object.defineProperty(globalThis, 'crypto', {
  value: { randomUUID: () => 'test-uuid-1234' },
});

import { getFavorites, toggleFavorite, isFavorite, getVoterId } from '../lib/storage';

describe('Storage - Favorites', () => {
  beforeEach(() => {
    localStorageMock.clear();
  });

  it('returns empty array when no favorites', () => {
    expect(getFavorites()).toEqual([]);
  });

  it('toggleFavorite adds and returns true', () => {
    const result = toggleFavorite('song-1');
    expect(result).toBe(true);
    expect(isFavorite('song-1')).toBe(true);
  });

  it('toggleFavorite removes and returns false', () => {
    toggleFavorite('song-1'); // add
    const result = toggleFavorite('song-1'); // remove
    expect(result).toBe(false);
    expect(isFavorite('song-1')).toBe(false);
  });

  it('manages multiple favorites', () => {
    toggleFavorite('song-1');
    toggleFavorite('song-2');
    toggleFavorite('song-3');
    expect(getFavorites()).toEqual(['song-1', 'song-2', 'song-3']);

    toggleFavorite('song-2'); // remove middle
    expect(getFavorites()).toEqual(['song-1', 'song-3']);
  });
});

describe('Storage - Voter ID', () => {
  beforeEach(() => {
    localStorageMock.clear();
  });

  it('generates a voter ID on first call', () => {
    const id = getVoterId();
    expect(id).toBeTruthy();
  });

  it('returns same ID on subsequent calls', () => {
    const id1 = getVoterId();
    const id2 = getVoterId();
    expect(id1).toBe(id2);
  });
});
