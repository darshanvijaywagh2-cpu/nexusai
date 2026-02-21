# ⚡ NexusAI

<div align="center">

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Stars](https://img.shields.io/github/stars/nexusai/nexusai?style=flat)
![Version](https://img.shields.io/badge/version-1.0.0-purple.svg)

### Universal AI Gateway — LiteLLM Alternative with India-First Features

**One SDK to rule all AI models. Built for India, loved worldwide.**

[Website](https://nexusai.in) • [Docs](https://docs.nexusai.in) • [Discord](https://discord.gg/nexusai) • [Twitter](https://twitter.com/nexusai)

</div>

---

## ✨ Why NexusAI?

| Feature | NexusAI | LiteLLM |
|---------|---------|---------|
| **India-First Features** | ✅ 🇮🇳 | ❌ |
| **Security Layer** | ✅ Built-in | ❌ |
| **Hindi Support** | ✅ Auto-detect | ❌ |
| **Smart Routing** | ✅ Cost + Speed | ✅ |
| **Team Mode** | ✅ Role-based | ❌ |
| **Open Source** | ✅ MIT | ✅ |
| **Free Tier** | ✅ Unlimited | ❌ Limited |

---

## 🚀 Quick Start

### One-Command Install

```bash
# Clone and run!
git clone https://github.com/nexusai/nexusai.git
cd nexusai
./startup.sh
```

### Python SDK

```bash
pip install nexusai
```

```python
from nexusai import NexusAI

# Initialize with any provider
ai = NexusAI()

# Chat with automatic routing
response = ai.chat(
    model="groq/llama3-70b",
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response)
```

### Docker (Recommended)

```bash
# One command to start everything!
docker-compose up -d
```

Then open http://localhost:3000

---

## 🎯 Features

### 🌍 Universal Model Support
- **OpenAI** (GPT-4, GPT-3.5)
- **Anthropic** (Claude 3)
- **Google Gemini**
- **Groq** (Free!)
- **Ollama** (Local models)
- **100+ more coming soon**

### 🛡️ Security Layer (Patent Pending)
- Prompt injection detection
- Auto-confirm for sensitive actions
- Sensitive data blocking
- Action history logging
- Team permissions

### 🇮🇳 India-First
- **Hindi/Indian language support** — Auto-detect + respond
- **GST reminders** — Never miss a deadline
- **NSE/BSE trading days** — Market status API
- **Festival calendar** — Diwali, Holi, etc.
- **UPI integration** — Coming soon

### 💰 Smart Cost Routing
- Auto-route to cheapest model
- Save up to 90% on API costs
- Usage analytics dashboard
- Cost alerts

### 👥 Team Mode
- Role-based permissions
- Workflow approvals
- Multiple team members
- Activity logging

---

## 📊 Dashboard

![Dashboard](https://via.placeholder.com/800x400?text=NexusAI+Dashboard)

### Pages
- **Chat** — Try any model instantly
- **Cost** — See savings in real-time
- **Models** — Manage all providers
- **Security** — Monitor threats
- **India** — India-specific tools

---

## 🔧 Configuration

### Environment Variables

```bash
# Copy .env.example to .env
cp .env.example .env

# Edit with your API keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=...
GROQ_API_KEY=...
```

### API Usage

```bash
# Chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"model": "groq/llama3-70b", "messages": [{"role": "user", "content": "Hello"}]}'

# List models
curl http://localhost:8000/models

# Cost summary
curl http://localhost:8000/cost
```

---

## 📁 Project Structure

```
nexusai/
├── sdk/
│   └── python/
│       └── nexusai.py          # Main SDK
├── server/
│   ├── main.py                 # FastAPI server
│   ├── requirements.txt
│   └── Dockerfile
├── dashboard/
│   ├── app/                    # Next.js pages
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── startup.sh
├── .env.example
└── README.md
```

---

## 🌍 Roadmap

- [ ] v1.0 — Initial release (You are here!)
- [ ] v1.1 — Hindi voice support
- [ ] v1.2 — UPI payment integration
- [ ] v2.0 — Enterprise features
- [ ] v2.1 — Mobile app

---

## 🤝 Contributing

We love contributions! Here's how you can help:

1. **Fork** the repo
2. **Create** a feature branch (`git checkout -b feature/amazing`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing`)
5. **Open** a Pull Request

### Development Setup

```bash
# Clone
git clone https://github.com/nexusai/nexusai.git
cd nexusai

# Python dev
cd server
pip install -r requirements.txt
python main.py

# Dashboard dev
cd ../dashboard
npm install
npm run dev
```

---

## 📝 License

**MIT License** — Free for personal and commercial use.

---

## 🙏 Acknowledgments

- [LiteLLM](https://github.com/BerriAI/litellm) — Inspiration
- [OpenAI](https://openai.com) — API
- [Anthropic](https://anthropic.com) — Claude
- [Groq](https://groq.com) — Free API
- **Our Contributors** — You! 💙

---

<div align="center">

**Made with ❤️ in India** 🇮🇳

[Star us on GitHub](https://github.com/nexusai/nexusai) • [Follow on Twitter](https://twitter.com/nexusai)

</div>
