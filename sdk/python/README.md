# NexusAI SDK
One SDK to Rule All AI Models

## Installation

```bash
pip install nexusai
```

## Quick Start

```python
from nexusai import NexusAI

# Initialize
nexus = NexusAI()

# Chat with any model
response = nexus.chat("groq/llama3-70b", [
    {"role": "user", "content": "Hello!"}
])

print(response['response'])
```

## Supported Providers

| Provider | Models | Cost |
|----------|--------|------|
| OpenAI | gpt-4o, gpt-4-turbo | $ |
| Anthropic | claude-3-opus, claude-3-sonnet | $ |
| Gemini | gemini-pro, gemini-flash | $ |
| Groq | llama3-70b, mixtral | FREE |
| Ollama | mistral, llama2 | FREE |

## Examples

### Basic Chat
```python
nexus.chat("openai/gpt-4o", [{"role": "user", "content": "Hi"}])
nexus.chat("anthropic/claude-3", [{"role": "user", "content": "Hi"}])
nexus.chat("gemini/gemini-pro", [{"role": "user", "content": "Hi"}])
nexus.chat("groq/llama3-70b", [{"role": "user", "content": "Hi"}])
```

### Auto-Fallback
```python
# If one fails, automatically tries next
nexus.chat("openai/gpt-4o", [...], fallback=True)
```

### Cost Tracking
```python
summary = nexus.get_cost_summary()
print(summary)
# {'total_tokens': 1500, 'by_provider': {...}}
```

### Create AI Agent
```python
agent = nexus.create_agent()
agent.add_tool(web_search)
agent.run("Find latest AI news")
```

## Environment Variables

```bash
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=AI...
GROQ_API_KEY=gsk_...
OLLAMA_URL=http://localhost:11434
```

## License

MIT
