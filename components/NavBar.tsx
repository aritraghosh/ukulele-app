'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Music, ListPlus } from 'lucide-react';

export function NavBar() {
  const pathname = usePathname();

  return (
    <header className="bg-gradient-to-r from-primary via-primary to-chart-2 text-primary-foreground shadow-lg">
      <div className="max-w-5xl mx-auto px-4 py-4 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2 group">
          <span className="text-3xl group-hover:rotate-12 transition-transform">🪕</span>
          <span className="text-xl font-extrabold tracking-tight">Uke Practice</span>
        </Link>
        <nav className="flex items-center gap-1">
          <Link
            href="/"
            className={`px-4 py-2 rounded-full text-sm font-semibold transition-all ${
              pathname === '/'
                ? 'bg-white/20 backdrop-blur-sm'
                : 'hover:bg-white/10'
            }`}
          >
            Songs
          </Link>
          <Link
            href="/requests"
            className={`px-4 py-2 rounded-full text-sm font-semibold transition-all flex items-center gap-1.5 ${
              pathname === '/requests'
                ? 'bg-white/20 backdrop-blur-sm'
                : 'hover:bg-white/10'
            }`}
          >
            <ListPlus className="h-4 w-4" />
            Requests
          </Link>
        </nav>
      </div>
    </header>
  );
}
