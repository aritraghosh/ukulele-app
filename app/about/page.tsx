export default function AboutPage() {
  return (
    <main className="max-w-3xl mx-auto px-4 py-12 space-y-8">
      <div className="text-center space-y-4">
        <h1 className="text-4xl font-extrabold tracking-tight bg-gradient-to-r from-primary via-chart-5 to-chart-3 bg-clip-text text-transparent">
          About StrumAlong
        </h1>
        <p className="text-5xl">🌺🎶🌴</p>
      </div>

      <div className="bg-gradient-to-r from-primary/10 via-chart-5/10 to-accent/20 rounded-2xl p-8 space-y-4">
        <p className="text-lg leading-relaxed">
          StrumAlong is a free ukulele practice app with <strong>1,100+ songs</strong> across
          every genre — pop, rock, folk, country, jazz, reggae, Disney, musical theatre, and more.
        </p>
        <p className="text-lg leading-relaxed">
          Each song comes with <strong>3 difficulty levels</strong> (easy, medium, advanced),
          complete with chord diagrams, strumming patterns, and lyrics with inline chord markers.
          Pick up your uke and start strumming!
        </p>
      </div>

      <div className="bg-card border-2 border-border rounded-2xl p-8 space-y-4 text-center">
        <h2 className="text-2xl font-bold">Created by</h2>
        <p className="text-xl font-semibold text-primary">Aritra Ghosh</p>
        <p className="text-muted-foreground">
          <a
            href="mailto:aritrag94@gmail.com"
            className="text-chart-2 font-medium hover:underline underline-offset-2"
          >
            aritrag94@gmail.com
          </a>
        </p>
      </div>

      <div className="text-center text-sm text-muted-foreground">
        <p>Built with Next.js, Tailwind CSS, and a whole lot of aloha spirit 🤙</p>
      </div>
    </main>
  );
}
