'use client'

import { Trash2 } from 'lucide-react'

import { deleteInvoiceAction } from '@/app/actions'
import { Button } from '@/components/ui/button'
import type { Invoice } from '@/lib/models'

export function InvoiceCard({ invoice }: { invoice: Invoice }) {
  return (
    <div className="flex items-center justify-between rounded-md border border-border bg-muted/50 p-2 pl-3">
      <div className="font-mono text-xs">{invoice.id}</div>
      <Button size="icon" onClick={() => deleteInvoiceAction(invoice.id)} className="size-7">
        <Trash2 className="size-3.5" />
      </Button>
    </div>
  )
}
