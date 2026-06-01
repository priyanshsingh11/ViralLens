import React from 'react';
import { ChatPanel } from '@/components/ChatPanel';
import { ChatMessage } from '@/types';
import Link from 'next/link';

export default function ChatPage() {
  const dummyMessages: ChatMessage[] = [
    { role: 'user', content: 'What happens at the 2-minute mark?' },
    { role: 'assistant', content: 'At the 2-minute mark, the speaker introduces the main concept of the framework, showing a diagram with 4 key components.' },
  ];

  return (
    <div className="container mx-auto p-4 max-w-5xl h-[calc(100vh-2rem)] flex flex-col">
      <header className="mb-4 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Video Chat</h1>
          <p className="text-sm text-muted-foreground">Example Video Analysis</p>
        </div>
        <Link href="/" className="text-sm hover:underline text-primary">
          Back to Home
        </Link>
      </header>
      
      <main className="flex-1 min-h-0">
        <ChatPanel messages={dummyMessages} />
      </main>
    </div>
  );
}
