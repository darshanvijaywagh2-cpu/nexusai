'use client'

import { BarChart, TrendingDown, TrendingUp } from 'lucide-react'

export default function Cost() {
  const costData = [
    { provider: 'Groq', cost: 0, tokens: 45000, calls: 892, color: 'bg-green-500' },
    { provider: 'OpenAI', cost: 45.20, tokens: 12500, calls: 156, color: 'bg-blue-500' },
    { provider: 'Gemini', cost: 3.50, tokens: 28000, calls: 445, color: 'bg-yellow-500' },
    { provider: 'Claude', cost: 12.80, tokens: 8200, calls: 98, color: 'bg-purple-500' },
    { provider: 'Ollama', cost: 0, tokens: 15000, calls: 320, color: 'bg-orange-500' },
  ]

  const totalCost = costData.reduce((sum, d) => sum + d.cost, 0)
  const totalTokens = costData.reduce((sum, d) => sum + d.tokens, 0)
  const savings = 87.50 // Estimated savings from smart routing

  const dailyData = [
    { day: 'Mon', cost: 12.30 },
    { day: 'Tue', cost: 8.50 },
    { day: 'Wed', cost: 15.20 },
    { day: 'Thu', cost: 6.80 },
    { day: 'Fri', cost: 11.40 },
    { day: 'Sat', cost: 3.20 },
    { day: 'Sun', cost: 2.10 },
  ]

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold">Cost Analytics</h1>
        <p className="text-muted-foreground">Track your AI spending and savings</p>
      </div>

      {/* Savings Alert */}
      <div className="p-6 rounded-xl bg-gradient-to-r from-green-500/20 to-emerald-500/20 border border-green-500/30">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-green-400">Smart Routing Savings</p>
            <p className="text-3xl font-bold text-green-500">${savings.toFixed(2)}</p>
            <p className="text-xs text-muted-foreground mt-1">This month vs using single provider</p>
          </div>
          <TrendingUp className="w-12 h-12 text-green-500" />
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-6 rounded-xl bg-card border border-border">
          <p className="text-sm text-muted-foreground">Total Spent</p>
          <p className="text-3xl font-bold">${totalCost.toFixed(2)}</p>
        </div>
        <div className="p-6 rounded-xl bg-card border border-border">
          <p className="text-sm text-muted-foreground">Total Tokens</p>
          <p className="text-3xl font-bold">{(totalTokens / 1000).toFixed(1)}K</p>
        </div>
        <div className="p-6 rounded-xl bg-card border border-border">
          <p className="text-sm text-muted-foreground">Total Calls</p>
          <p className="text-3xl font-bold">1,911</p>
        </div>
      </div>

      {/* Provider Breakdown */}
      <div className="rounded-xl bg-card border border-border p-6">
        <h3 className="font-semibold mb-4">Provider Breakdown</h3>
        <div className="space-y-4">
          {costData.map((provider, i) => (
            <div key={i} className="flex items-center gap-4">
              <div className={`w-3 h-3 rounded-full ${provider.color}`} />
              <div className="flex-1">
                <div className="flex justify-between mb-1">
                  <span className="font-medium">{provider.provider}</span>
                  <span className="text-muted-foreground">${provider.cost.toFixed(2)}</span>
                </div>
                <div className="h-2 bg-secondary rounded-full overflow-hidden">
                  <div 
                    className={`h-full ${provider.color}`} 
                    style={{ width: `${(provider.cost / totalCost) * 100 || 0}%` }}
                  />
                </div>
              </div>
              <div className="text-right text-sm text-muted-foreground">
                <p>{provider.tokens.toLocaleString()} tokens</p>
                <p>{provider.calls} calls</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Suggestions */}
      <div className="rounded-xl bg-card border border-border p-6">
        <h3 className="font-semibold mb-4">💡 Optimization Suggestions</h3>
        <div className="space-y-3">
          <div className="flex items-start gap-3 p-3 rounded-lg bg-yellow-500/10 border border-yellow-500/30">
            <TrendingDown className="w-5 h-5 text-yellow-500 shrink-0 mt-0.5" />
            <div>
              <p className="font-medium">Route 60% traffic to Groq</p>
              <p className="text-sm text-muted-foreground">Save ~$28/month by using free models for simple queries</p>
            </div>
          </div>
          <div className="flex items-start gap-3 p-3 rounded-lg bg-blue-500/10 border border-blue-500/30">
            <BarChart className="w-5 h-5 text-blue-500 shrink-0 mt-0.5" />
            <div>
              <p className="font-medium">Peak usage: 2-5 PM</p>
              <p className="text-sm text-muted-foreground">Consider caching responses during peak hours</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
