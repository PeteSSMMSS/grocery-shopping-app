/**
 * React Query hooks for supermarkets
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import * as supermarketService from '../services/supermarkets';
import type { SupermarketCreate, SupermarketUpdate } from '../services/supermarkets';

/**
 * Hook to fetch all supermarkets
 */
export const useSupermarkets = () => {
  return useQuery({
    queryKey: ['supermarkets'],
    queryFn: supermarketService.getSupermarkets,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

/**
 * Hook to fetch a single supermarket
 */
export const useSupermarket = (id: number) => {
  return useQuery({
    queryKey: ['supermarkets', id],
    queryFn: () => supermarketService.getSupermarket(id),
    enabled: !!id,
  });
};

/**
 * Hook to create a supermarket
 */
export const useCreateSupermarket = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (data: SupermarketCreate) => supermarketService.createSupermarket(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['supermarkets'] });
    },
  });
};

/**
 * Hook to update a supermarket
 */
export const useUpdateSupermarket = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: SupermarketUpdate }) => 
      supermarketService.updateSupermarket(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['supermarkets'] });
      queryClient.invalidateQueries({ queryKey: ['supermarkets', variables.id] });
    },
  });
};

/**
 * Hook to delete a supermarket
 */
export const useDeleteSupermarket = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (id: number) => supermarketService.deleteSupermarket(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['supermarkets'] });
    },
  });
};
