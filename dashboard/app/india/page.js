'use client'

import { Calendar, TrendingUp, Bell, Globe } from 'lucide-react'

const festivals = [
  { name: 'Holi', date: 'March 14, 2026', daysUntil: 21, type: 'Festival' },
  { name: 'Ganesh Chaturthi', date: 'September 7, 2026', daysUntil: 198, type: 'Festival' },
  { name: 'Diwali', date: 'October 20, 2026', daysUntil: 241, type: 'Festival' },
  { name: 'Dussehra', date: 'October 12, 2026', daysUntil: 233, type: 'Festival' },
]

const marketHolidays = [
  { date: 'March 20, 2026', name: 'Mahashivratri' },
  { date: 'April 3, 2026', name: 'Good Friday' },
  { date: 'April 14, 2026', name: 'Dr. Ambedkar Jayanti' },
]

export default function India() {
  const isTradingDay = true // Would be dynamic
  const currentTime = '10:30 AM IST'

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold">🇮🇳 India Features</h1>
        <p className="text-muted-foreground">India-specific integrations and utilities</p>
      </div>

      {/* Trading Status */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className={`p-6 rounded-xl border ${isTradingDay ? 'bg-green-500/10 border-green-500/30' : 'bg-red-500/10 border-red-500/30'}`}>
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold">NSE/BSE Status</h3>
            {isTradingDay ? (
              <span className="px-3 py-1 rounded-full bg-green-500/20 text-green-500 text-sm">OPEN</span>
            ) : (
              <span className="px-3 py-1 rounded-full bg-red-500/20 text-red-500 text-sm">CLOSED</span>
            )}
          </div>
          <p className="text-2xl font-bold">{currentTime}</p>
          <p className="text-sm text-muted-foreground">Market is {isTradingDay ? 'currently trading' : 'closed for today'}</p>
        </div>

        <div className="p-6 rounded-xl bg-card border border-border">
          <Calendar className="w-8 h-8 text-primary mb-3" />
          <h3 className="font-semibold mb-2">Next Holiday</h3>
          <p className="text-2xl font-bold">Holi</p>
          <p className="text-sm text-muted-foreground">March 14 (21 days)</p>
        </div>

        <div className="p-6 rounded-xl bg-card border border-border">
          <TrendingUp className="w-8 h-8 text-green-500 mb-3" />
          <h3 className="font-semibold mb-2">NIFTY</h3>
          <p className="text-2xl font-bold">22,450.30</p>
          <p className="text-sm text-green-500">+0.45% today</p>
        </div>
      </div>

      {/* Upcoming Festivals */}
      <div className="rounded-xl bg-card border border-border p-6">
        <h3 className="font-semibold mb-4">📅 Upcoming Festivals</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {festivals.map((festival, i) => (
            <div key={i} className="p-4 rounded-lg bg-secondary">
              <p className="font-medium">{festival.name}</p>
              <p className="text-sm text-muted-foreground">{festival.date}</p>
              <p className="text-xs text-primary mt-2">{festival.daysUntil} days</p>
            </div>
          ))}
        </div>
      </div>

      {/* GST Reminders */}
      <div className="rounded-xl bg-card border border-border p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-semibold">📋 GST Reminders</h3>
          <button className="px-3 py-1 rounded-lg bg-primary text-white text-sm">+ Add Reminder</button>
        </div>
        <div className="space-y-3">
          <div className="flex items-center justify-between p-3 rounded-lg bg-yellow-500/10 border border-yellow-500/30">
            <div className="flex items-center gap-3">
              <Bell className="w-5 h-5 text-yellow-500" />
              <span>GST Filing Due</span>
            </div>
            <span className="text-yellow-500">March 20, 2026</span>
          </div>
          <div className="flex items-center justify-between p-3 rounded-lg bg-secondary">
            <div className="flex items-center gap-3">
              <Bell className="w-5 h-5 text-muted-foreground" />
              <span>Quarterly Return</span>
            </div>
            <span className="text-muted-foreground">June 30, 2026</span>
          </div>
        </div>
      </div>

      {/* Indian Languages */}
      <div className="rounded-xl bg-card border border-border p-6">
        <h3 className="font-semibold mb-4">🌐 Language Support</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 rounded-lg bg-green-500/10 border border-green-500/30">
            <p className="font-medium">Hindi</p>
            <p className="text-sm text-green-500">✓ Supported</p>
            <p className="text-xs text-muted-foreground mt-2">Auto-detect + responses</p>
          </div>
          <div className="p-4 rounded-lg bg-green-500/10 border border-green-500/30">
            <p className="font-medium">Tamil</p>
            <p className="text-sm text-green-500">✓ Supported</p>
            <p className="text-xs text-muted-foreground mt-2">Beta</p>
          </div>
          <div className="p-4 rounded-lg bg-green-500/10 border border-green-500/30">
            <p className="font-medium">Bengali</p>
            <p className="text-sm text-green-500">✓ Supported</p>
            <p className="text-xs text-muted-foreground mt-2">Beta</p>
          </div>
        </div>
      </div>

      {/* Market Holidays */}
      <div className="rounded-xl bg-card border border-border p-6">
        <h3 className="font-semibold mb-4">🏛️ Market Holidays 2026</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-border">
                <th className="text-left py-2 px-4">Date</th>
                <th className="text-left py-2 px-4">Holiday</th>
              </tr>
            </thead>
            <tbody>
              {marketHolidays.map((holiday, i) => (
                <tr key={i} className="border-b border-border">
                  <td className="py-2 px-4">{holiday.date}</td>
                  <td className="py-2 px-4">{holiday.name}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
