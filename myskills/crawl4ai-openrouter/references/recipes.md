# Recipes

## Plain crawl to markdown

Use this when the user only needs the rendered page content:

```python
import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

async def main():
    browser = BrowserConfig(headless=True)
    run = CrawlerRunConfig(cache_mode=CacheMode.BYPASS)
    async with AsyncWebCrawler(config=browser) as crawler:
        result = await crawler.arun(url="https://example.com", config=run)
        print(result.markdown)

asyncio.run(main())
```

## Structured extraction with OpenRouter

Use this when the user wants JSON back:

```python
import asyncio
import json
import os

from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig, LLMConfig
from crawl4ai import LLMExtractionStrategy

async def main():
    llm = LLMConfig(
        provider=os.getenv(
            "CRAWL4AI_OPENROUTER_MODEL",
            "openrouter/nvidia/nemotron-3-super-120b-a12b:free",
        ),
        api_token=os.environ["OPENROUTER_API_KEY"],
        base_url=os.getenv("CRAWL4AI_OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
    )

    schema = {
        "type": "object",
        "properties": {
            "plans": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "price": {"type": "string"},
                    },
                    "required": ["name"],
                },
            }
        },
        "required": ["plans"],
    }

    run = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        extraction_strategy=LLMExtractionStrategy(
            llm_config=llm,
            instruction="Extract every pricing plan with name and displayed price.",
            schema=schema,
        ),
    )

    async with AsyncWebCrawler(config=BrowserConfig(headless=True)) as crawler:
        result = await crawler.arun(url="https://example.com/pricing", config=run)
        print(json.dumps(result.extracted_content, indent=2))

asyncio.run(main())
```

## Dynamic pages

- Add `wait_for="css:.loaded-selector"` when the target content hydrates late.
- Use `css_selector` to narrow the page before extraction when the site is noisy.
- Turn `headless` off only when diagnosing timing or rendering issues.
