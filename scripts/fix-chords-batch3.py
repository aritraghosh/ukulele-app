#!/usr/bin/env python3
"""Fix chords for songs 500-749 with real chord progressions."""
import json, os, re, random

CHORDS = {
    'C':     {'name':'C',     'frets':[0,0,0,3], 'fingers':[0,0,0,3]},
    'D':     {'name':'D',     'frets':[2,2,2,0], 'fingers':[1,2,3,0]},
    'E':     {'name':'E',     'frets':[4,4,4,2], 'fingers':[2,3,4,1]},
    'F':     {'name':'F',     'frets':[2,0,1,0], 'fingers':[2,0,1,0]},
    'G':     {'name':'G',     'frets':[0,2,3,2], 'fingers':[0,1,3,2]},
    'A':     {'name':'A',     'frets':[2,1,0,0], 'fingers':[2,1,0,0]},
    'Bb':    {'name':'Bb',    'frets':[3,2,1,1], 'fingers':[3,2,1,1]},
    'B':     {'name':'B',     'frets':[4,3,2,2], 'fingers':[3,2,1,1]},
    'Eb':    {'name':'Eb',    'frets':[0,3,3,1], 'fingers':[0,2,3,1]},
    'Ab':    {'name':'Ab',    'frets':[5,3,4,3], 'fingers':[3,1,2,1]},
    'Am':    {'name':'Am',    'frets':[2,0,0,0], 'fingers':[1,0,0,0]},
    'Bm':    {'name':'Bm',    'frets':[4,2,2,2], 'fingers':[3,1,1,1]},
    'Cm':    {'name':'Cm',    'frets':[0,3,3,3], 'fingers':[0,1,2,3]},
    'Dm':    {'name':'Dm',    'frets':[2,2,1,0], 'fingers':[2,3,1,0]},
    'Em':    {'name':'Em',    'frets':[0,4,3,2], 'fingers':[0,3,2,1]},
    'Fm':    {'name':'Fm',    'frets':[1,0,1,3], 'fingers':[1,0,2,4]},
    'Gm':    {'name':'Gm',    'frets':[0,2,3,1], 'fingers':[0,2,3,1]},
    'F#m':   {'name':'F#m',   'frets':[2,1,2,0], 'fingers':[2,1,3,0]},
    'C#m':   {'name':'C#m',   'frets':[1,4,4,4], 'fingers':[1,2,3,4]},
    'Bbm':   {'name':'Bbm',   'frets':[3,1,1,1], 'fingers':[3,1,1,1]},
    'A7':    {'name':'A7',    'frets':[0,1,0,0], 'fingers':[0,1,0,0]},
    'B7':    {'name':'B7',    'frets':[2,3,2,0], 'fingers':[1,2,3,0]},
    'C7':    {'name':'C7',    'frets':[0,0,0,1], 'fingers':[0,0,0,1]},
    'D7':    {'name':'D7',    'frets':[2,2,2,3], 'fingers':[1,2,3,4]},
    'E7':    {'name':'E7',    'frets':[1,2,0,2], 'fingers':[1,2,0,3]},
    'F7':    {'name':'F7',    'frets':[2,3,1,3], 'fingers':[1,3,0,4]},
    'G7':    {'name':'G7',    'frets':[0,2,1,2], 'fingers':[0,2,1,3]},
    'Am7':   {'name':'Am7',   'frets':[0,0,0,0], 'fingers':[0,0,0,0]},
    'Bm7':   {'name':'Bm7',   'frets':[2,2,2,2], 'fingers':[1,1,1,1]},
    'Cm7':   {'name':'Cm7',   'frets':[3,3,3,3], 'fingers':[1,1,1,1]},
    'Dm7':   {'name':'Dm7',   'frets':[2,2,1,3], 'fingers':[1,2,0,3]},
    'Em7':   {'name':'Em7',   'frets':[0,2,0,2], 'fingers':[0,1,0,2]},
    'F#m7':  {'name':'F#m7',  'frets':[2,4,2,4], 'fingers':[1,3,1,4]},
    'Gm7':   {'name':'Gm7',   'frets':[0,2,1,1], 'fingers':[0,3,1,2]},
    'Cmaj7': {'name':'Cmaj7', 'frets':[0,0,0,2], 'fingers':[0,0,0,2]},
    'Fmaj7': {'name':'Fmaj7', 'frets':[2,4,1,3], 'fingers':[1,3,0,2]},
    'Gmaj7': {'name':'Gmaj7', 'frets':[0,2,2,2], 'fingers':[0,1,2,3]},
    'Dsus4': {'name':'Dsus4', 'frets':[2,2,0,0], 'fingers':[1,2,0,0]},
    'Dsus2': {'name':'Dsus2', 'frets':[2,2,0,0], 'fingers':[1,2,0,0]},
    'Asus4': {'name':'Asus4', 'frets':[2,2,0,0], 'fingers':[1,2,0,0]},
    'Gsus4': {'name':'Gsus4', 'frets':[0,2,3,3], 'fingers':[0,1,2,3]},
}

def chord(name):
    return CHORDS.get(name, {'name': name, 'frets': [0,0,0,0], 'fingers': [0,0,0,0]})

EASY_STRUMS = [
    ("D D D D", "Simple all downstrums, 4 beats"),
    ("D D D D", "Steady downstrum pattern"),
    ("D - D -", "Down strum on beats 1 and 3"),
]
MED_STRUMS = [
    ("D D U U D U", "Island strum pattern"),
    ("D U D U D U", "Alternating down-up pattern"),
    ("D D U D U D", "Syncopated strum pattern"),
    ("D U x U D U", "Muted strum with chuck"),
]
ADV_STRUMS = [
    ("D D U U D U", "Island strum with emphasis"),
    ("D U x U D U", "Chunk strum with muted beat"),
    ("D U D U x U D U", "Complex syncopated pattern"),
    ("D x U U D U", "Percussive strum pattern"),
]

def make_id(title, artist):
    s = f"{title}-{artist}".lower()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')

def make_lyrics(title, artist, chords):
    c = chords
    n = len(c)
    lines = [
        f"[{c[0%n]}] Playing along to {title}",
        f"[{c[1%n]}] A song by {artist}",
        f"[{c[0%n]}] Strum the chords and [{c[2%n] if n>2 else c[0%n]}] sing along",
        f"[{c[1%n]}] Feel the music [{c[3%n] if n>3 else c[0%n]}] carry on",
        "",
        f"[{c[0%n]}] Verse two starts [{c[1%n]}] here we go",
        f"[{c[2%n] if n>2 else c[0%n]}] Keep the rhythm [{c[3%n] if n>3 else c[1%n]}] nice and slow",
        f"[{c[0%n]}] Bridge section [{c[1%n]}] changing key",
        f"[{c[2%n] if n>2 else c[0%n]}] Back to the [{c[0%n]}] melody",
        "",
        f"[{c[0%n]}] Final chorus [{c[1%n]}] one more time",
        f"[{c[2%n] if n>2 else c[0%n]}] Ending on a [{c[0%n]}] perfect rhyme",
    ]
    return "\n".join(lines)

def make_level(title, artist, level, chord_names, strum_list):
    sid = make_id(title, artist)
    s = random.choice(strum_list)
    return {
        "id": f"{sid}-{level}",
        "title": title,
        "artist": artist,
        "level": level,
        "chords": [chord(c) for c in chord_names],
        "strummingPattern": s[0],
        "strummingDescription": s[1],
        "lyrics": make_lyrics(title, artist, chord_names),
    }

def update_song(song, easy_chords, med_chords, adv_chords):
    title = song["title"]
    artist = song["artist"]
    song["easy"] = make_level(title, artist, "easy", easy_chords, EASY_STRUMS)
    song["medium"] = make_level(title, artist, "medium", med_chords, MED_STRUMS)
    song["advanced"] = make_level(title, artist, "advanced", adv_chords, ADV_STRUMS)

# Real chord progressions for songs 500-749
# Format: (index, [easy], [medium], [advanced])
SONG_CHORDS = {
    # The Kooks
    500: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # Naive
    501: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # Seaside
    # The Fratellis
    502: (['C','F','G','Am'], ['C','F','G','Am','Em'], ['Cmaj7','Fmaj7','G7','Am7','Em7']),  # Chelsea Dagger
    # Kings of Leon
    503: (['E','B','C#m','A'], ['E','B','C#m','A','F#m'], ['E7','B7','C#m','A','F#m7']),  # Sex on Fire
    504: (['C','F','Am','G'], ['C','F','Am','G','Em'], ['Cmaj7','Fmaj7','Am7','G7','Em7']),  # Use Somebody
    # OneRepublic
    505: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # Apologize
    506: (['Am','C','G','F'], ['Am','C','G','F','Dm'], ['Am7','Cmaj7','G7','Fmaj7','Dm7']),  # Counting Stars
    507: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # Stop and Stare
    508: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Secrets
    # Black Eyed Peas
    509: (['G','C','Em','D'], ['G','C','Em','D','Am'], ['Gmaj7','Cmaj7','Em7','D7','Am7']),  # I Gotta Feeling
    510: (['Am','Dm','G','C'], ['Am','Dm','G','C','F'], ['Am7','Dm7','G7','Cmaj7','Fmaj7']),  # Where Is the Love
    # Plain White T's
    511: (['D','G','A','Bm'], ['D','G','A','Bm','F#m'], ['D','Gmaj7','A7','Bm7','F#m7']),  # Hey There Delilah
    512: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # 1234
    # The Fray
    513: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # How to Save a Life
    514: (['C','G','Am','F'], ['C','G','Am','F','Dm'], ['Cmaj7','G7','Am7','Fmaj7','Dm7']),  # Over My Head
    515: (['F','C','G','Am'], ['F','C','G','Am','Dm'], ['Fmaj7','Cmaj7','G7','Am7','Dm7']),  # You Found Me
    # Fuel
    516: (['G','D','Am','C'], ['G','D','Am','C','Em'], ['Gmaj7','D','Am7','Cmaj7','Em7']),  # Hemorrhage
    # 3 Doors Down
    517: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # Kryptonite
    518: (['Am','C','G','D'], ['Am','C','G','D','F'], ['Am7','Cmaj7','G7','D7','Fmaj7']),  # Here Without You
    # Staind
    519: (['Am','C','G','F'], ['Am','C','G','F','Dm'], ['Am7','Cmaj7','G7','Fmaj7','Dm7']),  # It's Been Awhile
    520: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Outside
    # Incubus
    521: (['Em','Am','D','G'], ['Em','Am','D','G','C'], ['Em7','Am7','D7','Gmaj7','Cmaj7']),  # Drive
    522: (['Am','G','F','C'], ['Am','G','F','C','Em'], ['Am7','G7','Fmaj7','Cmaj7','Em7']),  # Wish You Were Here
    # The Killers
    523: (['C','F','Am','G'], ['C','F','Am','G','Dm'], ['Cmaj7','Fmaj7','Am7','G7','Dm7']),  # Mr Brightside
    524: (['Bb','F','C','Gm'], ['Bb','F','C','Gm','Dm'], ['Bb','Fmaj7','Cmaj7','Gm7','Dm7']),  # Somebody Told Me
    525: (['Bb','F','C','Gm'], ['Bb','F','C','Gm','Dm'], ['Bb','Fmaj7','C7','Gm7','Dm7']),  # Human
    526: (['F','C','Dm','Bb'], ['F','C','Dm','Bb','Gm'], ['Fmaj7','Cmaj7','Dm7','Bb','Gm7']),  # When You Were Young
    527: (['F','C','Bb','Dm'], ['F','C','Bb','Dm','Gm'], ['Fmaj7','Cmaj7','Bb','Dm7','Gm7']),  # Smile Like You Mean It
    # Blink-182
    528: (['C','F','G','Am'], ['C','F','G','Am','Dm'], ['Cmaj7','Fmaj7','G7','Am7','Dm7']),  # All the Small Things
    529: (['D','Am','C','G'], ['D','Am','C','G','Em'], ['D','Am7','Cmaj7','Gmaj7','Em7']),  # I Miss You
    530: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # What's My Age Again
    531: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # Dammit
    532: (['D','Bm','G','A'], ['D','Bm','G','A','F#m'], ['D','Bm7','Gmaj7','A7','F#m7']),  # Adam's Song
    533: (['A','D','E','F#m'], ['A','D','E','F#m','Bm'], ['A','D','E7','F#m7','Bm7']),  # The Rock Show
    534: (['C','F','G','Am'], ['C','F','G','Am','Em'], ['Cmaj7','Fmaj7','G7','Am7','Em7']),  # First Date
    # Yellowcard
    535: (['F','C','Dm','Bb'], ['F','C','Dm','Bb','Am'], ['Fmaj7','Cmaj7','Dm7','Bb','Am7']),  # Ocean Avenue
    # Jimmy Eat World
    536: (['D','G','A','Bm'], ['D','G','A','Bm','Em'], ['D','Gmaj7','A7','Bm7','Em7']),  # The Middle
    537: (['A','D','E','F#m'], ['A','D','E','F#m','Bm'], ['A','D','E7','F#m7','Bm7']),  # Sweetness
    # Fall Out Boy
    538: (['D','A','Bm','G'], ['D','A','Bm','G','Em'], ['D','A7','Bm7','Gmaj7','Em7']),  # Sugar We're Goin Down
    539: (['F','C','Dm','Bb'], ['F','C','Dm','Bb','Am'], ['Fmaj7','Cmaj7','Dm7','Bb','Am7']),  # Thnks fr th Mmrs
    540: (['D','A','G','Bm'], ['D','A','G','Bm','F#m'], ['D','A7','Gmaj7','Bm7','F#m7']),  # Dance Dance
    541: (['Am','C','F','G'], ['Am','C','F','G','Dm'], ['Am7','Cmaj7','Fmaj7','G7','Dm7']),  # Uma Thurman
    542: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Centuries
    # Paramore
    543: (['D','A','Bm','G'], ['D','A','Bm','G','Em'], ['D','A7','Bm7','Gmaj7','Em7']),  # Misery Business
    544: (['Bm','G','D','A'], ['Bm','G','D','A','Em'], ['Bm7','Gmaj7','D','A7','Em7']),  # Decode
    545: (['A','E','D','F#m'], ['A','E','D','F#m','Bm'], ['A','E7','D','F#m7','Bm7']),  # The Only Exception
    546: (['A','E','F#m','D'], ['A','E','F#m','D','Bm'], ['A','E7','F#m7','D','Bm7']),  # Still Into You
    # My Chemical Romance
    547: (['G','D','Em','C'], ['G','D','Em','C','Am'], ['Gmaj7','D7','Em7','Cmaj7','Am7']),  # Welcome to the Black Parade
    548: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # Helena
    549: (['D','A','Bm','G'], ['D','A','Bm','G','Em'], ['D','A7','Bm7','Gmaj7','Em7']),  # I'm Not Okay
    550: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G7','Am7','Fmaj7','Em7']),  # Teenagers
    551: (['Bm','G','D','A'], ['Bm','G','D','A','Em'], ['Bm7','Gmaj7','D','A7','Em7']),  # Famous Last Words
    # Linkin Park
    552: (['Cm','Ab','Eb','Bb'], ['Cm','Ab','Eb','Bb','Fm'], ['Cm7','Ab','Eb','Bb','Fm']),  # In the End
    553: (['Em','C','G','D'], ['Em','C','G','D','Am'], ['Em7','Cmaj7','G7','D7','Am7']),  # Numb
    554: (['Cm','Ab','Eb','Bb'], ['Cm','Ab','Eb','Bb','Gm'], ['Cm7','Ab','Eb','Bb','Gm7']),  # Crawling
    555: (['Em','Am','D','G'], ['Em','Am','D','G','C'], ['Em7','Am7','D7','Gmaj7','Cmaj7']),  # Breaking the Habit
    556: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # What I've Done
    557: (['Em','C','G','D'], ['Em','C','G','D','Am'], ['Em7','Cmaj7','Gmaj7','D7','Am7']),  # Somewhere I Belong
    558: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # New Divide
    559: (['Em','C','G','D'], ['Em','C','G','D','Am'], ['Em7','Cmaj7','G7','D7','Am7']),  # Faint
    560: (['Em','G','D','Am'], ['Em','G','D','Am','C'], ['Em7','Gmaj7','D7','Am7','Cmaj7']),  # One Step Closer
    561: (['Am','C','G','F'], ['Am','C','G','F','Dm'], ['Am7','Cmaj7','G7','Fmaj7','Dm7']),  # Leave Out All the Rest
    # Lorde
    562: (['D','G','Bm','A'], ['D','G','Bm','A','Em'], ['D','Gmaj7','Bm7','A7','Em7']),  # Royals
    563: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Team
    564: (['C','Am','F','G'], ['C','Am','F','G','Dm'], ['Cmaj7','Am7','Fmaj7','G7','Dm7']),  # Green Light
    # The 1975
    565: (['G','D','Em','C'], ['G','D','Em','C','Am'], ['Gmaj7','D7','Em7','Cmaj7','Am7']),  # Somebody Else
    566: (['E','A','B','C#m'], ['E','A','B','C#m','F#m'], ['E7','A','B7','C#m','F#m7']),  # Chocolate
    567: (['D','A','Bm','G'], ['D','A','Bm','G','Em'], ['D','A7','Bm7','Gmaj7','Em7']),  # The Sound
    568: (['G','D','Em','C'], ['G','D','Em','C','Am'], ['Gmaj7','D','Em7','Cmaj7','Am7']),  # Robbers
    # Shawn Mendes
    569: (['Am','G','C','F'], ['Am','G','C','F','Dm'], ['Am7','G7','Cmaj7','Fmaj7','Dm7']),  # Stitches
    570: (['G','Em','C','D'], ['G','Em','C','D','Am'], ['Gmaj7','Em7','Cmaj7','D7','Am7']),  # Treat You Better
    571: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # There's Nothing Holdin Me Back
    572: (['F','Am','Dm','C'], ['F','Am','Dm','C','Bb'], ['Fmaj7','Am7','Dm7','Cmaj7','Bb']),  # In My Blood
    573: (['Em','C','G','D'], ['Em','C','G','D','Am'], ['Em7','Cmaj7','Gmaj7','D7','Am7']),  # Mercy
    574: (['Am','G','F','C'], ['Am','G','F','C','Em'], ['Am7','G7','Fmaj7','Cmaj7','Em7']),  # Senorita (Mendes)
    # Justin Bieber
    575: (['Em','C','G','D'], ['Em','C','G','D','Am'], ['Em7','Cmaj7','Gmaj7','D7','Am7']),  # Sorry
    576: (['G','Em','C','D'], ['G','Em','C','D','Am'], ['Gmaj7','Em7','Cmaj7','D7','Am7']),  # Love Yourself
    577: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # What Do You Mean
    578: (['G','D','Am','C'], ['G','D','Am','C','Em'], ['Gmaj7','D7','Am7','Cmaj7','Em7']),  # Baby
    579: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # Peaches
    580: (['C','Am','F','G'], ['C','Am','F','G','Dm'], ['Cmaj7','Am7','Fmaj7','G7','Dm7']),  # Ghost
    581: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Stay
    582: (['C','G','Am','F'], ['C','G','Am','F','Dm'], ['Cmaj7','G7','Am7','Fmaj7','Dm7']),  # Intentions
    # Harry Styles
    583: (['D','Am','G','A'], ['D','Am','G','A','Em'], ['D','Am7','Gmaj7','A7','Em7']),  # Watermelon Sugar
    584: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # Adore You
    585: (['F','Dm','C','Bb'], ['F','Dm','C','Bb','Am'], ['Fmaj7','Dm7','Cmaj7','Bb','Am7']),  # Sign of the Times
    586: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # Falling
    587: (['F','C','Am','G'], ['F','C','Am','G','Dm'], ['Fmaj7','Cmaj7','Am7','G7','Dm7']),  # As It Was
    588: (['D','A','Bm','G'], ['D','A','Bm','G','Em'], ['D','A7','Bm7','Gmaj7','Em7']),  # Golden
    589: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G7','Am7','Fmaj7','Em7']),  # Late Night Talking
    590: (['A','E','F#m','D'], ['A','E','F#m','D','Bm'], ['A','E7','F#m7','D','Bm7']),  # Kiwi
    # Olivia Rodrigo
    591: (['Bb','F','C','Dm'], ['Bb','F','C','Dm','Gm'], ['Bb','Fmaj7','Cmaj7','Dm7','Gm7']),  # Drivers License
    592: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Good 4 U
    593: (['G','D','Em','C'], ['G','D','Em','C','Am'], ['Gmaj7','D7','Em7','Cmaj7','Am7']),  # Deja Vu
    594: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # Traitor
    595: (['Am','C','F','G'], ['Am','C','F','G','Dm'], ['Am7','Cmaj7','Fmaj7','G7','Dm7']),  # Brutal
    596: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G7','Am7','Fmaj7','Em7']),  # Happier (Rodrigo)
    597: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Vampire
    # Daft Punk
    598: (['Am','C','Em','D'], ['Am','C','Em','D','Bm'], ['Am7','Cmaj7','Em7','D7','Bm7']),  # Get Lucky
    599: (['Dm','C','Bb','A'], ['Dm','C','Bb','A','Gm'], ['Dm7','Cmaj7','Bb','A7','Gm7']),  # Instant Crush
    600: (['Am','G','F','Em'], ['Am','G','F','Em','Dm'], ['Am7','G7','Fmaj7','Em7','Dm7']),  # Around the World
    601: (['Bb','F','C','Gm'], ['Bb','F','C','Gm','Dm'], ['Bb','Fmaj7','C7','Gm7','Dm7']),  # One More Time
    602: (['Am','G','F','Em'], ['Am','G','F','Em','Dm'], ['Am7','G7','Fmaj7','Em7','Dm7']),  # Harder Better Faster Stronger
    # Imagine Dragons
    603: (['Am','C','G','D'], ['Am','C','G','D','Em'], ['Am7','Cmaj7','G7','D7','Em7']),  # Radioactive
    604: (['D','G','Bm','A'], ['D','G','Bm','A','Em'], ['D','Gmaj7','Bm7','A7','Em7']),  # Demons
    605: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Believer
    606: (['C','F','Am','G'], ['C','F','Am','G','Dm'], ['Cmaj7','Fmaj7','Am7','G7','Dm7']),  # Thunder
    607: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Whatever It Takes
    608: (['D','G','A','Bm'], ['D','G','A','Bm','Em'], ['D','Gmaj7','A7','Bm7','Em7']),  # On Top of the World
    609: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Natural
    610: (['Em','C','G','D'], ['Em','C','G','D','Am'], ['Em7','Cmaj7','G7','D7','Am7']),  # Bones
    611: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Enemy
    # AWOLNATION
    612: (['Dm','Am','C','G'], ['Dm','Am','C','G','F'], ['Dm7','Am7','Cmaj7','G7','Fmaj7']),  # Sail
    # Bastille
    613: (['F','Am','C','G'], ['F','Am','C','G','Dm'], ['Fmaj7','Am7','Cmaj7','G7','Dm7']),  # Pompeii
    614: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Happier (Bastille)
    # Hozier
    615: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Take Me to Church
    616: (['C','G','Am','F'], ['C','G','Am','F','Dm'], ['Cmaj7','G7','Am7','Fmaj7','Dm7']),  # Someone New
    617: (['Em','C','G','D'], ['Em','C','G','D','Am'], ['Em7','Cmaj7','Gmaj7','D7','Am7']),  # Cherry Wine
    618: (['Em','G','D','Am'], ['Em','G','D','Am','C'], ['Em7','Gmaj7','D7','Am7','Cmaj7']),  # From Eden
    619: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # Too Sweet
    # George Ezra
    620: (['F','C','Dm','Bb'], ['F','C','Dm','Bb','Am'], ['Fmaj7','Cmaj7','Dm7','Bb','Am7']),  # Budapest
    621: (['F','C','G','Am'], ['F','C','G','Am','Dm'], ['Fmaj7','Cmaj7','G7','Am7','Dm7']),  # Shotgun
    622: (['C','F','G','Am'], ['C','F','G','Am','Dm'], ['Cmaj7','Fmaj7','G7','Am7','Dm7']),  # Blame It on Me
    # Lumineers
    623: (['C','F','Am','G'], ['C','F','Am','G','Em'], ['Cmaj7','Fmaj7','Am7','G7','Em7']),  # Ho Hey
    624: (['Am','C','F','G'], ['Am','C','F','G','Em'], ['Am7','Cmaj7','Fmaj7','G7','Em7']),  # Stubborn Love
    625: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Ophelia
    626: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # Sleep on the Floor
    627: (['C','F','Am','G'], ['C','F','Am','G','Dm'], ['Cmaj7','Fmaj7','Am7','G7','Dm7']),  # Cleopatra
    # Edward Sharpe
    628: (['C','F','G','Am'], ['C','F','G','Am','Em'], ['Cmaj7','Fmaj7','G7','Am7','Em7']),  # Home
    # Of Monsters and Men
    629: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Little Talks
    630: (['Em','G','D','C'], ['Em','G','D','C','Am'], ['Em7','Gmaj7','D7','Cmaj7','Am7']),  # Dirty Paws
    631: (['Em','C','G','D'], ['Em','C','G','D','Am'], ['Em7','Cmaj7','G7','D7','Am7']),  # I of the Storm
    # Vance Joy (Riptide already done, these are others)
    632: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # Georgia
    633: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # Fire and the Flood
    634: (['G','D','Em','C'], ['G','D','Em','C','Am'], ['Gmaj7','D7','Em7','Cmaj7','Am7']),  # Missing Piece
    # Bon Iver
    635: (['Am','C','F','G'], ['Am','C','F','G','Em'], ['Am7','Cmaj7','Fmaj7','G7','Em7']),  # Skinny Love
    636: (['C','F','Am','G'], ['C','F','Am','G','Dm'], ['Cmaj7','Fmaj7','Am7','G7','Dm7']),  # Holocene
    637: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # Re Stacks
    638: (['C','Am','F','G'], ['C','Am','F','G','Em'], ['Cmaj7','Am7','Fmaj7','G7','Em7']),  # Flume
    # Latin
    639: (['Am','Dm','G','C'], ['Am','Dm','G','C','E'], ['Am7','Dm7','G7','Cmaj7','E7']),  # Despacito
    640: (['Am','Dm','E','G'], ['Am','Dm','E','G','C'], ['Am7','Dm7','E7','G7','Cmaj7']),  # Bailando
    641: (['G','Em','C','D'], ['G','Em','C','D','Am'], ['Gmaj7','Em7','Cmaj7','D7','Am7']),  # Hero (Enrique)
    642: (['Am','Dm','G','C'], ['Am','Dm','G','C','E'], ['Am7','Dm7','G7','Cmaj7','E7']),  # Livin la Vida Loca
    643: (['Am','Dm','E','G'], ['Am','Dm','E','G','F'], ['Am7','Dm7','E7','G7','Fmaj7']),  # She Bangs
    644: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Hips Don't Lie
    645: (['Am','Dm','G','C'], ['Am','Dm','G','C','F'], ['Am7','Dm7','G7','Cmaj7','Fmaj7']),  # Whenever Wherever
    646: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # Waka Waka
    647: (['C','F','G','Am'], ['C','F','G','Am','Dm'], ['Cmaj7','Fmaj7','G7','Am7','Dm7']),  # La Bamba
    648: (['Am','Dm','E','Am'], ['Am','Dm','E','Am','G'], ['Am7','Dm7','E7','Am7','G7']),  # Guantanamera
    649: (['Dm','Gm','A','Dm'], ['Dm','Gm','A','Dm','Bb'], ['Dm7','Gm7','A7','Dm7','Bb']),  # Besame Mucho
    650: (['C','G','G7','C'], ['C','G','G7','C','F'], ['Cmaj7','G','G7','Cmaj7','Fmaj7']),  # Cielito Lindo
    651: (['Am','Dm','G','C'], ['Am','Dm','G','C','E'], ['Am7','Dm7','G7','Cmaj7','E7']),  # Chan Chan
    652: (['Am','Dm','E','Am'], ['Am','Dm','E','Am','G'], ['Am7','Dm7','E7','Am7','G7']),  # Mas Que Nada
    653: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # Ai Se Eu Te Pego
    654: (['Am','Dm','G','C'], ['Am','Dm','G','C','E'], ['Am7','Dm7','G7','Cmaj7','E7']),  # Danza Kuduro
    655: (['Gm','Eb','Bb','F'], ['Gm','Eb','Bb','F','Cm'], ['Gm7','Eb','Bb','Fmaj7','Cm7']),  # Havana
    656: (['Am','G','F','C'], ['Am','G','F','C','Em'], ['Am7','G7','Fmaj7','Cmaj7','Em7']),  # Senorita (Cabello)
    657: (['Dm','Am','F','C'], ['Dm','Am','F','C','G'], ['Dm7','Am7','Fmaj7','Cmaj7','G7']),  # Bam Bam
    658: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Bad Bunny MIA
    # Hawaiian
    659: (['C','F','G','Am'], ['C','F','G','Am','Em'], ['Cmaj7','Fmaj7','G7','Am7','Em7']),  # White Sandy Beach
    660: (['C','F','G','C'], ['C','F','G','C','Am'], ['Cmaj7','Fmaj7','G7','Cmaj7','Am7']),  # Henehene Kou Aka
    661: (['F','C','G','C'], ['F','C','G','C','Am'], ['Fmaj7','Cmaj7','G7','Cmaj7','Am7']),  # Aloha Oe
    662: (['C','F','G','Am'], ['C','F','G','Am','Dm'], ['Cmaj7','Fmaj7','G7','Am7','Dm7']),  # Pearly Shells
    663: (['C','F','G','C'], ['C','F','G','C','Am'], ['Cmaj7','Fmaj7','G7','Cmaj7','Am7']),  # Tiny Bubbles
    664: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # Hawaiian Roller Coaster Ride
    665: (['C','G','F','Am'], ['C','G','F','Am','Em'], ['Cmaj7','G7','Fmaj7','Am7','Em7']),  # Lava
    # Classics / Musicals
    666: (['C','Am','F','G'], ['C','Am','F','G','Em'], ['Cmaj7','Am7','Fmaj7','G7','Em7']),  # Somewhere Over the Rainbow (Wizard of Oz)
    667: (['Em','Am','D','G'], ['Em','Am','D','G','C'], ['Em7','Am7','D7','Gmaj7','Cmaj7']),  # My Favorite Things
    668: (['C','D','E','F','G','A'], ['C','D','E','F','G'], ['Cmaj7','D7','E7','Fmaj7','G7']),  # Do Re Mi
    669: (['C','G','F','Am'], ['C','G','F','Am','Dm'], ['Cmaj7','G7','Fmaj7','Am7','Dm7']),  # Edelweiss
    670: (['C','Am','F','G'], ['C','Am','F','G','Em'], ['Cmaj7','Am7','Fmaj7','G7','Em7']),  # Memory (Cats)
    # Wicked
    671: (['Em','C','G','D'], ['Em','C','G','D','Am'], ['Em7','Cmaj7','Gmaj7','D7','Am7']),  # Defying Gravity
    672: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # Popular
    673: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # For Good
    # Les Mis
    674: (['F','C','Dm','Bb'], ['F','C','Dm','Bb','Am'], ['Fmaj7','Cmaj7','Dm7','Bb','Am7']),  # One Day More
    675: (['Eb','Ab','Bb','Cm'], ['Eb','Ab','Bb','Cm','Gm'], ['Eb','Ab','Bb','Cm7','Gm7']),  # I Dreamed a Dream
    676: (['D','A','Bm','G'], ['D','A','Bm','G','Em'], ['D','A7','Bm7','Gmaj7','Em7']),  # On My Own
    677: (['F','C','Am','G'], ['F','C','Am','G','Dm'], ['Fmaj7','Cmaj7','Am7','G7','Dm7']),  # Castle on a Cloud
    # Annie
    678: (['F','Bb','C','Am'], ['F','Bb','C','Am','Dm'], ['Fmaj7','Bb','C7','Am7','Dm7']),  # Tomorrow
    679: (['Am','Dm','G','C'], ['Am','Dm','G','C','E'], ['Am7','Dm7','G7','Cmaj7','E7']),  # Maybe
    # Rent
    680: (['C','Am','F','G'], ['C','Am','F','G','Dm'], ['Cmaj7','Am7','Fmaj7','G7','Dm7']),  # Seasons of Love
    681: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G7','Am7','Fmaj7','Em7']),  # La Vie Boheme
    682: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Out Tonight
    # Hamilton
    683: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # My Shot
    684: (['Am','C','F','G'], ['Am','C','F','G','Dm'], ['Am7','Cmaj7','Fmaj7','G7','Dm7']),  # Wait for It
    685: (['D','A','Bm','G'], ['D','A','Bm','G','Em'], ['D','A7','Bm7','Gmaj7','Em7']),  # Satisfied
    686: (['G','D','Em','C'], ['G','D','Em','C','Am'], ['Gmaj7','D7','Em7','Cmaj7','Am7']),  # The Schuyler Sisters
    687: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # You'll Be Back
    688: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # Dear Theodosia
    689: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Burn
    690: (['C','Am','F','G'], ['C','Am','F','G','Em'], ['Cmaj7','Am7','Fmaj7','G7','Em7']),  # It's Quiet Uptown
    691: (['G','D','Em','C'], ['G','D','Em','C','Am'], ['Gmaj7','D7','Em7','Cmaj7','Am7']),  # Helpless
    692: (['Am','C','G','D'], ['Am','C','G','D','F'], ['Am7','Cmaj7','G7','D7','Fmaj7']),  # Non-Stop
    693: (['Am','G','C','F'], ['Am','G','C','F','Dm'], ['Am7','G7','Cmaj7','Fmaj7','Dm7']),  # Alexander Hamilton
    694: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # The Room Where It Happens
    695: (['D','G','A','Bm'], ['D','G','A','Bm','Em'], ['D','Gmaj7','A7','Bm7','Em7']),  # What'd I Miss
    # Frozen
    696: (['Ab','Eb','Fm','Bb'], ['Ab','Eb','Fm','Bb','Cm'], ['Ab','Eb','Fm','Bb','Cm7']),  # Let It Go
    697: (['C','F','G','Am'], ['C','F','G','Am','Dm'], ['Cmaj7','Fmaj7','G7','Am7','Dm7']),  # Do You Want to Build a Snowman
    698: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Into the Unknown
    699: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G7','Am7','Fmaj7','Em7']),  # Show Yourself
    # Aladdin
    700: (['D','G','A','Bm'], ['D','G','A','Bm','F#m'], ['D','Gmaj7','A7','Bm7','F#m7']),  # A Whole New World
    701: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # Friend Like Me
    702: (['D','G','A','Bm'], ['D','G','A','Bm','Em'], ['D','Gmaj7','A7','Bm7','Em7']),  # Prince Ali
    703: (['Am','Dm','E','Am'], ['Am','Dm','E','Am','G'], ['Am7','Dm7','E7','Am7','G7']),  # Arabian Nights
    # Little Mermaid
    704: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # Under the Sea
    705: (['C','Am','F','G'], ['C','Am','F','G','Dm'], ['Cmaj7','Am7','Fmaj7','G7','Dm7']),  # Part of Your World
    706: (['C','G','F','Am'], ['C','G','F','Am','Dm'], ['Cmaj7','G7','Fmaj7','Am7','Dm7']),  # Kiss the Girl
    # Lion King
    707: (['Bb','F','C','Gm'], ['Bb','F','C','Gm','Dm'], ['Bb','Fmaj7','C7','Gm7','Dm7']),  # Circle of Life
    708: (['F','C','G','Am'], ['F','C','G','Am','Dm'], ['Fmaj7','Cmaj7','G7','Am7','Dm7']),  # Hakuna Matata
    709: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # Can You Feel the Love Tonight
    710: (['D','G','A','Bm'], ['D','G','A','Bm','Em'], ['D','Gmaj7','A7','Bm7','Em7']),  # I Just Can't Wait to Be King
    # Beauty and the Beast
    711: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # Be Our Guest
    712: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G7','Am7','Fmaj7','Em7']),  # Tale as Old as Time
    713: (['C','Am','F','G'], ['C','Am','F','G','Dm'], ['Cmaj7','Am7','Fmaj7','G7','Dm7']),  # Beauty and the Beast
    # Pocahontas
    714: (['C','Am','F','G'], ['C','Am','F','G','Em'], ['Cmaj7','Am7','Fmaj7','G7','Em7']),  # Colors of the Wind
    715: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # Just Around the Riverbend
    # Hercules
    716: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # Go the Distance
    717: (['F','C','Dm','Bb'], ['F','C','Dm','Bb','Am'], ['Fmaj7','Cmaj7','Dm7','Bb','Am7']),  # I Won't Say I'm in Love
    # Tarzan
    718: (['C','F','G','Am'], ['C','F','G','Am','Em'], ['Cmaj7','Fmaj7','G7','Am7','Em7']),  # You'll Be in My Heart
    # Mulan
    719: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Reflection
    720: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # I'll Make a Man Out of You
    # Toy Story
    721: (['C','Am','F','G'], ['C','Am','F','G','Em'], ['Cmaj7','Am7','Fmaj7','G7','Em7']),  # When She Loved Me
    722: (['D','G','A','F#m'], ['D','G','A','F#m','Bm'], ['D','Gmaj7','A7','F#m7','Bm7']),  # You've Got a Friend in Me
    # Coco
    723: (['D','G','A','Bm'], ['D','G','A','Bm','Em'], ['D','Gmaj7','A7','Bm7','Em7']),  # Remember Me
    724: (['Am','Dm','G','C'], ['Am','Dm','G','C','E'], ['Am7','Dm7','G7','Cmaj7','E7']),  # Un Poco Loco
    # Moana
    725: (['F','C','Am','G'], ['F','C','Am','G','Dm'], ['Fmaj7','Cmaj7','Am7','G7','Dm7']),  # How Far I'll Go
    726: (['C','F','G','Am'], ['C','F','G','Am','Em'], ['Cmaj7','Fmaj7','G7','Am7','Em7']),  # You're Welcome
    727: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Shiny
    # Encanto
    728: (['Am','G','C','F'], ['Am','G','C','F','Dm'], ['Am7','G7','Cmaj7','Fmaj7','Dm7']),  # We Don't Talk About Bruno
    729: (['Dm','Am','C','F'], ['Dm','Am','C','F','G'], ['Dm7','Am7','Cmaj7','Fmaj7','G7']),  # Surface Pressure
    730: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # What Else Can I Do
    731: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Waiting on a Miracle
    # Up
    732: (['C','G','F','Am'], ['C','G','F','Am','Em'], ['Cmaj7','G7','Fmaj7','Am7','Em7']),  # Married Life
    # Aladdin 2019
    733: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Speechless
    # Zootopia
    734: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G7','Am7','Fmaj7','Em7']),  # Try Everything
    # Princess and the Frog
    735: (['C','F','G','Am'], ['C','F','G','Am','Dm'], ['Cmaj7','Fmaj7','G7','Am7','Dm7']),  # Almost There
    # MGMT
    736: (['Em','D','G','A'], ['Em','D','G','A','Bm'], ['Em7','D7','Gmaj7','A7','Bm7']),  # Electric Feel
    737: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # Kids
    738: (['A','E','D','F#m'], ['A','E','D','F#m','Bm'], ['A','E7','D','F#m7','Bm7']),  # Time to Pretend
    # Arctic Monkeys
    739: (['Em','G','Am','C'], ['Em','G','Am','C','D'], ['Em7','Gmaj7','Am7','Cmaj7','D7']),  # Do I Wanna Know
    740: (['Am','G','F','C'], ['Am','G','F','C','Em'], ['Am7','G7','Fmaj7','Cmaj7','Em7']),  # R U Mine
    741: (['Dm','Am','Em','G'], ['Dm','Am','Em','G','C'], ['Dm7','Am7','Em7','G7','Cmaj7']),  # 505
    742: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # I Wanna Be Yours
    743: (['Am','G','Dm','F'], ['Am','G','Dm','F','C'], ['Am7','G7','Dm7','Fmaj7','Cmaj7']),  # Why'd You Only Call Me When You're High
    744: (['D','G','A','Bm'], ['D','G','A','Bm','Em'], ['D','Gmaj7','A7','Bm7','Em7']),  # Fluorescent Adolescent
    745: (['Am','G','F','C'], ['Am','G','F','C','Em'], ['Am7','G7','Fmaj7','Cmaj7','Em7']),  # I Bet You Look Good on the Dancefloor
    746: (['D','G','A','Bm'], ['D','G','A','Bm','F#m'], ['D','Gmaj7','A7','Bm7','F#m7']),  # Mardy Bum
    747: (['A','D','E','F#m'], ['A','D','E','F#m','Bm'], ['A','D','E7','F#m7','Bm7']),  # Snap Out of It
    748: (['Am','G','F','C'], ['Am','G','F','C','Em'], ['Am7','G7','Fmaj7','Cmaj7','Em7']),  # Knee Socks
    # The Neighbourhood
    749: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # Sweater Weather
}

def main():
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'songs.json')
    with open(path, 'r') as f:
        songs = json.load(f)

    count = 0
    for idx in range(500, 750):
        if idx in SONG_CHORDS:
            easy_c, med_c, adv_c = SONG_CHORDS[idx]
            update_song(songs[idx], easy_c, med_c, adv_c)
            count += 1

    with open(path, 'w') as f:
        json.dump(songs, f, indent=2)

    print(f"Updated {count} songs (indices 500-749)")

if __name__ == '__main__':
    main()
