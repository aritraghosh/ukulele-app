'use client';

import { Level } from '@/types';

interface LevelSelectorProps {
  value: Level;
  onChange: (level: Level) => void;
  disabled?: boolean;
}

const levels: { value: Level; label: string; emoji: string; color: string }[] = [
  { value: 'easy', label: 'Easy', emoji: '🌱', color: 'bg-green-500 text-white hover:bg-green-600' },
  { value: 'medium', label: 'Medium', emoji: '🔥', color: 'bg-amber-500 text-white hover:bg-amber-600' },
  { value: 'advanced', label: 'Advanced', emoji: '⚡', color: 'bg-purple-600 text-white hover:bg-purple-700' },
];

export function LevelSelector({ value, onChange, disabled }: LevelSelectorProps) {
  return (
    <div className="flex gap-2">
      {levels.map((level) => (
        <button
          key={level.value}
          onClick={() => onChange(level.value)}
          disabled={disabled}
          className={`px-4 py-2 rounded-full text-sm font-semibold transition-all ${
            value === level.value
              ? level.color + ' shadow-md scale-105'
              : 'bg-muted text-muted-foreground hover:bg-accent'
          } disabled:opacity-50`}
        >
          {level.emoji} {level.label}
        </button>
      ))}
    </div>
  );
}
