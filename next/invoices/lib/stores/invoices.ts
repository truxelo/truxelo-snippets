import { z } from 'zod'

import type { Invoice } from '@/lib/models'
import { InvoiceSchema } from '@/lib/models'

const DUMMY_INVOICES: Invoice[] = [
  { id: '019bf0a1-fe9f-77a2-8d96-9997044496d5' },
  { id: '019bf0a2-10fa-729c-b48f-f1af14c445a2' }
]

/** In-memory persistence layer for Invoice entities. */
class InvoiceStore {
  private invoices = new Map<string, Invoice>(DUMMY_INVOICES.map((invoice) => [invoice.id, invoice]))

  /** Retrieves a single invoice by its identifier. */
  async fetch(id: string): Promise<Invoice | null> {
    const data = this.invoices.get(id)
    if (!data) return null
    return InvoiceSchema.parse(data)
  }

  /** Returns all stored invoices. */
  async fetchAll(): Promise<Invoice[]> {
    const data = Array.from(this.invoices.values())
    return z.array(InvoiceSchema).parse(data)
  }

  /** Validates and persists a new invoice record. */
  async create(input: Invoice): Promise<Invoice> {
    const invoice = InvoiceSchema.parse(input)
    this.invoices.set(invoice.id, invoice)
    return invoice
  }

  /** Updates an existing invoice or throws if the ID is unknown. */
  async update(input: Invoice): Promise<Invoice> {
    const invoice = InvoiceSchema.parse(input)
    if (!this.invoices.has(invoice.id)) {
      throw new Error(`Invoice ${invoice.id} not found`)
    }
    this.invoices.set(invoice.id, invoice)
    return invoice
  }

  /** Removes an invoice from the storage. */
  async delete(id: string): Promise<void> {
    this.invoices.delete(id)
  }
}

/** Global singleton instance providing shared state across the server. */
export const invoiceStore = new InvoiceStore()
