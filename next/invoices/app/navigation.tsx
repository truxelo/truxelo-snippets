import { FileText, LayoutDashboard, LogOut, Settings, Truck } from 'lucide-react'
import type React from 'react'

import { Separator } from '@/components/ui/separator'
import { cn } from '@/lib/utils'

export function NavigationSidebar() {
  return (
    <aside className="relative flex h-screen w-64 flex-col border-r bg-muted py-2">
      <h1 className="px-6 pt-1 pb-3 font-black text-2xl">TRUXELO</h1>
      <Separator />
      <nav className="flex flex-1 flex-col gap-1 px-4 py-4">
        <NavigationItem icon={<LayoutDashboard size={17} strokeWidth={1.5} />} label="Tableau de bord" active={false} />
        <NavigationItem icon={<Truck size={17} strokeWidth={1.5} />} label="Ordres de transport" active={false} />
        <NavigationItem icon={<FileText size={17} strokeWidth={1.5} />} label="Factures" active={true} />
      </nav>
      <nav className="flex flex-col gap-1 border-t px-4 py-4">
        <NavigationItem icon={<Settings size={17} strokeWidth={1.5} />} label="Paramètres" active={false} />
        <NavigationItem icon={<LogOut size={17} strokeWidth={1.5} />} label="Déconnexion" />
      </nav>
    </aside>
  )
}

interface NavigationItemProps {
  icon: React.ReactNode
  label: string
  active?: boolean
}

function NavigationItem({ icon, label, active }: NavigationItemProps) {
  return (
    <div
      className={cn(
        'font-medium text-muted-foreground text-sm',
        'cursor-pointer rounded-md transition-all',
        'flex h-8 items-center gap-2 p-2',
        active && 'bg-indigo-100 text-neutral-800',
        !active && 'hover:bg-white/50'
      )}
    >
      <span className="shrink-0">{icon}</span>
      <span className="truncate">{label}</span>
    </div>
  )
}
