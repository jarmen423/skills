import argparse
import asyncio
import json
import os
from pathlib import Path

from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig, LLMConfig
from crawl4ai import LLMExtractionStrategy


DEFAULT_MODEL = "openrouter/nvidia/nemotron-3-super-120b-a12b:free"
DEFAULT_BASE_URL = "https://openrouter.ai/api/v1"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Crawl4AI extraction through OpenRouter."
    )
    parser.add_argument("--url", required=True, help="Target URL to crawl")
    parser.add_argument(
        "--instruction",
        required=True,
        help="Extraction instruction passed to LLMExtractionStrategy",
    )
    parser.add_argument(
        "--schema-file",
        required=True,
        help="Path to a JSON schema file for structured extraction",
    )
    parser.add_argument(
        "--model",
        default=os.getenv("CRAWL4AI_OPENROUTER_MODEL", DEFAULT_MODEL),
        help="Crawl4AI provider string for the OpenRouter-backed model",
    )
    parser.add_argument(
        "--base-url",
        default=os.getenv("CRAWL4AI_OPENROUTER_BASE_URL", DEFAULT_BASE_URL),
        help="OpenRouter base URL",
    )
    parser.add_argument(
        "--api-key-env",
        default="OPENROUTER_API_KEY",
        help="Environment variable that stores the OpenRouter API key",
    )
    parser.add_argument(
        "--css-selector",
        default=None,
        help="Optional CSS selector to limit the page content before extraction",
    )
    parser.add_argument(
        "--wait-for",
        default=None,
        help="Optional selector or wait expression for dynamic pages",
    )
    parser.add_argument(
        "--cache-mode",
        default="bypass",
        choices=["enabled", "disabled", "read_only", "write_only", "bypass"],
        help="Crawler cache mode",
    )
    parser.add_argument(
        "--headless",
        default="true",
        choices=["true", "false"],
        help="Run the browser headless",
    )
    parser.add_argument(
        "--max-input-tokens",
        type=int,
        default=None,
        help="Optional token budget for the extraction strategy",
    )
    return parser.parse_args()


def load_schema(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def resolve_cache_mode(name: str) -> CacheMode:
    mapping = {
        "enabled": CacheMode.ENABLED,
        "disabled": CacheMode.DISABLED,
        "read_only": CacheMode.READ_ONLY,
        "write_only": CacheMode.WRITE_ONLY,
        "bypass": CacheMode.BYPASS,
    }
    return mapping[name]


async def run_extraction(args: argparse.Namespace) -> dict:
    api_key = os.getenv(args.api_key_env)
    if not api_key:
        raise RuntimeError(
            f"Missing API key. Set the {args.api_key_env} environment variable."
        )

    llm_config = LLMConfig(
        provider=args.model,
        api_token=api_key,
        base_url=args.base_url,
    )

    strategy_kwargs = {
        "llm_config": llm_config,
        "instruction": args.instruction,
        "schema": load_schema(args.schema_file),
    }
    if args.max_input_tokens is not None:
        strategy_kwargs["max_input_tokens"] = args.max_input_tokens

    run_config = CrawlerRunConfig(
        cache_mode=resolve_cache_mode(args.cache_mode),
        css_selector=args.css_selector,
        wait_for=args.wait_for,
        extraction_strategy=LLMExtractionStrategy(**strategy_kwargs),
    )
    browser_config = BrowserConfig(headless=args.headless == "true")

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url=args.url, config=run_config)
        return {
            "success": result.success,
            "url": args.url,
            "status_code": getattr(result, "status_code", None),
            "markdown": getattr(result, "markdown", None),
            "extracted_content": getattr(result, "extracted_content", None),
            "error_message": getattr(result, "error_message", None),
        }


def main() -> None:
    args = parse_args()
    payload = asyncio.run(run_extraction(args))
    print(json.dumps(payload, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
