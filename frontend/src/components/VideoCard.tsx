import React from 'react';
import { VideoMetadata } from '@/types';

export const VideoCard = ({ video }: { video: VideoMetadata }) => {
  return (
    <div className="rounded-lg border bg-card text-card-foreground shadow-sm p-4">
      <h3 className="font-semibold leading-none tracking-tight">{video.title}</h3>
      <p className="text-sm text-muted-foreground mt-2 truncate">{video.url}</p>
      <div className="mt-4 flex items-center justify-between">
        <span className="text-xs text-muted-foreground">
          {video.duration_seconds ? `${video.duration_seconds}s` : 'Unknown duration'}
        </span>
        <span className={`text-xs px-2 py-1 rounded-full ${video.processed ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'}`}>
          {video.processed ? 'Processed' : 'Pending'}
        </span>
      </div>
    </div>
  );
};
