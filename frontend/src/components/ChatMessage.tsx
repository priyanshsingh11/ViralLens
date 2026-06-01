import React from 'react';
import { ChatMessage as ChatMessageType } from '@/types';

export const ChatMessage = ({ message }: { message: ChatMessageType }) => {
  const isUser = message.role === 'user';
  return (
    <div className={`flex w-full ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div className={`max-w-[80%] rounded-lg p-4 ${isUser ? 'bg-primary text-primary-foreground' : 'bg-muted text-foreground'}`}>
        <p className="text-sm whitespace-pre-wrap">{message.content}</p>
      </div>
    </div>
  );
};
