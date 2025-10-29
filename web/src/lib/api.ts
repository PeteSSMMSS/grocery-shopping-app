/**
 * API client for communicating with the backend.
 */

const API_BASE = (import.meta as any).env?.VITE_API_BASE || 'http://localhost:8080';

// ============= Types =============

export interface Category {
  id: number;
  name: string;
  updated_at: string;
}

export interface ProductPrice {
  id: number;
  product_id: number;
  price_cents: number;
  currency: string;
  valid_from: string;
  updated_at: string;
}

export interface Product {
  id: number;
  name: string;
  category_id: number | null;
  price_type: 'per_package' | 'per_kg' | 'per_100g' | 'per_liter';
  package_size: number | null;
  package_unit: string | null;  // g, kg, stück, l, ml
  is_active: boolean;
  updated_at: string;
  current_price: number | null;
  category?: Category;
  prices?: ProductPrice[];
}

export interface ListItem {
  id: number;
  list_id: number;
  product_id: number;
  qty: number;
  is_checked: boolean;
  added_at: string;
  updated_at: string;
  product: Product;
}

export interface ActiveList {
  id: number;
  name: string;
  is_active: boolean;
  updated_at: string;
  items: ListItem[];
  total_cents: number;
}

export interface Purchase {
  id: number;
  list_id: number;
  purchased_at: string;
  total_cents: number;
  updated_at: string;
  items: PurchaseItem[];
}

export interface PurchaseItem {
  id: number;
  purchase_id: number;
  product_id: number;
  qty: number;
  price_cents_at_purchase: number;
  updated_at: string;
  product: Product;
}

export interface SyncResponse {
  categories: Category[];
  products: Product[];
  product_prices: ProductPrice[];
  list_items: ListItem[];
  timestamp: string;
}

export interface MealIngredient {
  id: number;
  meal_id: number;
  product_id: number;
  quantity: number;
  quantity_unit: string;
  cost_cents: number;
  created_at: string;
  updated_at: string;
  product: Product;
}

export interface Meal {
  id: number;
  name: string;
  meal_type: 'breakfast' | 'lunch' | 'dinner';
  preparation: string | null;
  total_cost_cents: number;
  created_at: string;
  updated_at: string;
  ingredients: MealIngredient[];
}

export interface MealIngredientCreate {
  product_id: number;
  quantity: number;
  quantity_unit: string;
}

export interface MealCreate {
  name: string;
  meal_type: 'breakfast' | 'lunch' | 'dinner';
  preparation?: string;
  ingredients: MealIngredientCreate[];
}

export interface MealUpdate {
  name?: string;
  meal_type?: 'breakfast' | 'lunch' | 'dinner';
  preparation?: string;
  ingredients?: MealIngredientCreate[];
}

// ============= API Functions =============

async function fetchAPI<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  // Handle 204 No Content (e.g., successful DELETE)
  if (response.status === 204 || response.headers.get('content-length') === '0') {
    return undefined as T;
  }

  return response.json();
}

// Categories
export const api = {
  categories: {
    getAll: () => fetchAPI<Category[]>('/api/categories'),
    create: (name: string) => fetchAPI<Category>('/api/categories', {
      method: 'POST',
      body: JSON.stringify({ name }),
    }),
    update: (id: number, name: string) => fetchAPI<Category>(`/api/categories/${id}`, {
      method: 'PATCH',
      body: JSON.stringify({ name }),
    }),
    delete: (id: number) => fetchAPI<void>(`/api/categories/${id}`, { method: 'DELETE' }),
  },

  // Products
  products: {
    getAll: (params?: { search?: string; category?: number; active?: boolean }) => {
      const query = new URLSearchParams();
      if (params?.search) query.set('search', params.search);
      if (params?.category !== undefined) query.set('category', params.category.toString());
      if (params?.active !== undefined) query.set('active', params.active.toString());
      
      return fetchAPI<Product[]>(`/api/products?${query}`);
    },
    
    getOne: (id: number) => fetchAPI<Product>(`/api/products/${id}`),
    
    create: (data: { name: string; category_id?: number; unit_weight?: string; price_cents?: number }) => 
      fetchAPI<Product>('/api/products', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    
    update: (id: number, data: { name?: string; category_id?: number; unit_weight?: string; is_active?: boolean }) =>
      fetchAPI<Product>(`/api/products/${id}`, {
        method: 'PATCH',
        body: JSON.stringify(data),
      }),
    
    addPrice: (id: number, price_cents: number) =>
      fetchAPI<ProductPrice>(`/api/products/${id}/price`, {
        method: 'POST',
        body: JSON.stringify({ price_cents }),
      }),
    
    delete: (id: number) => fetchAPI<void>(`/api/products/${id}`, { method: 'DELETE' }),
  },

  // Shopping List
  list: {
    getActive: () => fetchAPI<ActiveList>('/api/lists/active'),
    
    addItem: (product_id: number, qty: number = 1) =>
      fetchAPI<ListItem>('/api/lists/active/items', {
        method: 'POST',
        body: JSON.stringify({ product_id, qty }),
      }),
    
    updateItem: (id: number, data: { qty?: number; is_checked?: boolean }) =>
      fetchAPI<ListItem>(`/api/lists/active/items/${id}`, {
        method: 'PATCH',
        body: JSON.stringify(data),
      }),
    
    removeItem: (id: number) =>
      fetchAPI<void>(`/api/lists/active/items/${id}`, { method: 'DELETE' }),
  },

  // Purchases
  purchase: {
    checkout: () => fetchAPI<Purchase>('/api/purchase/checkout', { method: 'POST' }),
    getHistory: (limit: number = 20) =>
      fetchAPI<Purchase[]>(`/api/purchase/history?limit=${limit}`),
    getOne: (id: number) => fetchAPI<Purchase>(`/api/purchase/${id}`),
  },

  // Sync
  sync: {
    since: (timestamp: string) =>
      fetchAPI<SyncResponse>(`/api/sync/since?ts=${encodeURIComponent(timestamp)}`),
    
    pushChanges: (changes: any[]) =>
      fetchAPI<any>('/api/sync/changes', {
        method: 'POST',
        body: JSON.stringify({ changes }),
      }),
  },

  // Meals
  meals: {
    getAll: () => fetchAPI<Meal[]>('/api/meals'),
    
    getOne: (id: number) => fetchAPI<Meal>(`/api/meals/${id}`),
    
    create: (data: MealCreate) =>
      fetchAPI<Meal>('/api/meals', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    
    update: (id: number, data: MealUpdate) =>
      fetchAPI<Meal>(`/api/meals/${id}`, {
        method: 'PATCH',
        body: JSON.stringify(data),
      }),
    
    delete: (id: number) => fetchAPI<void>(`/api/meals/${id}`, { method: 'DELETE' }),
  },

  // Shopping Events
  shoppingEvents: {
    create: (data: {
      name: string;
      event_date: string;
      total_price_cents: number;
      items: Array<{ product_id: number; product_name: string; qty: number; price_cents: number }>;
    }) =>
      fetchAPI<any>('/api/events/', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    
    getByMonth: (year: number, month: number) =>
      fetchAPI<any[]>(`/api/events/?year=${year}&month=${month}`),
    
    getById: (id: number) => fetchAPI<any>(`/api/events/${id}`),
    
    delete: (id: number) => fetchAPI<void>(`/api/events/${id}`, { method: 'DELETE' }),
  },
};

export default api;