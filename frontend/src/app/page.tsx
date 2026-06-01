import Link from 'next/link';
import { VideoCard } from '@/components/VideoCard';
import { VideoMetadata } from '@/types';

export default function Home() {
  const dummyVideo: VideoMetadata = {
    id: "1",
    title: "Example Video Analysis",
    url: "https://example.com/video.mp4",
    duration_seconds: 120,
    processed: true,
  };

  return (
    <div className="container mx-auto p-8 max-w-4xl">
      <header className="mb-12 text-center">
        <h1 className="text-4xl font-extrabold tracking-tight mb-4 text-primary">ViralLens</h1>
        <p className="text-xl text-muted-foreground">AI-Powered Video Comparison & Analysis</p>
      </header>

      <main className="space-y-8">
        <section className="bg-card border rounded-xl p-8 shadow-sm">
          <h2 className="text-2xl font-bold mb-4">Start New Analysis</h2>
          <p className="text-muted-foreground mb-6">Upload or link a video to begin the AI comparison process.</p>
          <Link href="/analyze" className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2">
            Go to Analysis Dashboard
          </Link>
        </section>

        <section>
          <h2 className="text-2xl font-bold mb-4">Recent Analyses</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Link href="/chat" className="block transition-transform hover:scale-[1.02]">
              <VideoCard video={dummyVideo} />
            </Link>
          </div>
        </section>
      </main>
    </div>
  );
}
