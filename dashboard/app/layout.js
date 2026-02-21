import './globals.css'
import Link from 'next/link'

export const metadata = {
  title: 'NexusAI Dashboard',
  description: 'One SDK to Rule All AI Models',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-background text-foreground">
        <div className="flex min-h-screen">
          {/* Sidebar */}
          <aside className="w-64 bg-card border-r border-border p-4">
            <div className="mb-8">
              <h1 className="text-xl font-bold text-primary">⚡ NexusAI</h1>
              <p className="text-xs text-muted-foreground">Unified AI Gateway</p>
            </div>
            
            <nav className="space-y-2">
              <Link href="/" className="flex items-center gap-3 px-3 py-2 rounded-lg bg-primary/10 text-primary">
                <span>🏠</span> Dashboard
              </Link>
              <Link href="/chat" className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-secondary text-muted-foreground hover:text-foreground">
                <span>💬</span> Chat
              </Link>
              <Link href="/cost" className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-secondary text-muted-foreground hover:text-foreground">
                <span>💰</span> Cost
              </Link>
              <Link href="/models" className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-secondary text-muted-foreground hover:text-foreground">
                <span>🤖</span> Models
              </Link>
              <Link href="/security" className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-secondary text-muted-foreground hover:text-foreground">
                <span>🛡️</span> Security
              </Link>
              <Link href="/india" className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-secondary text-muted-foreground hover:text-foreground">
                <span>🇮🇳</span> India
              </Link>
            </nav>
            
            <div className="absolute bottom-4 left-4 right-4">
              <div className="p-3 rounded-lg bg-secondary">
                <p className="text-xs text-muted-foreground">API Status</p>
                <p className="text-sm text-green-500">● Connected</p>
              </div>
            </div>
          </aside>
          
          {/* Main Content */}
          <main className="flex-1 p-8">
            {children}
          </main>
        </div>
      </body>
    </html>
  )
}
