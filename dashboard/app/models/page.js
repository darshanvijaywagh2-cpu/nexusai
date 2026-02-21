'use client'

import { Bot, CheckCircle, XCircle, Clock, Zap } from 'lucide-react'

const providers = [
  { 
    id: 'groq', 
    name: 'Groq', 
    status: 'online', 
    models: ['llama3-70b', 'mixtral-8x7b', 'whisper'],
    latency: 300,
    cost: 'Free',
    icon: '🚀'
  },
  { 
    id: 'openai', 
    name: 'OpenAI', 
    status: 'online', 
    models: ['gpt-4o', 'gpt-4-turbo', 'gpt-3.5-turbo'],
    latency: 800,
    cost: '$$$',
    icon: '🤖'
  },
  { 
    id: 'gemini', 
    name: 'Google Gemini', 
    status: 'online', 
    models: ['gemini-pro', 'gemini-flash'],
    latency: 600,
    cost: '$',
    icon: '🔮'
  },
  { 
    id: 'anthropic', 
    name: 'Anthropic', 
    status: 'online', 
    models: ['claude-3-opus', 'claude-3-sonnet'],
    latency: 1000,
    cost: '$$',
    icon: '📘'
  },
  { 
    id: 'ollama', 
    name: 'Ollama (Local)', 
    status: 'offline', 
    models: ['mistral', 'llama2', 'phi3'],
    latency: 100,
    cost: 'Free',
    icon: '💻'
  },
]

export default function Models() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold">Model Management</h1>
        <p className="text-muted-foreground">Configure and monitor AI providers</p>
      </div>

      {/* Provider Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {providers.map(provider => (
          <div key={provider.id} className="p-6 rounded-xl bg-card border border-border">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <span className="text-2xl">{provider.icon}</span>
                <div>
                  <h3 className="font-semibold">{provider.name}</h3>
                  <p className="text-xs text-muted-foreground">{provider.models.length} models</p>
                </div>
              </div>
              {provider.status === 'online' ? (
                <CheckCircle className="w-6 h-6 text-green-500" />
              ) : (
                <XCircle className="w-6 h-6 text-red-500" />
              )}
            </div>
            
            <div className="space-y-2 mb-4">
              {provider.models.map(model => (
                <div key={model} className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">{model}</span>
                  <span className={`px-2 py-0.5 rounded text-xs ${
                    provider.status === 'online' ? 'bg-green-500/20 text-green-500' : 'bg-secondary text-muted-foreground'
                  }`}>
                    {provider.status === 'online' ? 'Active' : 'Inactive'}
                  </span>
                </div>
              ))}
            </div>

            <div className="flex items-center justify-between pt-4 border-t border-border">
              <div className="flex items-center gap-2">
                <Clock className="w-4 h-4 text-muted-foreground" />
                <span className="text-sm">{provider.latency}ms</span>
              </div>
              <span className={`text-sm font-medium ${
                provider.cost === 'Free' ? 'text-green-500' : 'text-yellow-500'
              }`}>
                {provider.cost}
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* Add New Provider */}
      <div className="rounded-xl bg-card border border-border p-6">
        <h3 className="font-semibold mb-4">Add New Provider</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <input
            type="text"
            placeholder="Provider name"
            className="px-4 py-2 rounded-lg bg-secondary border border-border"
          />
          <input
            type="text"
            placeholder="API Key"
            className="px-4 py-2 rounded-lg bg-secondary border border-border"
          />
          <button className="px-4 py-2 rounded-lg bg-primary text-white hover:bg-primary/90 flex items-center justify-center gap-2">
            <Zap className="w-4 h-4" /> Add Provider
          </button>
        </div>
      </div>

      {/* Smart Routing */}
      <div className="rounded-xl bg-card border border-border p-6">
        <h3 className="font-semibold mb-4">Smart Routing Rules</h3>
        <div className="space-y-3">
          <div className="flex items-center justify-between p-3 rounded-lg bg-secondary">
            <span>Simple questions</span>
            <span className="text-primary">→ Groq (Free)</span>
          </div>
          <div className="flex items-center justify-between p-3 rounded-lg bg-secondary">
            <span>Complex analysis</span>
            <span className="text-purple-500">→ Claude 3 ($$)</span>
          </div>
          <div className="flex items-center justify-between p-3 rounded-lg bg-secondary">
            <span>Code generation</span>
            <span className="text-blue-500">→ GPT-4o ($$$)</span>
          </div>
          <div className="flex items-center justify-between p-3 rounded-lg bg-secondary">
            <span>Fallback on failure</span>
            <span className="text-yellow-500">→ Gemini (Auto)</span>
          </div>
        </div>
      </div>
    </div>
  )
}
