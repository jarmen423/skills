# Exa API Guide

## Setup

Use an environment variable or `.env` file:

```bash
export EXA_API_KEY="YOUR_API_KEY"
```

```env
EXA_API_KEY=YOUR_API_KEY
```

JavaScript initialization:

```javascript
import Exa from "exa-js";

const exa = new Exa(process.env.EXA_API_KEY);
```

Python initialization:

```python
import os
from exa_py import Exa

exa = Exa(api_key=os.environ.get("EXA_API_KEY"))
```

## Exa MCP

Codex install command:

```bash
codex mcp add exa --url https://mcp.exa.ai/mcp?exaApiKey=YOUR_API_KEY
```

Remote MCP URL:

```text
https://mcp.exa.ai/mcp?exaApiKey=YOUR_API_KEY
```

Enable specific tools:

```text
https://mcp.exa.ai/mcp?exaApiKey=YOUR_API_KEY&tools=web_search_exa,get_code_context_exa,people_search_exa
```

Enable all tools:

```text
https://mcp.exa.ai/mcp?exaApiKey=YOUR_API_KEY&tools=web_search_exa,web_search_advanced_exa,get_code_context_exa,crawling_exa,company_research_exa,people_search_exa,deep_researcher_start,deep_researcher_check
```

Enabled by default:

- `web_search_exa`
- `get_code_context_exa`
- `company_research_exa`

Optional via `tools=`:

- `web_search_advanced_exa`
- `crawling_exa`
- `people_search_exa`
- `deep_researcher_start`
- `deep_researcher_check`

JSON config for MCP clients:

```json
{
  "mcpServers": {
    "exa": {
      "url": "https://mcp.exa.ai/mcp?exaApiKey=YOUR_API_KEY"
    }
  }
}
```

Claude Desktop with `mcp-remote`:

```json
{
  "mcpServers": {
    "exa": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.exa.ai/mcp?exaApiKey=YOUR_API_KEY"]
    }
  }
}
```

Restart the MCP client after config changes if tools do not appear.

For coding agents, `get_code_context_exa` is especially useful when the task is to find implementation patterns, library examples, or code-related context rather than general web articles.

## Python Quick Start

Install:

```bash
pip install exa-py
```

Search and fetch text:

```python
from exa_py import Exa

exa = Exa(api_key="YOUR_API_KEY")

results = exa.search_and_contents(
    "React hooks best practices 2024",
    type="auto",
    num_results=10,
    text={"max_characters": 20000}
)

for result in results.results:
    print(result.title, result.url)
```

For coding agents, start with `type="auto"` and add domain filters only when you need to bias toward specific doc or code hosts.

## OpenAI SDK Integration

Use Exa as an OpenAI-compatible endpoint:

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.exa.ai",
    api_key="YOUR_EXA_API_KEY",
)

completion = client.chat.completions.create(
    model="exa",
    messages=[
        {"role": "user", "content": "What are the latest developments in quantum computing?"}
    ],
    extra_body={"text": True},
)

print(completion.choices[0].message.content)
print(completion.choices[0].message.citations)
```

Research mode:

```python
completion = client.chat.completions.create(
    model="exa-research",
    messages=[
        {"role": "user", "content": "What makes some LLMs so much better than others?"}
    ],
    stream=True,
)

for chunk in completion:
    if chunk.choices and chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

Wrap an existing OpenAI client with Exa:

```python
from openai import OpenAI
from exa_py import Exa

openai = OpenAI(api_key="OPENAI_API_KEY")
exa = Exa("EXA_API_KEY")

exa_openai = exa.wrap(openai)

completion = exa_openai.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What is the latest climate tech news?"}]
)
```

## cURL Quick Start

Start with `/search` for general retrieval:

```bash
curl -X POST 'https://api.exa.ai/search' \
  -H 'x-api-key: YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "latest developments in AI safety research",
    "type": "auto",
    "num_results": 10,
    "contents": {
      "text": {
        "max_characters": 20000
      }
    }
  }'
```

For deep research agents, move to `type: "deep"` only when broader search or structured extraction is needed.

## JavaScript Quick Start

Install:

```bash
npm install exa-js
```

Search and fetch text:

```javascript
import Exa from "exa-js";

const exa = new Exa("YOUR_API_KEY");

const results = await exa.searchAndContents("latest developments in AI safety research", {
  type: "deep",
  numResults: 10,
  text: {
    maxCharacters: 20000
  }
});

results.results.forEach(result => {
  console.log(result.title, result.url);
});
```

Equivalent raw HTTP example:

```bash
curl -X POST 'https://api.exa.ai/search' \
  -H 'x-api-key: YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "latest developments in AI safety research",
    "type": "deep",
    "num_results": 10,
    "contents": {
      "text": {
        "max_characters": 20000
      }
    }
  }'
```

## Function Calling

OpenAI pattern:

```python
import json
from openai import OpenAI
from exa_py import Exa

openai = OpenAI()
exa = Exa()

tools = [{
    "type": "function",
    "function": {
        "name": "exa_search",
        "description": "Search the web for current information.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"}
            },
            "required": ["query"]
        }
    }
}]

def exa_search(query: str) -> str:
    results = exa.search_and_contents(
        query,
        type="auto",
        num_results=10,
        text={"max_characters": 20000},
    )
    return "\n".join(f"{r.title}: {r.url}" for r in results.results)
```

Anthropic pattern:

```python
import anthropic
from exa_py import Exa

client = anthropic.Anthropic()
exa = Exa()

tools = [{
    "name": "exa_search",
    "description": "Search the web for current information.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Search query"}
        },
        "required": ["query"]
    }
}]

def exa_search(query: str) -> str:
    results = exa.search_and_contents(
        query,
        type="auto",
        num_results=10,
        text={"max_characters": 20000},
    )
    return "\n".join(f"{r.title}: {r.url}" for r in results.results)
```

## Structured Outputs

Use `deep` or `deep-reasoning` with `outputSchema` when the result should be grounded JSON with citations.

```javascript
import Exa from "exa-js";

const exa = new Exa("YOUR_API_KEY");

const results = await exa.search("articles about GPUs", {
  type: "deep",
  outputSchema: {
    type: "object",
    description: "Companies mentioned in articles",
    required: ["companies"],
    properties: {
      companies: {
        type: "array",
        description: "List of companies mentioned",
        items: {
          type: "object",
          required: ["name"],
          properties: {
            name: { type: "string", description: "Name of the company" },
            description: { type: "string", description: "Short description of what the company does" }
          }
        }
      }
    }
  },
  contents: {
    highlights: { maxCharacters: 4000 }
  }
});

console.log(results.output.content);
console.log(results.output.grounding);
```

## Search Modes

- `fast`: quickest lookups
- `auto`: balanced default
- `deep`: broader research and structured extraction
- `deep-reasoning`: deepest multi-step research

Use `auto` unless the task clearly needs lower latency or heavier research. Use `deep` as the default only when the user explicitly prefers deeper search.

## Content Modes

Choose one:

- Text: `{"text": {"max_characters": 20000}}`
- Highlights: `{"highlights": {"max_characters": 4000}}`

Use text for contiguous source material or code/documentation extraction. Use highlights for cheaper snippets and summaries.

## Domain Filtering

Usually optional. Example:

```json
{
  "includeDomains": ["arxiv.org", "github.com"],
  "excludeDomains": ["pinterest.com"]
}
```

For coding agents, common `includeDomains` candidates are `github.com`, official framework docs, and vendor documentation sites.

## Categories

Supported examples:

- `people`
- `company`
- `news`
- `research paper`

If a category is too restrictive, retry without it.

Category tips:

- Use singular category names.
- People search does not support date or text filters.
- Company search returns company entities rather than articles.

## Freshness

Use `maxAgeHours` to control recrawl behavior:

- `24`: refresh daily
- `1`: near real time
- `0`: always livecrawl
- `-1`: cache only
- omitted: default balance

## Endpoint Selection

Use `/search` when you need discovery and optional content retrieval in one request.

For `/search`, nest content under `contents`:

```json
{
  "query": "latest developments in AI safety research",
  "num_results": 10,
  "contents": {
    "text": {
      "max_characters": 20000
    }
  }
}
```

Use `/contents` when URLs are already known:

```python
from exa_py import Exa

exa = Exa(api_key="YOUR_API_KEY")

results = exa.get_contents(
    ["https://example.com/article", "https://example.com/blog-post"],
    text={"max_characters": 20000},
)
```

For `/contents`, content options are top-level, not nested under `contents`.

cURL example:

```bash
curl -X POST 'https://api.exa.ai/contents' \
  -H 'x-api-key: YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "urls": ["https://example.com/article", "https://example.com/blog-post"],
    "text": { "max_characters": 20000 }
  }'
```

JavaScript example:

```javascript
import Exa from "exa-js";

const exa = new Exa("YOUR_API_KEY");

const results = await exa.getContents(
  ["https://example.com/article", "https://example.com/blog-post"],
  { text: { maxCharacters: 20000 } }
);
```

## Common Mistakes

Avoid these:

- `useAutoprompt`
- `includeUrls` or `excludeUrls`
- `stream: true` on `/search` or `/contents`
- top-level `text`, `summary`, or `highlights` on `/search`
- deprecated highlights params such as `numSentences` or `highlightsPerUrl`
- `tokensNum`
- deprecated `livecrawl`

Use these instead:

- `includeDomains` and `excludeDomains`
- `contents.text` or `contents.highlights` on `/search`
- top-level `text` or `highlights` on `/contents`
- `maxCharacters`
- `maxAgeHours`

JavaScript SDK reminders:

- Prefer `numResults` rather than `num_results`.
- Prefer `maxCharacters` rather than `max_characters`.
- Prefer `outputSchema` rather than `output_schema`.

## Troubleshooting

If results are weak:

1. Simplify the query.
2. Keep `type="auto"` first.
3. Try `deep` only after that.

If results are slow:

1. Use `fast`.
2. Lower `num_results`.
3. Skip content extraction when URLs are enough.

If there are no results:

1. Remove filters.
2. Remove restrictive categories.
3. Retry with `auto`.

## Links

- Docs: [https://exa.ai/docs](https://exa.ai/docs)
- API docs: [https://docs.exa.ai](https://docs.exa.ai)
- OpenAI SDK docs: [https://docs.exa.ai/reference/openai-sdk](https://docs.exa.ai/reference/openai-sdk)
- MCP docs: [https://docs.exa.ai/reference/exa-mcp](https://docs.exa.ai/reference/exa-mcp)
- Tool-calling docs: [https://docs.exa.ai/reference/openai-tool-calling](https://docs.exa.ai/reference/openai-tool-calling)
- Dashboard: [https://dashboard.exa.ai](https://dashboard.exa.ai)
- Status: [https://status.exa.ai](https://status.exa.ai)
