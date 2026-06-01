# Example API Requests and Responses

## Analyze Endpoint

**POST** `/api/v1/analyze`

**Request Body:**
```json
{
  "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "instagram_url": "https://www.instagram.com/reel/C2-u_qBofA4/"
}
```

**Successful Response:**
```json
{
  "videoA": {
    "id": "e4b9e28d-12ab-47f2-98aa-1234567890ab",
    "platform": "youtube",
    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "creator_name": "Rick Astley",
    "creator_followers": 4500000,
    "views": 1500000000,
    "likes": 17000000,
    "comments": 650000,
    "engagement_rate": 1.1767,
    "upload_date": "2009-10-25T00:00:00Z",
    "duration_seconds": 212,
    "transcript": "We're no strangers to love...",
    "created_at": "2024-05-15T12:00:00Z"
  },
  "videoB": {
    "id": "a1b2c3d4-e5f6-7890-1234-56789abcdef0",
    "platform": "instagram",
    "url": "https://www.instagram.com/reel/C2-u_qBofA4/",
    "creator_name": "tech_creator",
    "creator_followers": 25000,
    "views": 100000,
    "likes": 5000,
    "comments": 200,
    "engagement_rate": 5.2000,
    "upload_date": "2024-02-15T08:30:00Z",
    "duration_seconds": 60,
    "transcript": "Here are 3 tips for FastAPI... \nHashtags: #fastapi #python",
    "created_at": "2024-05-15T12:05:00Z"
  },
  "status": "completed"
}
```

**Error Response (Invalid URL):**
```json
{
  "detail": "Invalid YouTube URL provided: https://invalid.url"
}
```
