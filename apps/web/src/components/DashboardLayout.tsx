'use client'

import { ReactNode } from 'react'
import Link from 'next/link'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'next/navigation'

export function DashboardLayout({ children }: { children: ReactNode }) {
  const router = useRouter()
  const { user, logout } = useAuthStore()

  const handleLogout = async () => {
    try {
      await logout()
      router.push('/auth/login')
    } catch (error) {
      console.error('Logout failed:', error)
    }
  }

  return (
    <div className="flex h-screen bg-slate-900">
      <div className="w-64 bg-slate-800 border-r border-slate-700">
        <div className="p-6 border-b border-slate-700">
          <h1 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400">
            Luminai
          </h1>
        </div>
        <nav className="p-4 space-y-2">
          <Link href="/dashboard" className="block px-4 py-2 text-white hover:bg-slate-700 rounded-lg transition">
            🎨 Dashboard
          </Link>
          <Link href="/dashboard/image-generator" className="block px-4 py-2 text-white hover:bg-slate-700 rounded-lg transition">
            🖼️ Image Generation
          </Link>
          <Link href="/dashboard/video-creator" className="block px-4 py-2 text-white hover:bg-slate-700 rounded-lg transition">
            🎬 Video Creator
          </Link>
          <Link href="/dashboard/projects" className="block px-4 py-2 text-white hover:bg-slate-700 rounded-lg transition">
            💾 Projects
          </Link>
          <Link href="/dashboard/settings" className="block px-4 py-2 text-white hover:bg-slate-700 rounded-lg transition">
            ⚙️ Settings
          </Link>
        </nav>
        <div className="absolute bottom-0 w-64 p-4 border-t border-slate-700 bg-slate-800">
          <div className="flex items-center justify-between mb-4">
            <span className="text-white text-sm font-medium">{user?.name}</span>
          </div>
          <button
            onClick={handleLogout}
            className="w-full px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition text-sm font-medium"
          >
            Logout
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-auto">
        {children}
      </div>
    </div>
  )
}
