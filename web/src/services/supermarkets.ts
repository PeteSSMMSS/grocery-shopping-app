/**
 * API service for supermarkets
 */
import api from './api';

export interface Supermarket {
  id: number;
  name: string;
  color: string | null;
  logo_url: string | null;
  created_at: string;
  updated_at: string;
}

export interface SupermarketCreate {
  name: string;
  color?: string;
  logo_url?: string;
}

export interface SupermarketUpdate {
  name?: string;
  color?: string;
  logo_url?: string;
}

/**
 * Get all supermarkets
 */
export const getSupermarkets = async (): Promise<Supermarket[]> => {
  const response = await api.get<Supermarket[]>('/api/supermarkets/');
  return response.data;
};

/**
 * Get a single supermarket by ID
 */
export const getSupermarket = async (id: number): Promise<Supermarket> => {
  const response = await api.get<Supermarket>(`/api/supermarkets/${id}`);
  return response.data;
};

/**
 * Create a new supermarket
 */
export const createSupermarket = async (data: SupermarketCreate): Promise<Supermarket> => {
  const response = await api.post<Supermarket>('/api/supermarkets/', data);
  return response.data;
};

/**
 * Update a supermarket
 */
export const updateSupermarket = async (id: number, data: SupermarketUpdate): Promise<Supermarket> => {
  const response = await api.patch<Supermarket>(`/api/supermarkets/${id}`, data);
  return response.data;
};

/**
 * Delete a supermarket
 */
export const deleteSupermarket = async (id: number): Promise<void> => {
  await api.delete(`/api/supermarkets/${id}`);
};
