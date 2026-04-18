'use client';

import { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Plus } from 'lucide-react';

interface RequestFormProps {
  onSubmit: (title: string, artist: string) => void;
  disabled?: boolean;
}

export function RequestForm({ onSubmit, disabled }: RequestFormProps) {
  const [title, setTitle] = useState('');
  const [artist, setArtist] = useState('');

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!title.trim() || !artist.trim()) return;
    onSubmit(title.trim(), artist.trim());
    setTitle('');
    setArtist('');
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-3">
      <Input
        placeholder="Song title..."
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        className="flex-1"
        disabled={disabled}
      />
      <Input
        placeholder="Artist..."
        value={artist}
        onChange={(e) => setArtist(e.target.value)}
        className="flex-1"
        disabled={disabled}
      />
      <Button type="submit" disabled={disabled || !title.trim() || !artist.trim()}>
        <Plus className="mr-1 h-4 w-4" />
        Request
      </Button>
    </form>
  );
}
