'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Music, ListPlus } from 'lucide-react';

export function NavBar() {
  const pathname = usePathname();

  return (
    <header className="border-b bg-card">
      <div className="max-w-5xl mx-auto px-4 py-4 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2">
          <Music className="h-7 w-7 text-primary" />
          <span className="text-xl font-bold">Uke Practice</span>
        </Link>
        <nav className="flex items-center gap-4">
          <Link
            href="/"
            className={`text-sm font-medium transition-colors ${
              pathname === '/' ? 'text-foreground' : 'text-muted-foreground hover:text-foreground'
            }`}
          >
            Songs
          </Link>
          <Link
            href="/requests"
            className={`text-sm font-medium transition-colors flex items-center gap-1 ${
              pathname === '/requests' ? 'text-foreground' : 'text-muted-foreground hover:text-foreground'
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
