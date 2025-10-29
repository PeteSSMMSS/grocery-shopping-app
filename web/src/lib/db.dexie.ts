/**
 * Dexie.js IndexedDB configuration for offline storage.
 */
import Dexie, { Table } from 'dexie';
import type { Category, Product, ProductPrice, ListItem } from './api';

export class GroceriesDB extends Dexie {
  categories!: Table<Category>;
  products!: Table<Product>;
  productPrices!: Table<ProductPrice>;
  listItems!: Table<ListItem>;
  offlineQueue!: Table<OfflineQueueItem>;

  constructor() {
    super('GroceriesDB');
    
    this.version(1).stores({
      categories: 'id, name, updated_at',
      products: 'id, name, category_id, is_active, updated_at',
      productPrices: 'id, product_id, valid_from, updated_at',
      listItems: 'id, list_id, product_id, updated_at',
      offlineQueue: '++id, timestamp, synced'
    });
  }
}

export interface OfflineQueueItem {
  id?: number;
  entity_type: string;
  entity_id?: number;
  operation: 'create' | 'update' | 'delete';
  data?: any;
  timestamp: string;
  synced: boolean;
}

export const db = new GroceriesDB();

// Helper functions for offline queue
export const offlineQueue = {
  async add(item: Omit<OfflineQueueItem, 'id' | 'timestamp' | 'synced'>) {
    await db.offlineQueue.add({
      ...item,
      timestamp: new Date().toISOString(),
      synced: false
    });
  },

  async getUnsyncedItems() {
    return db.offlineQueue.where('synced').equals(0 as any).toArray();
  },

  async markSynced(ids: number[]) {
    for (const id of ids) {
      await db.offlineQueue.update(id, { synced: true });
    }
  },

  async clearSynced() {
    await db.offlineQueue.where('synced').equals(1 as any).delete();
  }
};

// Sync helpers
export const syncHelpers = {
  async syncCategories(categories: Category[]) {
    await db.categories.bulkPut(categories);
  },

  async syncProducts(products: Product[]) {
    await db.products.bulkPut(products);
  },

  async syncProductPrices(prices: ProductPrice[]) {
    await db.productPrices.bulkPut(prices);
  },

  async syncListItems(items: ListItem[]) {
    await db.listItems.bulkPut(items);
  },

  async getLastSyncTime(): Promise<string> {
    const lastSync = localStorage.getItem('lastSyncTime');
    return lastSync || new Date(0).toISOString();
  },

  async setLastSyncTime(time: string) {
    localStorage.setItem('lastSyncTime', time);
  }
};

export default db;
