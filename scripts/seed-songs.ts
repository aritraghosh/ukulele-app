import Anthropic from '@anthropic-ai/sdk';
import * as fs from 'fs';
import * as path from 'path';

const client = new Anthropic();

const SONGS = [
  { title: 'Somewhere Over the Rainbow', artist: 'Israel Kamakawiwoole' },
  { title: "I'm Yours", artist: 'Jason Mraz' },
  { title: 'Riptide', artist: 'Vance Joy' },
  { title: "Can't Help Falling in Love", artist: 'Elvis Presley' },
  { title: 'Three Little Birds', artist: 'Bob Marley' },
  { title: 'Stand By Me', artist: 'Ben E. King' },
  { title: 'Hey Soul Sister', artist: 'Train' },
  { title: 'Leaving on a Jet Plane', artist: 'John Denver' },
  { title: 'Country Roads', artist: 'John Denver' },
  { title: 'Let It Be', artist: 'The Beatles' },
  { title: 'Hallelujah', artist: 'Leonard Cohen' },
  { title: 'You Are My Sunshine', artist: 'Traditional' },
  { title: 'Wonderwall', artist: 'Oasis' },
  { title: 'No Woman No Cry', artist: 'Bob Marley' },
  { title: 'What a Wonderful World', artist: 'Louis Armstrong' },
  { title: 'Banana Pancakes', artist: 'Jack Johnson' },
  { title: 'Better Together', artist: 'Jack Johnson' },
  { title: 'La Vie En Rose', artist: 'Edith Piaf' },
  { title: 'Hey Jude', artist: 'The Beatles' },
  { title: 'Imagine', artist: 'John Lennon' },
  { title: 'Have You Ever Seen the Rain', artist: 'CCR' },
  { title: 'House of the Rising Sun', artist: 'The Animals' },
  { title: 'A Thousand Years', artist: 'Christina Perri' },
  { title: 'Creep', artist: 'Radiohead' },
  { title: 'Island in the Sun', artist: 'Weezer' },
];

const LEVELS = ['easy', 'medium', 'advanced'] as const;

const levelGuide = {
  easy: 'Use only the simplest open chords (C, Am, F, G, Em, D). Minimize chord changes. Use basic down-strum patterns.',
  medium: 'Use standard open chords and common barre chords. Include suspensions and 7ths where appropriate. Use moderate strumming patterns with some syncopation.',
  advanced: 'Use extended chords (7ths, 9ths, diminished, augmented), jazz voicings, and complex fingerings. Use advanced strumming with muting, fingerpicking patterns, or syncopation.',
};

async function generateForSong(title: string, artist: string, level: string) {
  const message = await client.messages.create({
    model: 'claude-3-5-sonnet-20241022',
    max_tokens: 4096,
    messages: [
      {
        role: 'user',
        content: `You are a ukulele teacher. Generate chord data for the song "${title}" by "${artist}" at the ${level} level.

${levelGuide[level as keyof typeof levelGuide]}

Respond with ONLY valid JSON (no markdown, no backticks) in this exact format:
{
  "chords": [
    {
      "name": "Am",
      "frets": [2, 0, 0, 0],
      "fingers": [1, 0, 0, 0]
    }
  ],
  "strummingPattern": "D D U U D U",
  "strummingDescription": "A brief description of the strumming rhythm and feel",
  "lyrics": "[Am]Lyrics with [C]chord markers [G]inline like this\\n[F]Each line on a [C]new line"
}

Rules for the frets array: [G-string, C-string, E-string, A-string]. Use -1 for muted strings, 0 for open.
Rules for fingers array: 0=open/muted, 1=index, 2=middle, 3=ring, 4=pinky.
Include ALL unique chords used in the lyrics.
For the lyrics, include at least verse + chorus with chord annotations.
The strumming pattern should use D (down), U (up), x (mute), and - (rest).`,
      },
    ],
  });

  const text = message.content[0].type === 'text' ? message.content[0].text : '';
  return JSON.parse(text);
}

function makeId(title: string, artist: string): string {
  return `${title}-${artist}`.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/-+$/, '');
}

async function main() {
  const results = [];

  for (const song of SONGS) {
    const id = makeId(song.title, song.artist);
    console.log(`Generating: ${song.title} by ${song.artist}...`);

    const entry: Record<string, unknown> = {
      id,
      title: song.title,
      artist: song.artist,
    };

    for (const level of LEVELS) {
      try {
        console.log(`  ${level}...`);
        const data = await generateForSong(song.title, song.artist, level);
        entry[level] = {
          id: `${id}-${level}`,
          title: song.title,
          artist: song.artist,
          level,
          ...data,
        };
        // Rate limit buffer
        await new Promise((r) => setTimeout(r, 1000));
      } catch (err) {
        console.error(`  FAILED ${level}:`, err);
        entry[level] = {
          id: `${id}-${level}`,
          title: song.title,
          artist: song.artist,
          level,
          chords: [],
          strummingPattern: 'D D U U D U',
          strummingDescription: 'Basic strum pattern',
          lyrics: `[C]${song.title}\n[Am]by ${song.artist}`,
        };
      }
    }

    results.push(entry);
  }

  const outPath = path.join(__dirname, '..', 'data', 'songs.json');
  fs.writeFileSync(outPath, JSON.stringify(results, null, 2));
  console.log(`\nDone! Wrote ${results.length} songs to ${outPath}`);
}

main();
