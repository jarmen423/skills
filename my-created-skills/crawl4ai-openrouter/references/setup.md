# Setup

## What to verify first

1. Find a working Python interpreter.
2. Install Crawl4AI into that interpreter.
3. Run Crawl4AI's browser setup if the package requires Playwright assets on this machine.
4. Export `OPENROUTER_API_KEY` in the current shell.

## Windows patterns

If `python` is missing from `PATH`, locate it first:

```powershell
Get-ChildItem "$env:USERPROFILE" -Filter python.exe -Recurse -ErrorAction SilentlyContinue |
  Select-Object -First 10 -ExpandProperty FullName
```

Then invoke the chosen interpreter directly:

```powershell
& "C:\path\to\python.exe" -V
```

## Install

Prefer a project-local or task-local environment when possible.

```powershell
<python> -m pip install crawl4ai
```

If Crawl4AI needs browser assets on first use, run the package's setup command documented by the installed version before retrying the crawl.

## OpenRouter environment

Set the API key:

```powershell
$env:OPENROUTER_API_KEY = "..."
```

Optional overrides:

```powershell
$env:CRAWL4AI_OPENROUTER_MODEL = "openrouter/nvidia/nemotron-3-super-120b-a12b:free"
$env:CRAWL4AI_OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
```

## Source notes

- Crawl4AI docs show `LLMConfig` accepts `provider`, `api_token`, and optional `base_url`.
- OpenRouter docs show the OpenAI-compatible base URL `https://openrouter.ai/api/v1`.

Those two facts are sufficient to route Crawl4AI LLM extraction through OpenRouter with your API key.
