import * as fs from 'fs';
import * as path from 'path';

// Missing songs 11-25 with real ukulele chord data
const missingSongs = [
  {
    id: "hallelujah-leonard-cohen",
    title: "Hallelujah",
    artist: "Leonard Cohen",
    easy: {
      chords: [
        { name: "C", frets: [0,0,0,3], fingers: [0,0,0,3] },
        { name: "Am", frets: [2,0,0,0], fingers: [1,0,0,0] },
        { name: "F", frets: [2,0,1,0], fingers: [2,0,1,0] },
        { name: "G", frets: [0,2,3,2], fingers: [0,1,3,2] },
        { name: "Em", frets: [0,4,3,2], fingers: [0,3,2,1] }
      ],
      strummingPattern: "D D U U D U",
      strummingDescription: "Gentle fingerpicking-style strum in 6/8 time",
      lyrics: "[C]I've heard there was a [Am]secret chord\nThat [C]David played and it [Am]pleased the Lord\nBut [F]you don't really [G]care for music, [C]do ya? [G]\nIt [C]goes like this, the [F]fourth, the [G]fifth\nThe [Am]minor fall and the [F]major lift\nThe [G]baffled king com[Em]posing Halle[Am]lujah\n\n[F]Hallelu[Am]jah, [F]Hallelu[Am]jah\n[F]Hallelu[C]jah, Hallelu[G]u[C]jah"
    },
    medium: {
      chords: [
        { name: "C", frets: [0,0,0,3], fingers: [0,0,0,3] },
        { name: "Am", frets: [2,0,0,0], fingers: [1,0,0,0] },
        { name: "Am7", frets: [0,0,0,0], fingers: [0,0,0,0] },
        { name: "F", frets: [2,0,1,0], fingers: [2,0,1,0] },
        { name: "G", frets: [0,2,3,2], fingers: [0,1,3,2] },
        { name: "G7", frets: [0,2,1,2], fingers: [0,2,1,3] },
        { name: "Em7", frets: [0,2,0,2], fingers: [0,1,0,2] }
      ],
      strummingPattern: "D - D U - U D U",
      strummingDescription: "Arpeggiated strum with pauses for a reflective feel",
      lyrics: "[C]I've heard there was a [Am]secret chord\nThat [C]David played and it [Am7]pleased the Lord\nBut [F]you don't really [G7]care for music, [C]do ya? [G]\nIt [C]goes like this, the [F]fourth, the [G]fifth\nThe [Am]minor fall and the [F]major lift\nThe [G7]baffled king com[Em7]posing Halle[Am]lujah\n\n[F]Hallelu[Am]jah, [F]Hallelu[Am]jah\n[F]Hallelu[C]jah, Hallelu[G7]u[C]jah"
    },
    advanced: {
      chords: [
        { name: "Cmaj7", frets: [0,0,0,2], fingers: [0,0,0,2] },
        { name: "Am9", frets: [2,0,0,2], fingers: [1,0,0,2] },
        { name: "Fmaj7", frets: [2,4,1,3], fingers: [1,3,0,2] },
        { name: "G13", frets: [0,2,1,2], fingers: [0,2,1,3] },
        { name: "Em9", frets: [0,2,0,2], fingers: [0,1,0,2] },
        { name: "Dm7", frets: [2,2,1,3], fingers: [1,2,0,3] }
      ],
      strummingPattern: "D - U - D U x U",
      strummingDescription: "Fingerpicked arpeggios with ghost strums for intimacy",
      lyrics: "[Cmaj7]I've heard there was a [Am9]secret chord\nThat [Cmaj7]David played and it [Am9]pleased the Lord\nBut [Fmaj7]you don't really [G13]care for music, [Cmaj7]do ya?\nIt [Cmaj7]goes like this, the [Fmaj7]fourth, the [G13]fifth\nThe [Am9]minor fall and the [Fmaj7]major lift\nThe [G13]baffled king com[Em9]posing Halle[Am9]lujah\n\n[Fmaj7]Hallelu[Am9]jah, [Fmaj7]Hallelu[Am9]jah\n[Fmaj7]Hallelu[Cmaj7]jah, Hallelu[G13]u[Cmaj7]jah"
    }
  },
  {
    id: "you-are-my-sunshine-traditional",
    title: "You Are My Sunshine",
    artist: "Traditional",
    easy: {
      chords: [
        { name: "C", frets: [0,0,0,3], fingers: [0,0,0,3] },
        { name: "F", frets: [2,0,1,0], fingers: [2,0,1,0] },
        { name: "G", frets: [0,2,3,2], fingers: [0,1,3,2] }
      ],
      strummingPattern: "D D U U D U",
      strummingDescription: "Simple country strum with a steady beat",
      lyrics: "The other [C]night dear, as I lay sleeping\nI dreamed I [F]held you in my [C]arms\nBut when I [F]awoke dear, I was mis[C]taken\nSo I hung my [G]head and I [C]cried\n\nYou are my [C]sunshine, my only sunshine\nYou make me [F]happy when skies are [C]gray\nYou'll never [F]know dear, how much I [C]love you\nPlease don't take my [G]sunshine a[C]way"
    },
    medium: {
      chords: [
        { name: "C", frets: [0,0,0,3], fingers: [0,0,0,3] },
        { name: "C7", frets: [0,0,0,1], fingers: [0,0,0,1] },
        { name: "F", frets: [2,0,1,0], fingers: [2,0,1,0] },
        { name: "G7", frets: [0,2,1,2], fingers: [0,2,1,3] }
      ],
      strummingPattern: "D D U - D U D U",
      strummingDescription: "Country swing with a slight shuffle feel",
      lyrics: "The other [C]night dear, as I lay [C7]sleeping\nI dreamed I [F]held you in my [C]arms\nBut when I [F]awoke dear, I was mis[C]taken\nSo I hung my [G7]head and I [C]cried\n\nYou are my [C]sunshine, my only [C7]sunshine\nYou make me [F]happy when skies are [C]gray\nYou'll never [F]know dear, how much I [C]love you\nPlease don't take my [G7]sunshine a[C]way"
    },
    advanced: {
      chords: [
        { name: "Cmaj7", frets: [0,0,0,2], fingers: [0,0,0,2] },
        { name: "C9", frets: [0,0,0,1], fingers: [0,0,0,1] },
        { name: "Fmaj7", frets: [2,4,1,3], fingers: [1,3,0,2] },
        { name: "G9", frets: [0,2,1,0], fingers: [0,2,1,0] },
        { name: "Am7", frets: [0,0,0,0], fingers: [0,0,0,0] }
      ],
      strummingPattern: "D U x U D - U D",
      strummingDescription: "Jazzy country swing with muted ghost notes",
      lyrics: "[Cmaj7]The other night dear, as I lay [C9]sleeping\nI dreamed I [Fmaj7]held you in my [Cmaj7]arms\nBut when I [Fmaj7]awoke dear, I was mis[Am7]taken\nSo I hung my [G9]head and I [Cmaj7]cried\n\nYou are my [Cmaj7]sunshine, my only [C9]sunshine\nYou make me [Fmaj7]happy when skies are [Cmaj7]gray\nYou'll never [Fmaj7]know dear, how much I [Am7]love you\nPlease don't take my [G9]sunshine a[Cmaj7]way"
    }
  },
  {
    id: "wonderwall-oasis",
    title: "Wonderwall",
    artist: "Oasis",
    easy: {
      chords: [
        { name: "Em", frets: [0,4,3,2], fingers: [0,3,2,1] },
        { name: "G", frets: [0,2,3,2], fingers: [0,1,3,2] },
        { name: "D", frets: [2,2,2,0], fingers: [1,2,3,0] },
        { name: "C", frets: [0,0,0,3], fingers: [0,0,0,3] }
      ],
      strummingPattern: "D D U U D U",
      strummingDescription: "Driving folk-rock strum with emphasis on beats 1 and 3",
      lyrics: "[Em]Today is gonna be the day that they're [G]gonna throw it back to you\n[D]By now you shoulda somehow [C]realized what you gotta do\n[Em]I don't believe that anybody [G]feels the way I do\n[D]About you [C]now\n\n[C]And all the roads we [D]have to walk are winding\n[Em]And all the lights that [G]lead us there are blinding\n[C]There are many things that [D]I would like to say to you\nBut I don't know [G]how\n\nBecause [C]maybe, [D]you're gonna be the one that [Em]saves me\nAnd [C]after [D]all, you're my wonder[Em]wall"
    },
    medium: {
      chords: [
        { name: "Em7", frets: [0,2,0,2], fingers: [0,1,0,2] },
        { name: "G", frets: [0,2,3,2], fingers: [0,1,3,2] },
        { name: "Dsus4", frets: [2,2,0,0], fingers: [1,2,0,0] },
        { name: "Cadd9", frets: [0,0,0,3], fingers: [0,0,0,3] },
        { name: "A7sus4", frets: [0,2,0,0], fingers: [0,1,0,0] }
      ],
      strummingPattern: "D - D U - U D U",
      strummingDescription: "Signature Wonderwall strum with pauses on beat 2",
      lyrics: "[Em7]Today is gonna be the day that they're [G]gonna throw it back to you\n[Dsus4]By now you shoulda somehow [A7sus4]realized what you gotta do\n[Em7]I don't believe that anybody [G]feels the way I do\n[Dsus4]About you [A7sus4]now\n\n[Cadd9]And all the roads we [Dsus4]have to walk are winding\n[Em7]And all the lights that [G]lead us there are blinding\n[Cadd9]There are many things that [Dsus4]I would like to say to you\nBut I don't know [G]how\n\nBecause [Cadd9]maybe, [Dsus4]you're gonna be the one that [Em7]saves me\nAnd [Cadd9]after [Dsus4]all, you're my wonder[Em7]wall"
    },
    advanced: {
      chords: [
        { name: "Em7", frets: [0,2,0,2], fingers: [0,1,0,2] },
        { name: "Gmaj7", frets: [0,2,2,2], fingers: [0,1,2,3] },
        { name: "Dsus4", frets: [2,2,0,0], fingers: [1,2,0,0] },
        { name: "Cadd9", frets: [0,0,0,3], fingers: [0,0,0,3] },
        { name: "A7sus4", frets: [0,2,0,0], fingers: [0,1,0,0] },
        { name: "F#m7", frets: [2,4,2,4], fingers: [1,3,1,4] }
      ],
      strummingPattern: "D U x U D U x U",
      strummingDescription: "Layered strum with percussive mutes on the and-beats",
      lyrics: "[Em7]Today is gonna be the day that they're [Gmaj7]gonna throw it back to you\n[Dsus4]By now you shoulda somehow [A7sus4]realized what you gotta do\n[Em7]I don't believe that anybody [Gmaj7]feels the way I do\n[Dsus4]About you [A7sus4]now\n\n[Cadd9]And all the roads we [Dsus4]have to walk are winding\n[Em7]And all the lights that [Gmaj7]lead us there are blinding\n[Cadd9]There are many things that [Dsus4]I would like to say to you\nBut I don't know [Gmaj7]how\n\nBecause [Cadd9]maybe, [Dsus4]you're gonna be the one that [Em7]saves me\nAnd [Cadd9]after [Dsus4]all, you're my wonder[Em7]wall"
    }
  },
  {
    id: "no-woman-no-cry-bob-marley",
    title: "No Woman No Cry",
    artist: "Bob Marley",
    easy: {
      chords: [
        { name: "C", frets: [0,0,0,3], fingers: [0,0,0,3] },
        { name: "G", frets: [0,2,3,2], fingers: [0,1,3,2] },
        { name: "Am", frets: [2,0,0,0], fingers: [1,0,0,0] },
        { name: "F", frets: [2,0,1,0], fingers: [2,0,1,0] }
      ],
      strummingPattern: "D D U U D U",
      strummingDescription: "Laid-back reggae strum emphasizing the offbeat",
      lyrics: "[C]No [G]woman no [Am]cry [F]\n[C]No [G]woman no [Am]cry [F]\n\n[C]Said, said, [G]said I remember [Am]when we used to [F]sit\n[C]In the govern[G]ment yard in [Am]Trench[F]town\n[C]Oba, ob[G]serving the [Am]hypocrites [F]\n[C]As they would [G]mingle with the [Am]good people we [F]meet\n\n[C]Everything's gonna [G]be alright\n[Am]Everything's gonna [F]be alright"
    },
    medium: {
      chords: [
        { name: "C", frets: [0,0,0,3], fingers: [0,0,0,3] },
        { name: "G", frets: [0,2,3,2], fingers: [0,1,3,2] },
        { name: "Am7", frets: [0,0,0,0], fingers: [0,0,0,0] },
        { name: "Fmaj7", frets: [2,4,1,3], fingers: [1,3,0,2] },
        { name: "G7", frets: [0,2,1,2], fingers: [0,2,1,3] }
      ],
      strummingPattern: "D - U - D U - U",
      strummingDescription: "Reggae skank with emphasis on beats 2 and 4",
      lyrics: "[C]No [G7]woman no [Am7]cry [Fmaj7]\n[C]No [G7]woman no [Am7]cry [Fmaj7]\n\n[C]Said, said, [G7]said I remember [Am7]when we used to [Fmaj7]sit\n[C]In the govern[G7]ment yard in [Am7]Trench[Fmaj7]town\n\n[C]Everything's gonna [G7]be alright\n[Am7]Everything's gonna [Fmaj7]be alright"
    },
    advanced: {
      chords: [
        { name: "Cmaj9", frets: [0,0,0,2], fingers: [0,0,0,2] },
        { name: "G13", frets: [0,2,1,2], fingers: [0,2,1,3] },
        { name: "Am9", frets: [2,0,0,2], fingers: [1,0,0,2] },
        { name: "Fmaj9", frets: [2,4,1,0], fingers: [2,4,1,0] },
        { name: "Dm9", frets: [2,2,1,3], fingers: [1,2,0,3] }
      ],
      strummingPattern: "x U x U D U x U",
      strummingDescription: "Authentic reggae skank with muted downstrokes and offbeat accents",
      lyrics: "[Cmaj9]No [G13]woman no [Am9]cry [Fmaj9]\n[Cmaj9]No [G13]woman no [Am9]cry [Fmaj9]\n\n[Cmaj9]Said, said, [G13]said I remember [Am9]when we used to [Fmaj9]sit\n[Cmaj9]In the govern[G13]ment yard in [Am9]Trench[Fmaj9]town\n\n[Cmaj9]Everything's gonna [G13]be alright\n[Am9]Everything's gonna [Fmaj9]be alright"
    }
  },
  {
    id: "what-a-wonderful-world-louis-armstrong",
    title: "What a Wonderful World",
    artist: "Louis Armstrong",
    easy: {
      chords: [
        { name: "C", frets: [0,0,0,3], fingers: [0,0,0,3] },
        { name: "Em", frets: [0,4,3,2], fingers: [0,3,2,1] },
        { name: "F", frets: [2,0,1,0], fingers: [2,0,1,0] },
        { name: "G", frets: [0,2,3,2], fingers: [0,1,3,2] },
        { name: "Am", frets: [2,0,0,0], fingers: [1,0,0,0] }
      ],
      strummingPattern: "D D U U D U",
      strummingDescription: "Gentle, slow strum with a warm swing feel",
      lyrics: "I see [C]trees of [Em]green, [F]red roses [C]too\n[F]I see them [C]bloom, [Em]for me and [Am]you\nAnd I [F]think to myself, [G]what a wonderful [C]world [F] [C]\n\nI see [C]skies of [Em]blue and [F]clouds of [C]white\nThe [F]bright blessed [C]day, the [Em]dark sacred [Am]night\nAnd I [F]think to myself, [G]what a wonderful [C]world [F] [C]"
    },
    medium: {
      chords: [
        { name: "C", frets: [0,0,0,3], fingers: [0,0,0,3] },
        { name: "Em7", frets: [0,2,0,2], fingers: [0,1,0,2] },
        { name: "Fmaj7", frets: [2,4,1,3], fingers: [1,3,0,2] },
        { name: "G7", frets: [0,2,1,2], fingers: [0,2,1,3] },
        { name: "Am7", frets: [0,0,0,0], fingers: [0,0,0,0] },
        { name: "Dm7", frets: [2,2,1,3], fingers: [1,2,0,3] }
      ],
      strummingPattern: "D - U - D U - U",
      strummingDescription: "Jazzy swing strum, relaxed and lyrical",
      lyrics: "I see [C]trees of [Em7]green, [Fmaj7]red roses [C]too\n[Fmaj7]I see them [C]bloom, [Em7]for me and [Am7]you\nAnd I [Dm7]think to myself, [G7]what a wonderful [C]world [Fmaj7] [C]\n\nI see [C]skies of [Em7]blue and [Fmaj7]clouds of [C]white\nThe [Fmaj7]bright blessed [C]day, the [Em7]dark sacred [Am7]night\nAnd I [Dm7]think to myself, [G7]what a wonderful [C]world [Fmaj7] [C]"
    },
    advanced: {
      chords: [
        { name: "Cmaj9", frets: [0,0,0,2], fingers: [0,0,0,2] },
        { name: "Em9", frets: [0,2,0,2], fingers: [0,1,0,2] },
        { name: "Fmaj7", frets: [2,4,1,3], fingers: [1,3,0,2] },
        { name: "G13", frets: [0,2,1,2], fingers: [0,2,1,3] },
        { name: "Am9", frets: [2,0,0,2], fingers: [1,0,0,2] },
        { name: "Dm9", frets: [2,2,1,3], fingers: [1,2,0,3] },
        { name: "Bdim7", frets: [1,2,1,2], fingers: [1,3,2,4] }
      ],
      strummingPattern: "D - U x D U - U",
      strummingDescription: "Classic jazz ballad strum with chromatic passing chords",
      lyrics: "I see [Cmaj9]trees of [Em9]green, [Fmaj7]red roses [Cmaj9]too\n[Fmaj7]I see them [Cmaj9]bloom, [Em9]for me and [Am9]you\nAnd I [Dm9]think to myself, [G13]what a wonderful [Cmaj9]world [Fmaj7] [Cmaj9]\n\nI see [Cmaj9]skies of [Em9]blue and [Fmaj7]clouds of [Cmaj9]white\nThe [Fmaj7]bright blessed [Cmaj9]day, the [Em9]dark sacred [Am9]night\nAnd I [Dm9]think to myself, [G13]what a wonderful [Cmaj9]world"
    }
  },
  {
    id: "banana-pancakes-jack-johnson",
    title: "Banana Pancakes",
    artist: "Jack Johnson",
    easy: {
      chords: [
        { name: "G", frets: [0,2,3,2], fingers: [0,1,3,2] },
        { name: "D", frets: [2,2,2,0], fingers: [1,2,3,0] },
        { name: "Am", frets: [2,0,0,0], fingers: [1,0,0,0] },
        { name: "C", frets: [0,0,0,3], fingers: [0,0,0,3] }
      ],
      strummingPattern: "D D U U D U",
      strummingDescription: "Lazy morning strum, relaxed and groovy",
      lyrics: "[G]Can't you see that it's [D]just raining\n[Am]There ain't no need to [C]go outside\n\n[G]But baby, you hardly [D]even notice\n[Am]When I try to [C]show you this\n[G]Song is meant to [D]keep you\nFrom [Am]doing what you're [C]supposed to\n[G]Waking up too [D]early\n[Am]Maybe we could [C]sleep in\n\n[G]Make you banana [D]pancakes\n[Am]Pretend like it's the [C]weekend now"
    },
    medium: {
      chords: [
        { name: "G7", frets: [0,2,1,2], fingers: [0,2,1,3] },
        { name: "D7", frets: [2,2,2,3], fingers: [1,2,3,4] },
        { name: "Am7", frets: [0,0,0,0], fingers: [0,0,0,0] },
        { name: "C", frets: [0,0,0,3], fingers: [0,0,0,3] }
      ],
      strummingPattern: "D U x U D U x U",
      strummingDescription: "Funky muted strum with a Jack Johnson groove",
      lyrics: "[G7]Can't you see that it's [D7]just raining\n[Am7]There ain't no need to [C]go outside\n\n[G7]But baby, you hardly [D7]even notice\n[Am7]When I try to [C]show you this\n\n[G7]Make you banana [D7]pancakes\n[Am7]Pretend like it's the [C]weekend now"
    },
    advanced: {
      chords: [
        { name: "G7", frets: [0,2,1,2], fingers: [0,2,1,3] },
        { name: "D9", frets: [2,4,2,3], fingers: [1,3,1,2] },
        { name: "Am9", frets: [2,0,0,2], fingers: [1,0,0,2] },
        { name: "Cmaj7", frets: [0,0,0,2], fingers: [0,0,0,2] },
        { name: "Em7", frets: [0,2,0,2], fingers: [0,1,0,2] }
      ],
      strummingPattern: "D U x U D x U D",
      strummingDescription: "Neo-soul groove with heavy muting and syncopation",
      lyrics: "[G7]Can't you see that it's [D9]just raining\n[Am9]There ain't no need to [Cmaj7]go outside\n\n[G7]But baby, you hardly [D9]even notice\n[Am9]When I try to [Cmaj7]show you this\n\n[G7]Make you banana [D9]pancakes\n[Am9]Pretend like it's the [Cmaj7]weekend [Em7]now"
    }
  },
  {
    id: "better-together-jack-johnson",
    title: "Better Together",
    artist: "Jack Johnson",
    easy: {
      chords: [
        { name: "F", frets: [2,0,1,0], fingers: [2,0,1,0] },
        { name: "C", frets: [0,0,0,3], fingers: [0,0,0,3] },
        { name: "G", frets: [0,2,3,2], fingers: [0,1,3,2] },
        { name: "Am", frets: [2,0,0,0], fingers: [1,0,0,0] }
      ],
      strummingPattern: "D D U U D U",
      strummingDescription: "Warm, easygoing strum perfect for a beach day",
      lyrics: "There's no combi[F]nation of words I could put on the back of a [C]postcard\nNo [G]song that I could sing but I can [Am]try for your heart\nOur [F]dreams and they are made out of [C]real things\nLike a [G]shoebox of photographs with [Am]sepia-toned loving\n\n[F]Love is the [C]answer at least for [G]most of the questions in my [Am]heart\n[F]Like why are we [C]here and where do we [G]go and how come it's so [Am]hard\n\nIt's [F]always better when we're [C]together\n[G]Yeah we'll look at the stars when we're to[Am]gether"
    },
    medium: {
      chords: [
        { name: "Fmaj7", frets: [2,4,1,3], fingers: [1,3,0,2] },
        { name: "C", frets: [0,0,0,3], fingers: [0,0,0,3] },
        { name: "G7", frets: [0,2,1,2], fingers: [0,2,1,3] },
        { name: "Am7", frets: [0,0,0,0], fingers: [0,0,0,0] },
        { name: "Dm7", frets: [2,2,1,3], fingers: [1,2,0,3] }
      ],
      strummingPattern: "D - U - D U - U",
      strummingDescription: "Fingerpicked intro transitioning to light strumming",
      lyrics: "There's no combi[Fmaj7]nation of words I could put on the back of a [C]postcard\nNo [G7]song that I could sing but I can [Am7]try for your heart\n\nIt's [Fmaj7]always better when we're [C]together\n[G7]Yeah we'll look at the stars when we're to[Am7]gether"
    },
    advanced: {
      chords: [
        { name: "Fmaj9", frets: [2,4,1,0], fingers: [2,4,1,0] },
        { name: "Cmaj7", frets: [0,0,0,2], fingers: [0,0,0,2] },
        { name: "G13", frets: [0,2,1,2], fingers: [0,2,1,3] },
        { name: "Am9", frets: [2,0,0,2], fingers: [1,0,0,2] },
        { name: "Dm9", frets: [2,2,1,3], fingers: [1,2,0,3] }
      ],
      strummingPattern: "D U x U - U D U",
      strummingDescription: "Sophisticated fingerstyle with jazzy chord movements",
      lyrics: "There's no combi[Fmaj9]nation of words I could put on the back of a [Cmaj7]postcard\nNo [G13]song that I could sing but I can [Am9]try for your heart\n\nIt's [Fmaj9]always better when we're [Cmaj7]together\n[G13]Yeah we'll look at the stars when we're to[Am9]gether"
    }
  },
  {
    id: "la-vie-en-rose-edith-piaf",
    title: "La Vie En Rose",
    artist: "Edith Piaf",
    easy: {
      chords: [
        { name: "C", frets: [0,0,0,3], fingers: [0,0,0,3] },
        { name: "G", frets: [0,2,3,2], fingers: [0,1,3,2] },
        { name: "F", frets: [2,0,1,0], fingers: [2,0,1,0] },
        { name: "Am", frets: [2,0,0,0], fingers: [1,0,0,0] },
        { name: "Dm", frets: [2,2,1,0], fingers: [2,3,1,0] }
      ],
      strummingPattern: "D D U U D U",
      strummingDescription: "Gentle waltz-like strum in 3/4 feel",
      lyrics: "[C]Hold me close and hold me fast\nThis magic spell you [G]cast\nThis is la vie en [C]rose\n\n[C]When you kiss me heaven sighs\nAnd though I close my [G]eyes\nI see la vie en [C]rose\n\n[F]When you press me to your [C]heart\nI'm in a world a[Dm]part\nA world where roses [G]bloom\n\nAnd [C]when you speak, angels sing from above\n[G]Everyday words seem to turn into love [C]songs"
    },
    medium: {
      chords: [
        { name: "Cmaj7", frets: [0,0,0,2], fingers: [0,0,0,2] },
        { name: "G7", frets: [0,2,1,2], fingers: [0,2,1,3] },
        { name: "Fmaj7", frets: [2,4,1,3], fingers: [1,3,0,2] },
        { name: "Am7", frets: [0,0,0,0], fingers: [0,0,0,0] },
        { name: "Dm7", frets: [2,2,1,3], fingers: [1,2,0,3] }
      ],
      strummingPattern: "D - U - D - U -",
      strummingDescription: "Romantic waltz strum with space between beats",
      lyrics: "[Cmaj7]Hold me close and hold me fast\nThis magic spell you [G7]cast\nThis is la vie en [Cmaj7]rose\n\n[Fmaj7]When you press me to your [Cmaj7]heart\nI'm in a world a[Dm7]part\nA world where roses [G7]bloom"
    },
    advanced: {
      chords: [
        { name: "Cmaj9", frets: [0,0,0,2], fingers: [0,0,0,2] },
        { name: "G13", frets: [0,2,1,2], fingers: [0,2,1,3] },
        { name: "Fmaj9", frets: [2,4,1,0], fingers: [2,4,1,0] },
        { name: "Am9", frets: [2,0,0,2], fingers: [1,0,0,2] },
        { name: "Dm9", frets: [2,2,1,3], fingers: [1,2,0,3] },
        { name: "Bdim7", frets: [1,2,1,2], fingers: [1,3,2,4] }
      ],
      strummingPattern: "D - U x D - U -",
      strummingDescription: "French jazz waltz with chromatic passing tones",
      lyrics: "[Cmaj9]Hold me close and hold me fast\nThis magic spell you [Bdim7]cast [G13]\nThis is la vie en [Cmaj9]rose\n\n[Fmaj9]When you press me to your [Cmaj9]heart\nI'm in a world a[Dm9]part\nA world where roses [G13]bloom"
    }
  },
  {
    id: "hey-jude-the-beatles",
    title: "Hey Jude",
    artist: "The Beatles",
    easy: {
      chords: [
        { name: "C", frets: [0,0,0,3], fingers: [0,0,0,3] },
        { name: "F", frets: [2,0,1,0], fingers: [2,0,1,0] },
        { name: "G", frets: [0,2,3,2], fingers: [0,1,3,2] },
        { name: "Am", frets: [2,0,0,0], fingers: [1,0,0,0] }
      ],
      strummingPattern: "D D U U D U",
      strummingDescription: "Classic rock ballad strum building in intensity",
      lyrics: "Hey [C]Jude, don't make it [G]bad\nTake a [G]sad song and make it [C]better\nRe[F]member to let her into your [C]heart\nThen you can [G]start to make it [C]better\n\nHey [C]Jude don't be a[G]fraid\nYou were [G]made to go out and [C]get her\nThe [F]minute you let her under your [C]skin\nThen you be[G]gin to make it [C]better\n\n[C]Na na na [F]na na na na [G]na na na na, hey [C]Jude"
    },
    medium: {
      chords: [
        { name: "C", frets: [0,0,0,3], fingers: [0,0,0,3] },
        { name: "C7", frets: [0,0,0,1], fingers: [0,0,0,1] },
        { name: "F", frets: [2,0,1,0], fingers: [2,0,1,0] },
        { name: "G7", frets: [0,2,1,2], fingers: [0,2,1,3] },
        { name: "Am7", frets: [0,0,0,0], fingers: [0,0,0,0] },
        { name: "Dm7", frets: [2,2,1,3], fingers: [1,2,0,3] }
      ],
      strummingPattern: "D - D U - U D U",
      strummingDescription: "Building ballad strum with dynamic swells",
      lyrics: "Hey [C]Jude, don't make it [G7]bad\nTake a [G7]sad song and make it [C]better\nRe[F]member to let her into your [C]heart\nThen you can [G7]start to make it [C]better\n\n[C]Na na na [F]na na na na [G7]na na na na, hey [C]Jude"
    },
    advanced: {
      chords: [
        { name: "Cmaj7", frets: [0,0,0,2], fingers: [0,0,0,2] },
        { name: "C7", frets: [0,0,0,1], fingers: [0,0,0,1] },
        { name: "Fmaj9", frets: [2,4,1,0], fingers: [2,4,1,0] },
        { name: "G13", frets: [0,2,1,2], fingers: [0,2,1,3] },
        { name: "Am9", frets: [2,0,0,2], fingers: [1,0,0,2] },
        { name: "Dm9", frets: [2,2,1,3], fingers: [1,2,0,3] }
      ],
      strummingPattern: "D U - U D U x U",
      strummingDescription: "Full band feel with driving rhythm building to the na-na coda",
      lyrics: "Hey [Cmaj7]Jude, don't make it [G13]bad\nTake a [G13]sad song and make it [Cmaj7]better\nRe[Fmaj9]member to let her into your [Cmaj7]heart\nThen you can [G13]start to make it [Cmaj7]better\n\n[Cmaj7]Na na na [Fmaj9]na na na na [G13]na na na na, hey [Cmaj7]Jude"
    }
  },
  {
    id: "imagine-john-lennon",
    title: "Imagine",
    artist: "John Lennon",
    easy: {
      chords: [
        { name: "C", frets: [0,0,0,3], fingers: [0,0,0,3] },
        { name: "F", frets: [2,0,1,0], fingers: [2,0,1,0] },
        { name: "Am", frets: [2,0,0,0], fingers: [1,0,0,0] },
        { name: "Dm", frets: [2,2,1,0], fingers: [2,3,1,0] },
        { name: "G", frets: [0,2,3,2], fingers: [0,1,3,2] }
      ],
      strummingPattern: "D D U U D U",
      strummingDescription: "Gentle, flowing strum mimicking the piano feel",
      lyrics: "[C]Imagine there's no [F]heaven\n[C]It's easy if you [F]try\n[C]No hell [F]below us\n[C]Above us only [F]sky\n\n[F]Imagine [Am]all the [Dm]people\n[G]Living for to[C]day\n\n[C]Imagine there's no [F]countries\n[C]It isn't hard to [F]do\n[C]Nothing to kill or [F]die for\n[C]And no religion [F]too\n\n[F]Imagine [Am]all the [Dm]people\n[G]Living life in [C]peace\n\n[F]You may [G]say I'm a [C]dreamer\n[F]But I'm [G]not the only [C]one\n[F]I hope some[G]day you'll [C]join us\n[F]And the [G]world will be as [C]one"
    },
    medium: {
      chords: [
        { name: "Cmaj7", frets: [0,0,0,2], fingers: [0,0,0,2] },
        { name: "F", frets: [2,0,1,0], fingers: [2,0,1,0] },
        { name: "Am7", frets: [0,0,0,0], fingers: [0,0,0,0] },
        { name: "Dm7", frets: [2,2,1,3], fingers: [1,2,0,3] },
        { name: "G7", frets: [0,2,1,2], fingers: [0,2,1,3] }
      ],
      strummingPattern: "D - U - D U - U",
      strummingDescription: "Piano-style arpeggiated strum with sustained chords",
      lyrics: "[Cmaj7]Imagine there's no [F]heaven\n[Cmaj7]It's easy if you [F]try\n\n[F]Imagine [Am7]all the [Dm7]people\n[G7]Living for to[Cmaj7]day\n\n[F]You may [G7]say I'm a [Cmaj7]dreamer\n[F]But I'm [G7]not the only [Cmaj7]one"
    },
    advanced: {
      chords: [
        { name: "Cmaj9", frets: [0,0,0,2], fingers: [0,0,0,2] },
        { name: "Fmaj7", frets: [2,4,1,3], fingers: [1,3,0,2] },
        { name: "Am9", frets: [2,0,0,2], fingers: [1,0,0,2] },
        { name: "Dm9", frets: [2,2,1,3], fingers: [1,2,0,3] },
        { name: "G13", frets: [0,2,1,2], fingers: [0,2,1,3] },
        { name: "Em7", frets: [0,2,0,2], fingers: [0,1,0,2] }
      ],
      strummingPattern: "D - U x D - U -",
      strummingDescription: "Ethereal fingerpicking with lush jazz voicings",
      lyrics: "[Cmaj9]Imagine there's no [Fmaj7]heaven\n[Cmaj9]It's easy if you [Fmaj7]try\n\n[Fmaj7]Imagine [Am9]all the [Dm9]people\n[G13]Living for to[Cmaj9]day\n\n[Fmaj7]You may [G13]say I'm a [Cmaj9]dreamer\n[Fmaj7]But I'm [G13]not the only [Cmaj9]one\n[Fmaj7]I hope some[G13]day you'll [Em7]join us\n[Fmaj7]And the [G13]world will be as [Cmaj9]one"
    }
  },
  {
    id: "have-you-ever-seen-the-rain-ccr",
    title: "Have You Ever Seen the Rain",
    artist: "CCR",
    easy: {
      chords: [
        { name: "C", frets: [0,0,0,3], fingers: [0,0,0,3] },
        { name: "G", frets: [0,2,3,2], fingers: [0,1,3,2] },
        { name: "Am", frets: [2,0,0,0], fingers: [1,0,0,0] },
        { name: "F", frets: [2,0,1,0], fingers: [2,0,1,0] }
      ],
      strummingPattern: "D D U U D U",
      strummingDescription: "Steady rock strum with a driving feel",
      lyrics: "[C]Someone told me long ago\n[C]There's a calm before the storm, I [G]know\nIt's been coming [C]for some time\n\n[C]When it's over so they say\n[C]It'll rain a sunny day, I [G]know\nShining down like [C]water\n\n[F]I wanna [G]know\nHave you [C]ever [Am]seen the [F]rain\n[F]I wanna [G]know\nHave you [C]ever [Am]seen the [F]rain\n[G]Coming down on a sunny [C]day"
    },
    medium: {
      chords: [
        { name: "C", frets: [0,0,0,3], fingers: [0,0,0,3] },
        { name: "G7", frets: [0,2,1,2], fingers: [0,2,1,3] },
        { name: "Am7", frets: [0,0,0,0], fingers: [0,0,0,0] },
        { name: "Fmaj7", frets: [2,4,1,3], fingers: [1,3,0,2] },
        { name: "Em7", frets: [0,2,0,2], fingers: [0,1,0,2] }
      ],
      strummingPattern: "D - D U - U D U",
      strummingDescription: "Classic CCR rock groove with a slight swing",
      lyrics: "[C]Someone told me long ago\n[C]There's a calm before the storm, I [G7]know\nShining down like [C]water\n\n[Fmaj7]I wanna [G7]know\nHave you [C]ever [Am7]seen the [Fmaj7]rain\n[G7]Coming down on a sunny [C]day"
    },
    advanced: {
      chords: [
        { name: "Cmaj7", frets: [0,0,0,2], fingers: [0,0,0,2] },
        { name: "G13", frets: [0,2,1,2], fingers: [0,2,1,3] },
        { name: "Am9", frets: [2,0,0,2], fingers: [1,0,0,2] },
        { name: "Fmaj9", frets: [2,4,1,0], fingers: [2,4,1,0] },
        { name: "Em9", frets: [0,2,0,2], fingers: [0,1,0,2] }
      ],
      strummingPattern: "D U x U D U x U",
      strummingDescription: "Driving rock strum with muted ghost strokes",
      lyrics: "[Cmaj7]Someone told me long ago\n[Cmaj7]There's a calm before the storm, I [G13]know\n\n[Fmaj9]I wanna [G13]know\nHave you [Cmaj7]ever [Am9]seen the [Fmaj9]rain\n[G13]Coming down on a sunny [Cmaj7]day"
    }
  },
  {
    id: "house-of-the-rising-sun-the-animals",
    title: "House of the Rising Sun",
    artist: "The Animals",
    easy: {
      chords: [
        { name: "Am", frets: [2,0,0,0], fingers: [1,0,0,0] },
        { name: "C", frets: [0,0,0,3], fingers: [0,0,0,3] },
        { name: "D", frets: [2,2,2,0], fingers: [1,2,3,0] },
        { name: "F", frets: [2,0,1,0], fingers: [2,0,1,0] },
        { name: "Em", frets: [0,4,3,2], fingers: [0,3,2,1] }
      ],
      strummingPattern: "D D U U D U",
      strummingDescription: "Arpeggiated 6/8 time feel, each chord gets a full measure",
      lyrics: "[Am]There [C]is a [D]house in [F]New Orleans\n[Am]They [C]call the [Em]Rising Sun\n[Am]And it's [C]been the [D]ruin of [F]many a poor boy\nAnd [Am]God I [Em]know I'm [Am]one\n\n[Am]My [C]mother [D]was a [F]tailor\n[Am]She [C]sewed my [Em]new blue jeans\n[Am]My [C]father [D]was a [F]gamblin' man\n[Am]Down in [Em]New Or[Am]leans"
    },
    medium: {
      chords: [
        { name: "Am7", frets: [0,0,0,0], fingers: [0,0,0,0] },
        { name: "C", frets: [0,0,0,3], fingers: [0,0,0,3] },
        { name: "D7", frets: [2,2,2,3], fingers: [1,2,3,4] },
        { name: "Fmaj7", frets: [2,4,1,3], fingers: [1,3,0,2] },
        { name: "Em7", frets: [0,2,0,2], fingers: [0,1,0,2] }
      ],
      strummingPattern: "D - U D - U D -",
      strummingDescription: "Rolling arpeggio pattern in 6/8 time",
      lyrics: "[Am7]There [C]is a [D7]house in [Fmaj7]New Orleans\n[Am7]They [C]call the [Em7]Rising Sun\n[Am7]And it's [C]been the [D7]ruin of [Fmaj7]many a poor boy\nAnd [Am7]God I [Em7]know I'm [Am7]one"
    },
    advanced: {
      chords: [
        { name: "Am9", frets: [2,0,0,2], fingers: [1,0,0,2] },
        { name: "Cmaj7", frets: [0,0,0,2], fingers: [0,0,0,2] },
        { name: "D9", frets: [2,4,2,3], fingers: [1,3,1,2] },
        { name: "Fmaj9", frets: [2,4,1,0], fingers: [2,4,1,0] },
        { name: "Em9", frets: [0,2,0,2], fingers: [0,1,0,2] },
        { name: "Bdim7", frets: [1,2,1,2], fingers: [1,3,2,4] }
      ],
      strummingPattern: "D - U - D - U D",
      strummingDescription: "Classical fingerpicking arpeggio with dark minor voicings",
      lyrics: "[Am9]There [Cmaj7]is a [D9]house in [Fmaj9]New Orleans\n[Am9]They [Cmaj7]call the [Em9]Rising Sun\n[Am9]And it's [Cmaj7]been the [D9]ruin of [Fmaj9]many a poor boy\nAnd [Am9]God I [Em9]know I'm [Am9]one"
    }
  },
  {
    id: "a-thousand-years-christina-perri",
    title: "A Thousand Years",
    artist: "Christina Perri",
    easy: {
      chords: [
        { name: "C", frets: [0,0,0,3], fingers: [0,0,0,3] },
        { name: "G", frets: [0,2,3,2], fingers: [0,1,3,2] },
        { name: "Am", frets: [2,0,0,0], fingers: [1,0,0,0] },
        { name: "F", frets: [2,0,1,0], fingers: [2,0,1,0] },
        { name: "Em", frets: [0,4,3,2], fingers: [0,3,2,1] }
      ],
      strummingPattern: "D D U U D U",
      strummingDescription: "Gentle flowing strum in 3/4 time",
      lyrics: "[C]Heart beats fast, colors and [G]promises\n[Am]How to be brave, how can I [F]love when I'm afraid to fall\n[C]Watching you [G]stand alone\n[Am]All of my doubt suddenly [F]goes away somehow\n\n[Am]One [G]step [F]closer\n\n[C]I have died every day [G]waiting for you\n[Am]Darling don't be afraid I have [F]loved you\nFor a [C]thousand [G]years\nI'll love you for a [Am]thousand [F]more"
    },
    medium: {
      chords: [
        { name: "Cmaj7", frets: [0,0,0,2], fingers: [0,0,0,2] },
        { name: "Gsus4", frets: [0,2,3,3], fingers: [0,1,2,3] },
        { name: "Am7", frets: [0,0,0,0], fingers: [0,0,0,0] },
        { name: "Fmaj7", frets: [2,4,1,3], fingers: [1,3,0,2] },
        { name: "Em7", frets: [0,2,0,2], fingers: [0,1,0,2] }
      ],
      strummingPattern: "D - U - D - U -",
      strummingDescription: "Waltz-time strum with sustained chord rings",
      lyrics: "[Cmaj7]Heart beats fast, colors and [Gsus4]promises\n[Am7]How to be brave, how can I [Fmaj7]love when I'm afraid\n\n[Cmaj7]I have died every day [Gsus4]waiting for you\n[Am7]Darling don't be afraid I have [Fmaj7]loved you\nFor a [Cmaj7]thousand [Gsus4]years\nI'll love you for a [Am7]thousand [Fmaj7]more"
    },
    advanced: {
      chords: [
        { name: "Cmaj9", frets: [0,0,0,2], fingers: [0,0,0,2] },
        { name: "G6", frets: [0,2,0,2], fingers: [0,1,0,2] },
        { name: "Am9", frets: [2,0,0,2], fingers: [1,0,0,2] },
        { name: "Fmaj9", frets: [2,4,1,0], fingers: [2,4,1,0] },
        { name: "Em9", frets: [0,2,0,2], fingers: [0,1,0,2] },
        { name: "Dm9", frets: [2,2,1,3], fingers: [1,2,0,3] }
      ],
      strummingPattern: "D - U x D - U -",
      strummingDescription: "Delicate fingerpicked waltz with lush extensions",
      lyrics: "[Cmaj9]Heart beats fast, colors and [G6]promises\n[Am9]How to be brave, how can I [Fmaj9]love when I'm afraid\n\n[Cmaj9]I have died every day [G6]waiting for you\n[Am9]Darling don't be afraid I have [Fmaj9]loved you\nFor a [Cmaj9]thousand [G6]years\nI'll love you for a [Am9]thousand [Fmaj9]more"
    }
  },
  {
    id: "creep-radiohead",
    title: "Creep",
    artist: "Radiohead",
    easy: {
      chords: [
        { name: "G", frets: [0,2,3,2], fingers: [0,1,3,2] },
        { name: "C", frets: [0,0,0,3], fingers: [0,0,0,3] },
        { name: "Am", frets: [2,0,0,0], fingers: [1,0,0,0] }
      ],
      strummingPattern: "D D U U D U",
      strummingDescription: "Slow, building strum with heavy downstrokes",
      lyrics: "When you were here be[G]fore\nCouldn't look you in the [C]eye\nYou're just like an [Am]angel\nYour skin makes me [C]cry\n\nYou float like a [G]feather\nIn a beautiful [C]world\nI wish I was [Am]special\nYou're so very [C]special\n\nBut I'm a [G]creep, I'm a [C]weirdo\nWhat the hell am I doing [Am]here\nI don't be[C]long here"
    },
    medium: {
      chords: [
        { name: "G", frets: [0,2,3,2], fingers: [0,1,3,2] },
        { name: "B7", frets: [2,3,2,0], fingers: [1,2,3,0] },
        { name: "C", frets: [0,0,0,3], fingers: [0,0,0,3] },
        { name: "Cm", frets: [0,3,3,3], fingers: [0,1,2,3] }
      ],
      strummingPattern: "D - D U - U D U",
      strummingDescription: "Dynamic strum building from quiet to loud on chorus",
      lyrics: "When you were here be[G]fore\nCouldn't look you in the [B7]eye\nYou're just like an [C]angel\nYour skin makes me [Cm]cry\n\nBut I'm a [G]creep, I'm a [B7]weirdo\nWhat the hell am I doing [C]here\nI don't be[Cm]long here"
    },
    advanced: {
      chords: [
        { name: "Gmaj7", frets: [0,2,2,2], fingers: [0,1,2,3] },
        { name: "B7", frets: [2,3,2,0], fingers: [1,2,3,0] },
        { name: "Cmaj7", frets: [0,0,0,2], fingers: [0,0,0,2] },
        { name: "Cm6", frets: [0,3,3,3], fingers: [0,1,2,3] },
        { name: "Em9", frets: [0,2,0,2], fingers: [0,1,0,2] }
      ],
      strummingPattern: "D U x U D U x U",
      strummingDescription: "Angular, aggressive strum with muted accents on the crunch chords",
      lyrics: "When you were here be[Gmaj7]fore\nCouldn't look you in the [B7]eye\nYou're just like an [Cmaj7]angel\nYour skin makes me [Cm6]cry\n\nBut I'm a [Gmaj7]creep, I'm a [B7]weirdo\nWhat the hell am I doing [Cmaj7]here\nI don't be[Cm6]long here\n[Em9]Oh oh [Gmaj7]oh"
    }
  },
  {
    id: "island-in-the-sun-weezer",
    title: "Island in the Sun",
    artist: "Weezer",
    easy: {
      chords: [
        { name: "Am", frets: [2,0,0,0], fingers: [1,0,0,0] },
        { name: "Em", frets: [0,4,3,2], fingers: [0,3,2,1] },
        { name: "G", frets: [0,2,3,2], fingers: [0,1,3,2] },
        { name: "D", frets: [2,2,2,0], fingers: [1,2,3,0] }
      ],
      strummingPattern: "D D U U D U",
      strummingDescription: "Breezy summer strum, light and easygoing",
      lyrics: "[Am]When you're on a [Em]holiday\n[G]You can't find the [D]words to say\n[Am]All the things that [Em]come to you\n[G]And I wanna [D]feel it too\n\n[Am]On an island [Em]in the sun\n[G]We'll be playing [D]and having fun\n[Am]And it makes me [Em]feel so fine\n[G]I can't con[D]trol my brain\n\n[Am]Hip hip [Em]hip\n[G]We'll be playing and [D]having fun"
    },
    medium: {
      chords: [
        { name: "Am7", frets: [0,0,0,0], fingers: [0,0,0,0] },
        { name: "Em7", frets: [0,2,0,2], fingers: [0,1,0,2] },
        { name: "Gmaj7", frets: [0,2,2,2], fingers: [0,1,2,3] },
        { name: "Dsus2", frets: [2,2,0,0], fingers: [1,2,0,0] }
      ],
      strummingPattern: "D - U - D U - U",
      strummingDescription: "Laid-back island groove with open ringing strings",
      lyrics: "[Am7]When you're on a [Em7]holiday\n[Gmaj7]You can't find the [Dsus2]words to say\n\n[Am7]On an island [Em7]in the sun\n[Gmaj7]We'll be playing [Dsus2]and having fun"
    },
    advanced: {
      chords: [
        { name: "Am9", frets: [2,0,0,2], fingers: [1,0,0,2] },
        { name: "Em9", frets: [0,2,0,2], fingers: [0,1,0,2] },
        { name: "Gmaj9", frets: [0,2,2,2], fingers: [0,1,2,3] },
        { name: "Dsus2", frets: [2,2,0,0], fingers: [1,2,0,0] },
        { name: "Cmaj7", frets: [0,0,0,2], fingers: [0,0,0,2] }
      ],
      strummingPattern: "D U - U D U - U",
      strummingDescription: "Dreamy summer strum with extended voicings and space",
      lyrics: "[Am9]When you're on a [Em9]holiday\n[Gmaj9]You can't find the [Dsus2]words to say\n\n[Am9]On an island [Em9]in the sun\n[Gmaj9]We'll be playing [Dsus2]and having fun\n[Cmaj7]And it makes me [Em9]feel so fine\n[Gmaj9]I can't con[Dsus2]trol my brain"
    }
  }
];

// Read existing file, replace empty songs, write back
const filePath = path.join(__dirname, '..', 'data', 'songs.json');
const existing = JSON.parse(fs.readFileSync(filePath, 'utf-8'));

for (const newSong of missingSongs) {
  const idx = existing.findIndex((s: any) => s.id === newSong.id);
  if (idx >= 0) {
    // Build full entry with proper structure
    for (const level of ['easy', 'medium', 'advanced'] as const) {
      existing[idx][level] = {
        id: `${newSong.id}-${level}`,
        title: newSong.title,
        artist: newSong.artist,
        level,
        ...newSong[level]
      };
    }
  }
}

fs.writeFileSync(filePath, JSON.stringify(existing, null, 2));
console.log(`Updated ${missingSongs.length} songs in ${filePath}`);
