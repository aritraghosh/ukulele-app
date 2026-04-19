'use client';

import { useState } from 'react';

export default function RequestsPage() {
  const [title, setTitle] = useState('');
  const [artist, setArtist] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!title.trim() || !artist.trim()) return;
    setSubmitting(true);

    try {
      const res = await fetch('https://formsubmit.co/ajax/aritrag94@gmail.com', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({
          _subject: `StrumAlong Song Request: ${title} by ${artist}`,
          'Song Title': title,
          Artist: artist,
          _template: 'table',
        }),
      });
      if (res.ok) {
        setSubmitted(true);
        setTitle('');
        setArtist('');
      }
    } catch {
      // silent
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="max-w-3xl mx-auto px-4 py-8 space-y-8">
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-extrabold tracking-tight bg-gradient-to-r from-primary via-chart-5 to-chart-3 bg-clip-text text-transparent">
          🌺 Request a Song
        </h1>
        <p className="text-muted-foreground">
          Can't find a song? Let us know and we'll add it to the library!
        </p>
      </div>

      {submitted ? (
        <div className="bg-gradient-to-r from-chart-4/10 to-chart-2/10 rounded-2xl p-8 text-center space-y-4">
          <p className="text-5xl">🤙</p>
          <h2 className="text-xl font-bold">Mahalo!</h2>
          <p className="text-muted-foreground">
            Your request has been sent. We'll try to add it soon!
          </p>
          <button
            onClick={() => setSubmitted(false)}
            className="px-6 py-2 rounded-full bg-primary text-primary-foreground font-semibold hover:opacity-90 transition-opacity"
          >
            Request another song
          </button>
        </div>
      ) : (
        <form
          onSubmit={handleSubmit}
          className="bg-gradient-to-r from-primary/5 via-chart-5/5 to-accent/10 rounded-2xl p-8 space-y-5"
        >
          <div className="space-y-2">
            <label htmlFor="title" className="text-sm font-semibold">
              Song Title
            </label>
            <input
              id="title"
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. Hotel California"
              required
              className="w-full px-4 py-3 rounded-xl border-2 border-border bg-background focus:border-primary focus:outline-none transition-colors"
            />
          </div>
          <div className="space-y-2">
            <label htmlFor="artist" className="text-sm font-semibold">
              Artist
            </label>
            <input
              id="artist"
              type="text"
              value={artist}
              onChange={(e) => setArtist(e.target.value)}
              placeholder="e.g. Eagles"
              required
              className="w-full px-4 py-3 rounded-xl border-2 border-border bg-background focus:border-primary focus:outline-none transition-colors"
            />
          </div>
          <button
            type="submit"
            disabled={submitting || !title.trim() || !artist.trim()}
            className="w-full py-3 rounded-full bg-primary text-primary-foreground font-bold text-lg hover:opacity-90 disabled:opacity-40 disabled:cursor-not-allowed transition-opacity"
          >
            {submitting ? 'Sending...' : '🌴 Submit Request'}
          </button>
          <p className="text-xs text-muted-foreground text-center">
            Requests are sent directly to the creator for review.
          </p>
        </form>
      )}
    </main>
  );
}
