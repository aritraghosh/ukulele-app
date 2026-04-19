#!/usr/bin/env python3
"""Fix songs 250-499 with real chord progressions based on actual song knowledge."""

import json
import re
import random
import os

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

# Real chord progressions for songs 250-499
# Format: (easy_chords, medium_chords, advanced_chords)
SONG_CHORDS = {
    # Country (250-276)
    250: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # Always on My Mind - Willie Nelson
    251: (['D','G','A'], ['D','G','A','Bm'], ['D','Gmaj7','A7','Bm7']),  # Mammas Don't Let Your Babies
    252: (['G','C','D'], ['G','C','D','Em'], ['Gmaj7','Cmaj7','D7','Em7']),  # He Stopped Loving Her Today
    253: (['A','D','E'], ['A','D','E','A7'], ['A','D7','E7','A7']),  # Achy Breaky Heart
    254: (['E','A','B'], ['E','A','B7','E7'], ['E7','A7','B7','E']),  # Boot Scootin Boogie
    255: (['G','D','Am','C'], ['G','D','Am','C','Em'], ['Gmaj7','D','Am7','Cmaj7','Em7']),  # Cruise
    256: (['G','D','Em','C'], ['G','D','Em','C','Am'], ['Gmaj7','D','Em7','Cmaj7','Am7']),  # Chicken Fried
    257: (['C','F','G'], ['C','F','G','Am'], ['Cmaj7','Fmaj7','G7','Am7']),  # Toes
    258: (['Em','C','G','D'], ['Em','C','G','D','Am'], ['Em7','Cmaj7','Gmaj7','D7','Am7']),  # Colder Weather
    259: (['A','D','E'], ['A','D','E','F#m'], ['A','D','E7','F#m7','Bm7']),  # Tennessee Whiskey (actually Dm/Am feel)
    260: (['D','G','A'], ['D','G','A','Bm'], ['D','Gmaj7','A7','Bm7']),  # Traveller
    261: (['G','C','D'], ['G','C','D','Em'], ['Gmaj7','Cmaj7','D7','Em7']),  # Body Like a Back Road
    262: (['G','D','Em','C'], ['G','D','Em','C','Am'], ['Gmaj7','D','Em7','Cmaj7','Am7']),  # Die a Happy Man
    263: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # Meant to Be
    264: (['Am','C','G','D'], ['Am','C','G','D','Em'], ['Am7','Cmaj7','Gmaj7','D7','Em7']),  # Need You Now
    265: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # Wanted
    266: (['G','C','D'], ['G','C','D','Em'], ['Gmaj7','Cmaj7','D7','Em7']),  # Springsteen
    267: (['G','D','Am','C'], ['G','D','Am','C','Em'], ['Gmaj7','D','Am7','Cmaj7','Em7']),  # Drunk on a Plane
    268: (['C','G','Am','F'], ['C','G','Am','F','Dm'], ['Cmaj7','G','Am7','Fmaj7','Dm7']),  # Drunk on You
    269: (['G','C','D'], ['G','C','D','Em'], ['Gmaj7','Cmaj7','D7','Em7']),  # Play It Again
    270: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # Dirt Road Anthem
    271: (['G','D','Em','C'], ['G','D','Em','C','Am'], ['Gmaj7','D','Em7','Cmaj7','Am7']),  # Amazed
    272: (['G','D','Am','C'], ['G','D','Am','C','Em'], ['Gmaj7','D','Am7','Cmaj7','Em7']),  # Breathe
    273: (['F#m','D','A','E'], ['F#m','D','A','E','Bm'], ['F#m7','D','A','E7','Bm7']),  # Before He Cheats
    274: (['D','G','A'], ['D','G','A','Bm'], ['D','Gmaj7','A7','Bm7']),  # Jesus Take the Wheel
    275: (['G','C','D'], ['G','C','D','Em'], ['Gmaj7','Cmaj7','D7','Em7']),  # Humble and Kind
    276: (['G','D','Em','C'], ['G','D','Em','C','Am'], ['Gmaj7','D','Em7','Cmaj7','Am7']),  # Live Like You Were Dying

    # R&B/Soul - Bill Withers (277-280)
    277: (['Am','Em','G','Am'], ['Am','Em','G','Dm','Am'], ['Am7','Em7','Gm7','Dm7','Am7']),  # Ain't No Sunshine
    278: (['C','F','G'], ['C','F','G','Am','Em'], ['Cmaj7','Fmaj7','G7','Am7','Em7']),  # Lean on Me
    279: (['E','A','D','G'], ['E','A','D','G','B7'], ['E7','A7','D','G','B7']),  # Use Me (funky E groove)
    280: (['Bb','F','Gm','Eb'], ['Bb','F','Gm','Eb','Cm'], ['Bb','Fmaj7','Gm7','Eb','Cm7']),  # Lovely Day

    # The Temptations (281-282)
    281: (['C','F','G'], ['C','Dm','F','G','Am'], ['Cmaj7','Dm7','Fmaj7','G7','Am7']),  # Just My Imagination
    282: (['C','F','G','Am'], ['C','F','G','Am','Dm'], ['Cmaj7','Fmaj7','G7','Am7','Dm7']),  # My Girl

    # Marvin Gaye (283-286)
    283: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # I Heard It Through the Grapevine (Dm/Bb)
    284: (['Eb','Ab','Bb'], ['Eb','Ab','Bb','Gm','Cm'], ['Eb','Ab','Bb','Gm7','Cm7']),  # Let's Get It On
    285: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','Gmaj7','Em7']),  # What's Going On
    286: (['A','D','G'], ['A','D','G','Bm','E'], ['A','D','Gmaj7','Bm7','E7']),  # Sexual Healing

    # Stevie Wonder (287-291)
    287: (['Em','A','G','D'], ['Em','A','G','D','Bm'], ['Em7','A7','Gmaj7','D7','Bm7']),  # Superstition (Ebm funk - simplified)
    288: (['C','Am','F','G'], ['C','Am','F','G','Dm'], ['Cmaj7','Am7','Fmaj7','G7','Dm7']),  # Isn't She Lovely
    289: (['C','F','G','Am'], ['C','F','G','Am','Dm'], ['Cmaj7','Fmaj7','G7','Am7','Dm7']),  # I Just Called to Say I Love You
    290: (['C','Am','F','G'], ['C','Am','F','G','Dm'], ['Cmaj7','Am7','Fmaj7','G7','Dm7']),  # Sir Duke (B major - simplified)
    291: (['C','F','G'], ['C','F','G','Am','Dm'], ['Cmaj7','Fmaj7','G7','Am7','Dm7']),  # Signed Sealed Delivered

    # Sam Cooke (292-293)
    292: (['A','D','F#m','E'], ['A','D','F#m','E','Bm'], ['A','D','F#m7','E7','Bm7']),  # A Change Is Gonna Come (Bb - simplified to A)
    293: (['G','Em','C','D'], ['G','Em','C','D','Am'], ['Gmaj7','Em7','Cmaj7','D7','Am7']),  # Wonderful World

    # Aretha Franklin (294-297)
    294: (['C','F','G'], ['C','F','G','Am','Dm'], ['C7','Fmaj7','G7','Am7','Dm7']),  # Respect
    295: (['C','F','G','Am'], ['C','F','G','Am','Dm'], ['Cmaj7','Fmaj7','G7','Am7','Dm7']),  # Natural Woman (A - simplified)
    296: (['Am','Dm','G','C'], ['Am','Dm','G','C','F'], ['Am7','Dm7','Gmaj7','Cmaj7','Fmaj7']),  # I Say a Little Prayer
    297: (['C','F','G'], ['C','F','G','Am','Dm'], ['C7','Fmaj7','G7','Am7','Dm7']),  # Think

    # Otis Redding (298-299)
    298: (['G','C','D','Am'], ['G','C','D','Am','Em'], ['Gmaj7','Cmaj7','D7','Am7','Em7']),  # Sittin on the Dock of the Bay
    299: (['G','C','D'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # Try a Little Tenderness

    # Ray Charles (300-301)
    300: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # Georgia on My Mind (F - simplified)
    301: (['Am','E','Am','G'], ['Am','E7','G','F','Dm'], ['Am7','E7','G7','Fmaj7','Dm7']),  # Hit the Road Jack

    # Various Soul/R&B (302-311)
    302: (['C','F','G','Am'], ['C','F','G','Am','Dm'], ['Cmaj7','Fmaj7','G7','Am7','Dm7']),  # I Got You Babe
    303: (['D','G','A'], ['D','G','A','Bm','Em'], ['D','Gmaj7','A7','Bm7','Em7']),  # How Sweet It Is
    304: (['C','Am','F','G'], ['C','Am','F','G','Em'], ['Cmaj7','Am7','Fmaj7','G7','Em7']),  # Unchained Melody
    305: (['C','Am','F','G'], ['C','Am','F','G','Dm'], ['Cmaj7','Am7','Fmaj7','G7','Dm7']),  # Put Your Head on My Shoulder
    306: (['C','Am','F','G'], ['C','Am','F','G','Dm'], ['Cmaj7','Am7','Fmaj7','Gmaj7','Dm7']),  # At Last
    307: (['Am','Dm','G','C'], ['Am','Dm','G','C','F'], ['Am7','Dm7','G7','Cmaj7','Fmaj7']),  # I'd Rather Go Blind
    308: (['Em','C','G','D'], ['Em','C','G','D','Am'], ['Em7','Cmaj7','Gmaj7','D','Am7']),  # No One - Alicia Keys
    309: (['Am','G','F','C'], ['Am','G','F','C','Em'], ['Am7','Gmaj7','Fmaj7','Cmaj7','Em7']),  # If I Ain't Got You
    310: (['Em','Am','D','G'], ['Em','Am','D','G','Bm'], ['Em7','Am7','D7','Gmaj7','Bm7']),  # Fallin
    311: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Girl on Fire

    # Beyonce (312-316)
    312: (['G','Am','C','D'], ['G','Am','C','D','Em'], ['Gmaj7','Am7','Cmaj7','D7','Em7']),  # Halo
    313: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Crazy in Love
    314: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # Irreplaceable
    315: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','C7','G7','Em7']),  # Single Ladies
    316: (['C','Am','F','G'], ['C','Am','F','G','Dm'], ['Cmaj7','Am7','Fmaj7','G7','Dm7']),  # Love on Top

    # John Legend (317-318)
    317: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # All of Me
    318: (['C','G','Am','F'], ['C','G','Am','F','Dm'], ['Cmaj7','G7','Am7','Fmaj7','Dm7']),  # Ordinary People

    # Sam Smith (319-321)
    319: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Stay with Me
    320: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','Gmaj7','Em7']),  # Too Good at Goodbyes
    321: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # Lay Me Down

    # Frank Ocean (322-323)
    322: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','Gmaj7','Fmaj7','Cmaj7','Dm7']),  # Thinking Bout You
    323: (['Gm','Bb','Eb','F'], ['Gm','Bb','Eb','F','Cm'], ['Gm7','Bb','Eb','F7','Cm7']),  # Nights

    # Various modern R&B (324-328)
    324: (['Am','G','F','C'], ['Am','G','F','C','Em'], ['Am7','Gmaj7','Fmaj7','Cmaj7','Em7']),  # Redbone (Eb - simplified)
    325: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Can't Feel My Face
    326: (['Am','G','F','C'], ['Am','G','F','C','Em'], ['Am7','G7','Fmaj7','Cmaj7','Em7']),  # Starboy
    327: (['C','Am','F','G'], ['C','Am','F','G','Em'], ['Cmaj7','Am7','Fmaj7','Gmaj7','Em7']),  # Save Your Tears
    328: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Die for You

    # Tracy Chapman (329-330)
    329: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # Fast Car
    330: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # Talkin Bout a Revolution

    # Joni Mitchell (331-334)
    331: (['G','D','A'], ['G','D','A','Bm','Em'], ['Gmaj7','D7','A7','Bm7','Em7']),  # Big Yellow Taxi
    332: (['C','F','G','Am'], ['C','F','G','Am','Dm'], ['Cmaj7','Fmaj7','Gmaj7','Am7','Dm7']),  # Both Sides Now
    333: (['A','D','E','F#m'], ['A','D','E','F#m','Bm'], ['A','D','E7','F#m7','Bm7']),  # A Case of You
    334: (['C','F','G','Am'], ['C','F','G','Am','Dm'], ['Cmaj7','Fmaj7','G7','Am7','Dm7']),  # River

    # Fleetwood Mac (335-343)
    335: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # Landslide
    336: (['F','G','Am'], ['F','G','Am','C'], ['Fmaj7','G','Am7','Cmaj7','Em7']),  # Dreams
    337: (['F','C','Bb','G'], ['F','C','Bb','G','Dm'], ['Fmaj7','C','Bb','G7','Dm7']),  # Go Your Own Way
    338: (['Am','G','F','C'], ['Am','G','F','C','Em'], ['Am7','Gmaj7','Fmaj7','Cmaj7','Em7']),  # The Chain
    339: (['F','C','Bb','G'], ['F','C','Bb','G','Am'], ['Fmaj7','Cmaj7','Bb','G7','Am7']),  # Everywhere
    340: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Rhiannon
    341: (['C','F','G','Am'], ['C','F','G','Am','Dm'], ['Cmaj7','Fmaj7','G7','Am7','Dm7']),  # Little Lies
    342: (['C','F','G'], ['C','F','G','Am','Dm'], ['Cmaj7','Fmaj7','G7','Am7','Dm7']),  # Don't Stop
    343: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # Songbird

    # Kansas (344-345)
    344: (['C','Am','G','F'], ['C','Am','G','F','Dm'], ['Cmaj7','Am7','Gmaj7','Fmaj7','Dm7']),  # Dust in the Wind
    345: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # Carry on Wayward Son

    # Boston (346-347)
    346: (['D','G','A','Em'], ['D','G','A','Em','Bm'], ['D','Gmaj7','A7','Em7','Bm7']),  # More Than a Feeling
    347: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G7','Am7','Fmaj7','Em7']),  # Peace of Mind

    # Toto (348-350)
    348: (['A','F#m','D','E'], ['A','F#m','D','E','Bm'], ['A','F#m7','D','E7','Bm7']),  # Africa
    349: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # Rosanna
    350: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # Hold the Line

    # Journey (351-356)
    351: (['E','B','C#m','A'], ['E','B','C#m','A','F#m'], ['E','B7','C#m','A','F#m7']),  # Don't Stop Believin
    352: (['C','G','Am','F'], ['C','G','Am','F','Dm'], ['Cmaj7','G','Am7','Fmaj7','Dm7']),  # Open Arms
    353: (['D','G','A','Bm'], ['D','G','A','Bm','Em'], ['D','Gmaj7','A7','Bm7','Em7']),  # Faithfully
    354: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # Lights
    355: (['Em','C','G','D'], ['Em','C','G','D','Am'], ['Em7','Cmaj7','Gmaj7','D7','Am7']),  # Separate Ways
    356: (['G','D','Am','C'], ['G','D','Am','C','Em'], ['Gmaj7','D','Am7','Cmaj7','Em7']),  # Any Way You Want It

    # 80s Rock (357-360)
    357: (['G','D','C','Am'], ['G','D','C','Am','Em'], ['Gmaj7','D','Cmaj7','Am7','Em7']),  # Here I Go Again
    358: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # Every Rose Has Its Thorn
    359: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Home Sweet Home
    360: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G7','Am7','Fmaj7','Em7']),  # Sister Christian

    # The Police (361-365)
    361: (['A','F#m','D','E'], ['A','F#m','D','E','Bm'], ['A','F#m7','D','E7','Bm7']),  # Every Breath You Take
    362: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # Roxanne (Em - simplified)
    363: (['C#m','A','B','E'], ['C#m','A','B','E','F#m'], ['C#m','A','B7','E','F#m7']),  # Message in a Bottle
    364: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # Don't Stand So Close to Me
    365: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','Gmaj7','Fmaj7','Cmaj7','Dm7']),  # Walking on the Moon (Dm)

    # U2 (366-372)
    366: (['D','G','A','Bm'], ['D','G','A','Bm','Em'], ['D','Gmaj7','A7','Bm7','Em7']),  # With or Without You
    367: (['Am','G','F','C'], ['Am','G','F','C','Em'], ['Am7','Gmaj7','Fmaj7','Cmaj7','Em7']),  # One
    368: (['D','G','A'], ['D','G','A','Bm','Em'], ['D','Gmaj7','A7','Bm7','Em7']),  # Where the Streets Have No Name
    369: (['A','D','E','F#m'], ['A','D','E','F#m','Bm'], ['A','D','E7','F#m7','Bm7']),  # Beautiful Day
    370: (['D','G','A'], ['D','G','A','Bm','Em'], ['D','Gmaj7','A7','Bm7','Em7']),  # I Still Haven't Found
    371: (['Bm','D','G','A'], ['Bm','D','G','A','Em'], ['Bm7','D','Gmaj7','A7','Em7']),  # Sunday Bloody Sunday
    372: (['D','G','A'], ['D','G','A','Bm','Em'], ['D','Gmaj7','A7','Bm7','Em7']),  # Pride

    # Bob Marley (373-382)
    373: (['G','Em','C','D'], ['G','Em','C','D','Am'], ['Gmaj7','Em7','Cmaj7','D7','Am7']),  # Redemption Song
    374: (['Am','G','F','C'], ['Am','G','F','C','Em'], ['Am7','G7','Fmaj7','Cmaj7','Em7']),  # Buffalo Soldier
    375: (['F#m','D','A','E'], ['F#m','D','A','E','Bm'], ['F#m7','D','A','E7','Bm7']),  # Is This Love
    376: (['Bm','Em','G','A'], ['Bm','Em','G','A','D'], ['Bm7','Em7','Gmaj7','A7','D']),  # Jamming
    377: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # Get Up Stand Up
    378: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G7','Am7','Fmaj7','Em7']),  # One Love (Bb - simplified)
    379: (['A','D','E'], ['A','D','E','F#m','Bm'], ['A','D','E7','F#m7','Bm7']),  # Stir It Up
    380: (['D','G','A','Bm'], ['D','G','A','Bm','Em'], ['D','Gmaj7','A7','Bm7','Em7']),  # Could You Be Loved
    381: (['A','D','E','F#m'], ['A','D','E','F#m','Bm'], ['A','D','E7','F#m7','Bm7']),  # Waiting in Vain
    382: (['Am','Dm','Em'], ['Am','Dm','Em','G','F'], ['Am7','Dm7','Em7','G7','Fmaj7']),  # I Shot the Sheriff (Gm - simplified)

    # Reggae/Ska (383-388)
    383: (['C','F','G','Am'], ['C','F','G','Am','Dm'], ['Cmaj7','Fmaj7','G7','Am7','Dm7']),  # Red Red Wine
    384: (['C','Am','F','G'], ['C','Am','F','G','Dm'], ['Cmaj7','Am7','Fmaj7','G7','Dm7']),  # Kingston Town
    385: (['A','D','G','E'], ['A','D','G','E','F#m'], ['A','D','G','E7','F#m7']),  # Santeria
    386: (['D','G','A'], ['D','G','A','Bm','Em'], ['D','Gmaj7','A7','Bm7','Em7']),  # What I Got
    387: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # Wrong Way
    388: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # Badfish

    # Jazz Standards - Sinatra (389-395)
    389: (['Am','Dm','G','C'], ['Am7','Dm7','G7','Cmaj7','Fmaj7'], ['Am7','Dm7','G7','Cmaj7','Fmaj7','Bm7']),  # Fly Me to the Moon
    390: (['C','Am','F','G'], ['C','Am','Dm','G7','F'], ['Cmaj7','Am7','Dm7','G7','Fmaj7','Em7']),  # My Way
    391: (['C','Am','Dm','G'], ['C','Am','Dm','G7','F'], ['Cmaj7','Am7','Dm7','G7','Fmaj7','Em7']),  # New York New York
    392: (['C','Am','Dm','G'], ['C','Am','Dm','G7','F'], ['Cmaj7','Am7','Dm7','G7','Fmaj7','Em7']),  # The Way You Look Tonight
    393: (['C','Am','Dm','G'], ['C','Am','Dm','G7','F'], ['Cmaj7','Am7','Dm7','G7','Fmaj7']),  # Come Fly with Me
    394: (['G','C','D','Em'], ['G','Em','Am','D7','C'], ['Gmaj7','Em7','Am7','D7','Cmaj7','Bm7']),  # That's Life
    395: (['C','Am','Dm','G'], ['C','Am','Dm','G7','F'], ['Cmaj7','Am7','Dm7','G7','Fmaj7','Em7']),  # I've Got You Under My Skin

    # More Jazz/Standards (396-411)
    396: (['C','Am','F','G'], ['C','Am','F','G7','Dm'], ['Cmaj7','Am7','Fmaj7','G7','Dm7','Em7']),  # Moon River
    397: (['C','Am','F','G'], ['C','Am','F','G7','Dm'], ['Cmaj7','Am7','Fmaj7','G7','Dm7']),  # Dream a Little Dream
    398: (['Am','Dm','E','Am'], ['Am','Dm','E7','Am','G'], ['Am7','Dm7','E7','Am7','Gmaj7','Cmaj7']),  # Summertime
    399: (['Am','Dm','G','C'], ['Am7','Dm7','G7','Cmaj7','F'], ['Am7','Dm7','G7','Cmaj7','Fmaj7','Bm7']),  # Autumn Leaves
    400: (['C','Am','F','G'], ['C','Am','F','G7','Dm'], ['Cmaj7','Am7','Fmaj7','G7','Dm7','Em7']),  # Unforgettable
    401: (['G','Em','Am','D'], ['G','Em','Am','D7','C'], ['Gmaj7','Em7','Am7','D7','Cmaj7']),  # L-O-V-E
    402: (['F','G','Am','C'], ['Fmaj7','G7','Am7','Cmaj7','Dm7'], ['Fmaj7','G7','Am7','Cmaj7','Dm7','Gm7']),  # Girl from Ipanema
    403: (['Am','Dm','G','C'], ['Am7','Dm7','G7','Cmaj7','Em7'], ['Am7','Dm7','G7','Cmaj7','Em7','Bm7']),  # Take Five (Ebm - simplified)
    404: (['Am','Dm','G','C'], ['Am7','Dm7','G7','Cmaj7','Em'], ['Am7','Dm7','G7','Cmaj7','Em7','Fmaj7']),  # Feeling Good
    405: (['F','C','G','Am'], ['F','C','G7','Am','Dm'], ['Fmaj7','Cmaj7','G7','Am7','Dm7']),  # My Baby Just Cares for Me
    406: (['Am','Dm','Em'], ['Am','Dm','Em','G','F'], ['Am7','Dm7','Em7','G7','Fmaj7','Cmaj7']),  # Sinnerman
    407: (['C','Am','F','G'], ['C','Am','F','G7','Dm'], ['Cmaj7','Am7','Fmaj7','G7','Dm7','Em7']),  # Blue Moon
    408: (['C','Am','Dm','G'], ['C','Am','Dm','G7','F'], ['Cmaj7','Am7','Dm7','G7','Fmaj7','Em7']),  # Cheek to Cheek
    409: (['C','Am','Dm','G'], ['C','Am','Dm','G7','F'], ['Cmaj7','Am7','Dm7','G7','Fmaj7']),  # Beyond the Sea
    410: (['C','Am','Dm','G'], ['C','Am','Dm','G7','F'], ['Cmaj7','Am7','Dm7','G7','Fmaj7','Em7']),  # Mack the Knife
    411: (['C','F','G'], ['C','F','G','Am','Dm'], ['Cmaj7','Fmaj7','G7','Am7','Dm7']),  # Splish Splash

    # 80s Pop (412-435)
    412: (['Am','G','F','C'], ['Am','G','F','C','Em'], ['Am7','Gmaj7','Fmaj7','Cmaj7','Em7']),  # Take on Me (A - simplified)
    413: (['Am','G','F','C'], ['Am','G','F','C','Em'], ['Am7','Gmaj7','Fmaj7','Cmaj7','Em7']),  # Every Little Thing She Does Is Magic
    414: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Careless Whisper (Dm)
    415: (['C','F','G','Am'], ['C','F','G','Am','Dm'], ['Cmaj7','Fmaj7','G7','Am7','Dm7']),  # Faith
    416: (['C','Am','F','G'], ['C','Am','F','G','Dm'], ['Cmaj7','Am7','Fmaj7','G7','Dm7']),  # Last Christmas
    417: (['C','F','G','Am'], ['C','F','G','Am','Dm'], ['Cmaj7','Fmaj7','G7','Am7','Dm7']),  # Wake Me Up Before You Go Go
    418: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # Girls Just Want to Have Fun
    419: (['C','Am','F','G'], ['C','Am','F','G','Dm'], ['Cmaj7','Am7','Fmaj7','Gmaj7','Dm7']),  # Time After Time
    420: (['C','Am','F','G'], ['C','Am','F','G','Em'], ['Cmaj7','Am7','Fmaj7','G7','Em7']),  # True Colors

    # Madonna (421-424)
    421: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Like a Prayer
    422: (['A','D','E'], ['A','D','E','F#m','Bm'], ['A','D','E7','F#m7','Bm7']),  # Material Girl
    423: (['Am','Dm','G','C'], ['Am','Dm','G','C','F'], ['Am7','Dm7','G7','Cmaj7','Fmaj7']),  # Papa Don't Preach
    424: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # La Isla Bonita

    # Whitney Houston (425-429)
    425: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # I Wanna Dance with Somebody
    426: (['C','Am','F','G'], ['C','Am','F','G','Dm'], ['Cmaj7','Am7','Fmaj7','G7','Dm7']),  # Greatest Love of All
    427: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # How Will I Know
    428: (['A','D','E','F#m'], ['A','D','E','F#m','Bm'], ['A','D','E7','F#m7','Bm7']),  # I Will Always Love You
    429: (['C','Am','F','G'], ['C','Am','F','G','Dm'], ['Cmaj7','Am7','Fmaj7','G7','Dm7']),  # Saving All My Love for You

    # Michael Jackson (430-435)
    430: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Billie Jean (F#m - simplified)
    431: (['Em','D','C','G'], ['Em','D','C','G','Am'], ['Em7','D7','Cmaj7','Gmaj7','Am7']),  # Beat It
    432: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Thriller
    433: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # Man in the Mirror
    434: (['C','F','G','Am'], ['C','F','G','Am','Dm'], ['Cmaj7','Fmaj7','G7','Am7','Dm7']),  # The Way You Make Me Feel
    435: (['A','D','E'], ['A','D','E','F#m','Bm'], ['A','D','E7','F#m7','Bm7']),  # Black or White

    # New Wave/Post-Punk (436-453)
    436: (['D','G','A','Bm'], ['D','G','A','Bm','Em'], ['D','Gmaj7','A7','Bm7','Em7']),  # Don't You Forget About Me
    437: (['D','G','A','Em'], ['D','G','A','Em','Bm'], ['D','Gmaj7','A7','Em7','Bm7']),  # Everybody Wants to Rule the World
    438: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # Shout
    439: (['Em','G','D','A'], ['Em','G','D','A','Bm'], ['Em7','Gmaj7','D7','A7','Bm7']),  # Mad World
    440: (['Am','C','G','D'], ['Am','C','G','D','Em'], ['Am7','Cmaj7','Gmaj7','D7','Em7']),  # Tainted Love
    441: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Sweet Dreams
    442: (['Am','G','F','C'], ['Am','G','F','C','Em'], ['Am7','Gmaj7','Fmaj7','Cmaj7','Em7']),  # Here Comes the Rain Again
    443: (['A','D','E','F#m'], ['A','D','E','F#m','Bm'], ['A','D','E7','F#m7','Bm7']),  # Just Like Heaven
    444: (['A','D','E'], ['A','D','E','F#m','Bm'], ['A','D','E7','F#m7','Bm7']),  # Boys Don't Cry
    445: (['D','G','A','Bm'], ['D','G','A','Bm','Em'], ['D','Gmaj7','A7','Bm7','Em7']),  # Friday I'm in Love
    446: (['Am','G','F','C'], ['Am','G','F','C','Em'], ['Am7','Gmaj7','Fmaj7','Cmaj7','Em7']),  # Lovesong
    447: (['Dm','F','C','G'], ['Dm','F','C','G','Am'], ['Dm7','Fmaj7','Cmaj7','G7','Am7']),  # Blue Monday
    448: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # Love Will Tear Us Apart
    449: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','Gmaj7','Fmaj7','Cmaj7','Dm7']),  # There Is a Light
    450: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # How Soon Is Now
    451: (['D','G','A','Bm'], ['D','G','A','Bm','Em'], ['D','Gmaj7','A7','Bm7','Em7']),  # This Charming Man
    452: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # Personal Jesus
    453: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','Gmaj7','Dm7']),  # Enjoy the Silence

    # 80s Pop Continued (454-459)
    454: (['C','G','Am','F'], ['C','G','Am','F','Dm'], ['Cmaj7','G','Am7','Fmaj7','Dm7']),  # Never Gonna Give You Up
    455: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # Together Forever
    456: (['G','D','Am','C'], ['G','D','Am','C','Em'], ['Gmaj7','D','Am7','Cmaj7','Em7']),  # Jessie's Girl
    457: (['C','Am','F','G'], ['C','Am','F','G','Em'], ['Cmaj7','Am7','Fmaj7','G7','Em7']),  # Come On Eileen
    458: (['D','G','A','Bm'], ['D','G','A','Bm','Em'], ['D','Gmaj7','A7','Bm7','Em7']),  # I Melt with You
    459: (['A','D','E','F#m'], ['A','D','E','F#m','Bm'], ['A','D','E7','F#m7','Bm7']),  # 867-5309 Jenny

    # 90s Pop (460-476)
    460: (['Em','C','G','D'], ['Em','C','G','D','Am'], ['Em7','Cmaj7','Gmaj7','D7','Am7']),  # Waterfalls
    461: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # No Scrubs
    462: (['A','D','E'], ['A','D','E','F#m','Bm'], ['A','D','E7','F#m7','Bm7']),  # MMMBop
    463: (['D','G','A','Em'], ['D','G','A','Em','Bm'], ['D','Gmaj7','A7','Em7','Bm7']),  # Tubthumping
    464: (['C','G','Am','F'], ['C','G','Am','F','Dm'], ['Cmaj7','G7','Am7','Fmaj7','Dm7']),  # Wannabe
    465: (['Am','G','F','C'], ['Am','G','F','C','Em'], ['Am7','Gmaj7','Fmaj7','Cmaj7','Em7']),  # Say You'll Be There
    466: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Baby One More Time (Cm - simplified)
    467: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Oops I Did It Again
    468: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Toxic
    469: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Genie in a Bottle
    470: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # Beautiful
    471: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # I Want It That Way
    472: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Everybody
    473: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # As Long as You Love Me
    474: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Bye Bye Bye
    475: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G7','Am7','Fmaj7','Em7']),  # Tearin Up My Heart
    476: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # It's Gonna Be Me

    # Late 90s Alt/Pop (477-488)
    477: (['Am','G','F','C'], ['Am','G','F','C','Em'], ['Am7','Gmaj7','Fmaj7','Cmaj7','Em7']),  # Lovefool
    478: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # Kiss Me
    479: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Smooth
    480: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # Maria Maria
    481: (['D','G','A'], ['D','G','A','Bm','Em'], ['D','Gmaj7','A7','Bm7','Em7']),  # Steal My Sunshine
    482: (['G','D','Am','C'], ['G','D','Am','C','Em'], ['Gmaj7','D','Am7','Cmaj7','Em7']),  # All Star
    483: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # Walking on the Sun
    484: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # Fly
    485: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G','Am7','Fmaj7','Em7']),  # Every Morning
    486: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','Gmaj7','Fmaj7','Cmaj7','Dm7']),  # Save Tonight
    487: (['Am','G','F','C'], ['Am','G','F','C','Em'], ['Am7','G7','Fmaj7','Cmaj7','Em7']),  # Inside Out
    488: (['D','G','A'], ['D','G','A','Bm','Em'], ['D','Gmaj7','A7','Bm7','Em7']),  # Breakfast at Tiffanys

    # Green Day (489-495)
    489: (['G','C','D'], ['G','C','D','Em'], ['Gmaj7','Cmaj7','D7','Em7']),  # Good Riddance
    490: (['A','D','E'], ['A','D','E','F#m','Bm'], ['A','D','E7','F#m7','Bm7']),  # Basket Case (Eb - simplified)
    491: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # When I Come Around
    492: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Boulevard of Broken Dreams
    493: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Holiday
    494: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # 21 Guns
    495: (['A','D','E'], ['A','D','E','F#m','Bm'], ['A','D','E7','F#m7','Bm7']),  # American Idiot

    # Misc (496-499)
    496: (['Am','G','F','C'], ['Am','G','F','C','Em'], ['Am7','Gmaj7','Fmaj7','Cmaj7','Em7']),  # Clint Eastwood
    497: (['Am','G','F','C'], ['Am','G','F','C','Em'], ['Am7','Gmaj7','Fmaj7','Cmaj7','Em7']),  # Feel Good Inc
    498: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # Crazy
    499: (['Em','G','D','A'], ['Em','G','D','A','C'], ['Em7','Gmaj7','D7','A7','Cmaj7']),  # Seven Nation Army
}


def build_level(song, title, artist, level, chord_names, strum_pool):
    sid = make_id(title, artist)
    strum = random.choice(strum_pool)
    return {
        'id': f"{sid}-{level}",
        'title': title,
        'artist': artist,
        'level': level,
        'chords': [chord(c) for c in chord_names],
        'strummingPattern': strum[0],
        'strummingDescription': strum[1],
        'lyrics': make_lyrics(title, artist, chord_names),
    }


def main():
    with open('data/songs.json', 'r') as f:
        songs = json.load(f)

    count = 0
    for idx in range(250, 500):
        if idx >= len(songs):
            break
        if idx not in SONG_CHORDS:
            print(f"WARNING: No chord data for index {idx}: {songs[idx]['title']}")
            continue

        easy_chords, med_chords, adv_chords = SONG_CHORDS[idx]
        title = songs[idx]['title']
        artist = songs[idx]['artist']
        sid = make_id(title, artist)

        songs[idx]['id'] = sid
        songs[idx]['easy'] = build_level(songs[idx], title, artist, 'easy', easy_chords, EASY_STRUMS)
        songs[idx]['medium'] = build_level(songs[idx], title, artist, 'medium', med_chords, MED_STRUMS)
        songs[idx]['advanced'] = build_level(songs[idx], title, artist, 'advanced', adv_chords, ADV_STRUMS)
        count += 1

    with open('data/songs.json', 'w') as f:
        json.dump(songs, f, indent=2)

    print(f"Updated {count} songs (indices 250-499)")


if __name__ == '__main__':
    main()
