'use client';

import { ChordFingering } from '@/types';

interface ChordDiagramProps {
  chord: ChordFingering;
  size?: number;
}

export function ChordDiagram({ chord, size = 100 }: ChordDiagramProps) {
  const w = size;
  const h = size * 1.4;
  const padding = 16;
  const fretCount = 4;
  const stringCount = 4;
  const fretboardW = w - padding * 2;
  const fretboardH = h - padding * 2 - 20;
  const stringSpacing = fretboardW / (stringCount - 1);
  const fretSpacing = fretboardH / fretCount;
  const dotRadius = size * 0.06;

  const minFret = Math.min(...chord.frets.filter((f) => f > 0));
  const maxFret = Math.max(...chord.frets);
  const startFret = maxFret <= 4 ? 1 : minFret;
  const showNut = startFret === 1;

  return (
    <div className="flex flex-col items-center gap-1">
      <span className="text-sm font-bold">{chord.name}</span>
      <svg width={w} height={h} viewBox={`0 0 ${w} ${h}`}>
        {/* Nut or fret number */}
        {showNut ? (
          <rect
            x={padding}
            y={padding + 18}
            width={fretboardW}
            height={3}
            fill="currentColor"
          />
        ) : (
          <text
            x={padding - 8}
            y={padding + 18 + fretSpacing / 2 + 4}
            fontSize={10}
            fill="currentColor"
            textAnchor="middle"
          >
            {startFret}
          </text>
        )}

        {/* Fret lines */}
        {Array.from({ length: fretCount + 1 }).map((_, i) => (
          <line
            key={`fret-${i}`}
            x1={padding}
            y1={padding + 20 + i * fretSpacing}
            x2={padding + fretboardW}
            y2={padding + 20 + i * fretSpacing}
            stroke="currentColor"
            strokeWidth={1}
            strokeOpacity={0.3}
          />
        ))}

        {/* Strings */}
        {Array.from({ length: stringCount }).map((_, i) => (
          <line
            key={`string-${i}`}
            x1={padding + i * stringSpacing}
            y1={padding + 20}
            x2={padding + i * stringSpacing}
            y2={padding + 20 + fretboardH}
            stroke="currentColor"
            strokeWidth={1}
            strokeOpacity={0.5}
          />
        ))}

        {/* Finger dots and open/muted markers */}
        {chord.frets.map((fret, i) => {
          const x = padding + i * stringSpacing;
          if (fret === 0) {
            return (
              <circle
                key={`dot-${i}`}
                cx={x}
                cy={padding + 10}
                r={dotRadius}
                fill="none"
                stroke="currentColor"
                strokeWidth={1.5}
              />
            );
          }
          if (fret === -1) {
            return (
              <text
                key={`dot-${i}`}
                x={x}
                y={padding + 14}
                fontSize={10}
                fill="currentColor"
                textAnchor="middle"
              >
                x
              </text>
            );
          }
          const displayFret = fret - startFret + 1;
          return (
            <circle
              key={`dot-${i}`}
              cx={x}
              cy={padding + 20 + (displayFret - 0.5) * fretSpacing}
              r={dotRadius}
              fill="currentColor"
            />
          );
        })}
      </svg>
    </div>
  );
}
