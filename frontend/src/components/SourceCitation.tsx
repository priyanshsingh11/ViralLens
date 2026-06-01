import React from 'react';
import { Citation } from '@/types';

export const SourceCitation = ({ citation }: { citation: Citation }) => {
  return (
    <div className="text-xs bg-secondary text-secondary-foreground px-2 py-1 rounded inline-flex items-center gap-1 cursor-pointer hover:bg-secondary/80" title={citation.text}>
      <span className="font-semibold">[{citation.source_id}]</span>
      <span className="opacity-70">{citation.timestamp}s</span>
    </div>
  );
};
