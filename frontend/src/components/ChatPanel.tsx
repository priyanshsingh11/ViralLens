import React from 'react';
import { ChatMessage as ChatMessageComponent } from './ChatMessage';
import { ChatMessage as ChatMessageType } from '@/types';

export const ChatPanel = ({ messages }: { messages: ChatMessageType[] }) => {
  return (
    <div className="flex flex-col h-full border rounded-lg overflow-hidden bg-background">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="text-center text-muted-foreground mt-10 text-sm">
            No messages yet. Start a conversation about the video!
          </div>
        ) : (
          messages.map((msg, idx) => (
            <ChatMessageComponent key={idx} message={msg} />
          ))
        )}
      </div>
      <div className="p-4 border-t bg-card">
        <div className="flex gap-2">
          <input 
            type="text" 
            placeholder="Ask a question..." 
            className="flex-1 px-3 py-2 rounded-md border bg-background text-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          />
          <button className="px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90">
            Send
          </button>
        </div>
      </div>
    </div>
  );
};
