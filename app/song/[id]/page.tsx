'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { Level, Song } from '@/types';
import { getSongById, getSongAtLevel } from '@/lib/songs';
import { toggleFavorite, isFavorite, getReaction, setReaction } from '@/lib/storage';
import { ChordDiagram } from '@/components/ChordDiagram';
import { StrummingPattern } from '@/components/StrummingPattern';
import { LyricsDisplay } from '@/components/LyricsDisplay';
import { LevelSelector } from '@/components/LevelSelector';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Heart, Download, ArrowLeft, ThumbsUp, ThumbsDown, Send } from 'lucide-react';
import Link from 'next/link';

export default function SongPage() {
  const params = useParams();
  const id = params.id as string;
  const [level, setLevel] = useState<Level>('easy');
  const [fav, setFav] = useState(false);
  const [reaction, setReactionState] = useState<'like' | 'dislike' | null>(null);
  const [comment, setComment] = useState('');
  const [commentSent, setCommentSent] = useState(false);
  const [sendingComment, setSendingComment] = useState(false);

  const entry = getSongById(id);

  useEffect(() => {
    if (entry) {
      setFav(isFavorite(entry.id));
      setReactionState(getReaction(entry.id));
    }
  }, [entry]);

  if (!entry) {
    return (
      <main className="max-w-5xl mx-auto px-4 py-16 text-center space-y-4">
        <p className="text-5xl">🌺</p>
        <p className="text-muted-foreground text-lg">Song not found.</p>
        <Link href="/" className="text-primary font-semibold underline underline-offset-2">
          Back to library
        </Link>
      </main>
    );
  }

  const song: Song = getSongAtLevel(entry, level);

  function handleFavorite() {
    const result = toggleFavorite(entry!.id);
    setFav(result);
  }

  function handleReaction(type: 'like' | 'dislike') {
    const current = getReaction(entry!.id);
    const newReaction = current === type ? null : type;
    setReaction(entry!.id, newReaction);
    setReactionState(newReaction);
    // Send reaction to creator via email
    if (newReaction) {
      fetch('https://formsubmit.co/ajax/aritrag94@gmail.com', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({
          _subject: `StrumAlong ${newReaction === 'like' ? '👍 Like' : '👎 Dislike'}: ${entry!.title} by ${entry!.artist}`,
          Song: `${entry!.title} - ${entry!.artist}`,
          Reaction: newReaction,
          _template: 'table',
        }),
      }).catch(() => {});
    }
  }

  async function handleComment(e: React.FormEvent) {
    e.preventDefault();
    if (!comment.trim()) return;
    setSendingComment(true);
    try {
      const res = await fetch('https://formsubmit.co/ajax/aritrag94@gmail.com', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({
          _subject: `StrumAlong Comment: ${song.title} by ${song.artist}`,
          Song: `${song.title} - ${song.artist}`,
          Level: level,
          Comment: comment,
          _template: 'table',
        }),
      });
      if (res.ok) {
        setCommentSent(true);
        setComment('');
        setTimeout(() => setCommentSent(false), 4000);
      }
    } catch {
      // silent
    } finally {
      setSendingComment(false);
    }
  }

  function handleDownload() {
    const content = [
      `${song.title} - ${song.artist}`,
      `Level: ${song.level}`,
      '',
      `Chords: ${song.chords.map((c) => c.name).join(', ')}`,
      '',
      `Strumming: ${song.strummingPattern}`,
      song.strummingDescription,
      '',
      '--- Lyrics & Chords ---',
      song.lyrics,
    ].join('\n');

    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${song.title} - ${song.artist} (${song.level}).txt`;
    a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <main className="max-w-5xl mx-auto px-4 py-8 space-y-6">
      <Link href="/" className="inline-flex items-center gap-1.5 text-sm text-muted-foreground hover:text-primary transition-colors font-medium">
        <ArrowLeft className="h-4 w-4" />
        Back to library
      </Link>

      {/* Song header */}
      <div className="bg-gradient-to-r from-primary/10 via-chart-5/15 to-accent/30 rounded-2xl p-6 sm:p-8 space-y-5">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight">{song.title}</h1>
          <p className="text-lg text-muted-foreground">{song.artist}</p>
        </div>

        <LevelSelector value={level} onChange={setLevel} />

        {/* All actions in one row */}
        <div className="flex items-center gap-2 flex-wrap">
          <Button
            variant="outline"
            size="sm"
            onClick={handleFavorite}
            className="rounded-full"
          >
            <Heart className={`mr-1.5 h-4 w-4 ${fav ? 'fill-pink-500 text-pink-500' : ''}`} />
            {fav ? 'Saved' : 'Save'}
          </Button>
          <Button variant="outline" size="sm" onClick={handleDownload} className="rounded-full">
            <Download className="mr-1.5 h-4 w-4" />
            Download
          </Button>
          <div className="w-px h-6 bg-border mx-1" />
          <button
            onClick={() => handleReaction('like')}
            className={`flex items-center gap-1.5 px-4 py-2 rounded-full text-sm font-semibold transition-all ${
              reaction === 'like'
                ? 'bg-emerald-500 text-white shadow-md scale-105'
                : 'bg-white/60 border border-border hover:bg-white/90 text-muted-foreground'
            }`}
          >
            <ThumbsUp className="h-4 w-4" />
            Like
          </button>
          <button
            onClick={() => handleReaction('dislike')}
            className={`flex items-center gap-1.5 px-4 py-2 rounded-full text-sm font-semibold transition-all ${
              reaction === 'dislike'
                ? 'bg-orange-500 text-white shadow-md scale-105'
                : 'bg-white/60 border border-border hover:bg-white/90 text-muted-foreground'
            }`}
          >
            <ThumbsDown className="h-4 w-4" />
            Dislike
          </button>
        </div>
      </div>

      {/* Chords */}
      <Card className="border-2 overflow-hidden">
        <div className="bg-gradient-to-r from-primary/5 to-transparent px-6 py-3 border-b">
          <h3 className="text-sm font-bold uppercase tracking-wider text-primary">
            🎸 Chords
          </h3>
        </div>
        <CardContent className="pt-6">
          <div className="flex flex-wrap gap-6 justify-center sm:justify-start">
            {song.chords.map((chord) => (
              <ChordDiagram key={chord.name} chord={chord} size={110} />
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Strumming */}
      <Card className="border-2 overflow-hidden">
        <div className="bg-gradient-to-r from-chart-2/10 to-transparent px-6 py-3 border-b">
          <h3 className="text-sm font-bold uppercase tracking-wider text-chart-2">
            🥁 Strumming Pattern
          </h3>
        </div>
        <CardContent className="pt-6">
          <StrummingPattern
            pattern={song.strummingPattern}
            description={song.strummingDescription}
          />
        </CardContent>
      </Card>

      {/* Lyrics */}
      <Card className="border-2 overflow-hidden">
        <div className="bg-gradient-to-r from-chart-3/10 to-transparent px-6 py-3 border-b">
          <h3 className="text-sm font-bold uppercase tracking-wider text-chart-3">
            🎤 Lyrics & Chords
          </h3>
        </div>
        <CardContent className="pt-6">
          <div className="bg-muted/20 rounded-xl p-6 border border-border/50">
            <LyricsDisplay lyrics={song.lyrics} />
          </div>
        </CardContent>
      </Card>

      {/* Comments */}
      <Card className="border-2 overflow-hidden">
        <div className="bg-gradient-to-r from-chart-4/10 to-transparent px-6 py-3 border-b">
          <h3 className="text-sm font-bold uppercase tracking-wider text-chart-4">
            💬 Leave a Comment
          </h3>
        </div>
        <CardContent className="pt-6">
          {commentSent ? (
            <div className="text-center py-4 space-y-2">
              <p className="text-2xl">🤙</p>
              <p className="text-sm font-semibold text-chart-4">Mahalo! Your comment has been sent.</p>
            </div>
          ) : (
            <form onSubmit={handleComment} className="flex gap-3">
              <input
                type="text"
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                placeholder="Share your thoughts on this song..."
                required
                className="flex-1 px-4 py-3 rounded-xl border-2 border-border bg-background focus:border-chart-4 focus:outline-none transition-colors text-sm"
              />
              <button
                type="submit"
                disabled={sendingComment || !comment.trim()}
                className="px-5 py-3 rounded-xl bg-chart-4 text-white font-semibold hover:opacity-90 disabled:opacity-40 disabled:cursor-not-allowed transition-opacity flex items-center gap-2"
              >
                <Send className="h-4 w-4" />
                Send
              </button>
            </form>
          )}
        </CardContent>
      </Card>
    </main>
  );
}
