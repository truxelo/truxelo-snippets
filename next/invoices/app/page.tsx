import { Plus } from 'lucide-react'

import { Button } from '@/components/ui/button'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Separator } from '@/components/ui/separator'
import { invoiceStore, transportOrderStore } from '@/lib/stores'

import { createInvoiceAction } from './actions'
import { InvoiceCard, TransportOrderCard } from './cards'

export default async function Component() {
  const transportOrders = await transportOrderStore.fetchAll()
  const invoices = await invoiceStore.fetchAll()

  return (
    <main className="flex h-[calc(100dvh+0.5rem)] w-full flex-col py-2">
      <div className="flex shrink-0 flex-row items-center justify-between px-4 pt-1 pb-3">
        <h1 className="font-black text-2xl">FACTURES</h1>
        <form action={createInvoiceAction}>
          <Button size="sm" type="submit">
            <Plus className="size-4" />
            Nouvelle Facture
          </Button>
        </form>
      </div>
      <Separator />
      <div className="grid h-full min-h-0 w-full grid-cols-3 overflow-hidden">
        <ScrollArea className="col-span-2 overflow-hidden">
          <section className="flex flex-col gap-2 p-4">
            {invoices.map((invoice) => (
              <InvoiceCard key={invoice.id} invoice={invoice} />
            ))}
            {invoices.length === 0 && <p className="text-muted-foreground italic">Aucune facture trouvée.</p>}
          </section>
        </ScrollArea>
        <ScrollArea className="col-span-1 h-full overflow-hidden border-border border-l bg-muted/50">
          <aside className="flex flex-col gap-2 p-4">
            {transportOrders.map((transportOrder) => (
              <TransportOrderCard key={transportOrder.id} transportOrder={transportOrder} />
            ))}
            {transportOrders.length === 0 && (
              <p className="text-muted-foreground italic">Aucun ordres de transport facturable.</p>
            )}
          </aside>
        </ScrollArea>
      </div>
    </main>
  )
}
