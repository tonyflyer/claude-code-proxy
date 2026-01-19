# provider-support Specification

## Purpose
TBD - created by archiving change add-openrouter-support. Update Purpose after archive.
## Requirements
### Requirement: OpenRouter Provider Support
The proxy SHALL support routing requests through OpenRouter API when `PREFERRED_PROVIDER` is set to `"openrouter"`.

The system SHALL:
- Accept `OPENROUTER_API_KEY` environment variable for authentication
- Accept `OPENROUTER_API_BASE` environment variable (defaults to `https://openrouter.ai/api/v1`)
- Accept `OR_SITE_URL` and `OR_APP_NAME` for OpenRouter request metadata
- Map `haiku` model requests to `openrouter/{SMALL_MODEL}`
- Map `sonnet` model requests to `openrouter/{BIG_MODEL}`
- Set `custom_llm_provider` to `"openrouter"` for LiteLLM
- Include `HTTP-Referer` and `X-Title` headers when configured

#### Scenario: OpenRouter provider configured
- **WHEN** `PREFERRED_PROVIDER` is set to `"openrouter"` and `OPENROUTER_API_KEY` is provided
- **THEN** model names are prefixed with `openrouter/`
- **AND** requests are routed to `OPENROUTER_API_BASE`
- **AND** `extra_body` headers are included when `OR_SITE_URL` or `OR_APP_NAME` are set

#### Scenario: Model mapping with OpenRouter
- **WHEN** a request is made with model `"haiku"`
- **THEN** the model is mapped to `openrouter/{SMALL_MODEL}` where `{SMALL_MODEL}` defaults to `anthropic/claude-haiku-4.5`
- **AND** the request is sent to OpenRouter with appropriate headers

