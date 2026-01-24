import { v7 as uuidv7 } from 'uuid'
import { z } from 'zod'

// --- Schemas ---

/** Represents an invoice. */
export const InvoiceSchema = z.object({
  id: z.uuidv7()
})

// --- Types ---

/** Type inference for the Invoice entity */
export type Invoice = z.infer<typeof InvoiceSchema>

// --- Functions ---

/**
 * Initializes a new empty invoice.
 * @returns A basic Invoice object.
 */
export function createInvoice(): Invoice {
  return {
    id: uuidv7()
  }
}
