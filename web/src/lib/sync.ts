/**
 * Synchronization logic for offline/online sync.
 */
import { api } from './api';
import { offlineQueue, syncHelpers } from './db.dexie';

let isSyncing = false;

/**
 * Sync data from server to local IndexedDB.
 */
export async function syncFromServer(): Promise<void> {
  if (isSyncing) return;
  
  try {
    isSyncing = true;
    
    const lastSync = await syncHelpers.getLastSyncTime();
    const response = await api.sync.since(lastSync);
    
    // Update local database
    if (response.categories.length > 0) {
      await syncHelpers.syncCategories(response.categories);
    }
    
    if (response.products.length > 0) {
      await syncHelpers.syncProducts(response.products);
    }
    
    if (response.product_prices.length > 0) {
      await syncHelpers.syncProductPrices(response.product_prices);
    }
    
    if (response.list_items.length > 0) {
      await syncHelpers.syncListItems(response.list_items);
    }
    
    // Update last sync time
    await syncHelpers.setLastSyncTime(response.timestamp);
    
    console.log('✅ Sync from server completed', {
      categories: response.categories.length,
      products: response.products.length,
      prices: response.product_prices.length,
      listItems: response.list_items.length
    });
  } catch (error) {
    console.error('❌ Sync from server failed:', error);
    throw error;
  } finally {
    isSyncing = false;
  }
}

/**
 * Push local offline changes to server.
 */
export async function syncToServer(): Promise<void> {
  if (isSyncing) return;
  
  try {
    isSyncing = true;
    
    const unsyncedItems = await offlineQueue.getUnsyncedItems();
    
    if (unsyncedItems.length === 0) {
      console.log('✅ No offline changes to sync');
      return;
    }
    
    console.log(`📤 Syncing ${unsyncedItems.length} offline changes...`);
    
    // Push changes to server
    const response = await api.sync.pushChanges(unsyncedItems);
    
    // Mark items as synced
    await offlineQueue.markSynced(unsyncedItems.map(item => item.id!));
    
    // Clean up synced items older than 7 days
    await offlineQueue.clearSynced();
    
    console.log('✅ Sync to server completed', response);
  } catch (error) {
    console.error('❌ Sync to server failed:', error);
    throw error;
  } finally {
    isSyncing = false;
  }
}

/**
 * Full bidirectional sync.
 */
export async function fullSync(): Promise<void> {
  console.log('🔄 Starting full sync...');
  
  try {
    // First push local changes
    await syncToServer();
    
    // Then pull server changes
    await syncFromServer();
    
    console.log('✅ Full sync completed');
  } catch (error) {
    console.error('❌ Full sync failed:', error);
    throw error;
  }
}

/**
 * Check if online and sync if needed.
 */
export function setupAutoSync(intervalMinutes: number = 5): () => void {
  const intervalMs = intervalMinutes * 60 * 1000;
  
  const syncIfOnline = async () => {
    if (navigator.onLine) {
      try {
        await fullSync();
      } catch (error) {
        console.error('Auto-sync failed:', error);
      }
    }
  };
  
  // Initial sync
  syncIfOnline();
  
  // Periodic sync
  const interval = setInterval(syncIfOnline, intervalMs);
  
  // Sync when coming back online
  const onlineHandler = () => {
    console.log('📡 Back online, syncing...');
    syncIfOnline();
  };
  
  window.addEventListener('online', onlineHandler);
  
  // Cleanup function
  return () => {
    clearInterval(interval);
    window.removeEventListener('online', onlineHandler);
  };
}

/**
 * Check if currently online.
 */
export function isOnline(): boolean {
  return navigator.onLine;
}

/**
 * Register background sync for service worker.
 */
export async function registerBackgroundSync() {
  if ('serviceWorker' in navigator && 'sync' in (ServiceWorkerRegistration.prototype as any)) {
    try {
      const registration = await navigator.serviceWorker.ready;
      await (registration as any).sync.register('sync-groceries');
      console.log('✅ Background sync registered');
    } catch (error) {
      console.error('❌ Background sync registration failed:', error);
    }
  }
}
