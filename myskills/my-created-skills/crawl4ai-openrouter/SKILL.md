---
name: crawl4ai-openrouter
description: Use Crawl4AI for web crawling, markdown extraction, and LLM-powered structured extraction through OpenRouter. Use when the user mentions Crawl4AI, unclecode/crawl4ai, wants website data extracted with Crawl4AI, or needs an agent to crawl pages and turn them into structured JSON with OpenRouter-backed models.
---

# Crawl4AI OpenRouter

Use Crawl4AI when the user explicitly wants Crawl4AI or when a real browser crawl plus optional LLM extraction is the right fit.

Load only the reference file you need:

- Open [references/setup.md](references/setup.md) before first use on a machine or when the environment is failing.
- Open [references/recipes.md](references/recipes.md) when you need a concrete pattern for plain markdown crawl, CSS-based extraction, or LLM-based extraction.

## Default Operating Assumptions

- Default LLM provider: `openrouter/nvidia/nemotron-3-super-120b-a12b:free`
- Default API key env var: `OPENROUTER_API_KEY`
- Default OpenRouter base URL: `https://openrouter.ai/api/v1`
- Prefer `LLMConfig` plus `LLMExtractionStrategy` for schema-based extraction.
- Prefer passing the API token via environment variable, not inline in source.
- Prefer `headless=True` unless the task requires visual debugging.
- Prefer `CacheMode.BYPASS` when the user wants fresh content.

## Workflow

1. Confirm whether the task is:
   - plain crawl to markdown/text
   - structured extraction with a schema
   - dynamic page crawl that may need waits, JS, or browser tuning
2. Read [references/setup.md](references/setup.md) if you have not already verified Python, package install, and browser setup.
3. For repeated or non-trivial extraction, use [scripts/crawl4ai_extract.py](scripts/crawl4ai_extract.py) instead of rewriting the integration from scratch.
4. Set these env vars in the current shell when needed:
   - `OPENROUTER_API_KEY`
   - optionally `CRAWL4AI_OPENROUTER_MODEL`
   - optionally `CRAWL4AI_OPENROUTER_BASE_URL`
5. If the user provides a target JSON shape, save it as a schema file and pass it to the helper script with an extraction instruction.
6. Return the extracted JSON or the crawl markdown, and call out any crawl limitations such as auth walls, robots constraints, or weak page structure.

## Helper Script

Use the helper for the common case:

```powershell
<python> .\scripts\crawl4ai_extract.py `
  --url "https://example.com" `
  --instruction "Extract the pricing plans and limits." `
  --schema-file ".\schema.json"
```

Important flags:

- `--url`: target page
- `--instruction`: the extraction instruction for the LLM
- `--schema-file`: JSON schema file for structured output
- `--css-selector`: optional content narrowing before extraction
- `--wait-for`: optional CSS selector to wait for on dynamic pages
- `--headless false`: opt out of headless mode for debugging
- `--cache-mode enabled|bypass|read_only|write_only|disabled`
- `--max-input-tokens`: optional budget guardrail for large pages

## Notes

- Use OpenRouter by passing a provider string and a custom `base_url` through `LLMConfig`.
- The provider prefix `openrouter/` is an inference from Crawl4AI's LiteLLM-style provider naming plus OpenRouter's OpenAI-compatible endpoint. If that stops working in a future version, switch the provider string while keeping the same base URL and API key flow.
- Keep the skill focused on Crawl4AI. If the user needs generic scraping without Crawl4AI, use a more appropriate web-scraping workflow instead.
