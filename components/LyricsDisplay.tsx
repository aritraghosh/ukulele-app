'use client';

interface LyricsDisplayProps {
  lyrics: string;
}

export function LyricsDisplay({ lyrics }: LyricsDisplayProps) {
  const lines = lyrics.split('\n');

  return (
    <div className="font-mono text-sm leading-relaxed space-y-1">
      {lines.map((line, i) => (
        <div key={i} className="whitespace-pre-wrap">
          {renderLine(line)}
        </div>
      ))}
    </div>
  );
}

function renderLine(line: string) {
  const parts = line.split(/(\[[^\]]+\])/g);
  return parts.map((part, i) => {
    if (part.startsWith('[') && part.endsWith(']')) {
      return (
        <span key={i} className="text-primary font-bold">
          {part.slice(1, -1)}{' '}
        </span>
      );
    }
    return <span key={i}>{part}</span>;
  });
}
