## ADDED Requirements

### Requirement: Ollama Local Model Configuration

The system SHALL provide configuration examples for connecting to local Ollama models via the OpenAI-compatible API.

#### Scenario: Configure Ollama with default settings

- **WHEN** user copies Ollama example configuration to `.env`
- **THEN** the proxy SHALL forward requests to the local Ollama server at `http://localhost:11434/v1`

#### Scenario: Configure Ollama with custom model

- **WHEN** user sets `BIG_MODEL` to an Ollama model name (e.g., `llama3.2`)
- **THEN** the proxy SHALL map `sonnet` requests to that Ollama model

### Requirement: LMStudio Local Model Configuration

The system SHALL provide configuration examples for connecting to local LMStudio models via the OpenAI-compatible API.

#### Scenario: Configure LMStudio with default settings

- **WHEN** user copies LMStudio example configuration to `.env`
- **THEN** the proxy SHALL forward requests to the local LMStudio server at `http://localhost:11435/v1`

#### Scenario: Configure LMStudio with custom model

- **WHEN** user sets `SMALL_MODEL` to an LMStudio model name (e.g., `qwen2.5-7b-instruct`)
- **THEN** the proxy SHALL map `haiku` requests to that LMStudio model
