/**
 * API service for supermarkets
 */
import api from '../lib/api';
import type { Supermarket } from '../lib/api';

export type { Supermarket };

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
  return api.supermarkets.getAll();
};

/**
 * Get a single supermarket by ID
 */
export const getSupermarket = async (id: number): Promise<Supermarket> => {
  return api.supermarkets.getById(id);
};

/**
 * Create a new supermarket
 */
export const createSupermarket = async (data: SupermarketCreate): Promise<Supermarket> => {
  return api.supermarkets.create(data);
};

/**
 * Update a supermarket
 */
export const updateSupermarket = async (id: number, data: SupermarketUpdate): Promise<Supermarket> => {
  return api.supermarkets.update(id, data);
};

/**
 * Delete a supermarket
 */
export const deleteSupermarket = async (id: number): Promise<void> => {
  return api.supermarkets.delete(id);
};
