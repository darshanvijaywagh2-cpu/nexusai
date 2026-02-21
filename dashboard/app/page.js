import { BarChart3, MessageSquare, Bot, Users, TrendingUp, DollarSign } from 'lucide-react'

export default function Home() {
  const stats = [
    { label: 'Total API Calls', value: '12,847', change: '+12%', icon: BarChart3 },
    { label: 'Cost Saved', value: '$847', change: 'via smart routing', icon: DollarSign },
    { label: 'Models Active', value: '4', change: 'All online', icon: Bot },
    { label: 'Team Members', value: '3', change: 'Active', icon: Users },
  ]

  const recentActivity = [
    { action: 'Chat with Groq', time: '2 min ago', status: 'Success' },
    { action: 'Cost alert', time: '15 min ago', status: 'Info' },
    { action: 'Model fallback', time: '1 hour ago', status: 'Auto' },
    { action: 'New prompt saved', time: '2 hours ago', status: 'Success' },
  ]

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <p className="text-muted-foreground">Welcome back! Here's your AI usage overview.</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat, i) => (
          <div key={i} className="p-6 rounded-xl bg-card border border-border">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">{stat.label}</p>
                <p className="text-2xl font-bold mt-1">{stat.value}</p>
                <p className="text-xs text-green-500 mt-1">{stat.change}</p>
              </div>
              <stat.icon className="w-8 h-8 text-primary" />
            </div>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <a href="/chat" className="p-6 rounded-xl bg-card border border-border hover:border-primary/50 transition">
          <MessageSquare className="w-8 h-8 text-primary mb-3" />
          <h3 className="font-semibold">Start Chatting</h3>
          <p className="text-sm text-muted-foreground">Try any model instantly</p>
        </a>
        <a href="/cost" className="p-6 rounded-xl bg-card border border-border hover:border-primary/50 transition">
          <TrendingUp className="w-8 h-8 text-green-500 mb-3" />
          <h3 className="font-semibold">View Savings</h3>
          <p className="text-sm text-muted-foreground">$847 saved this month</p>
        </a>
        <a href="/models" className="p-6 rounded-xl bg-card border border-border hover:border-primary/50 transition">
          <Bot className="w-8 h-8 text-purple-500 mb-3" />
          <h3 className="font-semibold">Manage Models</h3>
          <p className="text-sm text-muted-foreground">Configure providers</p>
        </a>
      </div>

      {/* Recent Activity */}
      <div className="rounded-xl bg-card border border-border p-6">
        <h3 className="font-semibold mb-4">Recent Activity</h3>
        <div className="space-y-3">
          {recentActivity.map((activity, i) => (
            <div key={i} className="flex items-center justify-between py-2 border-b border-border last:border-0">
              <span>{activity.action}</span>
              <div className="text-right">
                <span className="text-xs text-muted-foreground">{activity.time}</span>
                <span className="ml-2 text-xs px-2 py-0.5 rounded bg-green-500/20 text-green-500">{activity.status}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
