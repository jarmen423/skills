---
name: google-developer-knowledge-api
description: Access Google's developer documentation programmatically using the Developer Knowledge REST API. Use when you need to search, retrieve, or reference official Google documentation (Firebase, Android, Cloud, Gemini, etc.) via direct HTTP calls instead of MCP.
---

# Google Developer Knowledge API

Direct REST API access to Google's public developer documentation without needing the MCP server.

## Overview

The Developer Knowledge API provides machine-readable access to Google's developer docs. It offers:
- **SearchDocumentChunks**: Find relevant page URIs and content snippets
- **GetDocument**: Fetch full content of a single document
- **BatchGetDocuments**: Fetch multiple documents at once

## Authentication

> **IMPORTANT**: Despite official documentation suggesting API keys work, the API actually requires **OAuth2 authentication** (access tokens or ADC).

### Option 1: Application Default Credentials (Recommended)

1. Install gcloud CLI if not already installed
2. Run:
   ```bash
   gcloud auth application-default login
   ```
3. Enable the API in your project:
   - Open [Developer Knowledge API page](https://console.cloud.google.com/start/api?id=developerknowledge.googleapis.com)
   - Select your project and click **Enable**

### Option 2: Service Account

1. Create a service account in Google Cloud Console
2. Download the JSON key file
3. Set the environment variable:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
   ```

### Option 3: Access Token

Get a token manually:
```bash
gcloud auth application-default print-access-token
```

## API Reference

**Base URL**: `https://developerknowledge.googleapis.com/v1alpha`

All requests require an `Authorization: Bearer <token>` header.

### Search for Document Chunks

```bash
GET /documents:searchDocumentChunks?query={query}
```

**Parameters**:
- `query` (required): Search query string
- `pageSize` (optional): Number of results per page
- `pageToken` (optional): Token for pagination

**Response** includes:
- `documentChunks[]`: Array of matching chunks
  - `parent`: Document identifier (use for GetDocument)
  - `content`: Snippet of matching content
  - `uri`: Original documentation URL

### Get Single Document

```bash
GET /{document_name}
```

**Parameters**:
- `document_name`: The `parent` value from search results (e.g., `documents/developers.google.com/...`)

**Response**: Full Markdown content of the document

### Batch Get Documents

```bash
POST /documents:batchGet
```

**Body** (JSON):
```json
{
  "names": [
    "documents/developers.google.com/path/to/doc1",
    "documents/developers.google.com/path/to/doc2"
  ]
}
```

Retrieves up to 100 documents in a single call.

## Python Client

See `scripts/developer_knowledge_client.py` for a ready-to-use Python client with automatic OAuth2 handling.

### Installation Requirements

```bash
pip install google-auth google-auth-httplib2
```

Or use the gcloud CLI fallback (no extra dependencies).

### Quick Usage

```python
from developer_knowledge_client import DeveloperKnowledgeClient

# Uses Application Default Credentials automatically
client = DeveloperKnowledgeClient()

# Search for documentation
results = client.search("Cloud Storage buckets")
for chunk in results.get("documentChunks", []):
    print(f"URL: {chunk.get('uri')}")
    print(f"Content: {chunk.get('content')[:200]}...")

# Get full document
doc = client.get_document(chunk["parent"])
print(doc.get("content"))
```

### Explicit Authentication

```python
# Using service account
client = DeveloperKnowledgeClient(service_account_file="/path/to/sa.json")

# Using explicit access token
client = DeveloperKnowledgeClient(access_token="ya29.xxxx")
```

### Convenience Method

```python
# Search and fetch full documents in one call
docs = client.search_and_get("Firebase authentication", max_results=3)
for doc in docs:
    print(doc["content"])
```

## cURL Examples

### Get Access Token
```bash
export TOKEN=$(gcloud auth application-default print-access-token)
```

### Search
```bash
curl -H "Authorization: Bearer $TOKEN" \
  "https://developerknowledge.googleapis.com/v1alpha/documents:searchDocumentChunks?query=BigQuery"
```

### Get Document
```bash
curl -H "Authorization: Bearer $TOKEN" \
  "https://developerknowledge.googleapis.com/v1alpha/documents/developers.google.com/path/to/doc"
```

## Covered Documentation

The API indexes these Google developer sites:
- developer.android.com (Android)
- firebase.google.com (Firebase)
- docs.cloud.google.com (Google Cloud)
- ai.google.dev (Gemini API / Google AI)
- developers.google.com (Ads, Maps, YouTube, etc.)
- developer.chrome.com (Chrome)
- developers.home.google.com (Google Home)
- www.tensorflow.org (TensorFlow)
- web.dev (Web)
- fuchsia.dev (Fuchsia)

## Limitations

- **Authentication**: Requires OAuth2 (API keys do NOT work despite documentation)
- **Markdown Quality**: Generated from HTML, may have formatting issues
- **Content Scope**: Only public documentation pages, no GitHub/OSS/blogs/YouTube
- **Data Freshness**: Re-indexed within 24 hours of publication

## When to Use This Instead of MCP

Use direct API calls when:
- MCP authentication is failing or not configured
- You need more control over request/response handling
- You're integrating into a pipeline that doesn't support MCP
- You want to use the API in a standalone script
- You need to handle OAuth2 tokens explicitly

## Official Documentation

- [API Overview](https://developers.google.com/knowledge/api)
- [Quickstart](https://developers.google.com/knowledge/quickstart)
- [Corpus Reference](https://developers.google.com/knowledge/reference/corpus-reference)
