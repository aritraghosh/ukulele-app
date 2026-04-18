'use client';

import { Level } from '@/types';

interface LevelSelectorProps {
  value: Level;
  onChange: (level: Level) => void;
  disabled?: boolean;
}

const levels: { value: Level; label: string; desc: string }[] = [
  { value: 'easy', label: 'Easy', desc: 'Simple open chords' },
  { value: 'medium', label: 'Medium', desc: 'Standard chords' },
  { value: 'advanced', label: 'Advanced', desc: 'Complex voicings' },
];

export function LevelSelector({ value, onChange, disabled }: LevelSelectorProps) {
  return (
    <div className="flex gap-2">
      {levels.map((level) => (
        <button
          key={level.value}
          onClick={() => onChange(level.value)}
          disabled={disabled}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
            value === level.value
              ? 'bg-primary text-primary-foreground'
              : 'bg-muted text-muted-foreground hover:bg-accent'
          } disabled:opacity-50`}
          title={level.desc}
        >
          {level.label}
        </button>
      ))}
    </div>
  );
}
