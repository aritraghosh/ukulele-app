# StrumAlong Design System

## Color Rules
- **Always use theme tokens**: `primary`, `secondary`, `accent`, `muted`, `chart-1` through `chart-5`
- **Never use raw Tailwind colors** (`emerald-500`, `pink-300`, etc.) — they break dark mode
- **Opacity variants**: use token + opacity (`primary/10`, `chart-2/20`)
- **Interactive states**: `hover:bg-primary/80`, not `hover:bg-emerald-600`

### Token Semantics
| Token | Light Color | Usage |
|---|---|---|
| `primary` | Coral | Brand, links, primary actions |
| `chart-2` | Ocean turquoise | Secondary accent, strumming |
| `chart-3` | Golden yellow | Tertiary accent, lyrics |
| `chart-4` | Palm green | Success, likes |
| `chart-5` | Sunset orange | Warning, dislikes |
| `accent` | Sunshine gold | Highlights |

## Spacing
- **Page padding**: `py-8` (all pages)
- **Page max-width**: `max-w-5xl` (content), `max-w-3xl` (forms)
- **Section gaps**: `space-y-6`
- **Card internal**: `p-6` standard, `px-6 py-3` for card headers

## Border Radius
- **Buttons/pills**: `rounded-full`
- **Cards/containers**: shadcn defaults (theme `--radius`)
- **Inner content blocks**: `rounded-xl`

## Typography
- **Headings**: Quicksand via `font-[family-name:var(--font-quicksand)]`
- **Body**: Geist (default sans)
- **Lyrics**: Geist Mono (`font-mono`)
- **Page title**: `text-3xl font-extrabold`
- **Section headers**: `text-sm font-bold uppercase tracking-wider`
- **Secondary text**: `text-sm text-muted-foreground`

## Accessibility
- Button groups: `role="group"` + `aria-label`
- Toggle buttons: `aria-pressed`
- SVG diagrams: `role="img"` + `aria-label`
- Active nav links: `aria-current="page"`
- Form inputs: `<label>` with `htmlFor`
