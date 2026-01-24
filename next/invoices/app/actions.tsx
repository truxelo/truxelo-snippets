'use server'

import { revalidatePath } from 'next/cache'

import { createInvoice } from '@/lib/models'
import { invoiceStore } from '@/lib/stores'

export async function createInvoiceAction() {
  const newInvoice = createInvoice()
  await invoiceStore.create(newInvoice)
  revalidatePath('/')
}

export async function deleteInvoiceAction(id: string) {
  await invoiceStore.delete(id)
  revalidatePath('/')
}
