'use client'

import { useState } from 'react'
import { Send, Bot } from 'lucide-react'

const models = [
  { id: 'groq/llama3-70b', name: 'Groq - Llama 3', provider: 'groq', speed: 'Fast', cost: 'Free' },
  { id: 'openai/gpt-4o', name: 'OpenAI - GPT-4o', provider: 'openai', speed: 'Medium', cost: '$$$' },
  { id: 'anthropic/claude-3', name: 'Claude 3', provider: 'anthropic', speed: 'Medium', cost: '$$' },
  { id: 'gemini/gemini-pro', name: 'Gemini Pro', provider: 'gemini', speed: 'Fast', cost: '$' },
  { id: 'ollama/mistral', name: 'Ollama - Mistral', provider: 'ollama', speed: 'Local', cost: 'Free' },
]

export default function Chat() {
  const [selectedModel, setSelectedModel] = useState(models[0])
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hello! Select a model and start chatting. I\'ll automatically route your request for optimal cost/speed.' }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const sendMessage = async () => {
    if (!input.trim()) return
    
    const userMsg = { role: 'user', content: input }
    setMessages(prev => [...prev, userMsg])
    setInput('')
    setLoading(true)
    
    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: selectedModel.id,
          messages: [...messages, userMsg]
        })
      })
      const data = await response.json()
      setMessages(prev => [...prev, { role: 'assistant', content: data.response }])
    } catch (err) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Error: Could not connect to API' }])
    }
    setLoading(false)
  }

  return (
    <div className="flex h-[calc(100vh-4rem)] gap-6">
      {/* Model Selector */}
      <div className="w-72 bg-card rounded-xl border border-border p-4">
        <h3 className="font-semibold mb-4">Select Model</h3>
        <div className="space-y-2">
          {models.map(model => (
            <button
              key={model.id}
              onClick={() => setSelectedModel(model)}
              className={`w-full text-left p-3 rounded-lg border transition ${
                selectedModel.id === model.id 
                  ? 'border-primary bg-primary/10' 
                  : 'border-border hover:border-primary/50'
              }`}
            >
              <p className="font-medium">{model.name}</p>
              <div className="flex gap-2 mt-1">
                <span className="text-xs text-muted-foreground">{model.speed}</span>
                <span className="text-xs text-green-500">{model.cost}</span>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex-1 flex flex-col bg-card rounded-xl border border-border">
        {/* Messages */}
        <div className="flex-1 p-4 overflow-y-auto space-y-4">
          {messages.map((msg, i) => (
            <div key={i} className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              {msg.role === 'assistant' && <Bot className="w-6 h-6 text-primary shrink-0" />}
              <div className={`max-w-[70%] p-3 rounded-lg ${
                msg.role === 'user' ? 'bg-primary text-primary-foreground' : 'bg-secondary'
              }`}>
                {msg.content}
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex gap-3">
              <Bot className="w-6 h-6 text-primary" />
              <div className="bg-secondary p-3 rounded-lg animate-pulse">Thinking...</div>
            </div>
          )}
        </div>

        {/* Input */}
        <div className="p-4 border-t border-border">
          <div className="flex gap-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
              placeholder="Message NexusAI..."
              className="flex-1 bg-secondary border border-border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
            />
            <button 
              onClick={sendMessage}
              disabled={loading}
              className="p-2 bg-primary text-white rounded-lg hover:bg-primary/90 disabled:opacity-50"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
          <p className="text-xs text-muted-foreground mt-2">
            Using {selectedModel.name} • {selectedModel.cost === 'Free' ? 'No cost' : 'Cost: ' + selectedModel.cost}
          </p>
        </div>
      </div>

      {/* Cost Panel */}
      <div className="w-64 bg-card rounded-xl border border-border p-4">
        <h3 className="font-semibold mb-4">Live Cost</h3>
        <div className="space-y-4">
          <div className="p-3 rounded-lg bg-green-500/10 border border-green-500/30">
            <p className="text-2xl font-bold text-green-500">$0.00</p>
            <p className="text-xs text-muted-foreground">This session</p>
          </div>
          <div className="p-3 rounded-lg bg-secondary">
            <p className="text-sm text-muted-foreground">Model</p>
            <p className="font-medium">{selectedModel.provider}</p>
          </div>
          <div className="p-3 rounded-lg bg-secondary">
            <p className="text-sm text-muted-foreground">Routing</p>
            <p className="font-medium text-green-500">Smart Auto</p>
          </div>
        </div>
      </div>
    </div>
  )
}
