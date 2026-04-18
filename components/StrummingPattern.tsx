'use client';

interface StrummingPatternProps {
  pattern: string;
  description: string;
}

export function StrummingPattern({ pattern, description }: StrummingPatternProps) {
  const beats = pattern.trim().split(/\s+/);

  return (
    <div className="space-y-3">
      <div className="flex items-center gap-1.5 justify-center flex-wrap">
        {beats.map((beat, i) => (
          <div
            key={i}
            className={`flex flex-col items-center w-12 h-16 justify-center rounded-xl border-2 transition-colors ${
              beat === 'D'
                ? 'border-primary/30 bg-primary/5'
                : beat === 'U'
                ? 'border-chart-2/30 bg-chart-2/5'
                : 'border-border bg-muted/30'
            }`}
          >
            {beat === 'D' && (
              <svg width="20" height="28" viewBox="0 0 20 28">
                <line x1="10" y1="2" x2="10" y2="20" className="stroke-primary" strokeWidth="2.5" strokeLinecap="round" />
                <polygon points="4,17 10,25 16,17" className="fill-primary" />
              </svg>
            )}
            {beat === 'U' && (
              <svg width="20" height="28" viewBox="0 0 20 28">
                <line x1="10" y1="8" x2="10" y2="26" className="stroke-chart-2" strokeWidth="2.5" strokeLinecap="round" />
                <polygon points="4,11 10,3 16,11" className="fill-chart-2" />
              </svg>
            )}
            {beat === 'x' && (
              <span className="text-lg font-bold text-muted-foreground">x</span>
            )}
            {beat === '-' && (
              <span className="text-lg text-muted-foreground">-</span>
            )}
          </div>
        ))}
      </div>
      <p className="text-sm text-muted-foreground text-center italic">{description}</p>
    </div>
  );
}
