export interface ChordFingering {
  name: string;
  frets: [number, number, number, number]; // G C E A strings
  fingers: [number, number, number, number];
}

export type Level = 'easy' | 'medium' | 'advanced';

export interface Song {
  id: string;
  title: string;
  artist: string;
  level: Level;
  chords: ChordFingering[];
  strummingPattern: string;
  strummingDescription: string;
  lyrics: string;
}

export interface SongEntry {
  id: string;
  title: string;
  artist: string;
  easy: Song;
  medium: Song;
  advanced: Song;
}

export interface SongRequest {
  id: string;
  title: string;
  artist: string;
  votes: number;
  created_at: string;
  hasVoted?: boolean;
}
