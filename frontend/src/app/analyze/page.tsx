import React from 'react';
import { LoadingSpinner } from '@/components/LoadingSpinner';

export default function AnalyzePage() {
  return (
    <div className="container mx-auto p-8 max-w-2xl">
      <h1 className="text-3xl font-bold mb-6">Analyze Video</h1>
      <div className="bg-card border rounded-xl p-6 shadow-sm">
        <form className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Video URL</label>
            <input 
              type="url" 
              placeholder="https://example.com/video.mp4" 
              className="w-full px-3 py-2 border rounded-md bg-background focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
          <button type="button" className="w-full bg-primary text-primary-foreground py-2 rounded-md font-semibold hover:bg-primary/90 transition-colors">
            Start Analysis
          </button>
        </form>
      </div>
      
      {/* Placeholder for processing state */}
      <div className="mt-8 hidden">
        <div className="flex flex-col items-center p-8 border rounded-xl bg-muted/50">
          <LoadingSpinner />
          <p className="mt-4 text-muted-foreground">Processing video frames and transcribing audio...</p>
        </div>
      </div>
    </div>
  );
}
