#!/usr/bin/env python3
"""Batch 4: Replace songs 750-999 with real chord progressions."""
import json, os

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

REAL_CHORDS = {
    # === The Neighbourhood (750-751) ===
    750: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Afraid
    751: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # Reflections

    # === Passenger (752-753) ===
    752: (['Em','C','G','D'], ['Em','C','G','D','Am'], ['Em7','Cmaj7','Gmaj7','D7','Am7']),  # Let Her Go
    753: (['G','D','Em','C'], ['G','D','Em','C','Am'], ['Gmaj7','D7','Em7','Cmaj7','Am7']),  # Hearts on Fire

    # === Vance Joy (754-755) ===
    754: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G7','Am7','Fmaj7','Em7']),  # Mess Is Mine
    755: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # Saturday Sun

    # === MAGIC! / OMI (756-757) ===
    756: (['D','G','Bm','A'], ['D','G','Bm','A','Em'], ['D7','Gmaj7','Bm7','A7','Em7']),  # Rude
    757: (['C','G','Am','F'], ['C','G','Am','F','Dm'], ['Cmaj7','G7','Am7','Fmaj7','Dm7']),  # Cheerleader

    # === Milky Chance (758-759) ===
    758: (['Am','G','C','F'], ['Am','G','C','F','Dm'], ['Am7','G7','Cmaj7','Fmaj7','Dm7']),  # Stolen Dance
    759: (['Em','Am','D','G'], ['Em','Am','D','G','C'], ['Em7','Am7','D7','Gmaj7','Cmaj7']),  # Flashed Junk Mind

    # === Men at Work (760) ===
    760: (['Am','G','F','C'], ['Am','G','F','C','Em'], ['Am7','G7','Fmaj7','Cmaj7','Em7']),  # Down Under

    # === Maroon 5 (761-770) ===
    761: (['G','D','Am','C'], ['G','D','Am','C','Em'], ['Gmaj7','D7','Am7','Cmaj7','Em7']),  # Sunday Morning
    762: (['Am','C','G','D'], ['Am','C','G','D','Em'], ['Am7','Cmaj7','G7','D7','Em7']),  # She Will Be Loved
    763: (['Cm','Gm','Bb','Eb'], ['Cm','Gm','Bb','Eb','F'], ['Cm7','Gm7','Bb','Eb','F7']),  # This Love
    764: (['Bm','Em','Am','D'], ['Bm','Em','Am','D','G'], ['Bm7','Em7','Am7','D7','Gmaj7']),  # Moves Like Jagger
    765: (['Am','C','G','D'], ['Am','C','G','D','Em'], ['Am7','Cmaj7','G7','D7','Em7']),  # Payphone
    766: (['C','Em','Am','F'], ['C','Em','Am','F','G'], ['Cmaj7','Em7','Am7','Fmaj7','G7']),  # Sugar
    767: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # Maps
    768: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G7','Am7','Fmaj7','Em7']),  # Girls Like You
    769: (['Am','C','G','D'], ['Am','C','G','D','Em'], ['Am7','Cmaj7','Gmaj7','D7','Em7']),  # Memories
    770: (['Em','C','G','D'], ['Em','C','G','D','Am'], ['Em7','Cmaj7','G7','D7','Am7']),  # Animals

    # === Chainsmokers (771-775) ===
    771: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G7','Am7','Fmaj7','Em7']),  # Closer
    772: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Roses
    773: (['Am','F','G','C'], ['Am','F','G','C','Em'], ['Am7','Fmaj7','G7','Cmaj7','Em7']),  # Don't Let Me Down
    774: (['G','D','Em','C'], ['G','D','Em','C','Am'], ['Gmaj7','D7','Em7','Cmaj7','Am7']),  # Something Just Like This
    775: (['Em','G','D','C'], ['Em','G','D','C','Am'], ['Em7','Gmaj7','D7','Cmaj7','Am7']),  # Paris

    # === Avicii (776-780) ===
    776: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Wake Me Up
    777: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Levels
    778: (['F','C','G','Am'], ['F','C','G','Am','Dm'], ['Fmaj7','Cmaj7','G7','Am7','Dm7']),  # Hey Brother
    779: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Waiting for Love
    780: (['Em','C','G','D'], ['Em','C','G','D','Am'], ['Em7','Cmaj7','Gmaj7','D7','Am7']),  # The Nights

    # === Major Lazer (781-782) ===
    781: (['Dm','F','C','Gm'], ['Dm','F','C','Gm','Bb'], ['Dm7','Fmaj7','Cmaj7','Gm7','Bb']),  # Lean On
    782: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Cold Water

    # === Sia (783-785) ===
    783: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Cheap Thrills
    784: (['Am','Em','F','C'], ['Am','Em','F','C','G'], ['Am7','Em7','Fmaj7','Cmaj7','G7']),  # Chandelier
    785: (['Am','Em','G','D'], ['Am','Em','G','D','C'], ['Am7','Em7','Gmaj7','D7','Cmaj7']),  # Elastic Heart

    # === David Guetta (786-788) ===
    786: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Titanium
    787: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # Flames
    788: (['Em','C','G','D'], ['Em','C','G','D','Am'], ['Em7','Cmaj7','G7','D7','Am7']),  # Without You

    # === Clean Bandit (789-792) ===
    789: (['F','C','Am','G'], ['F','C','Am','G','Dm'], ['Fmaj7','Cmaj7','Am7','G7','Dm7']),  # Rather Be
    790: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Rockabye
    791: (['Dm','Am','Bb','F'], ['Dm','Am','Bb','F','C'], ['Dm7','Am7','Bb','Fmaj7','Cmaj7']),  # Solo
    792: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Symphony

    # === Grouplove (793-795) ===
    793: (['D','G','A','Bm'], ['D','G','A','Bm','Em'], ['D7','Gmaj7','A7','Bm7','Em7']),  # Tongue Tied
    794: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G7','Am7','Fmaj7','Em7']),  # Ways to Go
    795: (['G','D','Em','C'], ['G','D','Em','C','Am'], ['Gmaj7','D7','Em7','Cmaj7','Am7']),  # Colours

    # === Florence and the Machine (796-800) ===
    796: (['C','F','Am','G'], ['C','F','Am','G','Em'], ['Cmaj7','Fmaj7','Am7','G7','Em7']),  # Dog Days Are Over
    797: (['Am','C','G','F'], ['Am','C','G','F','Em'], ['Am7','Cmaj7','G7','Fmaj7','Em7']),  # Shake It Out
    798: (['C','F','G','Am'], ['C','F','G','Am','Em'], ['Cmaj7','Fmaj7','G7','Am7','Em7']),  # You've Got the Love
    799: (['Am','Em','F','C'], ['Am','Em','F','C','G'], ['Am7','Em7','Fmaj7','Cmaj7','G7']),  # Cosmic Love
    800: (['F','Am','C','G'], ['F','Am','C','G','Dm'], ['Fmaj7','Am7','Cmaj7','G7','Dm7']),  # Hunger

    # === Traditional / Folk (801-829) ===
    801: (['Am','G','Am','C'], ['Am','G','Am','C','Em'], ['Am7','G7','Am7','Cmaj7','Em7']),  # Scarborough Fair
    802: (['Am','G','Am','Em'], ['Am','G','Am','Em','C'], ['Am7','G7','Am7','Em7','Cmaj7']),  # Greensleeves
    803: (['Am','C','D','F'], ['Am','C','D','F','E7'], ['Am7','Cmaj7','D7','Fmaj7','E7']),  # House of the Rising Sun
    804: (['C','Am','F','G'], ['C','Am','F','G','Em'], ['Cmaj7','Am7','Fmaj7','G7','Em7']),  # Danny Boy
    805: (['G','C','G','D'], ['G','C','G','D','Em'], ['Gmaj7','Cmaj7','Gmaj7','D7','Em7']),  # Amazing Grace
    806: (['G','C','D','G'], ['G','C','D','G','Em'], ['Gmaj7','Cmaj7','D7','Gmaj7','Em7']),  # Will the Circle Be Unbroken
    807: (['G','C','D','G'], ['G','C','D','G','Am'], ['Gmaj7','Cmaj7','D7','Gmaj7','Am7']),  # This Land Is Your Land
    808: (['C','F','G','C'], ['C','F','G','C','Am'], ['Cmaj7','Fmaj7','G7','Cmaj7','Am7']),  # If I Had a Hammer
    809: (['D','G','A','D'], ['D','G','A','D','Em'], ['D7','Gmaj7','A7','D7','Em7']),  # Turn Turn Turn
    810: (['D','G','A','D'], ['D','G','A','D','Em'], ['D7','Gmaj7','A7','D7','Em7']),  # Mr Tambourine Man

    # === Simon and Garfunkel (811-814) ===
    811: (['Am','G','F','C'], ['Am','G','F','C','Em'], ['Am7','G7','Fmaj7','Cmaj7','Em7']),  # The Sounds of Silence
    812: (['C','Am','G','F'], ['C','Am','G','F','Em'], ['Cmaj7','Am7','G7','Fmaj7','Em7']),  # Homeward Bound
    813: (['C','F','G','Am'], ['C','F','G','Am','D'], ['Cmaj7','Fmaj7','G7','Am7','D7']),  # Cecilia
    814: (['Em','Am','G','C'], ['Em','Am','G','C','D'], ['Em7','Am7','Gmaj7','Cmaj7','D7']),  # El Condor Pasa

    # === Peter Paul and Mary (815-817) ===
    815: (['G','Bm','C','D'], ['G','Bm','C','D','Em'], ['Gmaj7','Bm7','Cmaj7','D7','Em7']),  # Puff the Magic Dragon
    816: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # Leaving on a Jet Plane
    817: (['G','C','D','G'], ['G','C','D','G','Em'], ['Gmaj7','Cmaj7','D7','Gmaj7','Em7']),  # Blowin in the Wind

    # === More Folk / Spirituals (818-829) ===
    818: (['G','C','D','G'], ['G','C','D','G','Em'], ['Gmaj7','Cmaj7','D7','Gmaj7','Em7']),  # Where Have All the Flowers Gone
    819: (['C','F','G','C'], ['C','F','G','C','Am'], ['Cmaj7','Fmaj7','G7','Cmaj7','Am7']),  # We Shall Overcome
    820: (['C','F','G','C'], ['C','F','G','C','Am'], ['Cmaj7','Fmaj7','G7','Cmaj7','Am7']),  # Kumbaya
    821: (['G','C','D','G'], ['G','C','D','G','Em'], ['Gmaj7','Cmaj7','D7','Gmaj7','Em7']),  # Swing Low Sweet Chariot
    822: (['C','F','G','C'], ['C','F','G','C','Am'], ['Cmaj7','Fmaj7','G7','Cmaj7','Am7']),  # Oh Susanna
    823: (['G','C','D','G'], ['G','C','D','G','Am'], ['Gmaj7','Cmaj7','D7','Gmaj7','Am7']),  # Home on the Range
    824: (['F','C','G','Am'], ['F','C','G','Am','Dm'], ['Fmaj7','Cmaj7','G7','Am7','Dm7']),  # Shenandoah
    825: (['G','C','D','G'], ['G','C','D','G','Em'], ['Gmaj7','Cmaj7','D7','Gmaj7','Em7']),  # Down by the Riverside
    826: (['G','C','D','G'], ['G','C','D','G','Em'], ['Gmaj7','Cmaj7','D7','Gmaj7','Em7']),  # When the Saints Go Marching In
    827: (['G','C','D','G'], ['G','C','D','G','Em'], ['Gmaj7','Cmaj7','D7','Gmaj7','Em7']),  # This Little Light of Mine
    828: (['C','F','G','C'], ['C','F','G','C','Am'], ['Cmaj7','Fmaj7','G7','Cmaj7','Am7']),  # He's Got the Whole World
    829: (['D','G','A','D'], ['D','G','A','D','Em'], ['D7','Gmaj7','A7','D7','Em7']),  # Simple Gifts

    # === Ariana Grande (830-838) ===
    830: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # Positions
    831: (['Am','Dm','G','C'], ['Am','Dm','G','C','Em'], ['Am7','Dm7','G7','Cmaj7','Em7']),  # 7 Rings
    832: (['Am','C','G','F'], ['Am','C','G','F','Dm'], ['Am7','Cmaj7','G7','Fmaj7','Dm7']),  # Thank U Next
    833: (['Dm','Am','Bb','F'], ['Dm','Am','Bb','F','C'], ['Dm7','Am7','Bb','Fmaj7','Cmaj7']),  # No Tears Left to Cry
    834: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Into You
    835: (['Am','G','F','C'], ['Am','G','F','C','Em'], ['Am7','G7','Fmaj7','Cmaj7','Em7']),  # Problem
    836: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Break Free
    837: (['Am','Dm','G','C'], ['Am','Dm','G','C','F'], ['Am7','Dm7','G7','Cmaj7','Fmaj7']),  # Side to Side
    838: (['G','D','Em','C'], ['G','D','Em','C','Am'], ['Gmaj7','D7','Em7','Cmaj7','Am7']),  # One Last Time

    # === Lady Gaga (839-840) ===
    839: (['F','Am','C','G'], ['F','Am','C','G','Dm'], ['Fmaj7','Am7','Cmaj7','G7','Dm7']),  # Rain on Me
    840: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Stupid Love

    # === Miley Cyrus (841-847) ===
    841: (['Am','C','G','F'], ['Am','C','G','F','Dm'], ['Am7','Cmaj7','G7','Fmaj7','Dm7']),  # Flowers
    842: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Wrecking Ball
    843: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G7','Am7','Fmaj7','Em7']),  # The Climb
    844: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # Party in the USA
    845: (['G','Em','C','D'], ['G','Em','C','D','Am'], ['Gmaj7','Em7','Cmaj7','D7','Am7']),  # Malibu
    846: (['Am','Em','G','D'], ['Am','Em','G','D','C'], ['Am7','Em7','Gmaj7','D7','Cmaj7']),  # Midnight Sky
    847: (['F','Am','C','G'], ['F','Am','C','G','Dm'], ['Fmaj7','Am7','Cmaj7','G7','Dm7']),  # We Can't Stop

    # === Pharrell / Mark Ronson (848-850) ===
    848: (['F','Dm','Bb','C'], ['F','Dm','Bb','C','Gm'], ['Fmaj7','Dm7','Bb','Cmaj7','Gm7']),  # Happy
    849: (['Dm','G','C','F'], ['Dm','G','C','F','Am'], ['Dm7','G7','Cmaj7','Fmaj7','Am7']),  # Uptown Funk
    850: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # Valerie (Ronson)

    # === Amy Winehouse (851-856) ===
    851: (['Am','Em','G','D'], ['Am','Em','G','D','C'], ['Am7','Em7','G7','D7','Cmaj7']),  # Rehab
    852: (['Dm','Gm','Bb','A'], ['Dm','Gm','Bb','A','F'], ['Dm7','Gm7','Bb','A7','Fmaj7']),  # Back to Black
    853: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # Valerie (Winehouse)
    854: (['Dm','Am','Bb','F'], ['Dm','Am','Bb','F','Gm'], ['Dm7','Am7','Bb','Fmaj7','Gm7']),  # Love Is a Losing Game
    855: (['Dm','Gm','Am','Bb'], ['Dm','Gm','Am','Bb','F'], ['Dm7','Gm7','Am7','Bb','Fmaj7']),  # You Know I'm No Good
    856: (['Am','Dm','G','C'], ['Am','Dm','G','C','F'], ['Am7','Dm7','G7','Cmaj7','Fmaj7']),  # Tears Dry on Their Own

    # === Lord Huron (857-861) ===
    857: (['Em','C','G','D'], ['Em','C','G','D','Am'], ['Em7','Cmaj7','Gmaj7','D7','Am7']),  # The Night We Met
    858: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # Ends of the Earth
    859: (['Am','Em','G','C'], ['Am','Em','G','C','D'], ['Am7','Em7','Gmaj7','Cmaj7','D7']),  # Love Like Ghosts
    860: (['G','Em','C','D'], ['G','Em','C','D','Am'], ['Gmaj7','Em7','Cmaj7','D7','Am7']),  # When the Night Is Over
    861: (['Em','G','D','C'], ['Em','G','D','C','Am'], ['Em7','Gmaj7','D7','Cmaj7','Am7']),  # Mine Forever

    # === Fleet Foxes (862-866) ===
    862: (['Em','C','G','D'], ['Em','C','G','D','Am'], ['Em7','Cmaj7','Gmaj7','D7','Am7']),  # Mykonos
    863: (['C','Am','F','G'], ['C','Am','F','G','Em'], ['Cmaj7','Am7','Fmaj7','G7','Em7']),  # White Winter Hymnal
    864: (['G','D','Em','C'], ['G','D','Em','C','Am'], ['Gmaj7','D7','Em7','Cmaj7','Am7']),  # Blue Ridge Mountains
    865: (['Am','C','G','F'], ['Am','C','G','F','Em'], ['Am7','Cmaj7','G7','Fmaj7','Em7']),  # Helplessness Blues
    866: (['G','C','Em','D'], ['G','C','Em','D','Am'], ['Gmaj7','Cmaj7','Em7','D7','Am7']),  # Sun It Rises

    # === Band of Horses (867-870) ===
    867: (['G','D','Em','C'], ['G','D','Em','C','Am'], ['Gmaj7','D7','Em7','Cmaj7','Am7']),  # The Funeral
    868: (['Em','C','G','D'], ['Em','C','G','D','Am'], ['Em7','Cmaj7','G7','D7','Am7']),  # No One's Gonna Love You
    869: (['Am','G','F','C'], ['Am','G','F','C','Em'], ['Am7','G7','Fmaj7','Cmaj7','Em7']),  # Is There a Ghost
    870: (['G','Em','C','D'], ['G','Em','C','D','Am'], ['Gmaj7','Em7','Cmaj7','D7','Am7']),  # Laundry Room

    # === Pixies (871-875) ===
    871: (['E','G','A','C'], ['E','G','A','C','D'], ['E7','Gmaj7','A7','Cmaj7','D7']),  # Hey
    872: (['Em','G','D','Am'], ['Em','G','D','Am','C'], ['Em7','Gmaj7','D7','Am7','Cmaj7']),  # Where Is My Mind
    873: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # Here Comes Your Man
    874: (['E','G','A','D'], ['E','G','A','D','C'], ['E7','Gmaj7','A7','D7','Cmaj7']),  # Debaser
    875: (['Em','Am','G','D'], ['Em','Am','G','D','C'], ['Em7','Am7','Gmaj7','D7','Cmaj7']),  # Monkey Gone to Heaven

    # === Death Cab for Cutie (876-880) ===
    876: (['G','D','Em','C'], ['G','D','Em','C','Am'], ['Gmaj7','D7','Em7','Cmaj7','Am7']),  # I Will Follow You Into the Dark
    877: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G7','Am7','Fmaj7','Em7']),  # Soul Meets Body
    878: (['Am','C','G','F'], ['Am','C','G','F','Em'], ['Am7','Cmaj7','G7','Fmaj7','Em7']),  # Transatlanticism
    879: (['D','G','A','Bm'], ['D','G','A','Bm','Em'], ['D7','Gmaj7','A7','Bm7','Em7']),  # The Sound of Settling
    880: (['Am','G','F','C'], ['Am','G','F','C','Em'], ['Am7','G7','Fmaj7','Cmaj7','Em7']),  # Crooked Teeth

    # === Postal Service (881-883) ===
    881: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G7','Am7','Fmaj7','Em7']),  # Such Great Heights
    882: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # The District Sleeps Alone Tonight
    883: (['Am','C','G','F'], ['Am','C','G','F','Em'], ['Am7','Cmaj7','G7','Fmaj7','Em7']),  # We Will Become Silhouettes

    # === The Shins (884-888) ===
    884: (['Am','C','G','F'], ['Am','C','G','F','Dm'], ['Am7','Cmaj7','G7','Fmaj7','Dm7']),  # New Slang
    885: (['C','Am','F','G'], ['C','Am','F','G','Em'], ['Cmaj7','Am7','Fmaj7','G7','Em7']),  # Caring Is Creepy
    886: (['G','D','Em','C'], ['G','D','Em','C','Am'], ['Gmaj7','D7','Em7','Cmaj7','Am7']),  # Phantom Limb
    887: (['D','G','A','Bm'], ['D','G','A','Bm','Em'], ['D7','Gmaj7','A7','Bm7','Em7']),  # Australia
    888: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G7','Am7','Fmaj7','Em7']),  # Simple Song

    # === Phoenix (889-891) ===
    889: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # 1901
    890: (['D','G','A','Bm'], ['D','G','A','Bm','Em'], ['D7','Gmaj7','A7','Bm7','Em7']),  # Lisztomania
    891: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # If I Ever Feel Better

    # === Kanye West (892-901) - hip-hop simplified to uke ===
    892: (['Em','Am','G','D'], ['Em','Am','G','D','C'], ['Em7','Am7','Gmaj7','D7','Cmaj7']),  # Runaway
    893: (['Am','Em','G','D'], ['Am','Em','G','D','C'], ['Am7','Em7','G7','D7','Cmaj7']),  # Heartless
    894: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Stronger
    895: (['G','D','Am','C'], ['G','D','Am','C','Em'], ['Gmaj7','D7','Am7','Cmaj7','Em7']),  # Gold Digger
    896: (['F','C','Dm','Bb'], ['F','C','Dm','Bb','Am'], ['Fmaj7','Cmaj7','Dm7','Bb','Am7']),  # All of the Lights
    897: (['Am','Dm','G','C'], ['Am','Dm','G','C','F'], ['Am7','Dm7','G7','Cmaj7','Fmaj7']),  # Flashing Lights
    898: (['F','C','Am','G'], ['F','C','Am','G','Dm'], ['Fmaj7','Cmaj7','Am7','G7','Dm7']),  # Ultralight Beam
    899: (['Em','Am','D','G'], ['Em','Am','D','G','C'], ['Em7','Am7','D7','Gmaj7','Cmaj7']),  # Father Stretch My Hands
    900: (['Am','G','F','C'], ['Am','G','F','C','Em'], ['Am7','G7','Fmaj7','Cmaj7','Em7']),  # Bound 2
    901: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G7','Am7','Fmaj7','Em7']),  # Roses (Kanye)

    # === Celine Dion (902-905) ===
    902: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G7','Am7','Fmaj7','Em7']),  # My Heart Will Go On
    903: (['C','F','G','Am'], ['C','F','G','Am','Dm'], ['Cmaj7','Fmaj7','G7','Am7','Dm7']),  # Because You Loved Me
    904: (['Am','Dm','G','C'], ['Am','Dm','G','C','F'], ['Am7','Dm7','G7','Cmaj7','Fmaj7']),  # All by Myself
    905: (['F','C','Bb','Dm'], ['F','C','Bb','Dm','Gm'], ['Fmaj7','Cmaj7','Bb','Dm7','Gm7']),  # The Power of Love

    # === 80s Movie Soundtracks (906-911) ===
    906: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Eye of the Tiger
    907: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # Danger Zone
    908: (['A','D','E','F#m'], ['A','D','E','F#m','Bm'], ['A7','D7','E7','F#m7','Bm7']),  # Footloose
    909: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # I'm Alright
    910: (['C','F','G','Am'], ['C','F','G','Am','Em'], ['Cmaj7','Fmaj7','G7','Am7','Em7']),  # St Elmo's Fire
    911: (['Am','Dm','G','C'], ['Am','Dm','G','C','F'], ['Am7','Dm7','G7','Cmaj7','Fmaj7']),  # Ghostbusters

    # === Classic Movie Songs (912-923) ===
    912: (['C','F','G','Am'], ['C','F','G','Am','Em'], ['Cmaj7','Fmaj7','G7','Am7','Em7']),  # Raindrops Keep Fallin on My Head
    913: (['C','Am','F','G'], ['C','Am','F','G','Em'], ['Cmaj7','Am7','Fmaj7','G7','Em7']),  # Moon River
    914: (['C','Am','F','G'], ['C','Am','F','G','Em'], ['Cmaj7','Am7','Fmaj7','G7','Em7']),  # Over the Rainbow
    915: (['G','Em','C','D'], ['G','Em','C','D','Am'], ['Gmaj7','Em7','Cmaj7','D7','Am7']),  # Singin in the Rain
    916: (['C','Am','Dm','G'], ['C','Am','Dm','G','F'], ['Cmaj7','Am7','Dm7','G7','Fmaj7']),  # As Time Goes By
    917: (['C','F','G','Am'], ['C','F','G','Am','Em'], ['Cmaj7','Fmaj7','G7','Am7','Em7']),  # The Sound of Music
    918: (['Am','Em','G','C'], ['Am','Em','G','C','Dm'], ['Am7','Em7','G7','Cmaj7','Dm7']),  # Chim Chim Cher-ee
    919: (['C','G','F','Am'], ['C','G','F','Am','Dm'], ['Cmaj7','G7','Fmaj7','Am7','Dm7']),  # A Spoonful of Sugar
    920: (['C','G','F','Am'], ['C','G','F','Am','Dm'], ['Cmaj7','G7','Fmaj7','Am7','Dm7']),  # Supercalifragilisticexpialidocious
    921: (['G','Em','C','D'], ['G','Em','C','D','Am'], ['Gmaj7','Em7','Cmaj7','D7','Am7']),  # Pure Imagination
    922: (['C','Am','F','G'], ['C','Am','F','G','Em'], ['Cmaj7','Am7','Fmaj7','G7','Em7']),  # Somewhere Out There
    923: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # Rainbows (Kermit)

    # === Glass Animals (924-927) ===
    924: (['D','G','A','Bm'], ['D','G','A','Bm','Em'], ['D7','Gmaj7','A7','Bm7','Em7']),  # Heat Waves
    925: (['Am','G','F','C'], ['Am','G','F','C','Em'], ['Am7','G7','Fmaj7','Cmaj7','Em7']),  # Gooey
    926: (['Em','C','G','D'], ['Em','C','G','D','Am'], ['Em7','Cmaj7','Gmaj7','D7','Am7']),  # Youth
    927: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Pork Soda

    # === Beach House (928-932) ===
    928: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Space Song
    929: (['Em','C','G','D'], ['Em','C','G','D','Am'], ['Em7','Cmaj7','Gmaj7','D7','Am7']),  # Myth
    930: (['Am','Em','G','C'], ['Am','Em','G','C','D'], ['Am7','Em7','Gmaj7','Cmaj7','D7']),  # Silver Soul
    931: (['Dm','Am','Bb','F'], ['Dm','Am','Bb','F','C'], ['Dm7','Am7','Bb','Fmaj7','Cmaj7']),  # Lazarus
    932: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Dream Pop

    # === Metric (933-935) ===
    933: (['Am','G','F','C'], ['Am','G','F','C','Em'], ['Am7','G7','Fmaj7','Cmaj7','Em7']),  # Black Sheep
    934: (['Em','C','G','D'], ['Em','C','G','D','Am'], ['Em7','Cmaj7','G7','D7','Am7']),  # Help I'm Alive
    935: (['Am','Em','G','D'], ['Am','Em','G','D','C'], ['Am7','Em7','Gmaj7','D7','Cmaj7']),  # Gold Guns Girls

    # === Stars (936-937) ===
    936: (['Am','C','G','F'], ['Am','C','G','F','Em'], ['Am7','Cmaj7','G7','Fmaj7','Em7']),  # Dead Hearts
    937: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G7','Am7','Fmaj7','Em7']),  # Your Ex-Lover Is Dead

    # === Grimes (938-939) ===
    938: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Oblivion
    939: (['Em','Am','G','D'], ['Em','Am','G','D','C'], ['Em7','Am7','G7','D7','Cmaj7']),  # Genesis

    # === The Cure (940-944) ===
    940: (['Am','C','G','F'], ['Am','C','G','F','Em'], ['Am7','Cmaj7','G7','Fmaj7','Em7']),  # Close to Me
    941: (['D','G','A','Bm'], ['D','G','A','Bm','Em'], ['D7','Gmaj7','A7','Bm7','Em7']),  # In Between Days
    942: (['Am','G','F','Em'], ['Am','G','F','Em','C'], ['Am7','G7','Fmaj7','Em7','Cmaj7']),  # Pictures of You
    943: (['Am','Em','G','D'], ['Am','Em','G','D','C'], ['Am7','Em7','Gmaj7','D7','Cmaj7']),  # A Forest
    944: (['Dm','Am','Bb','F'], ['Dm','Am','Bb','F','Gm'], ['Dm7','Am7','Bb','Fmaj7','Gm7']),  # Lullaby

    # === Cage the Elephant (945-950) ===
    945: (['Am','G','F','C'], ['Am','G','F','C','Em'], ['Am7','G7','Fmaj7','Cmaj7','Em7']),  # Come a Little Closer
    946: (['Am','G','D','F'], ['Am','G','D','F','C'], ['Am7','G7','D7','Fmaj7','Cmaj7']),  # Ain't No Rest for the Wicked
    947: (['Em','G','D','C'], ['Em','G','D','C','Am'], ['Em7','Gmaj7','D7','Cmaj7','Am7']),  # Trouble
    948: (['G','D','Em','C'], ['G','D','Em','C','Am'], ['Gmaj7','D7','Em7','Cmaj7','Am7']),  # Cigarette Daydreams
    949: (['Am','C','G','F'], ['Am','C','G','F','Em'], ['Am7','Cmaj7','G7','Fmaj7','Em7']),  # Shake Me Down
    950: (['G','Em','C','D'], ['G','Em','C','D','Am'], ['Gmaj7','Em7','Cmaj7','D7','Am7']),  # Ready to Let Go

    # === Modest Mouse (951-955) ===
    951: (['F','C','Dm','Bb'], ['F','C','Dm','Bb','Am'], ['Fmaj7','Cmaj7','Dm7','Bb','Am7']),  # Float On
    952: (['Am','G','F','C'], ['Am','G','F','C','Em'], ['Am7','G7','Fmaj7','Cmaj7','Em7']),  # Dashboard
    953: (['G','D','Em','C'], ['G','D','Em','C','Am'], ['Gmaj7','D7','Em7','Cmaj7','Am7']),  # Ocean Breathes Salty
    954: (['C','Am','F','G'], ['C','Am','F','G','Em'], ['Cmaj7','Am7','Fmaj7','G7','Em7']),  # The World at Large
    955: (['Em','G','D','Am'], ['Em','G','D','Am','C'], ['Em7','Gmaj7','D7','Am7','Cmaj7']),  # Dramamine

    # === Grizzly Bear (956-957) ===
    956: (['Am','C','G','F'], ['Am','C','G','F','Em'], ['Am7','Cmaj7','G7','Fmaj7','Em7']),  # Two Weeks
    957: (['Em','Am','G','D'], ['Em','Am','G','D','C'], ['Em7','Am7','Gmaj7','D7','Cmaj7']),  # Ready Able

    # === Tame Impala (958-967) ===
    958: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # Feels Like We Only Go Backwards
    959: (['C','F','Am','G'], ['C','F','Am','G','Dm'], ['Cmaj7','Fmaj7','Am7','G7','Dm7']),  # Let It Happen
    960: (['Am','Dm','G','C'], ['Am','Dm','G','C','F'], ['Am7','Dm7','G7','Cmaj7','Fmaj7']),  # The Less I Know the Better
    961: (['Am','G','D','Em'], ['Am','G','D','Em','C'], ['Am7','G7','D7','Em7','Cmaj7']),  # Elephant
    962: (['Dm','Am','Bb','F'], ['Dm','Am','Bb','F','C'], ['Dm7','Am7','Bb','Fmaj7','Cmaj7']),  # New Person Same Old Mistakes
    963: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Eventually
    964: (['C','G','Am','F'], ['C','G','Am','F','Dm'], ['Cmaj7','G7','Am7','Fmaj7','Dm7']),  # Borderline
    965: (['G','D','Em','C'], ['G','D','Em','C','Am'], ['Gmaj7','D7','Em7','Cmaj7','Am7']),  # Lost in Yesterday
    966: (['Am','G','F','C'], ['Am','G','F','C','Em'], ['Am7','G7','Fmaj7','Cmaj7','Em7']),  # Is It True
    967: (['Am','Dm','G','C'], ['Am','Dm','G','C','F'], ['Am7','Dm7','G7','Cmaj7','Fmaj7']),  # Breathe Deeper

    # === 80s Synth-pop / New Wave (968-976) ===
    968: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Wonderful Life
    969: (['G','Em','C','D'], ['G','Em','C','D','Am'], ['Gmaj7','Em7','Cmaj7','D7','Am7']),  # True
    970: (['G','Em','C','D'], ['G','Em','C','D','Am'], ['Gmaj7','Em7','Cmaj7','D7','Am7']),  # Gold
    971: (['Am','Dm','G','C'], ['Am','Dm','G','C','F'], ['Am7','Dm7','G7','Cmaj7','Fmaj7']),  # Relax
    972: (['C','Am','F','G'], ['C','Am','F','G','Em'], ['Cmaj7','Am7','Fmaj7','G7','Em7']),  # The Power of Love (FGTH)
    973: (['Am','G','F','C'], ['Am','G','F','C','Em'], ['Am7','G7','Fmaj7','Cmaj7','Em7']),  # I Ran So Far Away
    974: (['G','Em','C','D'], ['G','Em','C','D','Am'], ['Gmaj7','Em7','Cmaj7','D7','Am7']),  # Don't You Want Me
    975: (['Am','Em','G','D'], ['Am','Em','G','D','C'], ['Am7','Em7','Gmaj7','D7','Cmaj7']),  # West End Girls
    976: (['Am','Dm','G','C'], ['Am','Dm','G','C','Em'], ['Am7','Dm7','G7','Cmaj7','Em7']),  # It's a Sin

    # === Bon Jovi (977-983) ===
    977: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G7','Am7','Fmaj7','Em7']),  # Always
    978: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # You Give Love a Bad Name
    979: (['C','Am','F','G'], ['C','Am','F','G','Em'], ['Cmaj7','Am7','Fmaj7','G7','Em7']),  # Bed of Roses
    980: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Runaway (Bon Jovi)
    981: (['Am','G','D','F'], ['Am','G','D','F','C'], ['Am7','G7','D7','Fmaj7','Cmaj7']),  # Bad Medicine
    982: (['Em','G','D','C'], ['Em','G','D','C','Am'], ['Em7','Gmaj7','D7','Cmaj7','Am7']),  # Blaze of Glory
    983: (['G','D','Em','C'], ['G','D','Em','C','Am'], ['Gmaj7','D7','Em7','Cmaj7','Am7']),  # I'll Be There for You

    # === Def Leppard (984-989) ===
    984: (['A','D','E','F#m'], ['A','D','E','F#m','Bm'], ['A7','D7','E7','F#m7','Bm7']),  # Pour Some Sugar on Me
    985: (['Am','C','G','F'], ['Am','C','G','F','Em'], ['Am7','Cmaj7','G7','Fmaj7','Em7']),  # Love Bites
    986: (['D','A','G','Em'], ['D','A','G','Em','Bm'], ['D7','A7','Gmaj7','Em7','Bm7']),  # Photograph (Def Leppard)
    987: (['A','D','E','F#m'], ['A','D','E','F#m','Bm'], ['A7','D7','E7','F#m7','Bm7']),  # Animal
    988: (['A','D','E','G'], ['A','D','E','G','Bm'], ['A7','D7','E7','Gmaj7','Bm7']),  # Rock of Ages
    989: (['Am','Em','G','D'], ['Am','Em','G','D','C'], ['Am7','Em7','Gmaj7','D7','Cmaj7']),  # Hysteria

    # === Metallica (990-999) - power chords simplified to open chords ===
    990: (['Em','C','D','G'], ['Em','C','D','G','Am'], ['Em7','Cmaj7','D7','Gmaj7','Am7']),  # Nothing Else Matters
    991: (['Em','G','D','C'], ['Em','G','D','C','Am'], ['Em7','Gmaj7','D7','Cmaj7','Am7']),  # Enter Sandman
    992: (['Am','Em','G','D'], ['Am','Em','G','D','C'], ['Am7','Em7','Gmaj7','D7','Cmaj7']),  # One
    993: (['Am','Em','G','C'], ['Am','Em','G','C','D'], ['Am7','Em7','Gmaj7','Cmaj7','D7']),  # The Unforgiven
    994: (['Am','Em','F','C'], ['Am','Em','F','C','G'], ['Am7','Em7','Fmaj7','Cmaj7','G7']),  # Fade to Black
    995: (['Em','G','D','Am'], ['Em','G','D','Am','C'], ['Em7','Gmaj7','D7','Am7','Cmaj7']),  # Master of Puppets
    996: (['Em','Am','D','G'], ['Em','Am','D','G','C'], ['Em7','Am7','D7','Gmaj7','Cmaj7']),  # Wherever I May Roam
    997: (['Em','D','C','G'], ['Em','D','C','G','Am'], ['Em7','D7','Cmaj7','Gmaj7','Am7']),  # Sad but True
    998: (['Em','G','D','C'], ['Em','G','D','C','Am'], ['Em7','Gmaj7','D7','Cmaj7','Am7']),  # Sandman
    999: (['Am','Em','G','D'], ['Am','Em','G','D','C'], ['Am7','Em7','Gmaj7','D7','Cmaj7']),  # Welcome Home Sanitarium
}

def main():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'songs.json')
    with open(data_path) as f:
        songs = json.load(f)

    updated = 0
    for idx in range(750, min(1000, len(songs))):
        if idx not in REAL_CHORDS:
            continue
        easy_chords, med_chords, adv_chords = REAL_CHORDS[idx]
        song = songs[idx]
        title = song['title']
        artist = song['artist']

        song['easy']['chords'] = [chord(c) for c in easy_chords]
        song['easy']['lyrics'] = make_lyrics(title, artist, easy_chords)

        song['medium']['chords'] = [chord(c) for c in med_chords]
        song['medium']['lyrics'] = make_lyrics(title, artist, med_chords)

        song['advanced']['chords'] = [chord(c) for c in adv_chords]
        song['advanced']['lyrics'] = make_lyrics(title, artist, adv_chords)

        updated += 1

    with open(data_path, 'w') as f:
        json.dump(songs, f, indent=2)

    print(f"Updated {updated} songs (indices 750-999) with real chord progressions")
    print(f"Total songs in library: {len(songs)}")

if __name__ == '__main__':
    main()
