# Change: 添加本地 Ollama 和 LMStudio 模型配置示例

## Why

用户需要在 .env 配置文件中添加对本地大语言模型服务（Ollama 和 LMStudio）的配置示例，方便快速配置和测试本地模型调用。

## What Changes

- 在 `.env.example` 文件中添加 Ollama 和 LMStudio 的配置示例
- 包含完整的配置变量说明和注释
- 提供测试用例验证配置有效性

## Impact

- Affected specs: `configuration`
- Affected code: `.env.example`
