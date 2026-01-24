import { v7 as uuidv7 } from 'uuid'
import { z } from 'zod'

// --- Constants ---

/** Available currencies for pricing */
export const CURRENCIES = ['EUR', 'USD', 'GBP'] as const

// --- Schemas ---

/** Physical location for transport logistics */
export const AddressSchema = z.object({
  street: z.string(),
  city: z.string(),
  postalCode: z.string()
})

/** Pricing details including amount and currency */
export const PriceSchema = z.object({
  amount: z.number().nonnegative(),
  currency: z.enum(CURRENCIES)
})

/** Client and Internal tracking references */
export const ReferencesSchema = z.object({
  internal: z.string(),
  client: z.string()
})

/** Root entity representing a simplified transport order */
export const TransportOrderSchema = z.object({
  id: z.uuidv7(),
  client: z.string(),
  loadingAddress: AddressSchema,
  unloadingAddress: AddressSchema,
  cargo: z.string(),
  price: PriceSchema,
  references: ReferencesSchema
})

// --- Types ---

/** Literal type for supported currencies */
export type Currency = (typeof CURRENCIES)[number]

/** Type inference for the Address sub-component */
export type Address = z.infer<typeof AddressSchema>

/** Type inference for the TransportOrder entity */
export type TransportOrder = z.infer<typeof TransportOrderSchema>

// --- Functions ---

/**
 * Initializes a new transport order with default values and a fresh UUID v7.
 * @param initial - Partial order object to override defaults.
 * @returns A complete TransportOrder object.
 */
export function createTransportOrder(initial: Partial<TransportOrder> = {}): TransportOrder {
  return {
    id: uuidv7(),
    client: initial.client ?? '',
    cargo: initial.cargo ?? '',
    loadingAddress: initial.loadingAddress ?? {
      street: '',
      city: '',
      postalCode: ''
    },
    unloadingAddress: initial.unloadingAddress ?? {
      street: '',
      city: '',
      postalCode: ''
    },
    price: initial.price ?? {
      amount: 0,
      currency: 'EUR'
    },
    references: initial.references ?? {
      internal: '',
      client: ''
    }
  }
}
