---
name: exa-web-search
description: Configure and use Exa as a web search tool for Codex, Exa MCP, `exa-py`, `exa-js`, cURL/HTTP integrations, or OpenAI-compatible Exa endpoints. Use when the user wants to add real-time web search to an agent, configure Exa MCP in Codex, build a coding agent that looks up documentation or code examples, answer current questions with Exa-backed retrieval, build a research or deep-research agent, use deep or deep-reasoning search with structured outputs, wrap an OpenAI client with Exa, or debug Exa search and contents parameters.
---

# Exa Web Search

Use Exa when the task needs live web retrieval and the user specifically wants Exa or an Exa MCP integration. Match the implementation to the project's actual interface: Codex MCP, Python SDK, JavaScript SDK, cURL/HTTP, or OpenAI-compatible chat completions.

## Workflow

1. Identify the integration path before writing code.
   - Use Exa MCP when the user wants Codex or another coding assistant to gain Exa tools.
   - Use `exa-py` when building a Python agent or a coding assistant that needs documentation and code-example lookup.
   - Use `exa-js` when building a JavaScript or TypeScript application.
   - Use Exa's OpenAI-compatible endpoint when the user wants a drop-in `OpenAI` client targeting Exa models.
   - Use an Exa-wrapped OpenAI client when the user wants Exa-backed retrieval around an existing OpenAI workflow.
   - Use direct HTTP when the project avoids SDK dependencies, uses shell automation, or needs a minimal cURL/REST example.
2. Configure authentication with `EXA_API_KEY`.
   - Prefer environment variables or a `.env` file.
   - Do not hardcode secrets into committed source files.
   - If the user pastes a live API key, treat it as sensitive and keep placeholders in committed examples.
3. Choose the correct endpoint.
   - Use `/search` or `search_and_contents(...)` when you need to find pages and optionally fetch content in one step.
   - Use `/contents` or `get_contents(...)` when the URLs are already known.
   - Use `/answer` only when the user explicitly wants Exa's answer endpoint rather than raw search results.
   - Use the OpenAI-compatible `/chat/completions` flow when the user wants quick-answer or research-style Exa models.
4. Choose the retrieval depth.
   - Start with `type="auto"` for most queries unless the user already selected a deeper mode.
   - Use `fast` for latency-sensitive lookups.
   - Use `deep` for research, enrichment, or structured extraction.
   - Use `deep-reasoning` for multi-step synthesis across many sources.
5. Choose one content mode.
   - Use text when downstream reasoning needs contiguous source text.
   - Use highlights when the user needs excerpts with lower token cost.
6. Implement the narrowest useful version first, then add filters, categories, or tool-calling only if the use case needs them.

## Quick Patterns

### Codex MCP setup

- Use the `codex mcp add exa --url ...` command from `references/exa-api-guide.md`.
- Keep the API key out of saved examples and use `YOUR_API_KEY` placeholders in the skill.
- Add `tools=` only when the user needs optional tools such as `get_code_context_exa`, crawling, people search, or deep researcher endpoints.
- Restart Codex or the MCP client if tools do not appear after config changes.

### Python coding agent

- Install `exa-py`.
- Initialize `Exa(api_key=os.environ.get("EXA_API_KEY"))`.
- Start with `search_and_contents(query, type="auto", num_results=10, text={"max_characters": 20000})` for documentation or programming-resource lookup.
- Prefer `type="auto"` for code examples and docs unless the task explicitly needs deeper research.
- Use domain filters when the agent should prefer authoritative programming sources such as `github.com`, framework docs, or vendor documentation.

### JavaScript app or agent

- Install `exa-js`.
- Initialize `new Exa(process.env.EXA_API_KEY)`.
- Start with `searchAndContents(query, { type: "deep", numResults: 10, text: { maxCharacters: 20000 } })` when the user wants deep retrieval and full text.

### cURL or HTTP integration

- Use raw `/search` requests when the user is building a shell-first workflow, generic HTTP client, or framework-agnostic research agent.
- Start with `type: "auto"` and full text under `contents.text`.
- Move to `deep` only when the agent needs broader research or structured extraction.
- Keep request bodies minimal and valid for the specific endpoint.

### OpenAI-compatible Exa client

- Point `OpenAI` at `base_url="https://api.exa.ai"` with the Exa API key.
- Use model `exa` for quick answers and `exa-research` or `exa-research-pro` for research flows.
- Include `extra_body={"text": True}` only when the user needs full source text in responses.

### Wrapped OpenAI client

- Use `exa.wrap(openai)` when the project already uses OpenAI and wants Exa-backed retrieval without a full rewrite.
- Preserve the original model choice unless the user explicitly wants to switch behavior.

### Tool-calling integration

- Expose a single narrow function such as `exa_search(query)` first.
- Let the model decide when to call it.
- Return compact, source-rich results rather than dumping full documents unless the agent truly needs long context.

### Structured extraction

- Use `type: "deep"` or `type: "deep-reasoning"` with `outputSchema` when the user needs grounded JSON instead of free text.
- Keep schemas tight and aligned to downstream fields.
- Prefer highlights over full text when structured output is enough.

## Parameter Rules

- For `/search`, nest content options inside `contents`.
- For `/contents`, put `text` or `highlights` at the top level.
- Choose exactly one content type per request: `text` or `highlights`.
- In Python, prefer snake_case SDK fields such as `num_results`, `max_characters`, and `output_schema`.
- In JavaScript, prefer camelCase SDK fields such as `numResults`, `maxCharacters`, and `outputSchema`.
- In raw HTTP, use the API field names expected by the endpoint payload.
- Prefer `maxAgeHours` over deprecated livecrawl flags.
- Use `includeDomains` and `excludeDomains`; do not invent URL-level include or exclude params.
- Avoid deprecated or invalid params called out in the reference file.

## Troubleshooting

- If results are weak, first simplify the query and try `type="auto"` unless the task specifically needs `deep`.
- If results are too slow, reduce `num_results`, skip contents, or switch to `fast`.
- If content is stale, add `maxAgeHours`.
- If a category returns sparse results, retry without the category.
- If the MCP tools do not appear, verify the config and restart the MCP client.

## Reference Map

Read only what is needed:

- `references/exa-api-guide.md` for Codex MCP setup, `exa-js`, cURL/HTTP usage, OpenAI-compatible Exa usage, deep search structured outputs, categories, freshness, endpoint selection, and common parameter mistakes.

## Output Expectations

- When implementing Exa, give the user runnable code or config, not just conceptual advice.
- Keep examples minimal and aligned to the project's stack.
- Preserve placeholders for secrets even if the user pasted a live key into the conversation, unless the user explicitly asks for a local-only command using that key.
