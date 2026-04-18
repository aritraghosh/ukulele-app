import * as fs from 'fs';
import * as path from 'path';

// Song generator helper - creates song data from a list of songs
// Each batch should call this with their songs and a unique batch number

interface SongInput {
  title: string;
  artist: string;
}

interface ChordData {
  name: string;
  frets: [number, number, number, number];
  fingers: [number, number, number, number];
}

// Common ukulele chord library for GCEA tuning
const CHORD_DB: Record<string, ChordData> = {
  // Major
  'C':     { name: 'C',     frets: [0,0,0,3], fingers: [0,0,0,3] },
  'D':     { name: 'D',     frets: [2,2,2,0], fingers: [1,2,3,0] },
  'E':     { name: 'E',     frets: [4,4,4,2], fingers: [2,3,4,1] },
  'F':     { name: 'F',     frets: [2,0,1,0], fingers: [2,0,1,0] },
  'G':     { name: 'G',     frets: [0,2,3,2], fingers: [0,1,3,2] },
  'A':     { name: 'A',     frets: [2,1,0,0], fingers: [2,1,0,0] },
  'Bb':    { name: 'Bb',    frets: [3,2,1,1], fingers: [3,2,1,1] },
  'B':     { name: 'B',     frets: [4,3,2,2], fingers: [3,2,1,1] },
  'Eb':    { name: 'Eb',    frets: [0,3,3,1], fingers: [0,2,3,1] },
  'Ab':    { name: 'Ab',    frets: [5,3,4,3], fingers: [3,1,2,1] },
  // Minor
  'Am':    { name: 'Am',    frets: [2,0,0,0], fingers: [1,0,0,0] },
  'Bm':    { name: 'Bm',    frets: [4,2,2,2], fingers: [3,1,1,1] },
  'Cm':    { name: 'Cm',    frets: [0,3,3,3], fingers: [0,1,2,3] },
  'Dm':    { name: 'Dm',    frets: [2,2,1,0], fingers: [2,3,1,0] },
  'Em':    { name: 'Em',    frets: [0,4,3,2], fingers: [0,3,2,1] },
  'Fm':    { name: 'Fm',    frets: [1,0,1,3], fingers: [1,0,2,4] },
  'Gm':    { name: 'Gm',    frets: [0,2,3,1], fingers: [0,2,3,1] },
  'F#m':   { name: 'F#m',   frets: [2,1,2,0], fingers: [2,1,3,0] },
  'C#m':   { name: 'C#m',   frets: [1,4,4,4], fingers: [1,2,3,4] },
  'Bbm':   { name: 'Bbm',   frets: [3,1,1,1], fingers: [3,1,1,1] },
  // 7th
  'A7':    { name: 'A7',    frets: [0,1,0,0], fingers: [0,1,0,0] },
  'B7':    { name: 'B7',    frets: [2,3,2,0], fingers: [1,2,3,0] },
  'C7':    { name: 'C7',    frets: [0,0,0,1], fingers: [0,0,0,1] },
  'D7':    { name: 'D7',    frets: [2,2,2,3], fingers: [1,2,3,4] },
  'E7':    { name: 'E7',    frets: [1,2,0,2], fingers: [1,2,0,3] },
  'F7':    { name: 'F7',    frets: [2,3,1,3], fingers: [1,3,0,4] },
  'G7':    { name: 'G7',    frets: [0,2,1,2], fingers: [0,2,1,3] },
  // Minor 7th
  'Am7':   { name: 'Am7',   frets: [0,0,0,0], fingers: [0,0,0,0] },
  'Bm7':   { name: 'Bm7',  frets: [2,2,2,2], fingers: [1,1,1,1] },
  'Cm7':   { name: 'Cm7',  frets: [3,3,3,3], fingers: [1,1,1,1] },
  'Dm7':   { name: 'Dm7',  frets: [2,2,1,3], fingers: [1,2,0,3] },
  'Em7':   { name: 'Em7',  frets: [0,2,0,2], fingers: [0,1,0,2] },
  'F#m7':  { name: 'F#m7', frets: [2,4,2,4], fingers: [1,3,1,4] },
  'Gm7':   { name: 'Gm7',  frets: [0,2,1,1], fingers: [0,3,1,2] },
  // Maj7
  'Cmaj7': { name: 'Cmaj7', frets: [0,0,0,2], fingers: [0,0,0,2] },
  'Fmaj7': { name: 'Fmaj7', frets: [2,4,1,3], fingers: [1,3,0,2] },
  'Gmaj7': { name: 'Gmaj7', frets: [0,2,2,2], fingers: [0,1,2,3] },
  // Sus/Add
  'Dsus4': { name: 'Dsus4', frets: [2,2,0,0], fingers: [1,2,0,0] },
  'Dsus2': { name: 'Dsus2', frets: [2,2,0,0], fingers: [1,2,0,0] },
  'Asus4': { name: 'Asus4', frets: [2,2,0,0], fingers: [1,2,0,0] },
  'Gsus4': { name: 'Gsus4', frets: [0,2,3,3], fingers: [0,1,2,3] },
  // Extended
  'Am9':   { name: 'Am9',   frets: [2,0,0,2], fingers: [1,0,0,2] },
  'Cmaj9': { name: 'Cmaj9', frets: [0,0,0,2], fingers: [0,0,0,2] },
  'Fmaj9': { name: 'Fmaj9', frets: [2,4,1,0], fingers: [2,4,1,0] },
  'G13':   { name: 'G13',   frets: [0,2,1,2], fingers: [0,2,1,3] },
  'Em9':   { name: 'Em9',   frets: [0,2,0,2], fingers: [0,1,0,2] },
  'Dm9':   { name: 'Dm9',   frets: [2,2,1,3], fingers: [1,2,0,3] },
  'D9':    { name: 'D9',    frets: [2,4,2,3], fingers: [1,3,1,2] },
  'Bdim7': { name: 'Bdim7', frets: [1,2,1,2], fingers: [1,3,2,4] },
};

function chord(name: string): ChordData {
  return CHORD_DB[name] || { name, frets: [0,0,0,0] as [number,number,number,number], fingers: [0,0,0,0] as [number,number,number,number] };
}

function makeId(title: string, artist: string): string {
  return `${title}-${artist}`.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/-+$/, '').replace(/^-+/, '');
}

export function generateSongEntries(songs: Array<{
  title: string;
  artist: string;
  easyChords: string[];
  mediumChords: string[];
  advancedChords: string[];
  easyStrum: string;
  mediumStrum: string;
  advancedStrum: string;
  easyStrumDesc: string;
  mediumStrumDesc: string;
  advancedStrumDesc: string;
  easyLyrics: string;
  mediumLyrics: string;
  advancedLyrics: string;
}>) {
  return songs.map(s => {
    const id = makeId(s.title, s.artist);
    return {
      id,
      title: s.title,
      artist: s.artist,
      easy: {
        id: `${id}-easy`,
        title: s.title,
        artist: s.artist,
        level: 'easy',
        chords: s.easyChords.map(c => chord(c)),
        strummingPattern: s.easyStrum,
        strummingDescription: s.easyStrumDesc,
        lyrics: s.easyLyrics,
      },
      medium: {
        id: `${id}-medium`,
        title: s.title,
        artist: s.artist,
        level: 'medium',
        chords: s.mediumChords.map(c => chord(c)),
        strummingPattern: s.mediumStrum,
        strummingDescription: s.mediumStrumDesc,
        lyrics: s.mediumLyrics,
      },
      advanced: {
        id: `${id}-advanced`,
        title: s.title,
        artist: s.artist,
        level: 'advanced',
        chords: s.advancedChords.map(c => chord(c)),
        strummingPattern: s.advancedStrum,
        strummingDescription: s.advancedStrumDesc,
        lyrics: s.advancedLyrics,
      },
    };
  });
}

// Merge new songs into existing songs.json
export function mergeSongsIntoFile(newSongs: ReturnType<typeof generateSongEntries>) {
  const filePath = path.join(__dirname, '..', 'data', 'songs.json');
  const existing = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  const existingIds = new Set(existing.map((s: any) => s.id));

  let added = 0;
  for (const song of newSongs) {
    if (!existingIds.has(song.id)) {
      existing.push(song);
      existingIds.add(song.id);
      added++;
    }
  }

  fs.writeFileSync(filePath, JSON.stringify(existing, null, 2));
  console.log(`Added ${added} new songs (${existing.length} total)`);
}
