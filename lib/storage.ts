const FAVORITES_KEY = 'ukulele-favorites';
const VOTER_KEY = 'ukulele-voter-id';

export function getFavorites(): string[] {
  if (typeof window === 'undefined') return [];
  const data = localStorage.getItem(FAVORITES_KEY);
  return data ? JSON.parse(data) : [];
}

export function toggleFavorite(songId: string): boolean {
  const favs = getFavorites();
  const idx = favs.indexOf(songId);
  if (idx >= 0) {
    favs.splice(idx, 1);
    localStorage.setItem(FAVORITES_KEY, JSON.stringify(favs));
    return false;
  } else {
    favs.push(songId);
    localStorage.setItem(FAVORITES_KEY, JSON.stringify(favs));
    return true;
  }
}

export function isFavorite(songId: string): boolean {
  return getFavorites().includes(songId);
}

export function getVoterId(): string {
  if (typeof window === 'undefined') return '';
  let id = localStorage.getItem(VOTER_KEY);
  if (!id) {
    id = crypto.randomUUID();
    localStorage.setItem(VOTER_KEY, id);
  }
  return id;
}
