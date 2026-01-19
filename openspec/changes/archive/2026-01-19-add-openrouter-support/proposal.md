# Change: Add OpenRouter Provider Support

## Why
Enable the Claude Code Proxy to route requests through OpenRouter, allowing users to access Claude models via OpenRouter's aggregation service with their existing API keys.

## What Changes
- Added OpenRouter-specific environment variables (`OPENROUTER_API_KEY`, `OPENROUTER_API_BASE`, `OR_SITE_URL`, `OR_APP_NAME`)
- Implemented `PREFERRED_PROVIDER="openrouter"` option for model mapping
- Added `openrouter/` prefix support in model validation logic
- Added OpenRouter API configuration block in request handler with custom provider and extra_body headers
- Updated `.env` configuration file with OpenRouter settings

## Impact
- Affected specs: `provider-support`
- Affected code:
  - `server.py` - Added OpenRouter API key, base URL configuration, and custom provider handling
  - `.env` - Added OpenRouter configuration example
