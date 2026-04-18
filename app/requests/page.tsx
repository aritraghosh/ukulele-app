'use client';

import { useState, useEffect, useCallback } from 'react';
import { SongRequest } from '@/types';
import { getVoterId } from '@/lib/storage';
import { RequestCard } from '@/components/RequestCard';
import { RequestForm } from '@/components/RequestForm';

export default function RequestsPage() {
  const [requests, setRequests] = useState<SongRequest[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  const fetchRequests = useCallback(async () => {
    try {
      const voterId = getVoterId();
      const res = await fetch(`/api/requests?voterId=${voterId}`);
      if (res.ok) {
        const data = await res.json();
        setRequests(data);
      }
    } catch {
      // silent fail
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchRequests();
  }, [fetchRequests]);

  async function handleSubmit(title: string, artist: string) {
    setSubmitting(true);
    try {
      const res = await fetch('/api/requests', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, artist }),
      });
      if (res.ok) {
        await fetchRequests();
      }
    } finally {
      setSubmitting(false);
    }
  }

  async function handleVote(id: string) {
    const voterId = getVoterId();
    const res = await fetch(`/api/requests/${id}/vote`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ voterId }),
    });
    if (res.ok) {
      // Optimistic update
      setRequests((prev) =>
        prev.map((r) =>
          r.id === id ? { ...r, votes: r.votes + 1, hasVoted: true } : r
        )
      );
    }
  }

  return (
    <main className="max-w-3xl mx-auto px-4 py-8 space-y-6">
      <div>
        <h1 className="text-2xl font-bold mb-1">Song Requests</h1>
        <p className="text-muted-foreground text-sm">
          Request a song and vote for ones you want to see added
        </p>
      </div>

      <RequestForm onSubmit={handleSubmit} disabled={submitting} />

      {loading ? (
        <p className="text-muted-foreground text-center py-8">Loading requests...</p>
      ) : requests.length === 0 ? (
        <p className="text-muted-foreground text-center py-8">
          No requests yet. Be the first!
        </p>
      ) : (
        <div className="space-y-3">
          {requests.map((req) => (
            <RequestCard key={req.id} request={req} onVote={handleVote} />
          ))}
        </div>
      )}
    </main>
  );
}
