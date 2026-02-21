'use client'

import { Shield, AlertTriangle, CheckCircle, Users, Lock } from 'lucide-react'

const securityEvents = [
  { type: 'blocked', message: 'Prompt injection attempt detected', time: '2 hours ago', severity: 'high' },
  { type: 'allowed', message: 'File read request auto-approved', time: '3 hours ago', severity: 'low' },
  { type: 'blocked', message: 'External API call to unknown domain', time: '5 hours ago', severity: 'medium' },
  { type: 'allowed', message: 'WhatsApp message sent successfully', time: '6 hours ago', severity: 'low' },
  { type: 'allowed', message: 'Safe search query executed', time: '8 hours ago', severity: 'low' },
]

const teamMembers = [
  { name: 'Darshan (You)', role: 'Admin', permissions: ['All'], status: 'active' },
  { name: 'Employee 1', role: 'Manager', permissions: ['Read', 'Write', 'Execute', 'Approve'], status: 'active' },
  { name: 'Contractor A', role: 'Viewer', permissions: ['Read'], status: 'pending' },
]

export default function Security() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold">Security Center</h1>
        <p className="text-muted-foreground">Monitor and control NexusClaw security</p>
      </div>

      {/* Security Status */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="p-6 rounded-xl bg-card border border-green-500/30">
          <Shield className="w-8 h-8 text-green-500 mb-3" />
          <p className="text-2xl font-bold">Secure</p>
          <p className="text-xs text-muted-foreground">No threats detected</p>
        </div>
        <div className="p-6 rounded-xl bg-card border border-border">
          <AlertTriangle className="w-8 h-8 text-yellow-500 mb-3" />
          <p className="text-2xl font-bold">2</p>
          <p className="text-xs text-muted-foreground">Pending Confirmations</p>
        </div>
        <div className="p-6 rounded-xl bg-card border border-border">
          <Lock className="w-8 h-8 text-muted-foreground mb-3" />
          <p className="text-2xl font-bold">15</p>
          <p className="text-xs text-muted-foreground">Actions Today</p>
        </div>
        <div className="p-6 rounded-xl bg-card border border-border">
          <Users className="w-8 h-8 text-muted-foreground mb-3" />
          <p className="text-2xl font-bold">3</p>
          <p className="text-xs text-muted-foreground">Team Members</p>
        </div>
      </div>

      {/* Recent Events */}
      <div className="rounded-xl bg-card border border-border p-6">
        <h3 className="font-semibold mb-4">Recent Security Events</h3>
        <div className="space-y-3">
          {securityEvents.map((event, i) => (
            <div key={i} className="flex items-center justify-between p-3 rounded-lg bg-secondary">
              <div className="flex items-center gap-3">
                {event.type === 'blocked' ? (
                  <AlertTriangle className="w-5 h-5 text-red-500" />
                ) : (
                  <CheckCircle className="w-5 h-5 text-green-500" />
                )}
                <span>{event.message}</span>
              </div>
              <div className="flex items-center gap-3">
                <span className={`px-2 py-0.5 rounded text-xs ${
                  event.severity === 'high' ? 'bg-red-500/20 text-red-500' :
                  event.severity === 'medium' ? 'bg-yellow-500/20 text-yellow-500' :
                  'bg-green-500/20 text-green-500'
                }`}>
                  {event.severity}
                </span>
                <span className="text-xs text-muted-foreground">{event.time}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Team Permissions */}
      <div className="rounded-xl bg-card border border-border p-6">
        <h3 className="font-semibold mb-4">Team Permissions</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-border">
                <th className="text-left py-3 px-4">Member</th>
                <th className="text-left py-3 px-4">Role</th>
                <th className="text-left py-3 px-4">Permissions</th>
                <th className="text-left py-3 px-4">Status</th>
              </tr>
            </thead>
            <tbody>
              {teamMembers.map((member, i) => (
                <tr key={i} className="border-b border-border">
                  <td className="py-3 px-4">{member.name}</td>
                  <td className="py-3 px-4">{member.role}</td>
                  <td className="py-3 px-4">
                    <div className="flex gap-1">
                      {member.permissions.map((perm, j) => (
                        <span key={j} className="px-2 py-0.5 rounded bg-secondary text-xs">{perm}</span>
                      ))}
                    </div>
                  </td>
                  <td className="py-3 px-4">
                    <span className={`px-2 py-0.5 rounded text-xs ${
                      member.status === 'active' ? 'bg-green-500/20 text-green-500' : 'bg-yellow-500/20 text-yellow-500'
                    }`}>
                      {member.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Security Settings */}
      <div className="rounded-xl bg-card border border-border p-6">
        <h3 className="font-semibold mb-4">Security Settings</h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between p-3 rounded-lg bg-secondary">
            <div>
              <p className="font-medium">Confirm Sensitive Actions</p>
              <p className="text-sm text-muted-foreground">Ask before sending messages, accessing files</p>
            </div>
            <input type="checkbox" defaultChecked className="w-5 h-5 accent-primary" />
          </div>
          <div className="flex items-center justify-between p-3 rounded-lg bg-secondary">
            <div>
              <p className="font-medium">Prompt Injection Detection</p>
              <p className="text-sm text-muted-foreground">Block malicious prompt attempts</p>
            </div>
            <input type="checkbox" defaultChecked className="w-5 h-5 accent-primary" />
          </div>
          <div className="flex items-center justify-between p-3 rounded-lg bg-secondary">
            <div>
              <p className="font-medium">Auto-block Payments</p>
              <p className="text-sm text-muted-foreground">Block all payment-related actions</p>
            </div>
            <input type="checkbox" defaultChecked className="w-5 h-5 accent-primary" />
          </div>
        </div>
      </div>
    </div>
  )
}
