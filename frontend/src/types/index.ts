export interface VideoMetadata {
  id: string;
  title: string;
  url: string;
  duration_seconds?: number;
  processed: boolean;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface Citation {
  source_id: string;
  timestamp: number;
  text: string;
}

export interface AnalysisResponse {
  job_id: string;
  status: string;
  message: string;
}
