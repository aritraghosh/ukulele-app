'use client';

interface StrummingPatternProps {
  pattern: string;
  description: string;
}

export function StrummingPattern({ pattern, description }: StrummingPatternProps) {
  const beats = pattern.trim().split(/\s+/);

  return (
    <div className="space-y-3">
      <div className="flex items-center gap-1 justify-center">
        {beats.map((beat, i) => (
          <div
            key={i}
            className="flex flex-col items-center w-10 h-16 justify-center rounded-md border border-border bg-muted/50"
          >
            {beat === 'D' && (
              <svg width="20" height="32" viewBox="0 0 20 32">
                <line x1="10" y1="4" x2="10" y2="24" stroke="currentColor" strokeWidth="2" />
                <polygon points="4,20 10,28 16,20" fill="currentColor" />
              </svg>
            )}
            {beat === 'U' && (
              <svg width="20" height="32" viewBox="0 0 20 32">
                <line x1="10" y1="8" x2="10" y2="28" stroke="currentColor" strokeWidth="2" />
                <polygon points="4,12 10,4 16,12" fill="currentColor" />
              </svg>
            )}
            {beat === 'x' && (
              <span className="text-lg font-bold text-muted-foreground">x</span>
            )}
            {beat === '-' && (
              <span className="text-lg text-muted-foreground">-</span>
            )}
            <span className="text-[10px] text-muted-foreground mt-1">{beat}</span>
          </div>
        ))}
      </div>
      <p className="text-sm text-muted-foreground text-center">{description}</p>
    </div>
  );
}
