import { z } from 'zod'

import type { TransportOrder } from '@/lib/models'
import { TransportOrderSchema } from '@/lib/models'

const DUMMY_TRANSPORT_ORDERS: TransportOrder[] = [
  {
    id: '019bf0f5-8a2d-7097-89b1-fda62111f9c0',
    client: 'Unicorn S.A.S.',
    cargo: 'Blé en vrac',
    loadingAddress: { street: 'Quai du Port', city: 'Rouen', postalCode: '76000' },
    unloadingAddress: { street: 'Avenue de Paris', city: 'Chartres', postalCode: '28000' },
    price: { amount: 1250, currency: 'EUR' },
    references: { internal: 'OT26000001', client: 'REF-UNISAS-1' }
  },
  {
    id: '019bf0f5-9f57-7df1-ad30-d0fdbb029607',
    client: 'Unicorn S.A.S.',
    cargo: 'Maïs vrac',
    loadingAddress: { street: 'Avenue de la Gare', city: 'Nogent-sur-Seine', postalCode: '10400' },
    unloadingAddress: { street: 'ZAC du Moulin', city: 'Metz', postalCode: '57000' },
    price: { amount: 890, currency: 'EUR' },
    references: { internal: 'OT26000002', client: 'REF-UNISAS-2' }
  },
  {
    id: '019bf0f5-b7f3-7e2b-8352-56a03d164905',
    client: 'Global Logistique',
    cargo: 'Sucre sacs',
    loadingAddress: { street: 'Usine Nord', city: 'Lille', postalCode: '59000' },
    unloadingAddress: { street: 'Port de Gennevilliers', city: 'Gennevilliers', postalCode: '92230' },
    price: { amount: 450, currency: 'EUR' },
    references: { internal: 'OT26000003', client: 'GL-992' }
  },
  {
    id: '019bf0f5-d562-7bcc-a68d-81f4fdae7beb',
    client: 'Global Logistique',
    cargo: 'Colza',
    loadingAddress: { street: 'Terminal Vrac', city: 'Bordeaux', postalCode: '33000' },
    unloadingAddress: { street: 'Huilerie', city: 'Marseille', postalCode: '13000' },
    price: { amount: 1580, currency: 'EUR' },
    references: { internal: 'OT26000004', client: 'GL-881' }
  },
  {
    id: '019bf0f5-e97e-74b1-91d2-da0b041cb5da',
    client: 'AgriVrac',
    cargo: 'Engrais',
    loadingAddress: { street: 'Plateforme Logistique', city: 'Orléans', postalCode: '45000' },
    unloadingAddress: { street: 'Ferme Sud', city: 'Bourges', postalCode: '18000' },
    price: { amount: 620, currency: 'EUR' },
    references: { internal: 'OT26000005', client: 'AV-001' }
  },
  {
    id: '019bf0f6-00ad-7911-9b55-028035dad470',
    client: 'Unicorn S.A.S.',
    cargo: 'Orge de brasserie',
    loadingAddress: { street: 'Silo de Reims', city: 'Reims', postalCode: '51100' },
    unloadingAddress: { street: 'Brasserie Kronenbourg', city: 'Obernai', postalCode: '67210' },
    price: { amount: 940, currency: 'EUR' },
    references: { internal: 'OT26000006', client: 'REF-UNISAS-3' }
  },
  {
    id: '019bf0f6-1f19-723c-a707-1ef70a5288b6',
    client: 'AgriVrac',
    cargo: 'Pommes de terre',
    loadingAddress: { street: 'Hangar B', city: 'Caen', postalCode: '14000' },
    unloadingAddress: { street: 'Marché de Rungis', city: 'Rungis', postalCode: '94150' },
    price: { amount: 510, currency: 'EUR' },
    references: { internal: 'OT26000007', client: 'AV-002' }
  },
  {
    id: '019bf0f6-3ea4-7d69-b430-2e61a6a31f11',
    client: 'Global Logistique',
    cargo: 'Amidon de maïs',
    loadingAddress: { street: 'Usine Est', city: 'Lestrem', postalCode: '62136' },
    unloadingAddress: { street: 'Entrepôt Export', city: 'Dunkerque', postalCode: '59140' },
    price: { amount: 380, currency: 'EUR' },
    references: { internal: 'OT26000008', client: 'GL-002' }
  },
  {
    id: '019bf0f6-550c-7bc5-a6b3-87deae0a04eb',
    client: 'AgriVrac',
    cargo: 'Semences',
    loadingAddress: { street: 'Centre de Recherche', city: 'Clermont-Ferrand', postalCode: '63000' },
    unloadingAddress: { street: 'Coopérative Locale', city: 'Dijon', postalCode: '21000' },
    price: { amount: 720, currency: 'EUR' },
    references: { internal: 'OT26000009', client: 'AV-003' }
  },
  {
    id: '019bf0f6-6d60-72c7-8764-4e62660f47c4',
    client: 'Unicorn S.A.S.',
    cargo: 'Aliment porcin',
    loadingAddress: { street: 'ZI Lamballe', city: 'Lamballe', postalCode: '22400' },
    unloadingAddress: { street: 'Ferme des Vallées', city: 'Rennes', postalCode: '35000' },
    price: { amount: 310, currency: 'EUR' },
    references: { internal: 'OT26000010', client: 'REF-UNISAS-4' }
  },
  {
    id: '019bf0f6-8ecc-7f85-99cc-dee49848b696',
    client: 'Global Logistique',
    cargo: 'Sucre en vrac',
    loadingAddress: { street: 'Sucrerie', city: 'Bazancourt', postalCode: '51110' },
    unloadingAddress: { street: 'Port Fluvial', city: 'Strasbourg', postalCode: '67000' },
    price: { amount: 860, currency: 'EUR' },
    references: { internal: 'OT26000011', client: 'GL-101' }
  },
  {
    id: '019bf0f6-a2fb-7db9-ae40-fb94a9359c52',
    client: 'AgriVrac',
    cargo: 'Huile brute',
    loadingAddress: { street: 'Raffinerie', city: 'Grand-Couronne', postalCode: '76530' },
    unloadingAddress: { street: 'Conditionnement', city: 'Le Havre', postalCode: '76600' },
    price: { amount: 290, currency: 'EUR' },
    references: { internal: 'OT26000012', client: 'AV-004' }
  },
  {
    id: '019bf0f6-b41e-7aea-8f68-64bdcf8d4564',
    client: 'Unicorn S.A.S.',
    cargo: 'Produits frais',
    loadingAddress: { street: 'Plateforme Sablé', city: 'Sablé-sur-Sarthe', postalCode: '72300' },
    unloadingAddress: { street: 'MIN Nantes', city: 'Nantes', postalCode: '44000' },
    price: { amount: 440, currency: 'EUR' },
    references: { internal: 'OT26000013', client: 'REF-UNISAS-5' }
  }
]

/** In-memory persistence layer for TransportOrder entities. */
class TransportOrderStore {
  private transportOrders = new Map<string, TransportOrder>(
    DUMMY_TRANSPORT_ORDERS.map((transportOrder) => [transportOrder.id, transportOrder])
  )

  /** Retrieves a single transport order by its identifier. */
  async fetch(id: string): Promise<TransportOrder | null> {
    const data = this.transportOrders.get(id)
    if (!data) return null
    return TransportOrderSchema.parse(data)
  }

  /** Returns all stored transport orders. */
  async fetchAll(): Promise<TransportOrder[]> {
    const data = Array.from(this.transportOrders.values())
    return z.array(TransportOrderSchema).parse(data)
  }

  /** Validates and persists a new transport order record. */
  async create(input: TransportOrder): Promise<TransportOrder> {
    const transportOrder = TransportOrderSchema.parse(input)
    this.transportOrders.set(transportOrder.id, transportOrder)
    return transportOrder
  }

  /** Updates an existing transport order or throws if the ID is unknown. */
  async update(input: TransportOrder): Promise<TransportOrder> {
    const transportOrder = TransportOrderSchema.parse(input)
    if (!this.transportOrders.has(transportOrder.id)) {
      throw new Error(`TransportOrder ${transportOrder.id} not found`)
    }
    this.transportOrders.set(transportOrder.id, transportOrder)
    return transportOrder
  }

  /** Removes a transport order from the storage. */
  async delete(id: string): Promise<void> {
    this.transportOrders.delete(id)
  }
}

/** Global singleton instance providing shared state across the server. */
export const transportOrderStore = new TransportOrderStore()
