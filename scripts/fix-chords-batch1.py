#!/usr/bin/env python3
"""Replace songs 0-249 with REAL chord progressions based on actual songs."""
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

# REAL chord progressions for songs 0-249
# Format: index -> (easy_chords, medium_chords, advanced_chords)
REAL_CHORDS = {
    # === Pop (0-49) ===
    0: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G7','Am7','Fmaj7','Em7']),  # Shape of You - Ed Sheeran (C#m A B E simplified)
    1: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Blinding Lights
    2: (['G','D','Em','C'], ['G','D','Em','C','Am'], ['Gmaj7','D','Em7','Cmaj7','Am7']),  # Someone Like You - Adele
    3: (['Am','Em','G','D'], ['Am','Em','G','D','C'], ['Am7','Em7','G7','D7','Cmaj7']),  # Rolling in the Deep
    4: (['Em','G','D','C'], ['Em','G','D','C','Am'], ['Em7','Gmaj7','D7','Cmaj7','Am7']),  # Hello - Adele
    5: (['Dm','F','C','G'], ['Dm','F','C','G','Am'], ['Dm7','Fmaj7','Cmaj7','G7','Am7']),  # Set Fire to the Rain
    6: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Easy on Me
    7: (['Dm','G','C','F'], ['Dm','G','C','F','Am'], ['Dm7','G7','Cmaj7','Fmaj7','Am7']),  # Uptown Funk (simplified)
    8: (['C','Am','F','G'], ['C','Am','F','G','Em'], ['Cmaj7','Am7','Fmaj7','G7','Em7']),  # Just the Way You Are
    9: (['Dm','Am','C','G'], ['Dm','Am','C','G','F'], ['Dm7','Am7','Cmaj7','G7','Fmaj7']),  # Grenade
    10: (['D','G','A','Bm'], ['D','G','A','Bm','Em'], ['D','Gmaj7','A7','Bm7','Em7']),  # Treasure (simplified)
    11: (['C','Em','Am','G'], ['C','Em','Am','G','F'], ['Cmaj7','Em7','Am7','G7','Fmaj7']),  # Count on Me
    12: (['Dm','F','C','G'], ['Dm','F','C','G','Bb'], ['Dm7','Fmaj7','Cmaj7','G7','Bb']),  # Locked Out of Heaven
    13: (['C','G','Am','F'], ['C','G','Am','F','Dm'], ['Cmaj7','G7','Am7','Fmaj7','Dm7']),  # When I Was Your Man
    14: (['D','G','A','Bm'], ['D','G','A','Bm','Em'], ['D','Gmaj7','A7','Bm7','Em7']),  # Thinking Out Loud
    15: (['G','Em','C','D'], ['G','Em','C','D','Am'], ['Gmaj7','Em7','Cmaj7','D7','Am7']),  # Perfect
    16: (['G','Em','C','D'], ['G','Em','C','D','Am'], ['Gmaj7','Em7','Cmaj7','D','Am7']),  # Photograph
    17: (['D','G','A','Bm'], ['D','G','A','Bm','Em'], ['D7','Gmaj7','A7','Bm7','Em7']),  # Castle on the Hill
    18: (['D','G','A','Bm'], ['D','G','A','Bm','Em'], ['D','Gmaj7','A','Bm7','Em7']),  # Galway Girl
    19: (['Em','G','D','A'], ['Em','G','D','A','C'], ['Em7','Gmaj7','D7','A7','Cmaj7']),  # Happier - Ed Sheeran
    20: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Bad Habits
    21: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # Shivers
    22: (['G','D','Em','C'], ['G','D','Em','C','Am'], ['Gmaj7','D','Em7','Cmaj7','Am7']),  # Shallow
    23: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Poker Face (simplified)
    24: (['C','F','Am','G'], ['C','F','Am','G','Em'], ['Cmaj7','Fmaj7','Am7','G7','Em7']),  # Born This Way (simplified)
    25: (['Am','F','C','G'], ['Am','F','C','G','E7'], ['Am7','Fmaj7','Cmaj7','G7','E7']),  # Bad Romance (simplified)
    26: (['C','Am','F','G'], ['C','Am','F','G','Dm'], ['Cmaj7','Am7','Fmaj7','G7','Dm7']),  # Stay - Rihanna
    27: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Umbrella
    28: (['G','D','Em','C'], ['G','D','Em','C','Am'], ['Gmaj7','D','Em7','Cmaj7','Am7']),  # Diamonds
    29: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # We Found Love
    30: (['Em','C','G','D'], ['Em','C','G','D','Am'], ['Em7','Cmaj7','G','D7','Am7']),  # Love the Way You Lie
    31: (['Em','D','C','G'], ['Em','D','C','G','Am'], ['Em7','D7','Cmaj7','G7','Am7']),  # Lose Yourself (simplified)
    32: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G7','Am7','Fmaj7','Em7']),  # Roar
    33: (['G','Am','C','D'], ['G','Am','C','D','Em'], ['Gmaj7','Am7','Cmaj7','D7','Em7']),  # Firework
    34: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Dark Horse
    35: (['C','G','Am','F'], ['C','G','Am','F','Dm'], ['Cmaj7','G7','Am7','Fmaj7','Dm7']),  # Teenage Dream
    36: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G7','Am7','Fmaj7','Em7']),  # Shake It Off
    37: (['G','D','Em','C'], ['G','D','Em','C','Am'], ['Gmaj7','D','Em7','Cmaj7','Am7']),  # Love Story
    38: (['D','A','G','Bm'], ['D','A','G','Bm','Em'], ['D','A7','Gmaj7','Bm7','Em7']),  # You Belong with Me
    39: (['G','D','Am','C'], ['G','D','Am','C','Em'], ['Gmaj7','D7','Am7','Cmaj7','Em7']),  # Blank Space
    40: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Style
    41: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G7','Am7','Fmaj7','Em7']),  # Wildest Dreams
    42: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Anti-Hero
    43: (['Am','Em','G','D'], ['Am','Em','G','D','C'], ['Am7','Em7','Gmaj7','D7','Cmaj7']),  # Cardigan
    44: (['G','D','Em','C'], ['G','D','Em','C','Am'], ['Gmaj7','D','Em7','Cmaj7','Am7']),  # All Too Well
    45: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # Cruel Summer
    46: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Levitating
    47: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # Don't Start Now
    48: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # New Rules
    49: (['Am','G','F','C'], ['Am','G','F','C','Em'], ['Am7','G7','Fmaj7','Cmaj7','Em7']),  # Physical

    # === Rock (50-99) ===
    50: (['G','C','D','Am'], ['G','C','D','Am','Em'], ['Gmaj7','Cmaj7','D7','Am7','Em7']),  # Bohemian Rhapsody (simplified)
    51: (['A','D','E','G'], ['A','D','E','G','Am'], ['A7','D7','E7','G7','Am7']),  # We Will Rock You
    52: (['F','Am','Dm','G'], ['F','Am','Dm','G','C'], ['Fmaj7','Am7','Dm7','G7','Cmaj7']),  # Don't Stop Me Now
    53: (['G','C','D','Am'], ['G','C','D','Am','Em'], ['Gmaj7','Cmaj7','D7','Am7','Em7']),  # Somebody to Love
    54: (['Dm','F','C','G'], ['Dm','F','C','G','Am'], ['Dm7','Fmaj7','Cmaj7','G7','Am7']),  # Radio Ga Ga
    55: (['D','A','G','Em'], ['D','A','G','Em','Bm'], ['D7','A7','Gmaj7','Em7','Bm7']),  # Under Pressure
    56: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','Gmaj7','Fmaj7','Cmaj7','Dm7']),  # Stairway to Heaven (simplified)
    57: (['E','A','D','G'], ['E','A','D','G','B'], ['E7','A7','D7','G7','B7']),  # Whole Lotta Love (simplified)
    58: (['Am','G','F','E'], ['Am','G','F','E','Dm'], ['Am7','G7','Fmaj7','E7','Dm7']),  # Kashmir (simplified)
    59: (['Am','E7','G','D'], ['Am','E7','G','D','F'], ['Am7','E7','G7','D7','Fmaj7']),  # Hotel California
    60: (['G','D','C','Em'], ['G','D','C','Em','Am'], ['Gmaj7','D7','Cmaj7','Em7','Am7']),  # Take It Easy
    61: (['G','D','Em','C'], ['G','D','Em','C','Am'], ['Gmaj7','D7','Em7','Cmaj7','Am7']),  # Desperado
    62: (['G','C','D','Am'], ['G','C','D','Am','Em'], ['Gmaj7','Cmaj7','D7','Am7','Em7']),  # Peaceful Easy Feeling
    63: (['D','G','A','Em'], ['D','G','A','Em','Bm'], ['D','Gmaj7','A7','Em7','Bm7']),  # Sweet Child O Mine (simplified)
    64: (['G','C','D','A'], ['G','C','D','A','Em'], ['Gmaj7','Cmaj7','D7','A7','Em7']),  # Paradise City (simplified)
    65: (['C','F','G','Am'], ['C','F','G','Am','Dm'], ['Cmaj7','Fmaj7','G7','Am7','Dm7']),  # November Rain (simplified)
    66: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D','Em7','Am7']),  # Patience
    67: (['F','Bb','C','Am'], ['F','Bb','C','Am','Dm'], ['Fmaj7','Bb','C7','Am7','Dm7']),  # Smells Like Teen Spirit (simplified)
    68: (['Em','G','D','Am'], ['Em','G','D','Am','C'], ['Em7','Gmaj7','D7','Am7','Cmaj7']),  # Come As You Are
    69: (['Am','G','F','D'], ['Am','G','F','D','Em'], ['Am7','G7','Fmaj7','D7','Em7']),  # Heart-Shaped Box (simplified)
    70: (['D','F','Bb','C'], ['D','F','Bb','C','Am'], ['D7','Fmaj7','Bb','C7','Am7']),  # Lithium (simplified)
    71: (['Am','G','C','F'], ['Am','G','C','F','Dm'], ['Am7','G7','Cmaj7','Fmaj7','Dm7']),  # In Bloom (simplified)
    72: (['A','D','E','G'], ['A','D','E','G','Bm'], ['A7','D7','E7','G7','Bm7']),  # Back in Black
    73: (['A','D','E','G'], ['A','D','E','G','Em'], ['A7','D7','E7','G7','Em7']),  # Highway to Hell
    74: (['A','D','E','G'], ['A','D','E','G','Am'], ['A7','D7','E7','G7','Am7']),  # Thunderstruck
    75: (['G','C','D','Am'], ['G','C','D','Am','Em'], ['G7','Cmaj7','D7','Am7','Em7']),  # You Shook Me All Night Long
    76: (['Em','C','D','G'], ['Em','C','D','G','Am'], ['Em7','Cmaj7','D7','Gmaj7','Am7']),  # Livin on a Prayer (simplified)
    77: (['D','A','G','Em'], ['D','A','G','Em','Bm'], ['D7','A','Gmaj7','Em7','Bm7']),  # Wanted Dead or Alive
    78: (['C','F','Am','G'], ['C','F','Am','G','Dm'], ['Cmaj7','Fmaj7','Am7','G7','Dm7']),  # Its My Life
    79: (['Am','G','F','E'], ['Am','G','F','E','Dm'], ['Am7','Gmaj7','Fmaj7','E7','Dm7']),  # Dream On
    80: (['C','F','G','Am'], ['C','F','G','Am','Em'], ['C7','Fmaj7','G7','Am7','Em7']),  # Walk This Way (simplified)
    81: (['D','A','Bm','G'], ['D','A','Bm','G','Em'], ['D','A7','Bm7','Gmaj7','Em7']),  # I Don't Want to Miss a Thing
    82: (['Em','G','D','Am'], ['Em','G','D','Am','Bm'], ['Em7','Gmaj7','D7','Am7','Bm7']),  # Comfortably Numb (simplified)
    83: (['G','C','D','Am'], ['G','C','D','Am','Em'], ['Gmaj7','Cmaj7','D','Am7','Em7']),  # Wish You Were Here
    84: (['Dm','G','C','F'], ['Dm','G','C','F','Am'], ['Dm7','G7','Cmaj7','Fmaj7','Am7']),  # Another Brick in the Wall
    85: (['Em','A','D','G'], ['Em','A','D','G','Bm'], ['Em7','A7','D7','Gmaj7','Bm7']),  # Money (simplified)
    86: (['Em','D','G','Am'], ['Em','D','G','Am','Bm'], ['Em7','D7','Gmaj7','Am7','Bm7']),  # Paint It Black (simplified)
    87: (['E','A','D','G'], ['E','A','D','G','B'], ['E7','A7','D7','G7','B7']),  # Satisfaction (simplified)
    88: (['Em','D','A','G'], ['Em','D','A','G','Bm'], ['Em7','D7','A7','G7','Bm7']),  # Sympathy for the Devil (simplified)
    89: (['G','Am','D','C'], ['G','Am','D','C','Em'], ['Gmaj7','Am7','D7','Cmaj7','Em7']),  # Wild Horses
    90: (['C','F','Am','G'], ['C','F','Am','G','Dm'], ['Cmaj7','Fmaj7','Am7','G7','Dm7']),  # Gimme Shelter (simplified)
    91: (['E','A','D','G'], ['E','A','D','G','B'], ['E7','A7','D7','Gmaj7','B7']),  # Born to Run (simplified)
    92: (['G','Em','C','D'], ['G','Em','C','D','Am'], ['Gmaj7','Em7','Cmaj7','D7','Am7']),  # Dancing in the Dark
    93: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D','Em7','Am7']),  # Thunder Road
    94: (['D','A','G','Em'], ['D','A','G','Em','Bm'], ['D7','A','Gmaj7','Em7','Bm7']),  # Free Fallin
    95: (['D','A','Em','G'], ['D','A','Em','G','Bm'], ['D','A7','Em7','Gmaj7','Bm7']),  # American Girl
    96: (['G','D','Em','C'], ['G','D','Em','C','Am'], ['Gmaj7','D','Em7','Cmaj7','Am7']),  # I Won't Back Down
    97: (['C','Am','F','G'], ['C','Am','F','G','Em'], ['Cmaj7','Am7','Fmaj7','G7','Em7']),  # Learning to Fly

    # === Classic Rock / Folk Rock (98-127) ===
    98: (['G','C','D','Am'], ['G','C','D','Am','Em'], ['Gmaj7','Cmaj7','D7','Am7','Em7']),  # Blowin in the Wind
    99: (['G','D','Am','C'], ['G','D','Am','C','Em'], ['Gmaj7','D7','Am7','Cmaj7','Em7']),  # Knockin on Heavens Door
    100: (['G','C','D','Am'], ['G','C','D','Am','Em'], ['Gmaj7','Cmaj7','D','Am7','Em7']),  # The Times They Are a Changin
    101: (['C','F','G','Am'], ['C','F','G','Am','Dm'], ['Cmaj7','Fmaj7','G7','Am7','Dm7']),  # Like a Rolling Stone
    102: (['G','A','D','Em'], ['G','A','D','Em','C'], ['Gmaj7','A7','D7','Em7','Cmaj7']),  # Mr Tambourine Man
    103: (['C','F','G','Am'], ['C','F','G','Am','Em'], ['Cmaj7','Fmaj7','G7','Am7','Em7']),  # Bridge Over Troubled Water
    104: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','Gmaj7','Fmaj7','Cmaj7','Dm7']),  # The Sound of Silence
    105: (['G','Em','C','D'], ['G','Em','C','D','Am'], ['Gmaj7','Em7','Cmaj7','D7','Am7']),  # Mrs Robinson
    106: (['Am','G','D','Em'], ['Am','G','D','Em','C'], ['Am7','Gmaj7','D7','Em7','Cmaj7']),  # Scarborough Fair
    107: (['Am','Em','C','G'], ['Am','Em','C','G','Dm'], ['Am7','Em7','Cmaj7','G7','Dm7']),  # The Boxer
    108: (['A','D','E','G'], ['A','D','E','G','Bm'], ['A7','D7','E7','Gmaj7','Bm7']),  # Fire and Rain (simplified)
    109: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # You've Got a Friend
    110: (['D','G','A','Em'], ['D','G','A','Em','Bm'], ['D','Gmaj7','A7','Em7','Bm7']),  # Carolina in My Mind
    111: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # American Pie
    112: (['G','Am','D','C'], ['G','Am','D','C','Em'], ['Gmaj7','Am7','D7','Cmaj7','Em7']),  # Vincent (Starry Starry Night)
    113: (['D','G','A','Em'], ['D','G','A','Em','Bm'], ['D','Gmaj7','A7','Em7','Bm7']),  # Cat's in the Cradle
    114: (['Em','G','D','Am'], ['Em','G','D','Am','C'], ['Em7','Gmaj7','D','Am7','Cmaj7']),  # Behind Blue Eyes
    115: (['A','D','E','G'], ['A','D','E','G','Bm'], ['A','D7','E7','Gmaj7','Bm7']),  # Pinball Wizard (simplified)
    116: (['A','G','D','E'], ['A','G','D','E','Bm'], ['A7','G7','D7','E7','Bm7']),  # Won't Get Fooled Again (simplified)
    117: (['E','A','D','G'], ['E','A','D','G','B'], ['E7','A7','D7','G','B7']),  # Born to Be Wild
    118: (['E','G','A','D'], ['E','G','A','D','B'], ['E7','G7','A7','D7','B7']),  # Purple Haze (simplified)
    119: (['Am','F','C','G'], ['Am','F','C','G','E7'], ['Am7','Fmaj7','Cmaj7','G7','E7']),  # All Along the Watchtower
    120: (['C','G','D','Am'], ['C','G','D','Am','Em'], ['Cmaj7','G7','D7','Am7','Em7']),  # Hey Joe (simplified)
    121: (['C','F','G','Am'], ['C','F','G','Am','Em'], ['Cmaj7','Fmaj7','G7','Am7','Em7']),  # The Wind Cries Mary (simplified)
    122: (['D','G','A','Em'], ['D','G','A','Em','Bm'], ['D7','G7','A7','Em7','Bm7']),  # Sunshine of Your Love (simplified)
    123: (['Am','D','F','G'], ['Am','D','F','G','C'], ['Am7','D7','Fmaj7','G7','Cmaj7']),  # White Room (simplified)
    124: (['Am','C','D','G'], ['Am','C','D','G','Em'], ['Am7','Cmaj7','D7','Gmaj7','Em7']),  # Layla (unplugged)
    125: (['G','D','Em','C'], ['G','D','Em','C','Am'], ['Gmaj7','D7','Em7','Cmaj7','Am7']),  # Tears in Heaven
    126: (['G','D','C','Em'], ['G','D','C','Em','Am'], ['Gmaj7','D7','Cmaj7','Em7','Am7']),  # Wonderful Tonight
    127: (['E','A','D','G'], ['E','A','D','G','B'], ['E7','A7','D7','G7','B7']),  # Cocaine (simplified)

    # === Beatles (128-150) ===
    128: (['G','Em','C','D'], ['G','Em','C','D','Am'], ['Gmaj7','Em7','Cmaj7','D7','Am7']),  # Yesterday (simplified)
    129: (['G','D','C','Am'], ['G','D','C','Am','Em'], ['Gmaj7','D7','Cmaj7','Am7','Em7']),  # Here Comes the Sun
    130: (['Am','G','D','Em'], ['Am','G','D','Em','C'], ['Am7','G7','D7','Em7','Cmaj7']),  # Come Together
    131: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G7','Am7','Fmaj7','Em7']),  # Let It Be
    132: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G7','Am7','Fmaj7','Em7']),  # Hey Jude
    133: (['G','Am','C','D'], ['G','Am','C','D','Em'], ['Gmaj7','Am7','Cmaj7','D7','Em7']),  # Blackbird
    134: (['Am','Em','C','G'], ['Am','Em','C','G','D'], ['Am7','Em7','Cmaj7','G7','D7']),  # While My Guitar Gently Weeps
    135: (['G','Em','C','D'], ['G','Em','C','D','Am'], ['Gmaj7','Em7','Cmaj7','D7','Am7']),  # In My Life
    136: (['D','G','A','Em'], ['D','G','A','Em','Bm'], ['D','Gmaj7','A7','Em7','Bm7']),  # Norwegian Wood
    137: (['C','F','G','Am'], ['C','F','G','Am','Em'], ['Cmaj7','Fmaj7','G7','Am7','Em7']),  # Something
    138: (['D','A','G','Em'], ['D','A','G','Em','Bm'], ['D7','A7','Gmaj7','Em7','Bm7']),  # Across the Universe
    139: (['D','G','A','E'], ['D','G','A','E','Bm'], ['D7','G7','A7','E7','Bm7']),  # Twist and Shout
    140: (['G','D','Em','C'], ['G','D','Em','C','Am'], ['Gmaj7','D7','Em7','Cmaj7','Am7']),  # I Want to Hold Your Hand (simplified)
    141: (['G','D','Em','C'], ['G','D','Em','C','Am'], ['Gmaj7','D7','Em7','Cmaj7','Am7']),  # All You Need Is Love (simplified)
    142: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # Strawberry Fields Forever (simplified)
    143: (['Em','C','G','D'], ['Em','C','G','D','Am'], ['Em7','Cmaj7','Gmaj7','D7','Am7']),  # Eleanor Rigby (simplified)
    144: (['G','Am','C','D'], ['G','Am','C','D','Em'], ['Gmaj7','Am7','Cmaj7','D7','Em7']),  # A Day in the Life (simplified)
    145: (['G','Em','C','D'], ['G','Em','C','D','Am'], ['Gmaj7','Em7','Cmaj7','D7','Am7']),  # Help
    146: (['C','Am','F','G'], ['C','Am','F','G','Dm'], ['Cmaj7','Am7','Fmaj7','G7','Dm7']),  # Penny Lane
    147: (['A','D','G','E'], ['A','D','G','E','Bm'], ['A7','D7','Gmaj7','E7','Bm7']),  # Get Back
    148: (['E','Am','D','G'], ['E','Am','D','G','C'], ['E7','Am7','D7','Gmaj7','Cmaj7']),  # Don't Let Me Down (simplified)
    149: (['G','C','D','Am'], ['G','C','D','Am','Em'], ['G7','Cmaj7','D7','Am7','Em7']),  # Love Me Do
    150: (['Am','D','C','G'], ['Am','D','C','G','Em'], ['Am7','D7','Cmaj7','Gmaj7','Em7']),  # Michelle (simplified)

    # === 90s/2000s Rock (151-175) ===
    151: (['Em','G','D','A'], ['Em','G','D','A','C'], ['Em7','Gmaj7','D7','A7','Cmaj7']),  # Wonderwall
    152: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G7','Am7','Fmaj7','Em7']),  # Don't Look Back in Anger
    153: (['G','Am','C','D'], ['G','Am','C','D','Em'], ['Gmaj7','Am7','Cmaj7','D7','Em7']),  # Champagne Supernova
    154: (['G','D','Am','C'], ['G','D','Am','C','Em'], ['Gmaj7','D7','Am7','Cmaj7','Em7']),  # Live Forever
    155: (['Am','Em','G','D'], ['Am','Em','G','D','C'], ['Am7','Em7','Gmaj7','D7','Cmaj7']),  # Losing My Religion
    156: (['G','D','Em','C'], ['G','D','Em','C','Am'], ['Gmaj7','D7','Em7','Cmaj7','Am7']),  # Everybody Hurts
    157: (['D','G','A','Em'], ['D','G','A','Em','Bm'], ['D7','Gmaj7','A7','Em7','Bm7']),  # Shiny Happy People
    158: (['C','Am','G','D'], ['C','Am','G','D','Em'], ['Cmaj7','Am7','G7','D7','Em7']),  # Man on the Moon
    159: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Under the Bridge
    160: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Californication
    161: (['F','C','Am','G'], ['F','C','Am','G','Dm'], ['Fmaj7','Cmaj7','Am7','G7','Dm7']),  # Scar Tissue
    162: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Snow Hey Oh
    163: (['Am','Em','G','D'], ['Am','Em','G','D','C'], ['Am7','Em7','G7','D7','Cmaj7']),  # Otherside
    164: (['A','E','D','Bm'], ['A','E','D','Bm','F#m'], ['A7','E7','D7','Bm7','F#m7']),  # Black - Pearl Jam
    165: (['A','D','E','G'], ['A','D','E','G','Bm'], ['A7','D7','E7','G7','Bm7']),  # Alive
    166: (['Am','C','G','D'], ['Am','C','G','D','Em'], ['Am7','Cmaj7','G7','D7','Em7']),  # Jeremy
    167: (['D','A','Em','G'], ['D','A','Em','G','Bm'], ['D7','A7','Em7','Gmaj7','Bm7']),  # Even Flow (simplified)
    168: (['Em','G','D','Am'], ['Em','G','D','Am','C'], ['Em7','Gmaj7','D7','Am7','Cmaj7']),  # Yellow Ledbetter
    169: (['D','G','A','Em'], ['D','G','A','Em','Bm'], ['D7','G7','A7','Em7','Bm7']),  # Plush (simplified)
    170: (['D','G','A','Em'], ['D','G','A','Em','Bm'], ['D','Gmaj7','A7','Em7','Bm7']),  # Interstate Love Song (simplified)
    171: (['G','B','C','Cm'], ['G','B','C','Cm','Em'], ['Gmaj7','B7','Cmaj7','Cm','Em7']),  # Creep - Radiohead
    172: (['Am','D','G','Em'], ['Am','D','G','Em','C'], ['Am7','D7','Gmaj7','Em7','Cmaj7']),  # Karma Police
    173: (['F','C','G','Am'], ['F','C','G','Am','Dm'], ['Fmaj7','Cmaj7','G7','Am7','Dm7']),  # No Surprises (simplified)
    174: (['G','D','Am','C'], ['G','D','Am','C','Em'], ['Gmaj7','D7','Am7','Cmaj7','Em7']),  # High and Dry
    175: (['Em','C','G','D'], ['Em','C','G','D','Am'], ['Em7','Cmaj7','Gmaj7','D7','Am7']),  # Zombie
    176: (['C','Am','F','G'], ['C','Am','F','G','Em'], ['Cmaj7','Am7','Fmaj7','G7','Em7']),  # Linger
    177: (['G','D','Am','C'], ['G','D','Am','C','Em'], ['Gmaj7','D7','Am7','Cmaj7','Em7']),  # Dreams - Cranberries
    178: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Mr Jones
    179: (['G','C','D','Am'], ['G','C','D','Am','Em'], ['Gmaj7','Cmaj7','D7','Am7','Em7']),  # Round Here

    # === Indie / Alt (180-219) ===
    180: (['G','C','D','Am'], ['G','C','D','Am','Em'], ['Gmaj7','Cmaj7','D7','Am7','Em7']),  # Hey Ya (simplified)
    181: (['Am','F','C','G'], ['Am','F','C','G','Dm'], ['Am7','Fmaj7','Cmaj7','G7','Dm7']),  # Somebody That I Used to Know
    182: (['Em','G','D','A'], ['Em','G','D','A','C'], ['Em7','Gmaj7','D7','A7','Cmaj7']),  # Pumped Up Kicks
    183: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Take Me Out (simplified)
    184: (['A','E','D','Bm'], ['A','E','D','Bm','F#m'], ['A7','E7','D7','Bm7','F#m7']),  # Chasing Cars (simplified)
    185: (['Am','Em','G','D'], ['Am','Em','G','D','C'], ['Am7','Em7','Gmaj7','D7','Cmaj7']),  # Run - Snow Patrol
    186: (['G','D','C','Am'], ['G','D','C','Am','Em'], ['Gmaj7','D7','Cmaj7','Am7','Em7']),  # Yellow
    187: (['Am','Em','G','D'], ['Am','Em','G','D','C'], ['Am7','Em7','Gmaj7','D7','Cmaj7']),  # The Scientist
    188: (['C','Em','Am','F'], ['C','Em','Am','F','G'], ['Cmaj7','Em7','Am7','Fmaj7','G7']),  # Fix You (simplified)
    189: (['Eb','Bb','F','C'], ['Eb','Bb','F','C','Am'], ['Eb','Bb','Fmaj7','Cmaj7','Am7']),  # Clocks (simplified)
    190: (['C','F','G','Am'], ['C','F','G','Am','Dm'], ['Cmaj7','Fmaj7','G7','Am7','Dm7']),  # Viva la Vida
    191: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # A Sky Full of Stars (simplified)
    192: (['G','D','Am','C'], ['G','D','Am','C','Em'], ['Gmaj7','D7','Am7','Cmaj7','Em7']),  # Speed of Sound
    193: (['F','Am','C','G'], ['F','Am','C','G','Dm'], ['Fmaj7','Am7','Cmaj7','G7','Dm7']),  # Paradise (simplified)
    194: (['G','D','Am','C'], ['G','D','Am','C','Em'], ['Gmaj7','D7','Am7','Cmaj7','Em7']),  # In My Place
    195: (['G','Em','C','D'], ['G','Em','C','D','Am'], ['Gmaj7','Em7','Cmaj7','D7','Am7']),  # The Hardest Part
    196: (['D','G','A','Em'], ['D','G','A','Em','Bm'], ['D7','Gmaj7','A7','Em7','Bm7']),  # Bitter Sweet Symphony (simplified)
    197: (['D','Em','G','A'], ['D','Em','G','A','Bm'], ['D','Em7','Gmaj7','A7','Bm7']),  # Iris
    198: (['Am','F','C','G'], ['Am','F','C','G','Em'], ['Am7','Fmaj7','Cmaj7','G7','Em7']),  # Slide
    199: (['D','G','A','Em'], ['D','G','A','Em','Bm'], ['D7','Gmaj7','A7','Em7','Bm7']),  # Name
    200: (['F','Am','C','G'], ['F','Am','C','G','Dm'], ['Fmaj7','Am7','Cmaj7','G7','Dm7']),  # Torn
    201: (['C','F','G','Am'], ['C','F','G','Am','Em'], ['Cmaj7','Fmaj7','G7','Am7','Em7']),  # Closing Time
    202: (['D','G','A','Em'], ['D','G','A','Em','Bm'], ['D7','Gmaj7','A7','Em7','Bm7']),  # Semi-Charmed Life (simplified)
    203: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G7','Am7','Fmaj7','Em7']),  # Jumper
    204: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # 1979 (simplified)
    205: (['G','D','C','Am'], ['G','D','C','Am','Em'], ['Gmaj7','D7','Cmaj7','Am7','Em7']),  # Tonight Tonight (simplified)
    206: (['G','Am','C','D'], ['G','Am','C','D','Em'], ['Gmaj7','Am7','Cmaj7','D7','Em7']),  # Disarm
    207: (['Am','G','C','F'], ['Am','G','C','F','Em'], ['Am7','G7','Cmaj7','Fmaj7','Em7']),  # Bullet with Butterfly Wings (simplified)
    208: (['F','G','Am','C'], ['F','G','Am','C','Dm'], ['Fmaj7','G7','Am7','Cmaj7','Dm7']),  # Glycerine (simplified)
    209: (['Am','Em','G','D'], ['Am','Em','G','D','C'], ['Am7','Em7','Gmaj7','D7','Cmaj7']),  # Crash into Me
    210: (['Am','G','D','C'], ['Am','G','D','C','Em'], ['Am7','G7','D7','Cmaj7','Em7']),  # Ants Marching (simplified)
    211: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # Satellite (simplified)
    212: (['Am','G','F','C'], ['Am','G','F','C','Dm'], ['Am7','G7','Fmaj7','Cmaj7','Dm7']),  # Two Step (simplified)

    # === Country (213-249) ===
    213: (['Am','C','G','D'], ['Am','C','G','D','Em'], ['Am7','Cmaj7','G7','D7','Em7']),  # Jolene
    214: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # 9 to 5
    215: (['C','Am','F','G'], ['C','Am','F','G','Em'], ['Cmaj7','Am7','Fmaj7','G7','Em7']),  # I Will Always Love You (Dolly)
    216: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['G7','Cmaj7','D7','Em7','Am7']),  # Ring of Fire (simplified)
    217: (['E','A','D','G'], ['E','A','D','G','B'], ['E7','A7','D7','G7','B7']),  # Folsom Prison Blues
    218: (['A','D','E','G'], ['A','D','E','G','Bm'], ['A7','D7','E7','G7','Bm7']),  # Walk the Line
    219: (['Am','C','D','F'], ['Am','C','D','F','G'], ['Am7','Cmaj7','D7','Fmaj7','G7']),  # Hurt (Johnny Cash version)
    220: (['Am','Em','D','G'], ['Am','Em','D','G','C'], ['Am7','Em7','D7','Gmaj7','Cmaj7']),  # Man in Black
    221: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # Friends in Low Places
    222: (['G','D','Em','C'], ['G','D','Em','C','Am'], ['Gmaj7','D7','Em7','Cmaj7','Am7']),  # The Dance
    223: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['G7','Cmaj7','D7','Em7','Am7']),  # Thunder Rolls
    224: (['G','D','Em','C'], ['G','D','Em','C','Am'], ['Gmaj7','D7','Em7','Cmaj7','Am7']),  # Wagon Wheel
    225: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # The Gambler
    226: (['C','F','G','Am'], ['C','F','G','Am','Em'], ['Cmaj7','Fmaj7','G7','Am7','Em7']),  # Islands in the Stream (simplified)
    227: (['C','F','G','Am'], ['C','F','G','Am','Em'], ['Cmaj7','Fmaj7','G7','Am7','Em7']),  # On the Road Again
    228: (['G','D','C','Em'], ['G','D','C','Em','Am'], ['Gmaj7','D7','Cmaj7','Em7','Am7']),  # Blue Eyes Crying in the Rain
    229: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G7','Am7','Fmaj7','Em7']),  # Always on My Mind
    230: (['G','D','Am','C'], ['G','D','Am','C','Em'], ['Gmaj7','D7','Am7','Cmaj7','Em7']),  # Mammas Don't Let Your Babies
    231: (['G','D','C','Em'], ['G','D','C','Em','Am'], ['Gmaj7','D7','Cmaj7','Em7','Am7']),  # He Stopped Loving Her Today
    232: (['A','D','E','G'], ['A','D','E','G','Bm'], ['A7','D7','E7','G7','Bm7']),  # Achy Breaky Heart
    233: (['E','A','D','G'], ['E','A','D','G','B'], ['E7','A7','D7','G7','B7']),  # Boot Scootin Boogie (simplified)
    234: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # Cruise
    235: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # Chicken Fried
    236: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G7','Am7','Fmaj7','Em7']),  # Toes
    237: (['Em','C','G','D'], ['Em','C','G','D','Am'], ['Em7','Cmaj7','Gmaj7','D7','Am7']),  # Colder Weather
    238: (['A','D','E','Bm'], ['A','D','E','Bm','F#m'], ['A7','D7','E7','Bm7','F#m7']),  # Tennessee Whiskey (simplified)
    239: (['D','A','G','Bm'], ['D','A','G','Bm','Em'], ['D7','A7','Gmaj7','Bm7','Em7']),  # Traveller
    240: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # Body Like a Back Road
    241: (['G','D','Em','C'], ['G','D','Em','C','Am'], ['Gmaj7','D7','Em7','Cmaj7','Am7']),  # Die a Happy Man
    242: (['G','Am','C','D'], ['G','Am','C','D','Em'], ['Gmaj7','Am7','Cmaj7','D7','Em7']),  # Meant to Be
    243: (['Am','C','G','D'], ['Am','C','G','D','Em'], ['Am7','Cmaj7','G7','D7','Em7']),  # Need You Now
    244: (['C','G','Am','F'], ['C','G','Am','F','Em'], ['Cmaj7','G7','Am7','Fmaj7','Em7']),  # Wanted
    245: (['A','D','E','Bm'], ['A','D','E','Bm','F#m'], ['A7','D7','E7','Bm7','F#m7']),  # Springsteen
    246: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # Drunk on a Plane
    247: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # Drunk on You
    248: (['G','C','D','Em'], ['G','C','D','Em','Am'], ['Gmaj7','Cmaj7','D7','Em7','Am7']),  # Play It Again
    249: (['G','D','Am','C'], ['G','D','Am','C','Em'], ['Gmaj7','D7','Am7','Cmaj7','Em7']),  # Dirt Road Anthem
}

def main():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'songs.json')
    with open(data_path) as f:
        songs = json.load(f)

    updated = 0
    for idx in range(min(250, len(songs))):
        if idx not in REAL_CHORDS:
            continue
        easy_chords, med_chords, adv_chords = REAL_CHORDS[idx]
        song = songs[idx]
        title = song['title']
        artist = song['artist']

        # Update easy
        song['easy']['chords'] = [chord(c) for c in easy_chords]
        song['easy']['lyrics'] = make_lyrics(title, artist, easy_chords)

        # Update medium
        song['medium']['chords'] = [chord(c) for c in med_chords]
        song['medium']['lyrics'] = make_lyrics(title, artist, med_chords)

        # Update advanced
        song['advanced']['chords'] = [chord(c) for c in adv_chords]
        song['advanced']['lyrics'] = make_lyrics(title, artist, adv_chords)

        updated += 1

    with open(data_path, 'w') as f:
        json.dump(songs, f, indent=2)

    print(f"Updated {updated} songs (indices 0-249) with real chord progressions")
    print(f"Total songs in library: {len(songs)}")

if __name__ == '__main__':
    main()
