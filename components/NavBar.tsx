'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { ListPlus, Info } from 'lucide-react';

export function NavBar() {
  const pathname = usePathname();

  return (
    <header className="bg-gradient-to-r from-primary via-chart-5 to-accent text-primary-foreground shadow-lg relative overflow-hidden">
      <div className="absolute bottom-0 left-0 right-0 h-3 opacity-30">
        <svg viewBox="0 0 1200 30" preserveAspectRatio="none" className="w-full h-full fill-background">
          <path d="M0,15 C200,30 400,0 600,15 C800,30 1000,0 1200,15 L1200,30 L0,30 Z" />
        </svg>
      </div>
      <div className="max-w-5xl mx-auto px-4 py-4 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2 group">
          <svg className="w-7 h-7 group-hover:rotate-12 transition-transform" viewBox="0 0 32 32" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
            <ellipse cx="12" cy="22" rx="8" ry="9" />
            <rect x="18" y="6" width="4" height="18" rx="2" />
            <circle cx="12" cy="20" r="2" fill="currentColor" className="text-primary" />
            <circle cx="12" cy="25" r="2" fill="currentColor" className="text-primary" />
            <rect x="21" y="2" width="2" height="6" rx="1" />
            <rect x="23" y="3" width="4" height="2" rx="1" />
            <rect x="21" y="8" width="2" height="6" rx="1" />
            <rect x="23" y="9" width="4" height="2" rx="1" />
          </svg>
          <span className="text-xl font-extrabold tracking-tight">StrumAlong</span>
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
          <Link
            href="/about"
            className={`px-4 py-2 rounded-full text-sm font-semibold transition-all flex items-center gap-1.5 ${
              pathname === '/about'
                ? 'bg-white/20 backdrop-blur-sm'
                : 'hover:bg-white/10'
            }`}
          >
            <Info className="h-4 w-4" />
            About
          </Link>
        </nav>
      </div>
    </header>
  );
}
