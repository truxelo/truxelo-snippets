import { MapPin } from 'lucide-react'

import { Checkbox } from '@/components/ui/checkbox'
import { Separator } from '@/components/ui/separator'
import type { TransportOrder } from '@/lib/models'

export function TransportOrderCard({ transportOrder }: { transportOrder: TransportOrder }) {
  return (
    <label
      htmlFor={transportOrder.id}
      className="flex flex-col justify-between gap-2 rounded-md border border-border bg-white p-2 pl-3"
    >
      <div className="flex w-full grow flex-col items-start">
        <div className="flex w-full flex-row items-center justify-between">
          <div className="flex flex-row items-center gap-2">
            <Checkbox id={transportOrder.id} />
            <div className="font-black">{transportOrder.references.internal}</div>
          </div>
          <div className="font-semibold text-muted-foreground text-sm">{transportOrder.references.client}</div>
        </div>
        <div className="ml-6 text-muted-foreground text-sm leading-tight">{transportOrder.client}</div>
      </div>
      <Separator />
      <div className="flex flex-row justify-between gap-2">
        <div className="flex flex-row items-center gap-1 text-sm">
          <MapPin size={14} strokeWidth={1.5} className="text-muted-foreground" />
          <span>{transportOrder.loadingAddress.city} </span>
          <span className="text-xs">→</span>
          <span>{transportOrder.unloadingAddress.city}</span>
        </div>
        <div className="flex flex-row items-center gap-1 font-bold text-sm">
          {transportOrder.price.amount} {transportOrder.price.currency}
        </div>
      </div>
    </label>
  )
}
