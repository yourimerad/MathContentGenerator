# 🔌 Math Content Generator - API Documentation v3

## Table of Contents

1. [Introduction](#introduction)
2. [Authentication](#authentication)
3. [Rate Limiting](#rate-limiting)
4. [Endpoints](#endpoints)
5. [Webhooks](#webhooks)
6. [Error Handling](#error-handling)
7. [Code Examples](#code-examples)
8. [SDKs](#sdks)
9. [GraphQL API](#graphql-api)
10. [Best Practices](#best-practices)

---

## 📖 Introduction

The Math Content Generator API provides programmatic access to our AI-powered educational content generation platform. Build custom integrations, automate workflows, or create entirely new educational experiences.

### Base URL
```
https://api.mathcontentgenerator.fr/v3
```

### API Versioning
- Current stable: `v3`
- Beta features: `v4-beta`
- Legacy support: `v2` (deprecated)

---

## 🔐 Authentication

### API Keys

Generate API keys from your dashboard at `app.mathcontentgenerator.fr/settings/api`.

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://api.mathcontentgenerator.fr/v3/user
```

### OAuth 2.0

For user-facing applications:

```javascript
const authUrl = `https://auth.mathcontentgenerator.fr/oauth/authorize?
  client_id=${CLIENT_ID}&
  redirect_uri=${REDIRECT_URI}&
  response_type=code&
  scope=read:content write:content`;
```

### JWT Tokens

For server-to-server communication:

```python
import jwt
import requests

token = jwt.encode(
    {"sub": CLIENT_ID, "exp": time.time() + 3600},
    PRIVATE_KEY,
    algorithm="RS256"
)

response = requests.get(
    "https://api.mathcontentgenerator.fr/v3/content",
    headers={"Authorization": f"Bearer {token}"}
)
```

---

## ⚡ Rate Limiting

| Plan | Requests/Hour | Burst | Concurrent |
|------|--------------|-------|------------|
| Free | 100 | 10/min | 1 |
| Pro | 1,000 | 100/min | 5 |
| Enterprise | 10,000 | 1,000/min | 50 |
| Custom | Unlimited | Custom | Custom |

### Headers
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

---

## 🚀 Endpoints

### Content Generation

#### Generate Course Content
```http
POST /v3/content/course
```

```json
{
  "level": "5eme",
  "chapter": "fractions",
  "objectives": ["addition", "multiplication"],
  "options": {
    "difficulty": "medium",
    "include_examples": true,
    "format": "latex",
    "language": "fr",
    "pedagogical_approach": "constructivist"
  }
}
```

**Response:**
```json
{
  "id": "cnt_1234567890",
  "status": "completed",
  "content": {
    "introduction": "...",
    "sections": [...],
    "examples": [...],
    "summary": "..."
  },
  "metadata": {
    "tokens_used": 2500,
    "generation_time": 3.2,
    "compliance_score": 0.98
  }
}
```

#### Generate Exercises
```http
POST /v3/content/exercises
```

```json
{
  "topic": "pythagorean_theorem",
  "count": 10,
  "types": ["application", "problem_solving"],
  "difficulty_distribution": {
    "easy": 3,
    "medium": 5,
    "hard": 2
  },
  "constraints": {
    "integer_solutions": true,
    "max_value": 100
  }
}
```

#### Generate Assessment
```http
POST /v3/content/assessment
```

```json
{
  "type": "summative",
  "duration_minutes": 60,
  "topics": ["fractions", "decimals"],
  "question_types": {
    "multiple_choice": 5,
    "short_answer": 10,
    "problem": 3
  },
  "unique_variants": 30
}
```

### Resource Management

#### Search Resources
```http
GET /v3/resources/search?q=pythagore&level=4eme&type=video
```

#### Upload Resource
```http
POST /v3/resources
Content-Type: multipart/form-data

file: [binary]
metadata: {
  "title": "Théorème de Pythagore - Animation",
  "type": "video",
  "level": "4eme",
  "tags": ["geometry", "pythagoras"]
}
```

### Student Analytics

#### Get Student Progress
```http
GET /v3/analytics/students/{student_id}/progress
```

```json
{
  "student_id": "std_123",
  "overall_progress": 0.67,
  "chapter_progress": {
    "fractions": 0.90,
    "geometry": 0.45,
    "algebra": 0.70
  },
  "strengths": ["calcul_mental", "raisonnement"],
  "weaknesses": ["geometrie_spatiale"],
  "predicted_grade": 14.5,
  "recommendations": [...]
}
```

#### Learning Analytics
```http
POST /v3/analytics/learning
```

```json
{
  "student_ids": ["std_123", "std_124"],
  "date_range": {
    "start": "2024-01-01",
    "end": "2024-03-31"
  },
  "metrics": ["engagement", "performance", "progress"]
}
```

### AI Assistant

#### Chat with AI
```http
POST /v3/ai/chat
```

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Comment expliquer les fractions à un élève en difficulté?"
    }
  ],
  "context": {
    "student_level": "6eme",
    "known_difficulties": ["abstraction"],
    "previous_attempts": 2
  }
}
```

#### Analyze Student Work
```http
POST /v3/ai/analyze
Content-Type: multipart/form-data

image: [binary]
metadata: {
  "type": "student_work",
  "exercise_id": "exc_789",
  "expected_answer": "x = 5"
}
```

### Collaboration

#### Share Content
```http
POST /v3/collaboration/share
```

```json
{
  "content_id": "cnt_123",
  "recipients": ["teacher@school.fr"],
  "permissions": ["view", "fork"],
  "message": "Voici ma séquence sur les fractions"
}
```

#### Team Spaces
```http
GET /v3/teams/{team_id}/content
POST /v3/teams/{team_id}/content
PUT /v3/teams/{team_id}/members
```

---

## 🔔 Webhooks

### Configure Webhooks
```http
POST /v3/webhooks
```

```json
{
  "url": "https://your-app.com/webhook",
  "events": ["content.generated", "student.progress"],
  "secret": "your_webhook_secret"
}
```

### Event Types

| Event | Description | Payload |
|-------|-------------|---------|
| `content.generated` | New content created | Content object |
| `content.updated` | Content modified | Diff object |
| `student.progress` | Progress milestone | Progress data |
| `assessment.completed` | Assessment finished | Results |
| `collaboration.invited` | Team invitation | Invitation details |

### Webhook Security
```python
import hmac
import hashlib

def verify_webhook(payload, signature, secret):
    expected = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
```

---

## ❌ Error Handling

### Error Response Format
```json
{
  "error": {
    "code": "INVALID_PARAMETER",
    "message": "The 'level' parameter must be a valid grade level",
    "details": {
      "parameter": "level",
      "provided": "13eme",
      "valid_values": ["CP", "CE1", "CE2", "CM1", "CM2", "6eme", ...]
    },
    "request_id": "req_abc123"
  }
}
```

### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `RATE_LIMITED` | 429 | Rate limit exceeded |
| `INVALID_API_KEY` | 401 | Invalid or expired API key |
| `INSUFFICIENT_PERMISSIONS` | 403 | Missing required permissions |
| `RESOURCE_NOT_FOUND` | 404 | Resource doesn't exist |
| `VALIDATION_ERROR` | 400 | Invalid request parameters |
| `INTERNAL_ERROR` | 500 | Server error |

---

## 💻 Code Examples

### Python
```python
from mathcontentgenerator import Client

client = Client(api_key="YOUR_API_KEY")

# Generate a course
course = client.content.create_course(
    level="5eme",
    chapter="fractions",
    objectives=["addition", "simplification"]
)

# Generate exercises with solutions
exercises = client.content.create_exercises(
    topic="fractions",
    count=20,
    include_solutions=True
)

# Analyze student performance
analysis = client.analytics.analyze_student(
    student_id="std_123",
    period="last_month"
)
```

### JavaScript/TypeScript
```typescript
import { MathContentGenerator } from '@mathcontent/sdk';

const mcg = new MathContentGenerator({
  apiKey: process.env.MCG_API_KEY
});

// Generate content with types
const course = await mcg.content.generateCourse({
  level: Grade.CINQUIEME,
  chapter: 'fractions',
  options: {
    difficulty: Difficulty.MEDIUM,
    includeExamples: true
  }
});

// Stream AI responses
const stream = await mcg.ai.chatStream({
  messages: [{ role: 'user', content: 'Explain fractions' }]
});

for await (const chunk of stream) {
  console.log(chunk.content);
}
```

### Ruby
```ruby
require 'math_content_generator'

client = MathContentGenerator::Client.new(
  api_key: ENV['MCG_API_KEY']
)

# Generate assessment
assessment = client.content.create_assessment(
  type: 'formative',
  topics: ['geometry', 'algebra'],
  duration: 45
)

# Upload resource
resource = client.resources.upload(
  file: File.open('pythagoras.pdf'),
  metadata: {
    title: 'Pythagoras Theorem Guide',
    level: '4eme'
  }
)
```

---

## 📦 SDKs

Official SDKs available for:

- **Python**: `pip install mathcontentgenerator`
- **JavaScript/Node**: `npm install @mathcontent/sdk`
- **Ruby**: `gem install math_content_generator`
- **PHP**: `composer require mathcontent/sdk`
- **Java**: Maven/Gradle packages
- **Go**: `go get github.com/mathcontent/go-sdk`

### Community SDKs
- **Rust**: `cargo add mcg-rust`
- **Swift**: SPM package
- **Kotlin**: Available on Maven

---

## 🔮 GraphQL API (Beta)

### Endpoint
```
https://api.mathcontentgenerator.fr/graphql
```

### Example Query
```graphql
query GetChapterContent($level: String!, $chapter: String!) {
  generateContent(level: $level, chapter: $chapter) {
    id
    sections {
      title
      content
      exercises {
        id
        question
        solution
        difficulty
      }
    }
    metadata {
      complianceScore
      estimatedDuration
      prerequisites
    }
  }
}
```

### Subscriptions
```graphql
subscription OnProgress($studentId: ID!) {
  studentProgress(studentId: $studentId) {
    timestamp
    chapter
    score
    timeSpent
    mistakes {
      concept
      frequency
    }
  }
}
```

---

## 🏆 Best Practices

### 1. Implement Retry Logic
```python
import time
from typing import Callable, Any

def retry_with_backoff(
    func: Callable,
    max_retries: int = 3,
    backoff_factor: float = 2.0
) -> Any:
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError:
            if attempt == max_retries - 1:
                raise
            time.sleep(backoff_factor ** attempt)
```

### 2. Cache Responses
```javascript
const cache = new Map();
const CACHE_TTL = 3600000; // 1 hour

async function getCachedContent(key) {
  const cached = cache.get(key);
  if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
    return cached.data;
  }
  
  const fresh = await fetchContent(key);
  cache.set(key, { data: fresh, timestamp: Date.now() });
  return fresh;
}
```

### 3. Batch Operations
```python
# Instead of multiple calls
exercises = []
for topic in topics:
    ex = client.generate_exercise(topic)
    exercises.append(ex)

# Use batch endpoint
exercises = client.batch.generate_exercises(topics)
```

### 4. Handle Webhooks Asynchronously
```python
from celery import Celery

app = Celery('webhook_processor')

@app.task
def process_webhook(payload):
    # Process webhook in background
    # Don't block the webhook response
    pass
```

### 5. Monitor API Usage
```javascript
// Track API metrics
const metrics = {
  requests: 0,
  errors: 0,
  latency: []
};

api.interceptors.response.use(
  (response) => {
    metrics.requests++;
    metrics.latency.push(response.duration);
    return response;
  },
  (error) => {
    metrics.errors++;
    throw error;
  }
);
```

---

## 📞 API Support

### Developer Resources
- **API Status**: [status.mathcontentgenerator.fr](https://status.mathcontentgenerator.fr)
- **Developer Portal**: [developers.mathcontentgenerator.fr](https://developers.mathcontentgenerator.fr)
- **API Playground**: [playground.mathcontentgenerator.fr](https://playground.mathcontentgenerator.fr)
- **Community Forum**: [forum.mathcontentgenerator.fr](https://forum.mathcontentgenerator.fr)

### Contact
- **Technical Support**: api-support@mathcontentgenerator.fr
- **Sales**: api-sales@mathcontentgenerator.fr
- **Security**: security@mathcontentgenerator.fr

---

*Last updated: December 2024 | API Version: 3.2.0*